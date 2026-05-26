"""Pluggable tool: web search via a configured provider (e.g. Tavily, Brave)."""

from __future__ import annotations


class WebSearchTool:
    name = "web_search"
    description = "Search the public web for recent information."

    def __init__(self, http_client, api_key: str) -> None:
        self._http = http_client
        self._api_key = api_key

    async def __call__(self, query: str, k: int = 5) -> list[dict]:
        raise NotImplementedError
