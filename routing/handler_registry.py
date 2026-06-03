# routing/handler_registry.py
#
# Intention:
#   Map an intent (from `classifier.py`) to the handler that serves it - a graph
#   entry point, a sub-graph, or a direct function. Decouples "what the user wants"
#   from "which code runs", so adding a new capability is a registry entry, not a
#   change to the router.
#
# What this file should contain:
#   - A `HandlerRegistry` class with:
#       * `register(intent, handler)` to bind an intent to a callable/sub-graph.
#       * `resolve(intent)` to fetch the handler (with a sensible default/fallback
#         handler for unknown intents).
#   - Handlers share a common async signature so the agent graph can call any of
#     them uniformly.
#   - Registration typically happens once at startup from `app/main.py`.
#
# Example (commented):
#
#   class HandlerRegistry:
#       def __init__(self): ...
#       def register(self, intent: Intent, handler: Handler) -> None: ...
#       def resolve(self, intent: Intent) -> Handler: ...
