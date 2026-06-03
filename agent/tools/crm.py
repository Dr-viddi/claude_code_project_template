# agent/tools/crm.py
#
# Purpose
#   Example *domain* tool - stands in for whatever business system the agent acts
#   on (CRM, ticketing, billing, internal API). Shows the shape every domain tool
#   should follow.
#
# When you want a file like this
#   When your agent needs to read or change state in a system you own (or a SaaS
#   you integrate with). Most "useful agent" projects need at least one of these.
#
# Why it matters
#   - Domain tools are where the agent stops being a chatbot and starts doing work.
#   - Co-locating reads and writes per system means audit/HITL/block decisions
#     have a clear scope ("the harness gates CRM writes, not CRM reads").
#   - An injected client lets tests use a fake; production wires the real client
#     once at startup.
#
# What goes in it
#   - A `CrmTool` class with:
#       * `name = "crm"` and a `description` precise enough for the planner/LLM
#         to know when to call it (and, importantly, when NOT to).
#       * Constructor taking an authenticated client (never built here).
#       * Async methods for supported operations, e.g. `get_customer(id)`,
#         `create_ticket(customer_id, summary)`.
#   - Strict argument validation - LLMs will pass malformed inputs.
#   - Writes/mutations gated by the harness control mode (contract.yaml).
#
# Example (commented)
#
#   class CrmTool:
#       name = "crm"
#       description = "Look up customers and manage support tickets in the CRM."
#       def __init__(self, client): self._client = client
#       async def get_customer(self, customer_id: str) -> dict: ...
#       async def create_ticket(self, customer_id: str, summary: str) -> dict: ...
