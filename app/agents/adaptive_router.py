# app/agents/adaptive_router.py
#
# Intention:
#   Pick the right tool(s) for the current query - vector search for internal
#   knowledge, web search for fresh facts, code search for repository questions,
#   or some combination. Unlike `services/query_router.py` (coarse-grained
#   path selection), this is a fine-grained tool-selection agent.
#
# What this file should contain:
#   - An `AdaptiveRouter` class with:
#       * Constructor taking the LLM client and the available tool registry.
#       * An async `select(query)` method returning the list of tool names the
#         pipeline should invoke for this query.
#   - Decisions should be logged with rationale for offline analysis.
#
# Example (commented):
#
#   class AdaptiveRouter:
#       def __init__(self, llm_client, tools: list): ...
#       async def select(self, query: str) -> list[str]: ...
