# memory/long_term.py
#
# Intention:
#   Long-term memory that persists across sessions. Two complementary stores:
#     - Episodic: notable past interactions ("what happened"), retrievable by
#       similarity so the agent can recall prior episodes.
#     - Entity: a structured store of facts about users/objects ("what we know"),
#       keyed by entity id and updated over time.
#
# What this file should contain:
#   - A `LongTermMemory` class with:
#       * `remember_episode(session_id, summary, embedding)` -> persist an episode.
#       * `recall_episodes(query, k)` -> similar past episodes.
#       * `upsert_entity(entity_id, attributes)` -> merge new facts.
#       * `get_entity(entity_id)` -> stored facts.
#   - Backed by a durable store (Postgres + pgvector, or a dedicated memory DB).
#   - Writes should pass through the security harness PII policy before persistence.
#
# Example (commented):
#
#   class LongTermMemory:
#       def __init__(self, db): ...
#       async def remember_episode(self, session_id: str, summary: str, embedding: list[float]) -> None: ...
#       async def recall_episodes(self, query: str, k: int = 5) -> list[dict]: ...
#       async def upsert_entity(self, entity_id: str, attributes: dict) -> None: ...
#       async def get_entity(self, entity_id: str) -> dict | None: ...
