"""Runtime defense harness package.

See ``adrian_init`` for the implementation and ``contract.yaml`` for the policy.
The harness is provider-agnostic: swap the body of ``adrian_init`` for a real vendor
SDK without touching the rest of the codebase.
"""

from __future__ import annotations

from security.adrian_init import (
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
