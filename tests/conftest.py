"""Shared pytest fixtures."""

from __future__ import annotations

import pytest


@pytest.fixture
def fake_llm():
    """Replace with a deterministic stub matching your LLM client interface."""

    class _FakeLLM:
        async def complete(self, prompt: str) -> str:
            return f"stub response for: {prompt[:40]}"

    return _FakeLLM()
