# agent/graph.py
#
# Intention:
#   Define the agent as a state machine (LangGraph `StateGraph` or equivalent).
#   This is the top-level orchestrator for a single turn - it wires the nodes in
#   `nodes.py` into a graph with conditional edges, and exposes a single entry
#   point that `app/main.py` calls. Replaces the linear "rag_pipeline" with an
#   explicit plan/act/observe loop that can branch, retry, and self-correct.
#
# What this file should contain:
#   - A typed `AgentState` (TypedDict / pydantic) carrying the conversation,
#     scratchpad, tool results, intent, and accumulated trace.
#   - A `build_graph(...)` factory that:
#       * Registers nodes from `agent.nodes` (plan, act, observe, ...).
#       * Adds conditional edges (e.g. observe -> plan to loop, or -> END).
#       * Wires in memory (`memory/`), routing (`routing/`), and the security
#         harness (`security/adrian_init.py`) at the right points.
#       * Compiles and returns the runnable graph.
#   - Every node transition opens a span via `observability/tracer.py`.
#
# Example (commented):
#
#   from typing import TypedDict
#   from langgraph.graph import StateGraph, END
#
#   class AgentState(TypedDict):
#       messages: list
#       intent: str | None
#       scratchpad: list
#       tool_results: list
#
#   def build_graph(deps) -> "CompiledGraph":
#       g = StateGraph(AgentState)
#       g.add_node("plan", deps.plan)
#       g.add_node("act", deps.act)
#       g.add_node("observe", deps.observe)
#       g.set_entry_point("plan")
#       g.add_edge("plan", "act")
#       g.add_edge("act", "observe")
#       g.add_conditional_edges("observe", deps.should_continue, {"loop": "plan", "done": END})
#       return g.compile()
