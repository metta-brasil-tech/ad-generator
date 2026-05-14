"""Indexer — vetoriza models/*.yaml no Qdrant pra busca semântica."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import click
import yaml
from dotenv import load_dotenv

load_dotenv()

from adapters.llm import EmbeddingAdapter
from adapters.vector_store import VectorStore


def load_models(knowledge_path: Path) -> list[dict]:
    """Load YAMLs from models/{marca}/*.yaml (recursive). Auto-tag marca from parent dir if missing."""
    models_dir = knowledge_path / "models"
    models: list[dict] = []
    for yaml_file in models_dir.rglob("*.yaml"):
        if yaml_file.name.startswith("_"):
            continue
        data = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
        if not data or not data.get("id"):
            continue
        # Brand namespace: parent dir name is canonical when models/{marca}/file.yaml
        rel_parent = yaml_file.parent.relative_to(models_dir).as_posix()
        if rel_parent and rel_parent != ".":
            inferred_marca = rel_parent.split("/")[0]
            if not data.get("marca"):
                data["marca"] = inferred_marca
            elif data["marca"] != inferred_marca:
                print(f"  ⚠ {yaml_file.name}: marca='{data['marca']}' contradicts path '{inferred_marca}/' — using YAML value")
        data["_source_file"] = f"{rel_parent}/{yaml_file.name}" if rel_parent != "." else yaml_file.name
        models.append(data)
    return models


@click.command()
@click.option("--re-index", is_flag=True, help="Drop and rebuild collection.")
@click.option("--dry-run", is_flag=True, help="Show what would be indexed without writing.")
def main(re_index: bool, dry_run: bool):
    knowledge_path = Path(os.getenv("BRAND_KNOWLEDGE_PATH", "../../brand-knowledge"))
    if not knowledge_path.exists():
        print(f"Knowledge path not found: {knowledge_path}", file=sys.stderr)
        sys.exit(1)

    models = load_models(knowledge_path)
    if not models:
        print("No models found in", knowledge_path / "models")
        sys.exit(1)

    print(f"Found {len(models)} models:")
    for m in models:
        print(f"  • {m['id']} ({m['_source_file']})")

    if dry_run:
        print("\n[dry-run] would index above. Exiting.")
        return

    embedder = EmbeddingAdapter()
    dim = int(os.getenv("EMBEDDING_DIM", "3072"))
    store = VectorStore()

    if re_index:
        try:
            store.client.delete_collection(store.collection)
            print(f"Dropped collection '{store.collection}'")
        except Exception as e:
            print(f"(could not drop existing: {e})")

    store.ensure_collection(vector_size=dim)
    print(f"Collection '{store.collection}' ready (dim={dim})")

    for m in models:
        intent_text = (m.get("embedding_text", {}).get("intent") or "").strip()
        visual_text = (m.get("embedding_text", {}).get("visual_features") or "").strip()
        if not intent_text or not visual_text:
            print(f"  ⚠ {m['id']}: missing embedding_text — skipping")
            continue

        try:
            iv = embedder.embed(intent_text)
            vv = embedder.embed(visual_text)
        except Exception as e:
            print(f"  ✗ {m['id']}: embedding failed: {e}")
            continue

        payload = {
            "model_id": m["id"],
            "marca": m.get("marca", "metta"),
            "display_name": m.get("display_name", ""),
            "formato": m.get("formato", ""),
            "teses": m.get("teses_compativeis", []),
            "funil": m.get("funil_recomendado", []),
            "yaml_path": f"brand-knowledge/models/{m['_source_file']}",
            "anti_padroes": m.get("anti_padroes", []),
        }
        store.upsert_model(m["id"], iv, vv, payload)
        print(f"  ✓ {m['id']}")

    print(f"\nIndexed {store.count()} points.")


if __name__ == "__main__":
    main()
