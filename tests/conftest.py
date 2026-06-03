# tests/conftest.py
#
# Purpose
#   Shared pytest fixtures. Scoped narrowly per .claude/rules/testing.md -
#   prefer function-scoped unless setup is genuinely expensive.
#
# When you want a file like this
#   Every project with more than a handful of tests. As soon as two tests
#   construct the same fake, hoist it into a fixture.
#
# Why it matters
#   - Fixtures eliminate "construct the same fake LLM client at the top of
#     every test" duplication.
#   - Narrow scopes (function > module > session) keep tests independent.
#   - Mocking AT THE BOUNDARY (LLM client, harness backend, HTTP client) -
#     never your own services - keeps the fakes honest.
#
# What goes in it (typical)
#   - `fake_llm`        - deterministic LLM client stub. Mock at the boundary,
#                         never inside the agent's own modules.
#   - `fake_redis`      - in-memory Redis (e.g. `fakeredis`) for memory tests.
#   - `fake_deps`       - bundle of stubbed deps for building the agent graph.
#   - `harness_disabled`- forces the security harness into audit-only mode so
#                         tests never depend on the vendor backend.
#   - HTTP fixture via `respx` / `vcr.py` for recorded responses - no live network.
#
# Example (commented)
#
#   @pytest.fixture
#   def fake_llm():
#       class _FakeLLM:
#           async def complete(self, system: str, user: str) -> str:
#               return f"stub for: {user[:40]}"
#       return _FakeLLM()
