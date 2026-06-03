# memory/conversation.py
#
# Purpose
#   Short-term, per-session memory. Holds a sliding window of recent turns so the
#   agent has the immediate context for follow-ups and pronoun references.
#
# When you want a file like this
#   Any agent with multi-turn conversations. Single-shot APIs can skip this.
#
# Why it matters
#   - Without a bounded window, prompt size grows unboundedly and costs spike.
#   - Redis with TTL gives "remembers within a session, forgets after a day"
#     almost for free.
#   - When the window overflows, summarize the oldest turns and hand the summary
#     to long_term.py - that's the standard short→long memory hand-off.
#
# What goes in it
#   - A `ConversationStore` class with:
#       * Constructor taking the backend handle (Redis client / in-memory dict)
#         and `max_turns` (window size).
#       * `load(session_id)` -> ordered list of recent messages.
#       * `append(session_id, message)` -> push and trim to the window.
#   - Optional: a `summarize_overflow` callback that compresses trimmed turns.
#
# Example (commented)
#
#   class ConversationStore:
#       def __init__(self, redis_url: str = "", max_turns: int = 20): ...
#       async def load(self, session_id: str) -> list[Message]: ...
#       async def append(self, session_id: str, msg: Message) -> None: ...
