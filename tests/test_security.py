# tests/test_security.py
#
# Intention:
#   Unit tests for the runtime defense harness seam (`security/adrian_init.py`) and
#   the agent contract (`security/contract.yaml`). The vendor backend is mocked -
#   we test OUR wiring and policy parsing, not the third-party service.
#
# What this file should contain:
#   - Contract parsing: `contract.yaml` loads, required keys present, control_mode is
#     one of audit|human_in_the_loop|block, thresholds are valid.
#   - Fail-safe behavior: with the harness disabled, `init()` falls back to audit-only
#     (no-op) so the app still boots in local/dev/test.
#   - Gating: in `block` mode a tool call exceeding the action threshold is blocked;
#     in `audit` mode it is allowed but recorded.
#   - PII policy: configured PII classes are scrubbed before egress (mock the sweep).
#   - No real api key, no real network - mock the harness client.
#
# Example (commented):
#
#   def test_contract_control_mode_is_valid():
#       contract = load_contract("security/contract.yaml")
#       assert contract["control_mode"] in {"audit", "human_in_the_loop", "block"}
#
#   @pytest.mark.asyncio
#   async def test_block_mode_blocks_high_severity_tool_call(monkeypatch): ...
