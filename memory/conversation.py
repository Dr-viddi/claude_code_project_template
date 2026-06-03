# memory/conversation.py
#
# Intention:
#   Short-term, per-session memory. Holds a sliding window of recent turns so the
#   agent has the immediate context it needs for follow-ups and pronoun references.
#   Backed by Redis (fast, TTL'd).
#
# What this file should contain:
#   - A `ConversationStore` class with:
#       * Constructor taking `redis_url` and `max_turns` (window size).
#       * `load(session_id)` -> ordered list of recent messages.
#       * `append(session_id, message)` -> push + trim to the window.
#   - Optional: a summarizer that compresses turns that fall out of the window and
#     hands the summary to `long_term.py`.
#
# Example (commented):
#
#   class ConversationStore:
#       def __init__(self, redis_url: str, max_turns: int = 20): ...
#       async def load(self, session_id: str) -> list[Message]: ...
#       async def append(self, session_id: str, msg: Message) -> None: ...
