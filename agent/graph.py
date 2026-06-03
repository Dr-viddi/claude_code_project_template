# agent/graph.py
#
# Purpose
#   The agent orchestrator. Wires routing + tools + memory + prompts + the security
#   harness into a bounded plan → act → observe loop. Exposes a single public
#   surface (`Agent.ainvoke(request)`) that app/main.py calls.
#
# When you want a file like this
#   Any agent that does more than a single LLM call. As soon as the agent has to
#   choose between tools or iterate, you want an explicit orchestrator rather
#   than nested if-statements in a route handler.
#
# Why it matters
#   - One bounded loop = predictable latency + cost. The max-steps guard prevents
#     runaway agents from looping forever.
#   - The orchestrator is the right place to wrap memory reads/writes, cache
#     lookups, and the harness gate around tool calls.
#   - A `from_settings` / `build` factory means tests can inject fakes for every
#     dependency without monkey-patching.
#
# What goes in it
#   - An `AgentDeps` dataclass bundling the dependencies (llm, tools, classifier,
#     memory, harness, max_steps).
#   - An `Agent` class with:
#       * `build(settings, harness=None)` - construct concrete impls from Settings.
#       * `ainvoke(request)` - one turn: classify → cache check → loop → memory
#         write → response. Refusal short-circuits before the loop runs.
#   - LangGraph note: this hand-rolled loop is a stand-in for a `StateGraph`. The
#     public surface (`ainvoke`) stays the same when you port - see ADR-0001.
#
# Example (commented)
#
#   @dataclass
#   class AgentDeps:
#       llm: LLMClient
#       tools: dict[str, Tool]
#       classifier: Classifier
#       conversation: ConversationStore
#       cache: SemanticCache
#       long_term: LongTermMemory
#       harness: Harness
#       system_prompt: str
#       max_steps: int = 4
#
#   class Agent:
#       def __init__(self, deps: AgentDeps): self.deps = deps
#
#       @classmethod
#       def build(cls, settings, harness=None) -> "Agent": ...
#
#       async def ainvoke(self, req: ChatRequest) -> ChatResponse:
#           # 1. cache hit? short-circuit
#           # 2. classify intent (chitchat / qa / task / refuse)
#           # 3. loop: plan → act (harness-gated) → observe, bounded by max_steps
#           # 4. write conversation + cache
#           # 5. return ChatResponse with trace_id, tools_used, answer
#           ...
