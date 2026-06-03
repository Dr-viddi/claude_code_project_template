"""Runtime defense harness.

A small, dependency-free, provider-agnostic implementation of the 8-layer model
from the blueprint. It intercepts tool calls, scores a verdict by severity, and
enforces a control mode (audit / human_in_the_loop / block) read from
``contract.yaml``. Audit mode is the default: it logs but never blocks, so the app
boots with no external backend.

To use a real vendor harness (e.g. the "Adrian" SDK named in the blueprint), keep
this module's interface and replace the body of ``Harness.gate`` / ``init`` - nothing
else in the codebase depends on the concrete implementation.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)

_SEVERITY_ORDER = ["low", "medium", "high", "critical"]
# Toy heuristics standing in for layers 3-6 (PII scrub, reasoning analysis,
# verdict tiering). Replace with your detector / vendor backend.
_CRITICAL_MARKERS = ("rm -rf", "drop table", "exfiltrate", "password", "secret_key")
_HIGH_MARKERS = ("delete", "ignore previous instructions", "wire transfer")


class ControlMode(StrEnum):
    AUDIT = "audit"
    HUMAN_IN_THE_LOOP = "human_in_the_loop"
    BLOCK = "block"


class HarnessBlocked(Exception):
    def __init__(self, verdict: Verdict) -> None:
        super().__init__(f"blocked: {verdict.severity} ({verdict.reason})")
        self.verdict = verdict


class ReviewRequired(Exception):
    def __init__(self, verdict: Verdict) -> None:
        super().__init__(f"review required: {verdict.severity} ({verdict.reason})")
        self.verdict = verdict


@dataclass
class Verdict:
    severity: str
    reason: str
    allowed: bool


@dataclass
class Harness:
    control_mode: ControlMode = ControlMode.AUDIT
    action_threshold: str = "high"
    allowed_tools: list[str] = field(default_factory=list)
    enabled: bool = True
    events: list[dict[str, Any]] = field(default_factory=list)

    def _score(self, tool: str, arguments: dict[str, Any]) -> Verdict:
        blob = f"{tool} {arguments}".lower()
        if self.allowed_tools and tool not in self.allowed_tools:
            return Verdict("critical", f"tool '{tool}' not in contract scope", allowed=False)
        if any(m in blob for m in _CRITICAL_MARKERS):
            return Verdict("critical", "matched critical marker", allowed=False)
        if any(m in blob for m in _HIGH_MARKERS):
            return Verdict("high", "matched high-risk marker", allowed=False)
        return Verdict("low", "no risk markers", allowed=True)

    def _meets_threshold(self, severity: str) -> bool:
        return _SEVERITY_ORDER.index(severity) >= _SEVERITY_ORDER.index(self.action_threshold)

    def gate(self, tool: str, arguments: dict[str, Any]) -> Verdict:
        """Layer 2 + 7: capture the action, score it (layers 4-6), enforce control mode."""
        verdict = self._score(tool, arguments)
        self.events.append({"tool": tool, "severity": verdict.severity, "reason": verdict.reason})

        if not self.enabled or self.control_mode is ControlMode.AUDIT:
            if verdict.severity != "low":
                logger.warning(
                    "harness(audit): %s on %s (%s)", verdict.severity, tool, verdict.reason
                )
            return verdict

        if self._meets_threshold(verdict.severity) and not verdict.allowed:
            if self.control_mode is ControlMode.BLOCK:
                raise HarnessBlocked(verdict)
            if self.control_mode is ControlMode.HUMAN_IN_THE_LOOP:
                raise ReviewRequired(verdict)
        return verdict


def load_contract(path: str | Path) -> dict[str, Any]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"contract at {path} is not a mapping")
    return data


def init(
    contract_path: str | Path = "security/contract.yaml",
    *,
    enabled: bool = True,
    override_mode: str | None = None,
) -> Harness:
    """Build the harness from the contract. Fails SAFE: on any error it returns an
    audit-only harness rather than leaving the agent ungated."""
    try:
        contract = load_contract(contract_path)
        mode = override_mode or contract.get("control_mode", "audit")
        tiers = contract.get("severity_tiers", {})
        return Harness(
            control_mode=ControlMode(mode),
            action_threshold=tiers.get("action_threshold", "high"),
            allowed_tools=list(contract.get("scope", {}).get("allowed_tools", [])),
            enabled=enabled,
        )
    except (OSError, ValueError, KeyError) as exc:
        logger.error("harness init failed (%s); falling back to audit-only", exc)
        return Harness(control_mode=ControlMode.AUDIT, enabled=enabled)


def shutdown(harness: Harness | None = None) -> None:
    if harness is not None:
        logger.info("harness shutdown: %d events recorded", len(harness.events))
