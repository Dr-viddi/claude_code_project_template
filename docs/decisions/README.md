# Architecture Decision Records

Short records of the non-obvious choices in this repo and *why* they were made.
Format is lightweight [MADR](https://adr.github.io/madr/). Newest decisions get the
next number; supersede rather than rewrite.

| ADR | Decision | Status |
| --- | -------- | ------ |
| [0001](0001-hand-rolled-agent-loop.md) | Hand-rolled agent loop instead of LangGraph (for now) | Accepted |
| [0002](0002-runtime-defense-harness-as-a-seam.md) | Runtime defense harness as a provider-agnostic seam | Accepted |
| [0003](0003-audit-mode-default-fail-safe.md) | Harness defaults to audit mode and fails safe | Accepted |
| [0004](0004-offline-first-defaults.md) | Offline-first defaults (EchoLLM + in-memory stores) | Accepted |

New ADR: copy [`_template.md`](_template.md) to `NNNN-short-title.md`.
