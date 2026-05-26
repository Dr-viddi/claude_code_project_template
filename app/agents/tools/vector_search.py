"""Pluggable tool: vector search over the project corpus."""

from __future__ import annotations


class VectorSearchTool:
    name = "vector_search"
    description = "Search the indexed corpus for semantically similar passages."

    def __init__(self, retriever) -> None:
        self._retriever = retriever

    async def __call__(self, query: str, k: int = 5) -> list[dict]:
        raise NotImplementedError
