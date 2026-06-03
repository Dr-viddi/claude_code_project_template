"""The agent orchestrator.

A small, hand-rolled plan -> act -> observe loop that wires routing, tools, memory,
the prompt, and the security harness together. It is a dependency-free stand-in for
a LangGraph ``StateGraph`` - install the ``langgraph`` extra and port ``ainvoke`` to a
compiled graph when you outgrow it. The public surface (``Agent.ainvoke``) stays the
same either way.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from agent.llm import LLMClient, build_llm
from agent.nodes import AgentState, act, observe, plan, should_continue
from agent.prompts.system import get_system
from agent.tools import CodeSearchTool, CrmTool, Tool, WebSearchTool
from app.config import Settings
from app.models import ChatRequest, ChatResponse, Message
from memory.conversation import ConversationStore
from memory.long_term import LongTermMemory
from memory.semantic_cache import SemanticCache
from observability import tracer
from routing.classifier import Classifier, Intent
from security import Harness
from security import init as init_harness


@dataclass
class AgentDeps:
    llm: LLMClient
    tools: dict[str, Tool]
    classifier: Classifier
    conversation: ConversationStore
    cache: SemanticCache
    long_term: LongTermMemory
    harness: Harness
    system_prompt: str
    max_steps: int = 4
    extra: dict[str, object] = field(default_factory=dict)


class Agent:
    def __init__(self, deps: AgentDeps) -> None:
        self.deps = deps

    @classmethod
    def build(cls, settings: Settings, harness: Harness | None = None) -> Agent:
        tools: dict[str, Tool] = {
            t.name: t for t in (WebSearchTool(), CodeSearchTool("."), CrmTool())
        }
        deps = AgentDeps(
            llm=build_llm(settings),
            tools=tools,
            classifier=Classifier(),
            conversation=ConversationStore(),
            cache=SemanticCache(),
            long_term=LongTermMemory(),
            harness=harness
            or init_harness(settings.contract_path, enabled=settings.harness_enabled),
            system_prompt=get_system().text,
            max_steps=settings.max_agent_steps,
        )
        return cls(deps)

    async def ainvoke(self, request: ChatRequest) -> ChatResponse:
        trace_id = uuid4().hex
        session_id = str(request.session_id)
        query = request.messages[-1].content if request.messages else ""

        with tracer.span("agent", trace_id=trace_id):
            cached = await self.deps.cache.get(query)
            if cached is not None:
                return ChatResponse(session_id=request.session_id, answer=cached, trace_id=trace_id)

            intent = await self.deps.classifier.classify(
                query, await self.deps.conversation.load(session_id)
            )
            state = AgentState(query=query, intent=intent.value)

            if intent is Intent.REFUSE:
                await observe(self.deps, state)
            else:
                while should_continue(self.deps, state):
                    plan(self.deps, state)
                    await act(self.deps, state)
                    if state.next_tool is None:
                        await observe(self.deps, state)

            answer = state.answer or ""
            await self.deps.conversation.append(session_id, Message(role="user", content=query))
            await self.deps.conversation.append(
                session_id, Message(role="assistant", content=answer)
            )
            await self.deps.cache.put(query, answer)

        return ChatResponse(
            session_id=request.session_id,
            answer=answer,
            tools_used=state.tools_used,
            trace_id=trace_id,
        )
