# security/adrian_init.py
#
# Intention:
#   Single integration point for the runtime defense harness. The harness wraps the
#   agent so that every tool call and reasoning step is intercepted, analyzed, and
#   gated BEFORE it executes - a runtime complement to static input/output filters.
#
#   "Adrian" (adrian-sdk) is the third-party harness named in the source blueprint
#   (Apache-2.0, `pip install adrian-sdk`, self-host or hosted). This file is the
#   ONLY place that name should appear: keep it a thin, swappable seam so you can
#   substitute another vendor or your own implementation without touching the agent.
#
# The harness provides 8 layers (see `contract.yaml` for the per-agent config):
#   1. Define the agent contract     - scope, boundaries, enforcement mode (your config).
#   2. Capture actions + reasoning    - intercept tool calls, pair them with the
#                                       reasoning trace, correlate across the session.
#   3. Scrub PII before it leaves      - client-side regex (emails, phones, IDs) +
#                                       server-side LLM sweep (names, contextual ids).
#   4. Analyze the reasoning trace     - catch intent BEFORE the action runs
#                                       (meaningfully higher detection than action-only).
#   5. Harden the analyser             - run it sandboxed (no tools, no MCP, no
#                                       internet); treat inputs as untrusted, spotlight
#                                       them as data; structured-only outputs.
#   6. Tier the verdict by severity    - multi-tier score (low risk -> critical) with a
#                                       per-agent action threshold.
#   7. Choose the control mode         - audit / human-in-the-loop / block; tool calls
#                                       gated pre-execution.
#   8. Push alerts to channels         - severity-gated routing to Slack/Discord; the
#                                       payload includes verdict + reasoning + action.
#
# What this file should contain:
#   - `init(...)` - read `contract.yaml`, authenticate (api key from env, never
#     hardcoded), install the interceptors, and wrap the agent graph.
#   - `shutdown()` - flush buffered traces and detach cleanly.
#   - A no-op / "audit-only" fallback when the harness is disabled, so local dev and
#     unit tests run without the backend.
#   - Optionally a context manager so callers can `with harness(...): run_agent()`.
#
# Example (commented) - the "two-line wrap" from the blueprint:
#
#   import os
#   import adrian   # third-party; swap for your provider
#
#   def init() -> None:
#       adrian.init(
#           api_key=os.environ["ADRIAN_API_KEY"],   # e.g. "adr_live_..."
#           contract="security/contract.yaml",
#       )
#       # your LangGraph / LangChain agent then runs unchanged
#
#   def shutdown() -> None:
#       adrian.shutdown()
#
# Wiring: call `init()` at startup in `app/main.py` and `shutdown()` on app exit.
