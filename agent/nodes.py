# agent/nodes.py
#
# Purpose
#   The individual steps of the agent loop defined in graph.py. Each node is a
#   small function `(deps, state) -> state_delta`. Keeping them in one module
#   makes the graph wiring readable and lets each node be tested in isolation.
#
# When you want a file like this
#   Whenever your agent loop has more than 2-3 distinct steps. Separating "what
#   the steps do" from "how they're wired" pays off the first time you need to
#   reorder, A/B test, or replace a step.
#
# Why it matters
#   - Pure-ish functions (no I/O except through `deps`) are easy to unit-test
#     with stubbed deps.
#   - Each node opens a tracing span via observability/tracer, so you get
#     per-step timing and cost without changing callers.
#   - `should_continue` lives next to the other nodes so the loop's exit
#     condition is one quick read away.
#
# What goes in it (typical agentic loop)
#   - `AgentState` dataclass: query, intent, scratchpad, tools_used, answer,
#     steps, next_tool, next_args.
#   - `plan(deps, state)`     - decide the next action (pick a tool or finish).
#   - `act(deps, state)`      - gate the tool call through the harness, execute it,
#                               append result to scratchpad.
#   - `observe(deps, state)`  - compose an answer from query + scratchpad.
#                               Short-circuits to a refusal message when intent==REFUSE.
#   - `should_continue(deps, state)` - bounded by `deps.max_steps`.
#
# Example (commented)
#
#   async def act(deps, state) -> None:
#       if state.next_tool is None:
#           return
#       tool = deps.tools[state.next_tool]
#       with tracer.span("act", tool=tool.name):
#           deps.harness.gate(tool.name, state.next_args)   # raises in block/HITL
#           result = await tool(**state.next_args)
#       state.scratchpad.append({"tool": tool.name, "result": result})
#       state.tools_used.append(tool.name)
#       state.next_tool, state.next_args = None, {}
