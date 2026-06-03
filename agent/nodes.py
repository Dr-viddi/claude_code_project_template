"""The steps of the agent loop: plan -> act -> observe.

Each node mutates an ``AgentState``. The planner here is a transparent heuristic so
the template runs offline and deterministically; replace it with an LLM-driven
planner (tool-calling) for real work. The graph in ``graph.py`` wires these together
and enforces the iteration cap.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from observability import tracer

if TYPE_CHECKING:
    from agent.graph import AgentDeps


@dataclass
class AgentState:
    query: str
    intent: str
    scratchpad: list[dict[str, Any]] = field(default_factory=list)
    tools_used: list[str] = field(default_factory=list)
    answer: str | None = None
    steps: int = 0
    next_tool: str | None = None
    next_args: dict[str, Any] = field(default_factory=dict)


def plan(deps: AgentDeps, state: AgentState) -> None:
    """Decide the next action: pick a tool, or signal ready-to-answer (next_tool=None)."""
    state.steps += 1
    q = state.query.lower()

    if state.tools_used or state.intent in {"chitchat", "qa"}:
        state.next_tool = None  # enough context; answer next
        return

    if any(k in q for k in ("search", "find", "latest", "look up")):
        state.next_tool, state.next_args = "web_search", {"query": state.query, "k": 3}
    elif "code" in q:
        state.next_tool, state.next_args = "code_search", {"pattern": _extract_pattern(state.query)}
    else:
        state.next_tool = None


async def act(deps: AgentDeps, state: AgentState) -> None:
    """Gate the chosen tool through the harness, then execute it."""
    if state.next_tool is None:
        return
    tool = deps.tools[state.next_tool]
    with tracer.span("act", tool=tool.name):
        deps.harness.gate(tool.name, state.next_args)  # raises in block / HITL mode
        result = await tool(**state.next_args)
    state.scratchpad.append({"tool": tool.name, "result": result})
    state.tools_used.append(tool.name)
    state.next_tool, state.next_args = None, {}


async def observe(deps: AgentDeps, state: AgentState) -> None:
    """Produce an answer from the query + scratchpad once we have enough."""
    if state.intent == "refuse":
        state.answer = "I can't help with that request."
        return
    context = "\n".join(str(item["result"]) for item in state.scratchpad)
    state.answer = await deps.llm.complete(
        system=deps.system_prompt, user=_compose(state.query, context)
    )


def should_continue(deps: AgentDeps, state: AgentState) -> bool:
    return state.answer is None and state.steps < deps.max_steps


def _compose(query: str, context: str) -> str:
    return f"Context:\n{context}\n\nQuestion: {query}" if context else query


def _extract_pattern(query: str) -> str:
    tokens = [t for t in query.split() if t.lower() not in {"search", "the", "code", "for", "find"}]
    return tokens[-1] if tokens else query
