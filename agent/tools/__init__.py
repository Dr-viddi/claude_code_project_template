"""Agent tools - the only place the agent reaches external systems.

Every tool exposes ``name``, ``description``, and an async ``__call__``. The ``act``
node dispatches to them; the planner/router decides which to call. Tool calls are
gated by the security harness before they execute.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


class ToolError(Exception):
    """Raised when a tool's arguments are invalid or its backend fails."""


@runtime_checkable
class Tool(Protocol):
    name: str
    description: str

    async def __call__(self, *args: Any, **kwargs: Any) -> Any: ...


from agent.tools.code_search import CodeSearchTool  # noqa: E402
from agent.tools.crm import CrmTool  # noqa: E402
from agent.tools.web_search import WebSearchTool  # noqa: E402

__all__ = ["Tool", "ToolError", "CodeSearchTool", "CrmTool", "WebSearchTool"]
