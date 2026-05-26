"""Tests for hybrid_retriever + reranker."""

from __future__ import annotations

import pytest

from app.components.hybrid_retriever import RetrievedChunk


def test_fused_score_averages_dense_and_sparse():
    chunk = RetrievedChunk(doc_id="d1", text="hello", dense_score=0.8, sparse_score=0.4)
    assert chunk.fused_score == pytest.approx(0.6)
