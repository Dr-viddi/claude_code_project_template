# observability/feedback.py
#
# Intention:
#   Capture explicit user feedback (thumbs up/down, free-text comment) and
#   correlate it with the trace_id of the response that triggered it. Drives
#   the offline eval rubric over time.
#
# What this file should contain:
#   - An async `record(trace_id, rating, note=None)` function.
#   - Storage backend pluggable - Postgres for relational queries, a warehouse
#     sink for analytics, or both.
#
# Example (commented):
#
#   async def record(
#       trace_id: str,
#       rating: Literal["up", "down"],
#       note: str | None = None,
#   ) -> None: ...
