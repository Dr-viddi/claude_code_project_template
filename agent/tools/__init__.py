# Package marker for `agent.tools`.
#
# Each tool is a small class with `name`, `description`, and an async `__call__`
# (the agent's planner uses `description` to decide when to invoke it). The `act`
# node dispatches to them; the harness gates each call before it executes.
#
# Tools are the ONLY place the agent reaches external systems. Keeping them
# isolated here makes the security boundary obvious: anything outside this
# directory has no network, no filesystem-write, no DB-mutation surface.
#
# Conventions for adding a tool
#   - One file per tool. Name = filename = `name` class attribute.
#   - Validate arguments at the boundary (LLMs pass malformed inputs).
#   - Use a strict timeout and a circuit breaker on any external call.
#   - Treat tool output as UNTRUSTED before it influences the next action.
#   - List the tool in `security/contract.yaml` `scope.allowed_tools`.
