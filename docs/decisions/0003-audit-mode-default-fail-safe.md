# ADR-0003: Harness defaults to audit mode and fails safe

- **Status:** Accepted
- **Date:** 2026-06-03

## Context

The harness can run in three control modes: `audit` (observe + log), `human_in_the_loop`
(pause risky actions for approval), and `block` (reject them). Two questions need a
default: which mode ships, and what happens when the harness can't initialize (bad
contract, missing backend)?

Getting the failure mode wrong is dangerous in both directions: fail *open* (run the
agent ungated) silently removes all protection; fail *closed* (refuse to start) turns
a config typo into an outage.

## Decision

- **Default mode is `audit`.** A fresh clone runs, logs verdicts, and blocks nothing,
  so the app boots anywhere and teams can observe real traffic before turning on
  enforcement. Production sets `block` or `human_in_the_loop` explicitly via
  `contract.yaml` / env.
- **`init()` fails safe to audit, not open.** If the contract is missing or invalid,
  the harness logs the error and returns an **audit-mode** harness that still records
  every action - never a no-op that leaves the agent ungated, and never a hard crash
  that takes the service down.

## Consequences

- Onboarding and CI work with zero configuration; enforcement is an explicit,
  reviewable opt-in.
- A broken contract degrades to "observed but not enforced" with a loud log line,
  which is recoverable, rather than to "unprotected" or "down".
- "Audit by default" must be called out for production deployers so they don't ship
  an unenforced agent by accident - documented in `docs/deployment.md` and the
  `deploy` skill pre-flight.

## Alternatives considered

- **Default to `block`** - safest posture, but a fresh clone would block its own demo
  traffic and every misconfiguration becomes a hard failure. Bad first-run experience.
- **Fail closed on init error** - defensible for high-risk deployments, but turns
  config mistakes into outages; we prefer fail-safe-to-audit plus alerting.
