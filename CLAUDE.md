# Project Brain

This file is auto-loaded at the start of every Claude Code session. Keep it lean -
push detail into `.claude/rules/*.md` and reference it from here.

## Overview

**Name:** `<project-name>`
**Purpose:** One-paragraph description of what this agent does and who uses it.
**Status:** alpha / beta / production

## Tech Stack

- **Language:** Python 3.11+
- **Web framework:** FastAPI
- **Agent orchestration:** LangGraph (state machine: plan → act → observe)
- **Runtime defense:** `security/` harness wrapping the agent (8 layers)
- **Vector store:** `<pgvector | qdrant | weaviate | ...>`
- **Cache / short-term memory:** Redis
- **Long-term memory:** episodic + entity store (`<pgvector | dedicated memory db>`)
- **Container runtime:** Docker + docker-compose (`deploy/`)
- **Tests:** pytest
- **Lint/format:** ruff + black
- **Type check:** mypy

## Architecture

```
client → app/main.py (FastAPI)
           → routing/ (classify intent → resolve handler)
           → agent/graph.py (LangGraph: plan → act → observe loop)
                → agent/nodes.py        (plan, act, observe, grade)
                → agent/tools/          (crm, web_search, code_search)
                → agent/prompts/        (system + per-intent templates)
           → memory/ (conversation window · semantic cache · long-term store)
           → security/ (runtime defense harness gates every tool call)
           → observability/ (tracer · cost_tracker · feedback)
```

Every tool call and reasoning step passes through the **runtime defense harness**
(`security/adrian_init.py`, configured by `security/contract.yaml`) before it
executes. See `docs/architecture.md` for the full diagram and the 8 layers.

## Conventions

Modular rules live in `.claude/rules/`:

- `code-style.md` - formatting, naming, import order
- `testing.md` - what to test, fixtures, golden datasets, judges
- `api-conventions.md` - error envelope, versioning, schema rules

## Workflow Rules

1. **Never commit `CLAUDE.local.md`, `.env`, or `.claude/settings.local.json`.**
2. **Always run `make check` before pushing** (lint + type + test).
3. **Add a regression test** for every bug fix.
4. **Update `evaluation/golden_dataset.json`** when prompts, tools, or routing change.
5. **Guard the guardrails.** Any change to `security/` (harness or `contract.yaml`)
   or `agent/tools/` must run `/review` (code-reviewer) and `/security-review`
   (security-auditor) before merge.

## Common Commands

```bash
make install      # editable install + dev deps
make run          # docker compose up (deploy/docker-compose.yml)
make test         # pytest
make eval         # offline eval against golden dataset (evaluation/eval_runner.py)
make check        # lint + type + test
```

## Hierarchy

This is the root `CLAUDE.md`. Subdirectories may add their own `CLAUDE.md` for
locality - e.g. `agent/CLAUDE.md` for agent-specific conventions, or
`security/CLAUDE.md` for the contract policy. Child files load on demand, not at
session start.

## Personal Overrides

Per-developer settings (local paths, debug shortcuts, private prefs) go in
`CLAUDE.local.md`, which is gitignored. Copy `CLAUDE.local.md.example` to start.
