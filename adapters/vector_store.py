"""Qdrant adapter — vector search nos modelos de ad indexados."""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models as qdrant_models
    _QDRANT_OK = True
except ImportError:
    _QDRANT_OK = False


@dataclass
class SearchResult:
    model_id: str
    score: float
    payload: dict[str, Any]


class VectorStore:
    def __init__(self, url: str | None = None, collection: str | None = None):
        if not _QDRANT_OK:
            raise ImportError("qdrant-client not installed. Run: pip install qdrant-client")
        self.url = url or os.getenv("QDRANT_URL", "http://localhost:6333")
        self.collection = collection or os.getenv("QDRANT_COLLECTION", "ad-styles")
        api_key = os.getenv("QDRANT_API_KEY") or None
        self.client = QdrantClient(url=self.url, api_key=api_key)

    def ensure_collection(self, vector_size: int):
        """Create collection if it doesn't exist."""
        try:
            self.client.get_collection(self.collection)
        except Exception:
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config={
                    "intent": qdrant_models.VectorParams(
                        size=vector_size, distance=qdrant_models.Distance.COSINE
                    ),
                    "visual": qdrant_models.VectorParams(
                        size=vector_size, distance=qdrant_models.Distance.COSINE
                    ),
                },
            )

    def upsert_model(
        self,
        model_id: str,
        intent_vector: list[float],
        visual_vector: list[float],
        payload: dict,
    ):
        # Use deterministic int ID from hash of model_id
        point_id = abs(hash(model_id)) % (2**63)
        self.client.upsert(
            collection_name=self.collection,
            points=[
                qdrant_models.PointStruct(
                    id=point_id,
                    vector={"intent": intent_vector, "visual": visual_vector},
                    payload={**payload, "model_id": model_id},
                )
            ],
        )

    def search(
        self,
        query_vector: list[float],
        vector_name: str = "intent",
        limit: int = 5,
        score_threshold: float | None = None,
    ) -> list[SearchResult]:
        results = self.client.search(
            collection_name=self.collection,
            query_vector=(vector_name, query_vector),
            limit=limit,
            score_threshold=score_threshold,
        )
        return [
            SearchResult(
                model_id=r.payload.get("model_id", ""),
                score=r.score,
                payload=r.payload,
            )
            for r in results
        ]

    def count(self) -> int:
        return self.client.count(collection_name=self.collection).count
