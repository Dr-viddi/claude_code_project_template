# Package marker for `agent.tools`.
#
# Each tool is a small class/callable with `name`, `description`, and an async
# `__call__` (or `invoke`). The `act` node in `agent/nodes.py` dispatches to them;
# `routing/` and the planner decide which to call. Tools are the ONLY place the
# agent reaches external systems, so every tool validates its arguments and runs
# behind a timeout.
#
# Files here mirror image 4's "Domain tools, live web retrieval, repo search (MCP)":
#   crm.py          - example domain/business tool
#   web_search.py   - live web retrieval
#   code_search.py  - repository search, typically wired through an MCP server
#
# Add a retrieval/rerank tool here if your agent does RAG-over-tools (a vector
# search tool that returns hybrid-ranked, reranked passages).
