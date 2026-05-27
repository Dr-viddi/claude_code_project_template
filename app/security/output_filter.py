# app/security/output_filter.py
#
# Intention:
#   Third guard layer. Last gate on the response path. Redacts PII the model
#   may have surfaced, refuses unsafe completions, and enforces tone or policy
#   constraints before the client sees the answer.
#
# What this file should contain:
#   - An `OutputFilter` class with an async `filter(text)` method returning the
#     sanitized response. May also raise a `GuardViolation` on a hard refusal.
#   - Common checks: PII regex sweep, profanity / toxicity scoring, policy
#     keyword match, citation integrity (no fabricated doc_ids).
#
# Example (commented):
#
#   class OutputFilter:
#       async def filter(self, text: str) -> str: ...
