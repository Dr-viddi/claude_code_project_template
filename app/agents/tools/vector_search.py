# app/agents/tools/vector_search.py
#
# Intention:
#   Tool wrapper around the project's vector retriever so the adaptive router
#   can select it like any other tool. Exposes internal knowledge to the agent loop.
#
# What this file should contain:
#   - A `VectorSearchTool` class with:
#       * Class attributes `name = "vector_search"` and a `description` the
#         router (and the LLM) uses to decide when to call it.
#       * Constructor taking the underlying retriever.
#       * An async `__call__(query, k=5)` returning a list of `{doc_id, snippet, score}`.
#   - Validate `k` (e.g. cap at 25) - the LLM can request silly values.
#
# Example (commented):
#
#   class VectorSearchTool:
#       name = "vector_search"
#       description = "Search the indexed corpus for semantically similar passages."
#       def __init__(self, retriever): ...
#       async def __call__(self, query: str, k: int = 5) -> list[dict]: ...
