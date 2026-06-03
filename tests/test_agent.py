# tests/test_agent.py
#
# Intention:
#   Unit tests for the agent graph (`agent/graph.py`), its nodes (`agent/nodes.py`),
#   and memory integration (`memory/`). Verify control flow and state transitions;
#   verify answer *quality* via `evaluation/` not here.
#
# What this file should contain:
#   - Graph construction tests: nodes registered, entry point set, terminal edge
#     reachable.
#   - Node tests with `fake_llm` from `conftest.py`: `plan` produces a plan,
#     `observe` filters junk, `should_continue` ends on an answer.
#   - A loop-termination test: the graph must not spin forever (cap iterations).
#   - Memory round-trip: conversation window load/append; semantic-cache hit/miss
#     using the `fake_redis` fixture.
#   - Naming: `test_<unit>_<scenario>_<expected>`. No network.
#
# Example (commented):
#
#   def test_graph_has_entry_point_and_terminates():
#       graph = build_graph(deps=fake_deps())
#       assert graph.entry_point == "plan"
#
#   @pytest.mark.asyncio
#   async def test_should_continue_ends_when_answer_present():
#       assert should_continue({"answer": "done"}) == "done"
