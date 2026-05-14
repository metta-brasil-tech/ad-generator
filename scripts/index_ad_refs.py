"""Embed ad descriptions + save to local JSON file (file-based vector store).

No Qdrant needed — 68 items is trivial scale for in-memory cosine similarity.

Output: artifacts/banco/_embeddings.json

Usage: python scripts/index_ad_refs.py [--re-index]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from adapters.llm import EmbeddingAdapter

BANCO_DIR = Path(__file__).resolve().parent.parent / "artifacts" / "banco"
STORE_FILE = BANCO_DIR / "_embeddings.json"


def build_embedding_text(desc: dict) -> str:
    parts = []
    if desc.get("tese_central"):
        parts.append(f"Tese: {desc['tese_central']}")
    if desc.get("intent"):
        parts.append(f"Intent: {desc['intent']}")
    if desc.get("mood"):
        parts.append(f"Mood: {desc['mood']}")
    if desc.get("composition"):
        parts.append(f"Composicao: {desc['composition']}")
    if desc.get("headline_text"):
        parts.append(f"Headline: {desc['headline_text']}")
    if desc.get("body_text"):
        parts.append(f"Body: {desc['body_text']}")
    if desc.get("tags"):
        parts.append(f"Tags: {', '.join(desc['tags'])}")
    if desc.get("keywords_pt"):
        parts.append(f"Keywords PT: {', '.join(desc['keywords_pt'])}")
    if desc.get("keywords_en"):
        parts.append(f"Keywords EN: {', '.join(desc['keywords_en'])}")
    return "\n".join(parts)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--re-index", action="store_true")
    args = p.parse_args()

    json_files = sorted(BANCO_DIR.glob("*.json"))
    json_files = [f for f in json_files if not f.name.startswith("_")]
    if not json_files:
        print(f"No description JSONs in {BANCO_DIR}", file=sys.stderr)
        sys.exit(1)
    print(f"Found {len(json_files)} description files")

    if STORE_FILE.exists() and not args.re_index:
        existing = json.loads(STORE_FILE.read_text(encoding="utf-8"))
        print(f"Existing store has {len(existing.get('items', []))} items (use --re-index to rebuild)")
        sys.exit(0)

    embedder = EmbeddingAdapter()
    items = []
    for jf in json_files:
        try:
            desc = json.loads(jf.read_text(encoding="utf-8"))
            text = build_embedding_text(desc)
            vec = embedder.embed(text)
            items.append({
                "filename": desc.get("_filename"),
                "png_path": desc.get("_png_path"),
                "style_id": desc.get("style_id"),
                "intent": desc.get("intent"),
                "tese_central": desc.get("tese_central"),
                "mood": desc.get("mood"),
                "palette": desc.get("palette"),
                "has_person_photo": desc.get("has_person_photo"),
                "tags": desc.get("tags", []),
                "headline_text": desc.get("headline_text"),
                "description_text": text,
                "embedding": vec,
            })
            print(f"  + {jf.stem[:60]:60s} style={desc.get('style_id')}")
        except Exception as e:
            print(f"  ! {jf.name}: {e}")

    store = {"version": "1.0", "dim": len(items[0]["embedding"]) if items else 0, "items": items}
    STORE_FILE.write_text(json.dumps(store, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    sz_mb = STORE_FILE.stat().st_size / 1024 / 1024
    print(f"\nSaved {len(items)} items to {STORE_FILE} ({sz_mb:.1f} MB)")


if __name__ == "__main__":
    main()
