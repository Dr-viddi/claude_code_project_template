# ADR-0002: Runtime defense harness as a provider-agnostic seam

- **Status:** Accepted
- **Date:** 2026-06-03

## Context

A production agent needs runtime defense: gating tool calls before they execute,
scrubbing PII, scoring risk, and enforcing a control mode (audit / human-in-the-loop
/ block). There are managed products that do this, and the reference blueprint that
inspired this repo names one specifically. Two failure modes to avoid:

1. **Hard-coupling to a vendor** - importing a specific SDK throughout the code makes
   the whole agent depend on a paid, third-party service and is hard to swap.
2. **Hand-waving it** - leaving "security" as a TODO so the repo can't actually run
   the gate, which is the most interesting part to demonstrate.

## Decision

Define the harness as a small interface (`security/harness.py`: `init`, `gate`,
`shutdown`, `Verdict`, `HarnessBlocked`, `ReviewRequired`) with a **self-contained,
dependency-free implementation** of the 8-layer model. Layers 1–2 and 6–7 work as
shipped; layers 3–5 and 8 (PII LLM sweep, sandboxed analyser, alert routing) are
deliberately light stubs. The agent depends only on this interface, so a managed
backend can be dropped in by replacing the body of `gate`/`init` with no changes
elsewhere.

## Consequences

- The gate is real and testable today (`tests/test_security.py`), and the demo shows
  blocking/HITL behaviour without any external account.
- Swapping in a managed backend - or hardening the stub layers - is a single-file
  change behind a stable interface.
- The stubbed layers are honest about being stubs (see the table in
  `docs/architecture.md`) so no one mistakes the toy heuristics for production
  detection.

## Alternatives considered

- **Import a managed SDK directly** - couples the repo to a vendor and breaks the
  offline/no-key guarantee. Rejected as the default; supported via the seam.
- **Static input/content/output guards only** - simpler, but doesn't model
  *pre-execution* gating of tool calls, which is the property worth demonstrating.
