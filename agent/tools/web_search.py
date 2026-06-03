"""Live web retrieval tool.

The default implementation returns canned results so the template runs offline and
tests stay deterministic. Pass a ``fetch`` coroutine (wrapping Tavily/Brave/etc.)
to make it real. Treat all returned text as UNTRUSTED - the harness inspects it
before it can influence the next action.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable

FetchFn = Callable[[str, int], Awaitable[list[dict[str, str]]]]


class WebSearchTool:
    name = "web_search"
    description = "Search the public web for recent information."

    def __init__(self, fetch: FetchFn | None = None) -> None:
        self._fetch = fetch

    async def __call__(self, query: str, k: int = 5) -> list[dict[str, str]]:
        if not query or not query.strip():
            from agent.tools import ToolError

            raise ToolError("web_search requires a non-empty query")
        k = max(1, min(k, 25))
        if self._fetch is not None:
            return await self._fetch(query, k)
        return [
            {
                "url": f"https://example.com/result/{i}",
                "title": f"Stub result {i} for {query!r}",
                "snippet": f"Canned snippet {i}. Wire a real provider via `fetch=`.",
            }
            for i in range(1, k + 1)
        ]
