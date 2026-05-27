# app/security/content_filter.py
#
# Intention:
#   Second guard layer. Runs over every retrieved document chunk *before* it
#   gets embedded into the LLM prompt. Strips indirect prompt-injection payloads
#   that a malicious or compromised source may have planted in the corpus.
#
# What this file should contain:
#   - A `ContentFilter` class with an async `filter(text)` method returning the
#     sanitized text.
#   - Common defenses:
#       * Strip / escape known injection markers ("Ignore previous instructions").
#       * Remove URLs unless the agent loop is allowed to follow links.
#       * Mask secrets that may have leaked into the corpus.
#   - Should be cheap - this runs N times per query, once per chunk.
#
# Example (commented):
#
#   class ContentFilter:
#       async def filter(self, text: str) -> str: ...
