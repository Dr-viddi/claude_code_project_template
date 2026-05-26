"""LLM-driven source selection. Picks the best tool(s) for the current query."""

from __future__ import annotations


class AdaptiveRouter:
    def __init__(self, llm_client, tools: list) -> None:
        self._llm = llm_client
        self._tools = tools

    async def select(self, query: str) -> list[str]:
        raise NotImplementedError
