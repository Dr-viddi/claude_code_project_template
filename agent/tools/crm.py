"""Example domain tool: a CRM. In-memory fake so the template runs with no backend.

Replace ``_FAKE_CUSTOMERS`` and the method bodies with calls to your real system
(an authenticated client injected via the constructor). Mutations should be gated
by the harness control mode (see security/contract.yaml).
"""

from __future__ import annotations

from typing import Any
from uuid import uuid4

_FAKE_CUSTOMERS: dict[str, dict[str, Any]] = {
    "cus_001": {"id": "cus_001", "name": "Ada Lovelace", "plan": "pro"},
    "cus_002": {"id": "cus_002", "name": "Alan Turing", "plan": "free"},
}


class CrmTool:
    name = "crm"
    description = "Look up customers and open support tickets in the CRM."

    def __init__(self, customers: dict[str, dict[str, Any]] | None = None) -> None:
        self._customers = dict(_FAKE_CUSTOMERS if customers is None else customers)
        self._tickets: list[dict[str, Any]] = []

    async def get_customer(self, customer_id: str) -> dict[str, Any]:
        if customer_id not in self._customers:
            from agent.tools import ToolError

            raise ToolError(f"unknown customer: {customer_id}")
        return self._customers[customer_id]

    async def create_ticket(self, customer_id: str, summary: str) -> dict[str, Any]:
        await self.get_customer(customer_id)  # validates existence
        ticket = {"id": f"tkt_{uuid4().hex[:8]}", "customer_id": customer_id, "summary": summary}
        self._tickets.append(ticket)
        return ticket

    async def __call__(self, customer_id: str) -> dict[str, Any]:
        return await self.get_customer(customer_id)
