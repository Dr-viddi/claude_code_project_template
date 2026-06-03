"""Runtime defense harness package.

See ``harness`` for the implementation and ``contract.yaml`` for the policy. The
harness is provider-agnostic: swap the body of ``harness`` for a managed backend
without touching the rest of the codebase.
"""

from __future__ import annotations

from security.harness import (
    ControlMode,
    Harness,
    HarnessBlocked,
    ReviewRequired,
    Verdict,
    init,
    load_contract,
    shutdown,
)

__all__ = [
    "ControlMode",
    "Harness",
    "HarnessBlocked",
    "ReviewRequired",
    "Verdict",
    "init",
    "load_contract",
    "shutdown",
]
