# tests/conftest.py
#
# Intention:
#   Shared pytest fixtures. Scoped narrowly per `.claude/rules/testing.md` -
#   prefer function-scoped fixtures unless setup is genuinely expensive.
#
# What this file should contain:
#   - `fake_llm`        - deterministic stub of the LLM client. Mock at the boundary,
#                         never your own nodes/services.
#   - `fake_redis`      - in-memory Redis (e.g. `fakeredis`) for memory tests
#                         (conversation window, semantic cache).
#   - `fake_deps`       - a bundle of stubbed dependencies for building the agent
#                         graph in `test_agent.py` (llm, tools, memory, router).
#   - `harness_disabled`- forces the security harness into audit-only/no-op mode so
#                         tests never touch the vendor backend.
#   - HTTP fixture via `respx` / `vcr.py` for recorded responses - no live network.
#
# Example (commented):
#
#   @pytest.fixture
#   def fake_llm():
#       class _FakeLLM:
#           async def complete(self, prompt: str) -> str:
#               return f"stub response for: {prompt[:40]}"
#       return _FakeLLM()
#
#   @pytest.fixture
#   def harness_disabled(monkeypatch):
#       monkeypatch.setenv("ADRIAN_ENABLED", "0")
