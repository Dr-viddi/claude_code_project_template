"""Semantic cache. Hashes query embedding and returns cached responses on near-match."""

from __future__ import annotations


class SemanticCache:
    def __init__(self, redis_url: str, threshold: float = 0.97) -> None:
        self._redis_url = redis_url
        self._threshold = threshold

    async def get(self, query: str) -> str | None:
        raise NotImplementedError

    async def put(self, query: str, response: str) -> None:
        raise NotImplementedError
