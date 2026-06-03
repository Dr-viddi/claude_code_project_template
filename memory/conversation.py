"""Short-term per-session memory: a sliding window of recent turns.

Default backend is an in-process dict so the template runs with no Redis. For
production, back ``_store`` with Redis (lists + TTL) - the interface stays the same.
"""

from __future__ import annotations

from collections import defaultdict

from app.models import Message


class ConversationStore:
    def __init__(self, max_turns: int = 20) -> None:
        self._max_turns = max_turns
        self._store: dict[str, list[Message]] = defaultdict(list)

    async def load(self, session_id: str) -> list[Message]:
        return list(self._store[session_id])

    async def append(self, session_id: str, message: Message) -> None:
        window = self._store[session_id]
        window.append(message)
        if len(window) > self._max_turns:
            del window[: len(window) - self._max_turns]
