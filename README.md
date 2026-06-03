# Production Agent — Project Blueprint

A **reference / anatomy** of a production-shaped AI agent project. Not a runnable
app: every source and config file is a comment-only stub that explains its
**purpose**, **when you want a file like it**, **why it matters**, and a small
**commented example** of what real content would look like.

Use it as a lookup when starting a new AI or agent project: walk the tree, pick
the pieces you need, copy the examples, and skip the rest. It pairs two
mental models you'll see referenced throughout the repo:

- **The Claude Code project anatomy** — `CLAUDE.md` "project brain" + `.claude/`
  (settings, rules, commands, skills, sub-agents, hooks). Reusable across any
  project, not just AI ones.
- **The production-agent architecture** — agent loop (plan → act → observe),
  tools, layered memory, intent routing, an 8-layer runtime defense harness,
  evaluation with judges, observability, deploy configs.

> **Not runnable on purpose.** Treat each file as documentation. When you start
> a new project, copy the *shape* — directory layout, file names, file roles —
> and write the real code in that new repo. Specific projects make the hard
> tradeoffs against a real problem; this repo only describes the menu.

```mermaid
flowchart LR
    c([client]) --> api["FastAPI<br/>/v1/chat"]
    api --> route["routing<br/>intent"]
    route --> loop
    subgraph loop["agent loop"]
        direction LR
        p["plan"] --> a["act"] --> o["observe"]
    end
    a -.gated.-> h["defense<br/>harness"]
    a --> t["tools"]
    loop --> mem["memory"]
    mem --> r([response])
    api -.-> obs["observability"]
```

Full diagram + 8-layer harness table: [`docs/architecture.md`](docs/architecture.md).
Design rationale: [`docs/decisions/`](docs/decisions/) (ADRs).

---

## What's in the tree

```
.
├── CLAUDE.md                 # Project brain - loaded at session start
├── CLAUDE.local.md.example   # Personal overrides (gitignored when renamed)
├── AGENTS.md                 # Multi-agent collaboration notes
├── .mcp.json                 # External tool connections (MCP)
├── .claudeignore             # Files Claude should never read
├── .claude/
│   ├── settings.json         # Permissions, hooks, env vars (checked in)
│   ├── settings.local.json.example  # Per-machine overrides
│   ├── rules/                # Modular conventions (code-style, testing, API)
│   ├── commands/             # Custom slash commands
│   ├── skills/               # Auto-invoked reusable expertise
│   ├── agents/               # Specialized sub-agents
│   └── hooks/                # Lifecycle event scripts
│
├── app/                      # FastAPI entry, config, schemas, Dockerfile
├── agent/                    # Agent core
│   ├── graph.py              #   plan → act → observe orchestrator
│   ├── nodes.py              #   individual loop steps
│   ├── llm.py                #   pluggable LLM client (offline default + real provider)
│   ├── tools/                #   one file per tool (crm, web_search, code_search…)
│   └── prompts/              #   versioned system + per-intent templates
├── memory/                   # conversation window, semantic_cache, long_term
├── routing/                  # intent classifier + handler registry
├── security/                 # Runtime defense harness
│   ├── harness.py            #   gates every tool call (8-layer model)
│   └── contract.yaml         #   agent contract: scope, thresholds, control mode
├── evaluation/               # golden_dataset, eval_runner, judges/, results/
├── observability/            # tracer, feedback, cost_tracker
├── data/                     # raw → processed → index config
├── tests/                    # patterns for agent/tool/security/routing/API tests
├── deploy/                   # docker-compose (dev) + docker-compose.prod (hardened)
├── docs/                     # architecture, API reference, deployment, decisions/
├── scripts/                  # seed, migrate, healthcheck (optional helpers)
├── frontend/                 # optional UI, containerized separately
├── pyproject.toml
└── README.md
```

## File-by-file reference

Every entry below is a comment-only stub in this repo. The description says what
role the file plays so you can decide whether your project needs one like it.

### Root

| Path | What it is |
| --- | --- |
| `CLAUDE.md` | The "project brain" — auto-loaded at the start of every Claude Code session. Overview, tech stack, architecture, conventions, workflow rules. Keep it lean; push detail into `.claude/rules/`. |
| `CLAUDE.local.md.example` | Template for per-developer overrides. Copy to `CLAUDE.local.md` (gitignored) for personal notes that shouldn't be shared. |
| `AGENTS.md` | Cross-tool agent guidance (the vendor-neutral counterpart to `CLAUDE.md`), for when more than one AI coding tool touches the repo. |
| `README.md` | This file — what the blueprint is and how to use it. |
| `LICENSE` | Open-source license for the repo. |
| `Makefile` | The task runner and single source of truth for dev commands (`install`, `check`, `serve`, `test`, `lint`, `eval`). `make check` = lint + type + test. |
| `pyproject.toml` | Python project metadata, dependencies, optional extras, and tool config (ruff, black, mypy, pytest) in one place. |
| `.env.example` | Documents every environment variable the app reads. Copy to `.env` (gitignored) and fill in real values. |
| `.gitignore` | Files git must never track (secrets, caches, build artifacts, local settings). |
| `.claudeignore` | Files Claude Code should never read (large data, vendored code, secrets). |
| `.mcp.json` | Model Context Protocol server definitions — external tools/data sources the team shares, committed so everyone gets the same wiring. |
| `.pre-commit-config.yaml` | Pre-commit hooks (format, lint, type-check) that run locally before each commit. |

