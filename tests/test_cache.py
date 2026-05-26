"""Tests for the semantic cache."""

from __future__ import annotations

import pytest

from app.services.semantic_cache import SemanticCache


@pytest.mark.asyncio
async def test_cache_miss_returns_none():
    cache = SemanticCache(redis_url="redis://localhost:6379/0")
    with pytest.raises(NotImplementedError):
        await cache.get("nothing here yet")
