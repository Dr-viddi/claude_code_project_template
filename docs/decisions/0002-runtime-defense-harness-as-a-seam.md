# ADR-0002: Runtime defense harness as a provider-agnostic seam

- **Status:** Accepted (recommendation)
- **Date:** 2026-06-03

> Recommendation for projects built on this blueprint. Applies the first time you
> implement `security/harness.py` and `security/contract.yaml`.

## Context

A production agent needs runtime defense: gating tool calls before they execute,
scrubbing PII, scoring risk, and enforcing a control mode (audit / human-in-the-
loop / block). There are managed products that do this. Two failure modes to
avoid:

1. **Hard-coupling to a vendor** - importing a specific SDK throughout the code
   makes the agent depend on a paid, third-party service and is hard to swap.
2. **Hand-waving it** - leaving "security" as a TODO so the repo can't actually
   run the gate, which is the most interesting part to demonstrate.

## Decision

Define the harness as a small interface (`security/harness.py`: `init`, `gate`,
`shutdown`, `Verdict`, `HarnessBlocked`, `ReviewRequired`) and own a **self-
contained, dependency-free implementation** of the 8-layer model. Layers 1–2 and
6–7 work as shipped; layers 3–5 and 8 (PII LLM sweep, sandboxed analyser, alert
routing) are deliberately light stubs that you extend or delegate to a managed
backend. The agent depends only on this interface, so swapping in a managed
backend is a single-file change.

## Consequences

- The gate is real and testable from day one (`tests/test_security.py`).
- Swapping in a managed backend - or hardening the stub layers - is a single-file
  change behind a stable interface.
- Be honest about which layers are stubs (see the table in
  `docs/architecture.md`) so nobody mistakes regex heuristics for real detection.

## Alternatives considered

- **Import a managed SDK directly** - couples the project to a vendor and breaks
  the offline/no-key guarantee. Rejected as the default; supported via the seam.
- **Static input/content/output guards only** - simpler, but doesn't model
  *pre-execution* gating of tool calls, which is the property worth demonstrating.
