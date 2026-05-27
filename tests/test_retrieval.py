# tests/test_retrieval.py
#
# Intention:
#   Unit tests for `app/components/hybrid_retriever.py` and `reranker.py`.
#   Verify code correctness (fusion math, top-N truncation, error paths);
#   verify *quality* via `evaluation/` not here.
#
# What this file should contain:
#   - Tests for the fused-score calculation across edge cases (zeros, ties).
#   - Tests for behavior when one backend errors (timeout, empty result).
#   - Tests for reranker top-N truncation and stable ordering.
#   - Naming: `test_<unit>_<scenario>_<expected>`, e.g.
#     `test_hybrid_retriever_empty_query_returns_empty_list`.
#   - No network. Mock the backends.
#
# Example (commented):
#
#   def test_fused_score_averages_dense_and_sparse():
#       chunk = RetrievedChunk(doc_id="d1", text="x", dense_score=0.8, sparse_score=0.4)
#       assert chunk.fused_score == pytest.approx(0.6)
