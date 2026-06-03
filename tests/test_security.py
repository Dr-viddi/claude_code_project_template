# tests/test_security.py
#
# Purpose
#   Unit tests for the runtime defense harness seam (security/harness.py) and
#   the agent contract (security/contract.yaml). The vendor backend (if any)
#   is mocked - we test OUR wiring and policy parsing, not the third-party service.
#
# When you want a file like this
#   Any time the harness exists. Untested guardrails are not guardrails.
#
# Why it matters
#   - The fail-safe property (init falls back to audit, never leaves the agent
#     ungated) is a security invariant that must never silently regress.
#   - Block-mode and HITL-mode tests prove the control modes actually take
#     effect, rather than silently no-op'ing on misconfigured contracts.
#   - Contract parsing tests catch typos in the YAML before they ship.
#
# What goes in it
#   - Contract parsing: contract.yaml loads, required keys present,
#     control_mode is one of audit/human_in_the_loop/block, thresholds are valid.
#   - Fail-safe: with the harness disabled or contract path invalid, `init()`
#     returns an audit-only harness rather than crashing or no-op'ing.
#   - Gating: in `block` mode a tool call exceeding the action threshold is blocked;
#     in `audit` mode it is allowed but recorded.
#   - PII policy: configured PII classes are scrubbed before egress (mock the sweep).
#   - No real api key, no real network - mock the harness client.
#
# Example (commented)
#
#   def test_init_fails_safe_to_audit_on_bad_path():
#       harness = init("security/does-not-exist.yaml")
#       assert harness.control_mode is ControlMode.AUDIT
#
#   def test_block_mode_blocks_out_of_scope_tool():
#       harness = init(CONTRACT, override_mode="block")
#       with pytest.raises(HarnessBlocked):
#           harness.gate("shell", {"cmd": "ls"})