### `.claude/` — Claude Code project configuration

| Path | What it is |
| --- | --- |
| `.claude/settings.json` | Checked-in harness config: permissions, hooks, env vars shared by the whole team. |
| `.claude/settings.local.json.example` | Template for per-machine settings (copy to `settings.local.json`, gitignored). |
| `.claude/rules/code-style.md` | Formatting, naming, import order, typing, comment, error, and logging conventions. |
| `.claude/rules/testing.md` | Test philosophy, layout, fixtures, coverage targets, and the evaluation workflow. |
| `.claude/rules/api-conventions.md` | API versioning, request/response shape, error envelope, streaming, and route security rules. |
| `.claude/commands/review.md` | Custom `/review` slash command — a repeatable code-review prompt. |
| `.claude/commands/fix-issue.md` | Custom `/fix-issue` slash command — end-to-end "read → plan → implement → test → commit" workflow. |
| `.claude/skills/review/SKILL.md` | Auto-invoked code-review expertise (the reusable knowledge behind reviews). |
| `.claude/skills/deploy/SKILL.md` | Auto-invoked deploy expertise — build, tag, ship a container image. |
| `.claude/skills/deploy/deploy-config.md` | Supporting reference data for the deploy skill (registries, environments, pre-flight checks). |
| `.claude/agents/code-reviewer.md` | Definition of an isolated-context sub-agent specialized for code review. |
| `.claude/agents/security-auditor.md` | Definition of a sub-agent specialized for security audits of risky diffs. |
| `.claude/hooks/format-python.sh` | Lifecycle hook that auto-formats Python after edits. |
| `.claude/hooks/validate-bash.sh` | Lifecycle hook that rejects dangerous shell commands before they run. |

### `app/` — HTTP entry point

| Path | What it is |
| --- | --- |
| `app/main.py` | FastAPI app: mounts `/v1` routes, wires the agent + harness, defines `/healthz` and `/metrics`. |
| `app/models.py` | Pydantic request/response schemas — the typed API boundary. |
| `app/config.py` | Settings loaded from env with sensible defaults so a fresh clone runs. |
| `app/Dockerfile` | Container image build for the API service. |
| `app/__init__.py` | Package marker. |

### `agent/` — Agent core

| Path | What it is |
| --- | --- |
| `agent/graph.py` | The plan → act → observe orchestrator with bounded iteration (hand-rolled; LangGraph optional — see ADR-0001). |
| `agent/nodes.py` | The individual loop steps (plan, act, observe, grade) as testable functions. |
| `agent/llm.py` | Pluggable LLM client behind a small Protocol: offline `EchoLLM` default + real provider behind an extra. |
| `agent/tools/web_search.py` | Example tool: web search (canned results offline). |
| `agent/tools/code_search.py` | Example tool: local code search via ripgrep. |
| `agent/tools/crm.py` | Example tool: in-memory CRM lookup, modeling a stateful business integration. |
| `agent/tools/__init__.py` | Tool registry / `Tool` protocol shared by all tools. |
| `agent/prompts/system.py` | The base system prompt. |
| `agent/prompts/templates.py` | Versioned per-intent prompt templates. |
| `agent/prompts/__init__.py` | Package marker for prompts. |
| `agent/__init__.py` | Package marker exposing the agent's public surface. |

### `routing/` — Intent routing

| Path | What it is |
| --- | --- |
| `routing/classifier.py` | Classifies an incoming request into an intent. |
| `routing/handler_registry.py` | Maps each intent to the handler that serves it. |
| `routing/__init__.py` | Package marker. |

### `memory/` — Layered memory

| Path | What it is |
| --- | --- |
| `memory/conversation.py` | Short-term conversation window (recent turns). |
| `memory/semantic_cache.py` | Semantic cache to skip repeated LLM calls. |
| `memory/long_term.py` | Long-term store (vectors / facts) behind a swappable interface. |
| `memory/__init__.py` | Package marker. |

### `security/` — Runtime defense harness

| Path | What it is |
| --- | --- |
| `security/harness.py` | The seam that gates every tool call / reasoning step before it executes (8-layer model; see ADR-0002/0003). |
| `security/contract.yaml` | The agent contract: scope, risk thresholds, PII policy, and control mode (audit / human-in-the-loop / block). Reviewed like code. |
| `security/__init__.py` | Package marker. |

### `evaluation/` — Feature-quality evals

