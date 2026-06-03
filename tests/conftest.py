"""Shared pytest fixtures. Everything runs offline: EchoLLM, in-memory stores,
audit-mode harness. No network, no API key, no external services."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from agent.graph import Agent
from app.config import Settings
from app.main import app


@pytest.fixture
def settings() -> Settings:
    return Settings(llm_provider="echo", harness_enabled=True, control_mode="audit")


@pytest.fixture
def agent(settings: Settings) -> Agent:
    return Agent.build(settings)


@pytest.fixture
def client() -> TestClient:
    # TestClient runs the lifespan, so app.state.agent is built.
    with TestClient(app) as c:
        yield c
