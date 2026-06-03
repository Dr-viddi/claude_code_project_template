# tests/test_api.py
#
# Purpose
#   HTTP-surface tests via FastAPI's `TestClient`. Verify status codes, response
#   envelope shape, and that domain errors map to the documented codes.
#
# When you want a file like this
#   Any HTTP-fronted service. Three or four route-level tests catch most
#   regressions in the contract (which is what your clients depend on).
#
# Why it matters
#   - TestClient runs the FastAPI lifespan, so it exercises real startup
#     wiring - errors in app/main.py that unit tests miss show up here.
#   - One test per status-code path (200, 400, 403, 500) is the cheapest way
#     to lock the API contract.
#   - Errors mapped to the uniform envelope (.claude/rules/api-conventions.md)
#     stay consistent only if a test enforces it.
#
# What goes in it
#   - `/healthz` returns 200 + {"status": "ok"}.
#   - `/readyz` returns 200 once the lifespan completes.
#   - `/v1/chat` returns 200 with answer + trace_id on a happy path.
#   - One error-path test per documented error code (HARNESS_BLOCKED,
#     INTENT_REFUSED, TOOL_TIMEOUT, ...): assert status + envelope `code`.
#
# Example (commented)
#
#   def test_healthz(client):
#       resp = client.get("/healthz")
#       assert resp.status_code == 200 and resp.json() == {"status": "ok"}
#
#   def test_chat_returns_answer_and_trace(client):
#       resp = client.post("/v1/chat", json={"messages": [{"role": "user", "content": "hi"}]})
#       assert resp.status_code == 200
#       assert resp.json()["trace_id"]
