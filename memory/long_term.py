# memory/long_term.py
#
# Purpose
#   Long-term memory persisted across sessions. Two complementary stores:
#     - Episodic: notable past interactions ("what happened"), retrievable by
#       similarity so the agent can recall prior episodes.
#     - Entity: a structured store of facts about users/objects ("what we know"),
#       keyed by entity id and updated over time.
#
# When you want a file like this
#   When the agent should "remember you" across sessions: assistants, coaching
#   agents, internal copilots. Skip for stateless utility agents.
#
# Why it matters
#   - Differentiates a stateless chatbot from an actual assistant - "you told me
#     last week..." is the property users actually want.
#   - Splitting episodic (unstructured + searchable) from entity (structured +
#     keyed) avoids the mistake of cramming both into one bag.
#   - PII handling here is critical: long-term memory is the easiest place to
#     accidentally retain regulated data forever.
#
# What goes in it
#   - A `LongTermMemory` class with:
#       * `remember_episode(session_id, summary)` - persist an episode.
#       * `recall_episodes(query, k)` -> similar past episodes (vector search).
#       * `upsert_entity(entity_id, attributes)` -> merge new facts.
#       * `get_entity(entity_id)` -> stored facts.
#   - Backed by a durable store (Postgres + pgvector for episodes, a table or
#     keyspace for entities).
#   - Writes pass through the harness PII policy before persistence.
#
# Example (commented)
#
#   class LongTermMemory:
#       def __init__(self, db): self._db = db
#       async def remember_episode(self, session_id: str, summary: str) -> None: ...
#       async def recall_episodes(self, query: str, k: int = 5) -> list[dict]: ...
#       async def upsert_entity(self, entity_id: str, attributes: dict) -> None: ...
#       async def get_entity(self, entity_id: str) -> dict | None: ...
