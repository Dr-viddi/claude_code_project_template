"""Intent classification.

The default classifier is a transparent heuristic so it runs offline and is easy to
test. Swap ``classify`` for a small model or an LLM call when you need nuance - the
``Intent`` contract stays the same.
"""

from __future__ import annotations

from enum import StrEnum

from app.models import Message

_INJECTION_MARKERS = ("ignore previous instructions", "disregard the above", "system prompt")
_TOOL_HINTS = ("search", "look up", "find", "latest", "customer", "ticket", "code")
_CHITCHAT = ("hi", "hello", "hey", "thanks", "thank you", "bye")


class Intent(StrEnum):
    CHITCHAT = "chitchat"
    QA = "qa"
    TASK = "task"
    REFUSE = "refuse"


class Classifier:
    async def classify(self, query: str, history: list[Message] | None = None) -> Intent:
        q = query.lower().strip()
        if any(marker in q for marker in _INJECTION_MARKERS):
            return Intent.REFUSE
        if q in _CHITCHAT or any(q.startswith(c + " ") for c in _CHITCHAT):
            return Intent.CHITCHAT
        if any(hint in q for hint in _TOOL_HINTS):
            return Intent.TASK
        return Intent.QA
