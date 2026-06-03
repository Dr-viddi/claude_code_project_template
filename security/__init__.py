# Package marker for `security`.
#
# The runtime defense harness that wraps the agent. Intercepts tool calls and
# reasoning traces, scrubs PII, analyzes intent before an action runs, scores a
# verdict by severity, and enforces a control mode (audit / human-in-the-loop /
# block).
#
#   harness.py    - integration point: init + gate + shutdown
#   contract.yaml - the agent contract: scope, boundaries, thresholds, routing
#
# The interface is provider-agnostic: harness.py can be a self-contained local
# implementation (audit-mode default, fail-safe) or a thin wrapper around a
# managed runtime-defense backend - nothing else in the codebase changes.
