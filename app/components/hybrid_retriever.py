# app/components/hybrid_retriever.py
#
# Intention:
#   Combine dense (vector) and sparse (BM25 / keyword) search to return a single
#   ranked candidate list. Hybrid retrieval recovers from cases where pure-vector
#   misses exact terms (codes, product IDs) and where pure-keyword misses paraphrases.
#
# What this file should contain:
#   - A `RetrievedChunk` dataclass: doc_id, text, dense_score, sparse_score, plus
#     a fused score (e.g. Reciprocal Rank Fusion, or weighted average).
#   - A `HybridRetriever` class with:
#       * Constructor taking a dense backend, a sparse backend, and a top-k.
#       * An async `retrieve(query)` method that runs both backends in parallel
#         and merges results.
#   - Pluggable fusion strategy (RRF, weighted-sum, learned).
#
# Example (commented):
#
#   @dataclass
#   class RetrievedChunk:
#       doc_id: str
#       text: str
#       dense_score: float
#       sparse_score: float
#       @property
#       def fused_score(self) -> float:
#           return 0.5 * self.dense_score + 0.5 * self.sparse_score
#
#   class HybridRetriever:
#       def __init__(self, dense, sparse, k: int = 20): ...
#       async def retrieve(self, query: str) -> list[RetrievedChunk]: ...
