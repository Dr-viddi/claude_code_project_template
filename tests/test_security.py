"""Harness wiring, contract parsing, and control-mode gating. Vendor backend mocked
away entirely - this is the local implementation."""

from __future__ import annotations

import pytest

from security import ControlMode, HarnessBlocked, ReviewRequired, init, load_contract

CONTRACT = "security/contract.yaml"


def test_contract_parses_with_valid_control_mode():
    contract = load_contract(CONTRACT)

    assert contract["control_mode"] in {"audit", "human_in_the_loop", "block"}
    assert "crm" in contract["scope"]["allowed_tools"]


def test_default_init_is_audit_and_allows_low_risk():
    harness = init(CONTRACT)

    verdict = harness.gate("web_search", {"query": "hello"})

    assert harness.control_mode is ControlMode.AUDIT
    assert verdict.allowed


def test_audit_mode_records_but_never_raises():
    harness = init(CONTRACT)  # audit

    verdict = harness.gate("crm", {"cmd": "rm -rf /"})  # critical marker

    assert verdict.severity == "critical"
    assert harness.events  # captured


def test_block_mode_blocks_critical_action():
    harness = init(CONTRACT, override_mode="block")

    with pytest.raises(HarnessBlocked):
        harness.gate("crm", {"cmd": "please rm -rf the database"})


def test_block_mode_blocks_out_of_scope_tool():
    harness = init(CONTRACT, override_mode="block")

    with pytest.raises(HarnessBlocked):
        harness.gate("shell", {"cmd": "ls"})


def test_hitl_mode_requires_review_for_high_risk():
    harness = init(CONTRACT, override_mode="human_in_the_loop")

    with pytest.raises(ReviewRequired):
        harness.gate("crm", {"cmd": "delete the account"})


def test_init_fails_safe_to_audit_on_bad_path():
    harness = init("security/does-not-exist.yaml")

    assert harness.control_mode is ControlMode.AUDIT
