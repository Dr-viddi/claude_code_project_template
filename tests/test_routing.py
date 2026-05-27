# tests/test_routing.py
#
# Intention:
#   Unit tests for `app/services/query_router.py` and `app/agents/adaptive_router.py`.
#   Verify that each route value is reachable, deterministic given a fixed LLM,
#   and that refusal paths short-circuit downstream stages.
#
# What this file should contain:
#   - Enum-value assertions for `Route` (RAG, AGENT, DIRECT, REFUSE).
#   - Tests using `fake_llm` from `conftest.py` with stubbed classifications.
#   - A test that adaptive_router never picks a disabled tool.
#
# Example (commented):
#
#   def test_route_enum_values():
#       assert Route.RAG.value == "rag"
#       assert Route.REFUSE.value == "refuse"