| Path | What it is |
| --- | --- |
| `evaluation/golden_dataset.json` | The golden set of inputs + expected qualities; the regression gate for prompt/tool/routing changes. |
| `evaluation/eval_runner.py` | Runs the golden set (`offline`) and samples production traffic (`online`). |
| `evaluation/judges/relevance_judge.py` | Example judge that scores an output dimension. |
| `evaluation/judges/__init__.py` | Package marker for judges. |
| `evaluation/results/.gitkeep` | Keeps the (otherwise gitignored) results output directory in the tree. |
| `evaluation/__init__.py` | Package marker. |

### `observability/` — Tracing, cost, feedback

| Path | What it is |
| --- | --- |
| `observability/tracer.py` | Spans/traces across the request and agent loop. |
| `observability/cost_tracker.py` | Token/cost accounting per request and model. |
| `observability/feedback.py` | Captures user/automated feedback for online evals. |
| `observability/__init__.py` | Package marker. |

### `data/` — Data layout

| Path | What it is |
| --- | --- |
| `data/raw/.gitkeep` | Placeholder for untouched source data (gitignored contents). |
| `data/processed/.gitkeep` | Placeholder for cleaned/derived data. |
| `data/index_config/embedding.yaml` | Embedding/index configuration for the vector store. |

### `tests/` — Unit tests

| Path | What it is |
| --- | --- |
| `tests/test_agent.py` | Agent graph, nodes, and memory integration. |
| `tests/test_tools.py` | Tool validation, timeouts, and contracts. |
| `tests/test_security.py` | Harness wiring + `contract.yaml` parsing/gating. |
| `tests/test_routing.py` | Intent classifier + handler registry. |
| `tests/test_api.py` | API routes — every status-code path. |
| `tests/conftest.py` | Shared fixtures (`fake_llm`, `fake_redis`, `fake_deps`, …). |
| `tests/__init__.py` | Package marker. |

### `deploy/` — Runtime composition

| Path | What it is |
| --- | --- |
| `deploy/docker-compose.yml` | Local dev stack (app + dependencies). |
| `deploy/docker-compose.prod.yml` | Hardened production overrides. |

### `frontend/` — Optional UI

| Path | What it is |
| --- | --- |
| `frontend/app.py` | Minimal UI that calls the API. |
| `frontend/requirements.txt` | Frontend-only dependencies, kept separate from the backend. |
| `frontend/Dockerfile` | Container build for the UI, deployed separately. |
| `frontend/static/.gitkeep` | Placeholder for static assets. |

### `scripts/` — Operational helpers

| Path | What it is |
| --- | --- |
| `scripts/seed.py` | Seeds local/dev data. |
| `scripts/migrate.py` | Runs database migrations. |
| `scripts/healthcheck.py` | Standalone health probe for deploys/orchestrators. |

### `docs/` — Documentation

| Path | What it is |
| --- | --- |
| `docs/architecture.md` | Full architecture diagram + the 8-layer harness table. |
| `docs/api-reference.md` | Endpoint-by-endpoint API reference. |
| `docs/deployment.md` | How to deploy, including the "audit by default" production caveat. |
| `docs/decisions/README.md` | Index of Architecture Decision Records and how to use them. |
| `docs/decisions/_template.md` | Blank ADR template. |
| `docs/decisions/0001-hand-rolled-agent-loop.md` | Why start with a hand-rolled loop before LangGraph. |
| `docs/decisions/0002-runtime-defense-harness-as-a-seam.md` | Why the harness is a provider-agnostic interface. |
| `docs/decisions/0003-audit-mode-default-fail-safe.md` | Why the harness defaults to audit mode and fails safe. |
| `docs/decisions/0004-offline-first-defaults.md` | Why every external dependency has an offline default. |

### `.github/` — CI

| Path | What it is |
| --- | --- |
| `.github/workflows/ci.yml` | CI pipeline: lint, type-check, test, and nightly offline evals. |

## How to use it

```bash
# 1. Browse it on GitHub or clone for offline reading
git clone <this-repo> production-agent-blueprint
cd production-agent-blueprint

# 2. Start a new project somewhere else
mkdir ../my-new-agent && cd ../my-new-agent
git init

# 3. For each file you need, copy the SHAPE from the blueprint and write the
#    actual code in your new repo. Use the blueprint's "When you want a file
#    like this" sections as a checklist for what to include.
```

The blueprint deliberately doesn't try to be a working starter — that pushed it
toward "generic" without enough specificity to be useful. Instead, a real project
solves a specific problem and earns each file it copies.

## Conventions

- **`CLAUDE.md` is the contract.** It loads at session start; keep it lean and push
  detail into `.claude/rules/*.md`.
- **`.claude/rules/*.md`** are scoped, modular conventions.
- **Hooks block what shouldn't happen** (`validate-bash.sh` rejects dangerous commands).
- **Sub-agents own isolated context** (code review, security audits).
- **MCP servers** live in `.mcp.json`, committed so the team shares the same external tools.
- **The agent contract (`security/contract.yaml`) is reviewed like code.**
- **Non-obvious decisions are ADRs** in `docs/decisions/`.

## Related

- Concrete project repos (built on this shape, with real tools and real evals):
  `<links to follow>`
