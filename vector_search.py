"""Vector search helper — usado pelo style-selector pra recuperar candidatos do Qdrant.

Gracefully degrade: se Qdrant indisponível ou collection vazia, retorna lista vazia
e o style-selector cold-ranks com o catálogo completo.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from adapters.llm import EmbeddingAdapter
from adapters.vector_store import VectorStore, SearchResult


@dataclass
class StyleCandidate:
    model_id: str
    intent_score: float
    visual_score: float
    combined_score: float
    yaml_path: str
    display_name: str
    teses: list
    funil: list
    anti_padroes: list


def search_styles(
    query_text: str,
    top_k: int = 5,
) -> tuple[list[StyleCandidate], str]:
    """Search styles by semantic similarity. Returns (candidates, status_message).

    Gracefully returns ([], 'qdrant_unavailable') if Qdrant/embeddings fail.
    """
    try:
        embedder = EmbeddingAdapter()
        store = VectorStore()
    except Exception as e:
        return [], f"qdrant_or_embedder_init_failed: {e}"

    if store.count() == 0:
        return [], "qdrant_collection_empty — run indexer.py first"

    try:
        query_vec = embedder.embed(query_text)
    except Exception as e:
        return [], f"embedding_failed: {e}"

    try:
        intent_hits = store.search(query_vec, vector_name="intent", limit=top_k)
        visual_hits = store.search(query_vec, vector_name="visual", limit=top_k)
    except Exception as e:
        return [], f"qdrant_search_failed: {e}"

    # Merge by model_id, weight intent 70% / visual 30%
    merged: dict[str, dict] = {}
    for r in intent_hits:
        mid = r.model_id
        merged.setdefault(mid, {"intent": 0, "visual": 0, "payload": r.payload})
        merged[mid]["intent"] = r.score
    for r in visual_hits:
        mid = r.model_id
        merged.setdefault(mid, {"intent": 0, "visual": 0, "payload": r.payload})
        merged[mid]["visual"] = r.score

    candidates = []
    for mid, d in merged.items():
        combined = 0.7 * d["intent"] + 0.3 * d["visual"]
        p = d["payload"]
        candidates.append(StyleCandidate(
            model_id=mid,
            intent_score=d["intent"],
            visual_score=d["visual"],
            combined_score=combined,
            yaml_path=p.get("yaml_path", ""),
            display_name=p.get("display_name", ""),
            teses=p.get("teses", []),
            funil=p.get("funil", []),
            anti_padroes=p.get("anti_padroes", []),
        ))

    candidates.sort(key=lambda c: c.combined_score, reverse=True)
    return candidates[:top_k], "ok"


@dataclass
class AdRef:
    filename: str
    png_path: str
    style_id: str
    intent: str
    tese_central: str
    mood: str
    palette: str
    has_person_photo: bool
    tags: list
    headline_text: str
    description_text: str
    score: float


_AD_REFS_STORE = None


def _load_ad_refs_store() -> dict | None:
    """Load embeddings from local JSON file. Cached after first load."""
    global _AD_REFS_STORE
    if _AD_REFS_STORE is not None:
        return _AD_REFS_STORE
    import json
    store_file = Path(__file__).resolve().parent / "artifacts" / "banco" / "_embeddings.json"
    if not store_file.exists():
        return None
    try:
        _AD_REFS_STORE = json.loads(store_file.read_text(encoding="utf-8"))
        return _AD_REFS_STORE
    except Exception:
        return None


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    import math
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def search_ad_refs(
    query_text: str,
    style_filter: str | None = None,
    top_k: int = 3,
) -> tuple[list[AdRef], str]:
    """Search banco ad references via in-memory brute-force cosine similarity.

    No Qdrant needed — 68 items is trivial.
    """
    store = _load_ad_refs_store()
    if not store or not store.get("items"):
        return [], "store_missing — run scripts/index_ad_refs.py first"

    try:
        embedder = EmbeddingAdapter()
        query_vec = embedder.embed(query_text)
    except Exception as e:
        return [], f"embedding_failed: {e}"

    # Score every item
    items = store["items"]
    style_variants = None
    if style_filter:
        style_variants = {style_filter, style_filter.split("-")[0]}

    scored = []
    for item in items:
        score = _cosine_similarity(query_vec, item["embedding"])
        # Boost score if style matches filter
        if style_variants and item.get("style_id") in style_variants:
            score += 0.10  # boost matching style
        scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)

    # Optional: filter to style only when matches exist
    if style_filter:
        matching = [(s, i) for s, i in scored if i.get("style_id") in style_variants]
        if matching:
            scored = matching

    refs = []
    for score, item in scored[:top_k]:
        refs.append(AdRef(
            filename=item.get("filename", ""),
            png_path=item.get("png_path", ""),
            style_id=item.get("style_id", ""),
            intent=item.get("intent", ""),
            tese_central=item.get("tese_central", ""),
            mood=item.get("mood", ""),
            palette=item.get("palette", ""),
            has_person_photo=item.get("has_person_photo", False),
            tags=item.get("tags", []),
            headline_text=item.get("headline_text", ""),
            description_text=item.get("description_text", ""),
            score=score,
        ))

    return refs, f"ok ({len(refs)} refs, filter={style_filter}, pool={len(items)})"


def refs_to_prompt_addendum(refs: list[AdRef]) -> str:
    """Format ad refs as a description-only addendum (for OpenAI image-gen which doesn't accept image refs)."""
    if not refs:
        return ""
    lines = ["\n\nReferências visuais do banco Metta (siga este estilo de composição/mood):"]
    for i, r in enumerate(refs, 1):
        lines.append(f"{i}. [{r.style_id}] mood: {r.mood}; composition: {r.description_text[:200]}")
    return "\n".join(lines)


def candidates_to_context(candidates: list[StyleCandidate]) -> str:
    """Format candidates as markdown context to inject into style-selector skill."""
    if not candidates:
        return "Vector search retornou 0 candidatos — rank do catálogo cold."

    lines = ["## Vector search top candidates\n"]
    for i, c in enumerate(candidates, 1):
        lines.append(f"{i}. **{c.model_id}** — {c.display_name}")
        lines.append(f"   - score: combined={c.combined_score:.3f} (intent={c.intent_score:.3f} / visual={c.visual_score:.3f})")
        lines.append(f"   - teses: {', '.join(c.teses) if c.teses else 'n/a'}")
        lines.append(f"   - funil: {', '.join(c.funil) if c.funil else 'n/a'}")
        if c.anti_padroes:
            lines.append(f"   - anti-padrões: {'; '.join(c.anti_padroes[:2])}")
    return "\n".join(lines)
