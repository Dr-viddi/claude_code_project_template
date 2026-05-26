"""LLM-driven query rewriting: expand abbreviations, dereference pronouns, add context."""

from __future__ import annotations

from app.models import Message


class QueryRewriter:
    def __init__(self, llm_client) -> None:
        self._llm = llm_client

    async def rewrite(self, query: str, history: list[Message]) -> str:
        raise NotImplementedError
