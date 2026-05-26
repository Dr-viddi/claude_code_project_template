"""Top-level RAG pipeline: rewrite → route → cache → retrieve → rerank → generate."""

from __future__ import annotations

from app.config import Settings
from app.models import ChatRequest, ChatResponse


class RAGPipeline:
    def __init__(
        self,
        rewriter,
        router,
        cache,
        retriever,
        reranker,
        generator,
        guards,
    ) -> None:
        self._rewriter = rewriter
        self._router = router
        self._cache = cache
        self._retriever = retriever
        self._reranker = reranker
        self._generator = generator
        self._guards = guards

    @classmethod
    def from_settings(cls, settings: Settings) -> "RAGPipeline":
        raise NotImplementedError("Wire up concrete implementations here.")

    async def run(self, req: ChatRequest) -> ChatResponse:
        raise NotImplementedError
