"""Tests for query_router and adaptive_router."""

from __future__ import annotations

from app.services.query_router import Route


def test_route_enum_values():
    assert Route.RAG.value == "rag"
    assert Route.AGENT.value == "agent"
    assert Route.DIRECT.value == "direct"
    assert Route.REFUSE.value == "refuse"
