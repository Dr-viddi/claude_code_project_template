# Package marker for `agent`.
#
# The intelligence layer: the loop orchestrator, individual loop nodes, the
# pluggable LLM client, the tools the agent can invoke, and the prompt registry.
#
# Submodules:
#   graph.py      - the orchestrator (plan → act → observe), invoked by app/main
#   nodes.py      - individual loop steps (plan, act, observe, grading)
#   llm.py        - LLMClient protocol + offline default + real-provider implementations
#   tools/        - one file per tool (crm, web_search, code_search, ...)
#   prompts/      - versioned system prompts + per-intent templates
