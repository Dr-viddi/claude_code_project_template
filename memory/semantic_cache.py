"""Repeat-query cache.

The minimal backend keys on a normalized form of the query (exact-ish match). For
production, replace ``_key`` + ``_store`` with an embedding + Redis vector search so
*semantically* similar queries hit. Fails open: a cache miss is just ``None``.
"""

from __future__ import annotations


class SemanticCache:
    def __init__(self, threshold: float = 0.97) -> None:
        self.threshold = threshold
        self._store: dict[str, str] = {}

    @staticmethod
    def _key(query: str) -> str:
        return " ".join(query.lower().split())

    async def get(self, query: str) -> str | None:
        return self._store.get(self._key(query))

    async def put(self, query: str, response: str) -> None:
        self._store[self._key(query)] = response
