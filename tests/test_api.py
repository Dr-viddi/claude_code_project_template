"""HTTP surface: status codes and response envelope via FastAPI's TestClient."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_healthz(client: TestClient):
    resp = client.get("/healthz")

    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_readyz(client: TestClient):
    resp = client.get("/readyz")

    assert resp.status_code == 200
    assert resp.json()["status"] == "ready"


def test_chat_returns_answer_and_trace(client: TestClient):
    resp = client.post("/v1/chat", json={"messages": [{"role": "user", "content": "hello"}]})

    assert resp.status_code == 200
    body = resp.json()
    assert body["answer"]
    assert body["trace_id"]
