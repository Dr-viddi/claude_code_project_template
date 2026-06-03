# security/harness.py
#
# Purpose
#   The runtime defense harness. Wraps the agent so every tool call (and
#   reasoning step) is intercepted, scored for risk, and gated BEFORE it
#   executes. A runtime complement to the static input/output filters most
#   apps already have.
#
# When you want a file like this
#   Any agent that calls tools with side effects (writes, mutations, external
#   calls). Read-only chat assistants can get by with input/output guards alone;
#   anything that *acts* needs pre-execution gating.
#
# Why it matters
#   - Catches misuse and prompt-injection-driven actions *before* they happen,
#     not in post-hoc logs.
#   - Three control modes give a clean rollout path: ship in `audit` to learn,
#     promote to `human_in_the_loop` to gate risky writes, escalate to `block`
#     once policies are tight.
#   - Fail-SAFE init (audit-mode fallback on bad config) means a typo in the
#     contract degrades to observed-but-not-enforced, not unprotected or down.
#   - See ADR-0002 for why this is a seam rather than a vendor import, and
#     ADR-0003 for why audit-mode + fail-safe is the default.
#
# The 8-layer model (see docs/architecture.md table for full mapping)
#   1. Agent contract            - contract.yaml
#   2. Capture actions/reasoning - intercept inside `gate(...)`
#   3. Scrub PII before egress   - extend or delegate to a managed backend
#   4. Analyze reasoning trace   - heuristic locally; LLM analyser when managed
#   5. Harden the analyser       - sandboxed (no tools / no MCP / no internet)
#   6. Tier verdict by severity  - low / medium / high / critical
#   7. Choose control mode       - audit | human_in_the_loop | block
#   8. Push alerts to channels   - severity-gated Slack / Discord
#
# What goes in it
#   - `ControlMode` enum: AUDIT, HUMAN_IN_THE_LOOP, BLOCK.
#   - `Verdict` dataclass: severity, reason, allowed.
#   - `HarnessBlocked` and `ReviewRequired` exceptions (control-flow signals,
#     not errors - hence the N818 ruff ignore for this file).
#   - `Harness` dataclass with:
#       * `gate(tool, arguments) -> Verdict` - the layer 2 + 7 enforcement point.
#       * Score logic (heuristic locally; LLM analyser when delegated).
#   - `load_contract(path)` - read + validate contract.yaml.
#   - `init(path, *, enabled, override_mode=None)` - factory. Fails SAFE to
#     audit-only on any error rather than leaving the agent ungated.
#   - `shutdown(harness)` - flush buffered events, detach cleanly.
#
# Example (commented)
#
#   class Harness:
#       def gate(self, tool: str, arguments: dict) -> Verdict:
#           verdict = self._score(tool, arguments)
#           self.events.append({"tool": tool, "severity": verdict.severity})
#           if self.control_mode is ControlMode.AUDIT:    return verdict
#           if not self._meets_threshold(verdict.severity): return verdict
#           if self.control_mode is ControlMode.BLOCK:    raise HarnessBlocked(verdict)
#           if self.control_mode is ControlMode.HUMAN_IN_THE_LOOP:
#               raise ReviewRequired(verdict)
#           return verdict
#
#   def init(contract_path: str, *, enabled: bool = True, override_mode=None) -> Harness:
#       try:
#           contract = load_contract(contract_path)
#           return Harness(control_mode=ControlMode(override_mode or contract["control_mode"]),
#                          allowed_tools=list(contract["scope"]["allowed_tools"]),
#                          enabled=enabled)
#       except Exception as exc:
#           logger.error("harness init failed (%s); falling back to audit-only", exc)
#           return Harness(control_mode=ControlMode.AUDIT, enabled=enabled)
