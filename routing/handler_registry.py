# routing/handler_registry.py
#
# Purpose
#   Map an intent (from classifier.py) to the handler that serves it - a graph
#   entry point, a sub-graph, or a direct function. Decouples "what the user
#   wants" from "which code runs", so adding a capability is a registry entry,
#   not a change to the router.
#
# When you want a file like this
#   When you have more than 2-3 intents OR you anticipate adding new ones
#   without touching the router. A static if/elif works at first; the registry
#   pays off as soon as different handlers come from different packages.
#
# Why it matters
#   - Open/closed principle: new capabilities register themselves, the router
#     never changes.
#   - A safe fallback handler turns "unknown intent" into a graceful degraded
#     response instead of a crash.
#   - Tests can register fakes per intent without monkey-patching the dispatch.
#
# What goes in it
#   - A `HandlerRegistry` class with:
#       * `register(intent, handler)` to bind an intent to a callable/sub-graph.
#       * `resolve(intent)` to fetch the handler (with a sensible fallback).
#   - Handlers share a common async signature so the agent graph can call any
#     of them uniformly.
#   - Registration happens once at startup from app/main.py.
#
# Example (commented)
#
#   Handler = Callable[..., Awaitable[object]]
#
#   class HandlerRegistry:
#       def __init__(self, fallback: Handler): self.fallback = fallback; self._h = {}
#       def register(self, intent: Intent, handler: Handler) -> None: ...
#       def resolve(self, intent: Intent) -> Handler: ...
