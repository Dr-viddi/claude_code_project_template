# Package marker for `security`.
#
# The runtime defense harness that wraps the agent. Instead of three static
# input/content/output guards, this is an always-on harness that intercepts tool
# calls and reasoning traces, scrubs PII, analyzes intent before an action runs,
# scores a verdict by severity, and enforces a control mode (audit / human-in-the-
# loop / block).
#
#   adrian_init.py  - the integration point: initialize + wrap the agent
#   contract.yaml   - the agent contract: scope, boundaries, thresholds, routing
#
# NOTE: "Adrian" (adrian-sdk) is a specific third-party vendor harness referenced
# by the source blueprint. Treat `adrian_init.py` as a provider-agnostic seam: you
# can wire in that SDK, a different runtime-defense product, or your own
# implementation of the same 8-layer model. Nothing else in the codebase should
# depend on the concrete vendor - only on this package's interface.
