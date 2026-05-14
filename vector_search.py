"""Vector search helper — usado pelo style-selector pra recuperar candidatos do Qdrant.

Gracefully degrade: se Qdrant indisponível ou collection vazia, retorna lista vazia
e o style-selector cold-ranks com o catálogo completo.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
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
