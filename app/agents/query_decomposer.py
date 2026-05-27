# app/agents/query_decomposer.py
#
# Intention:
#   Split compound questions ("compare X and Y, and tell me which one supports Z")
#   into independent sub-questions that can be retrieved in parallel and then
#   recombined. Boosts recall on multi-hop queries.
#
# What this file should contain:
#   - A `QueryDecomposer` class with:
#       * Constructor taking the LLM client.
#       * An async `decompose(query)` method returning a list of sub-questions
#         (a single-item list when no decomposition is needed).
#   - Decomposition prompt lives in `app/prompts/templates.py`.
#
# Example (commented):
#
#   class QueryDecomposer:
#       def __init__(self, llm_client): ...
#       async def decompose(self, query: str) -> list[str]: ...
