# app/services/query_rewriter.py
#
# Intention:
#   Transform an incoming user query into a retrieval-friendly form before it
#   reaches the vector store. Resolves pronouns ("it", "that one") against the
#   conversation history, expands abbreviations, and adds implicit context.
#
# What this file should contain:
#   - A `QueryRewriter` class with:
#       * Constructor taking the LLM client.
#       * An async `rewrite(query, history)` method that returns the canonical
#         retrieval query.
#   - Prompt template lives in `app/prompts/templates.py` - do not inline prompts.
#
# Example (commented):
#
#   class QueryRewriter:
#       def __init__(self, llm_client): ...
#       async def rewrite(self, query: str, history: list[Message]) -> str: ...
