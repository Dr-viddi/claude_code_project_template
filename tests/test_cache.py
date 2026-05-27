# tests/test_cache.py
#
# Intention:
#   Unit tests for `app/services/semantic_cache.py`. Cover hit, miss, TTL,
#   and threshold edge cases (just-above / just-below the similarity cutoff).
#
# What this file should contain:
#   - Tests using the `fake_redis` fixture from `conftest.py` - no live Redis.
#   - Tests for the bypass path when `CACHE_BYPASS=1`.
#   - Tests for behavior on Redis errors (the cache should fail open, not block
#     the request).
#
# Example (commented):
#
#   @pytest.mark.asyncio
#   async def test_cache_miss_returns_none(fake_redis):
#       cache = SemanticCache(redis_url="redis://stub")
#       assert await cache.get("never seen") is None
