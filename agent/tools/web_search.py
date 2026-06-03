# agent/tools/web_search.py
#
# Intention:
#   Live web retrieval tool. Lets the agent pull in fresh facts that aren't in the
#   corpus or domain systems. Wraps an external search provider (Tavily, Brave,
#   Google CSE, ...).
#
# What this file should contain:
#   - A `WebSearchTool` class with:
#       * `name = "web_search"` and a clear `description`.
#       * Constructor taking an HTTP client and the provider API key.
#       * An async `__call__(query, k=5)` returning normalized results
#         (`{url, title, snippet}`).
#   - Timeout, retry-with-backoff, and a circuit breaker - web calls are the most
#     common source of agent latency spikes.
#   - Treat returned text as UNTRUSTED: it flows through the security harness
#     (PII scrub / injection analysis) before it can influence a tool call.
#
# Example (commented):
#
#   class WebSearchTool:
#       name = "web_search"
#       description = "Search the public web for recent information."
#       def __init__(self, http_client, api_key: str): ...
#       async def __call__(self, query: str, k: int = 5) -> list[dict]: ...
