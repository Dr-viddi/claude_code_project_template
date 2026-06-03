# observability/feedback.py
#
# Purpose
#   Capture explicit user feedback (thumbs up/down, free-text comment) and
#   correlate it with the `trace_id` of the response that triggered it.
#
# When you want a file like this
#   Any production agent. The day after launch, you'll want to know which
#   responses users hated and which they liked - and you need a place to put
#   the answer.
#
# Why it matters
#   - Feedback + trace_id = ground truth. Over time, this fuels offline-eval
#     rubrics (judges trained on real production signal).
#   - Storage backend pluggable: Postgres for relational queries, warehouse
#     sink for analytics, both for serious work.
#   - Anonymous + minimal payload = low PII surface even before scrubbing.
#
# What goes in it
#   - An async `record(trace_id, rating, note=None)` function.
#   - An accessor for tests / debug (`all_feedback()` style).
#
# Example (commented)
#
#   async def record(
#       trace_id: str,
#       rating: Literal["up", "down"],
#       note: str | None = None,
#   ) -> None: ...
