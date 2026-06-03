# Package marker for `agent`.
#
# The agent core: a state-machine orchestrator (LangGraph or equivalent) plus the
# nodes, tools, and prompts it drives. This replaces the older RAG-pipeline
# orchestration - here the control flow is a graph of plan -> act -> observe steps
# rather than a linear pipeline.
#
# Submodules:
#   graph.py    - the state machine definition (nodes + edges + state schema)
#   nodes.py    - individual graph nodes (plan, act, observe, grade, decompose)
#   tools/      - callable tools the agent can invoke
#   prompts/    - versioned system prompts and per-intent templates
