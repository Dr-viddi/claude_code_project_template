# app/components/reranker.py
#
# Intention:
#   Re-order the candidate chunks produced by `hybrid_retriever.py` using a stronger
#   relevance model (typically a cross-encoder). Improves precision on the top-N
#   passages that get fed into the LLM prompt.
#
# What this file should contain:
#   - A `Reranker` class with:
#       * Constructor taking a model identifier and a top-N (5 is a common default).
#       * An async `rerank(query, chunks)` method returning the top-N chunks
#         scored by the cross-encoder.
#   - Boundary mocks for tests live in `tests/conftest.py` - this module should not
#     swallow exceptions from the model client.
#
# Example (commented):
#
#   class Reranker:
#       def __init__(self, model_name: str, top_n: int = 5): ...
#       async def rerank(
#           self, query: str, chunks: list[RetrievedChunk]
#       ) -> list[RetrievedChunk]: ...
