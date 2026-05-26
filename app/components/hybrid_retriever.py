"""Hybrid retriever: combines dense (vector) and sparse (BM25) search.

Returns a single ranked list. Downstream `reranker.py` re-orders by relevance.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RetrievedChunk:
    doc_id: str
    text: str
    dense_score: float
    sparse_score: float

    @property
    def fused_score(self) -> float:
        return 0.5 * self.dense_score + 0.5 * self.sparse_score


class HybridRetriever:
    def __init__(self, dense_backend, sparse_backend, k: int = 20) -> None:
        self._dense = dense_backend
        self._sparse = sparse_backend
        self._k = k

    async def retrieve(self, query: str) -> list[RetrievedChunk]:
        raise NotImplementedError
