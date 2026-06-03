# agent/nodes.py
#
# Intention:
#   The individual steps of the agent graph defined in `graph.py`. Each node is a
#   pure-ish function `(state) -> state_delta`. Keeping them in one module makes
#   the graph wiring readable and the nodes independently testable.
#
# What this file should contain (typical agentic loop):
#   - `plan(state)`     - decide the next action from the current state. Folds in
#                         the old "query_decomposer" idea: a plan may be several
#                         sub-steps.
#   - `act(state)`      - execute the chosen tool call(s) from `agent/tools/`.
#   - `observe(state)`  - inspect tool results, update the scratchpad. Folds in the
#                         old "document_grader" idea: grade/keep only useful results.
#   - `should_continue(state)` - conditional-edge predicate: loop again or finish.
#   - Optional `rewrite(state)` - normalize the user query before planning (the old
#                         "query_rewriter" concern) if you don't do it in routing.
#
# Conventions:
#   - Nodes never call the LLM directly with inline prompts - pull them from
#     `agent/prompts/`.
#   - Nodes never reach the network except through a tool in `agent/tools/`.
#   - Each node opens a tracing span and records token cost.
#
# Example (commented):
#
#   async def plan(state: AgentState) -> dict:
#       prompt = SYSTEM_PLAN.render(goal=state["messages"][-1].content)
#       decision = await llm.complete(prompt)
#       return {"scratchpad": state["scratchpad"] + [decision]}
#
#   async def act(state: AgentState) -> dict: ...
#   async def observe(state: AgentState) -> dict: ...
#   def should_continue(state: AgentState) -> str:
#       return "done" if state.get("answer") else "loop"
