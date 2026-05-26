"""Self-correcting retrieval: an LLM grades each retrieved chunk for relevance."""

from __future__ import annotations

from app.components.hybrid_retriever import RetrievedChunk


class DocumentGrader:
    def __init__(self, llm_client, threshold: float = 0.5) -> None:
        self._llm = llm_client
        self._threshold = threshold

    async def grade(self, query: str, chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
        raise NotImplementedError
