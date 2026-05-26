"""Cross-encoder reranker over hybrid retrieval candidates."""

from __future__ import annotations

from app.components.hybrid_retriever import RetrievedChunk


class Reranker:
    def __init__(self, model_name: str, top_n: int = 5) -> None:
        self._model_name = model_name
        self._top_n = top_n

    async def rerank(self, query: str, chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
        raise NotImplementedError
