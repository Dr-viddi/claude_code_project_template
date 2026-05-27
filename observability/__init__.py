# Package marker for `observability`.
#
# Tracing, feedback, and cost tracking. Every pipeline stage opens a span via
# `tracer.span(...)`, attaches token usage via `cost_tracker.record(...)`, and
# user-supplied ratings land via `feedback.record(...)`.
