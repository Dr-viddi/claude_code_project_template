# Package marker for `observability`.
#
# Tracing, feedback, and cost tracking. Each agent step opens a span via
# `tracer.span(...)`, attaches token usage via `cost_tracker.record(...)`, and
# user-supplied ratings land via `feedback.record(...)`.
#
# These three together let you answer the three production questions you'll
# always be asked: "Is it slow?" (tracer), "Is it expensive?" (cost_tracker),
# "Is it any good?" (feedback + evals).
