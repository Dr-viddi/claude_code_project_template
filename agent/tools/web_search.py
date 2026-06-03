# agent/tools/web_search.py
#
# Purpose
#   Live web retrieval tool. Lets the agent pull in fresh facts that aren't in the
#   corpus or your domain systems. Wraps an external search provider (Tavily,
#   Brave, Google CSE, ...).
#
# When you want a file like this
#   Any agent that needs current information (news, prices, releases) or that
#   answers questions outside a private corpus.
#
# Why it matters
#   - Without timeouts/retries/circuit-breakers, web calls are the #1 source of
#     agent latency spikes and outages.
#   - Returned text is UNTRUSTED. Indirect prompt-injection lives in real-world
#     search results, so this is exactly where the harness's content checks earn
#     their keep.
#   - An injected `fetch` lets tests run without network (recorded responses or
#     a canned stub).
#
# What goes in it
#   - A `WebSearchTool` class with:
#       * `name = "web_search"` and a `description` the planner uses.
#       * Constructor taking an HTTP client or a `fetch` callable + provider key.
#       * Async `__call__(query, k=5)` returning normalized results
#         (`{url, title, snippet}`).
#   - Hard timeout (e.g. 5s), bounded retries with backoff, breaker on repeated
#     failure - this is the most common cause of agent latency spikes.
#   - Bound `k` (e.g. cap at 25) - LLMs request silly values.
#   - Pass returned snippets through the harness content checks before they
#     enter the next prompt.
#
# Example (commented)
#
#   class WebSearchTool:
#       name = "web_search"
#       description = "Search the public web for recent information."
#       def __init__(self, fetch=None): self._fetch = fetch
#       async def __call__(self, query: str, k: int = 5) -> list[dict]: ...
