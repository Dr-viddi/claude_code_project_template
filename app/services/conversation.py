# app/services/conversation.py
#
# Intention:
#   Persist a rolling window of chat history per `conversation_id` so the LLM has
#   the context it needs to handle follow-up questions and pronoun references.
#
# What this file should contain:
#   - A `ConversationStore` class with:
#       * Constructor taking `redis_url` and `max_turns` (window size).
#       * `load(conversation_id)` -> ordered list of `Message`.
#       * `append(conversation_id, message)` -> push + trim to the window.
#   - Optional: a summarizer that compresses older turns once the window fills.
#
# Example (commented):
#
#   class ConversationStore:
#       def __init__(self, redis_url: str, max_turns: int = 20): ...
#       async def load(self, cid: UUID) -> list[Message]: ...
#       async def append(self, cid: UUID, msg: Message) -> None: ...
