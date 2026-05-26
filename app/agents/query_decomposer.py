"""Splits compound queries into independent sub-questions for parallel retrieval."""

from __future__ import annotations


class QueryDecomposer:
    def __init__(self, llm_client) -> None:
        self._llm = llm_client

    async def decompose(self, query: str) -> list[str]:
        raise NotImplementedError
