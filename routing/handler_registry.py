"""Map an intent to the handler that serves it, with a safe fallback.

Decouples "what the user wants" from "which code runs": adding a capability is a
``register`` call, not a change to the router.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable

from routing.classifier import Intent

Handler = Callable[..., Awaitable[object]]


class HandlerRegistry:
    def __init__(self, fallback: Handler) -> None:
        self.fallback = fallback
        self._handlers: dict[Intent, Handler] = {}

    def register(self, intent: Intent, handler: Handler) -> None:
        self._handlers[intent] = handler

    def resolve(self, intent: Intent) -> Handler:
        return self._handlers.get(intent, self.fallback)
