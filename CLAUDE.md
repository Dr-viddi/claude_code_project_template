# Project Brain

This file is auto-loaded at the start of every Claude Code session. Keep it lean —
push detail into `.claude/rules/*.md` and reference it from here.

## Overview

**Name:** `production-agent-blueprint`
**Purpose:** A reference / anatomy of a production-shaped AI agent project. Not a
runnable app — every file documents *purpose*, *when you want it*, *why it matters*,
and a small commented example. Use as a lookup when starting new AI/agent projects.
**Status:** reference (no runnable code by design)

## Why this exists

Two failure modes a portfolio template usually hits:
- *Too generic* — has the shape of a production agent but no real tradeoffs visible.
- *Too specific* — opinionated on one agent shape; useless for a different problem.

This repo picks neither: it's explicitly a **menu**. Real projects (built on top of
the shape this repo describes) carry the judgment a reviewer wants to see.

## Tech stack (the typical, when you build on this shape)

- **Language:** Python 3.11+
- **Web framework:** FastAPI
- **Agent orchestration:** LangGraph (state machine: plan → act → observe) or a
  small hand-rolled equivalent until you outgrow it.
- **LLM:** pluggable behind a small Protocol (`agent/llm.py`) — Anthropic / OpenAI /
  local.
- **Runtime defense:** a harness wrapping the agent (8-layer model, see
  `security/contract.yaml`). Local stub or a managed backend behind the same seam.
- **Vector store / cache / memory:** pgvector or qdrant + Redis are common picks.
- **Container runtime:** Docker + docker-compose (`deploy/`).
- **Tests:** pytest. **Lint/format:** ruff + black. **Type check:** mypy.

These are not requirements of *this* repo — they're the typical choices documented
on each file so you don't have to re-derive them.

## Architecture

```
client → app/main.py (FastAPI)
           → routing/ (classify intent → resolve handler)
           → agent/graph.py (plan → act → observe loop)
                → agent/nodes.py        (plan, act, observe, grade)
                → agent/tools/          (one file per tool)
                → agent/prompts/        (system + per-intent templates)
           → memory/ (conversation window · semantic cache · long-term store)
           → security/ (runtime defense harness gates every tool call)
           → observability/ (tracer · cost_tracker · feedback)
```

Every tool call passes through the **runtime defense harness**
(`security/harness.py`, configured by `security/contract.yaml`) before it
executes. See `docs/architecture.md` for the full diagram and the 8 layers.

## Conventions

Modular rules live in `.claude/rules/`:

- `code-style.md` — formatting, naming, import order
- `testing.md` — what to test, fixtures, golden datasets, judges
- `api-conventions.md` — error envelope, versioning, schema rules

Non-obvious choices are recorded as ADRs in `docs/decisions/`. Read them before
reworking the agent loop, the harness, or the offline defaults.

## Workflow rules (carried into real projects)

1. **Never commit `CLAUDE.local.md`, `.env`, or `.claude/settings.local.json`.**
2. **Always run `make check` before pushing** (lint + type + test).
3. **Add a regression test** for every bug fix.
4. **Update `evaluation/golden_dataset.json`** when prompts, tools, or routing change.
5. **Guard the guardrails.** Any change to `security/` or `agent/tools/` runs
   `/review` and `/security-review` before merge.

## Hierarchy

This is the root `CLAUDE.md`. Subdirectories may add their own (e.g.
`agent/CLAUDE.md`, `security/CLAUDE.md`) — child files load on demand.

## Personal overrides

Per-developer settings live in `CLAUDE.local.md` (gitignored). Copy
`CLAUDE.local.md.example` to start.
