# agent/tools/crm.py
#
# Intention:
#   Example *domain* tool - stands in for whatever business system the agent acts
#   on (CRM, ticketing, billing, internal API). Shows the shape every domain tool
#   should follow. Replace with your real integration(s).
#
# What this file should contain:
#   - A `CrmTool` class with:
#       * `name = "crm"` and a `description` precise enough for the planner/LLM to
#         know when to call it (and, importantly, when NOT to).
#       * Constructor taking an authenticated client (injected, never built here).
#       * Async methods for the supported operations, e.g.
#         `get_customer(customer_id)`, `create_ticket(...)`.
#   - Strict argument validation - the LLM will pass malformed inputs.
#   - Writes/mutations should be gated by the security harness control mode
#     (see `security/contract.yaml`): audit / human-in-the-loop / block.
#
# Example (commented):
#
#   class CrmTool:
#       name = "crm"
#       description = "Look up customers and manage support tickets in the CRM."
#       def __init__(self, client): ...
#       async def get_customer(self, customer_id: str) -> dict: ...
#       async def create_ticket(self, customer_id: str, summary: str) -> dict: ...
