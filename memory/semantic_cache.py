# memory/semantic_cache.py
#
# Purpose
#   Repeat-query cache. Skips the full agent loop when a semantically similar
#   query has already been answered. Backed by Redis vector search in production
#   (keys are quantized embeddings, values are the prior response).
#
# When you want a file like this
#   Any agent with non-trivial latency or cost per request, AND repetitive
#   queries. Customer support, internal-doc QA, and FAQ-flavored use cases are
#   ideal. Skip it for one-off creative tasks.
#
# Why it matters
#   - A well-tuned cache eliminates 20-60% of LLM cost on FAQ-shaped workloads.
#   - The threshold knob (cosine similarity) is the lever between "high cache
#     hit rate, occasional wrong answer" and "rare hits, always-fresh".
#   - Fails OPEN: a cache error should never block a request - log and continue.
#
# What goes in it
#   - A `SemanticCache` class with:
#       * Constructor taking the backend and a similarity threshold
#         (0.95-0.98 is a common starting point).
#       * `get(query)` -> cached response if a near-neighbor exists, else None.
#       * `put(query, response)` -> store embedding + response with TTL.
#   - Lookup must be O(log n) via the vector index, not a Python loop.
#   - Honor a debug bypass flag (see CLAUDE.local.md.example).
#
# Example (commented)
#
#   class SemanticCache:
#       def __init__(self, redis_url: str = "", threshold: float = 0.97): ...
#       async def get(self, query: str) -> str | None: ...
#       async def put(self, query: str, response: str) -> None: ...
