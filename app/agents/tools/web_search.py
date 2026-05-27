# app/agents/tools/web_search.py
#
# Intention:
#   Tool wrapper around an external web-search API (Tavily, Brave, Google CSE, ...).
#   Lets the agent loop pull in fresh facts that aren't in the corpus.
#
# What this file should contain:
#   - A `WebSearchTool` class with:
#       * Class attributes `name = "web_search"` and a clear `description`.
#       * Constructor taking an HTTP client and the provider API key.
#       * An async `__call__(query, k=5)` returning normalized results
#         (`{url, title, snippet}`).
#   - Timeouts, retry-with-backoff, and a circuit breaker - this is the most
#     common source of pipeline latency spikes.
#   - Pass returned snippets through `app/security/content_filter.py` before
#     they enter the prompt.
#
# Example (commented):
#
#   class WebSearchTool:
#       name = "web_search"
#       description = "Search the public web for recent information."
#       def __init__(self, http_client, api_key: str): ...
#       async def __call__(self, query: str, k: int = 5) -> list[dict]: ...
