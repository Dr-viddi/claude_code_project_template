"""Long-term memory: episodic recall + an entity store, persisted across sessions.

In-memory by default. For production, back both stores with a durable DB
(Postgres + pgvector for episodes, a table/keyspace for entities). Scrub PII per
the harness policy before persisting.
"""

from __future__ import annotations

from typing import Any


class LongTermMemory:
    def __init__(self) -> None:
        self._episodes: list[dict[str, Any]] = []
        self._entities: dict[str, dict[str, Any]] = {}

    async def remember_episode(self, session_id: str, summary: str) -> None:
        self._episodes.append({"session_id": session_id, "summary": summary})

    async def recall_episodes(self, query: str, k: int = 5) -> list[dict[str, Any]]:
        needle = query.lower()
        scored = [e for e in self._episodes if needle in e["summary"].lower()]
        return scored[:k]

    async def upsert_entity(self, entity_id: str, attributes: dict[str, Any]) -> None:
        self._entities.setdefault(entity_id, {}).update(attributes)

    async def get_entity(self, entity_id: str) -> dict[str, Any] | None:
        return self._entities.get(entity_id)
