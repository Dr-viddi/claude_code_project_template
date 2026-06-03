# tests/test_agent.py
#
# Purpose
#   Unit tests for the agent graph (agent/graph.py), its nodes (agent/nodes.py),
#   and memory integration (memory/). Verify control flow and state transitions.
#
# When you want a file like this
#   The agent loop is the single most consequential file in this kind of
#   project. It deserves its own focused test file.
#
# Why it matters
#   - The bounded loop guarantee (`max_steps` exit) is the property you most
#     want to never regress. Test it directly.
#   - Memory round-trips (conversation append/load, cache hit/miss) are the
#     other "did I wire this correctly?" tests that pay off forever.
#   - Verify CODE correctness here; verify ANSWER QUALITY in evaluation/, not here.
#
# What goes in it
#   - Graph construction tests: nodes registered, entry point set, terminal edge
#     reachable.
#   - Per-node tests with `fake_llm` from conftest: `plan` produces a plan,
#     `observe` filters junk, `should_continue` exits on an answer.
#   - A loop-termination test: the agent must not spin forever even with a
#     pathological query that keeps suggesting tool calls.
#   - Memory round-trip: window load/append; semantic-cache hit/miss using
#     `fake_redis`.
#
# Example (commented)
#
#   @pytest.mark.asyncio
#   async def test_should_continue_ends_when_answer_present():
#       state = AgentState(query="x", intent="qa")
#       state.answer = "done"
#       assert not should_continue(deps, state)
#
#   @pytest.mark.asyncio
#   async def test_loop_is_bounded_by_max_steps(agent):
#       resp = await agent.ainvoke(_req("Find and search and look up the latest code news"))
#       assert resp.answer  # terminated rather than spinning
