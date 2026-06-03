# memory/semantic_cache.py
#
# Intention:
#   Repeat-query cache. Skip the full agent loop when a semantically similar query
#   has already been answered. Backed by Redis vector search: keys are quantized
#   embeddings, values are the prior response.
#
# What this file should contain:
#   - A `SemanticCache` class with:
#       * Constructor taking `redis_url` and a cosine-similarity threshold
#         (0.95-0.98 is a common starting point).
#       * `get(query)` -> cached response if a near-neighbor exists, else None.
#       * `put(query, response)` -> stores embedding + response with TTL.
#   - Lookup must be O(log n) via the vector index, not a Python loop.
#   - Fail OPEN: a cache error should never block a request.
#   - Honor a debug bypass flag (see `CLAUDE.local.md.example`).
#
# Example (commented):
#
#   class SemanticCache:
#       def __init__(self, redis_url: str, threshold: float = 0.97): ...
#       async def get(self, query: str) -> str | None: ...
#       async def put(self, query: str, response: str) -> None: ...
