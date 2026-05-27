# tests/conftest.py
#
# Intention:
#   Shared pytest fixtures. Scoped narrowly per `.claude/rules/testing.md` -
#   prefer function-scoped fixtures unless setup is genuinely expensive.
#
# What this file should contain:
#   - A `fake_llm` fixture returning a deterministic stub of whatever LLM client
#     the project uses. Mock at the boundary, never your own services.
#   - A `fake_vector_store` fixture with a small in-memory corpus.
#   - A `fake_redis` fixture (e.g. `fakeredis`) for cache + conversation tests.
#   - HTTP fixture using `respx` / `vcr.py` for recorded responses - no network
#     in unit tests.
#
# Example (commented):
#
#   @pytest.fixture
#   def fake_llm():
#       class _FakeLLM:
#           async def complete(self, prompt: str) -> str:
#               return f"stub response for: {prompt[:40]}"
#       return _FakeLLM()
