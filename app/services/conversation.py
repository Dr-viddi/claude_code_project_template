"""Conversation memory. Stores rolling message history per conversation_id."""

from __future__ import annotations

from uuid import UUID

from app.models import Message


class ConversationStore:
    def __init__(self, redis_url: str, max_turns: int = 20) -> None:
        self._redis_url = redis_url
        self._max_turns = max_turns

    async def load(self, conversation_id: UUID) -> list[Message]:
        raise NotImplementedError

    async def append(self, conversation_id: UUID, message: Message) -> None:
        raise NotImplementedError
