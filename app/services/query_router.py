# app/services/query_router.py
#
# Intention:
#   Classify each query into the appropriate pipeline path so we don't run the
#   expensive RAG flow on small talk, and so out-of-scope or unsafe queries get
#   refused early.
#
# What this file should contain:
#   - A `Route` enum: `RAG`, `AGENT`, `DIRECT`, `REFUSE` (extend as needed).
#   - A `QueryRouter` class with:
#       * Constructor taking the LLM client (or a small classifier).
#       * An async `route(query)` method returning a `Route`.
#   - Routing rationale (free-text reason) should be attached to the trace span
#     so the team can audit decisions in production.
#
# Example (commented):
#
#   class Route(str, Enum):
#       RAG = "rag"; AGENT = "agent"; DIRECT = "direct"; REFUSE = "refuse"
#
#   class QueryRouter:
#       def __init__(self, llm_client): ...
#       async def route(self, query: str) -> Route: ...
