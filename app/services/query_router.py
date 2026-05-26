"""Routes incoming queries to the right pipeline path: RAG, agent, direct LLM, refusal."""

from __future__ import annotations

from enum import Enum


class Route(str, Enum):
    RAG = "rag"
    AGENT = "agent"
    DIRECT = "direct"
    REFUSE = "refuse"


class QueryRouter:
    def __init__(self, llm_client) -> None:
        self._llm = llm_client

    async def route(self, query: str) -> Route:
        raise NotImplementedError
