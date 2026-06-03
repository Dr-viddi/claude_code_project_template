# Architecture

End-to-end view of the production-agent layout: an agent state machine wrapped by a
runtime defense harness, with memory, routing, evaluation, and observability around it.

## Request flow

```
client
  │ HTTPS
  ▼
app/main.py  (FastAPI, /v1/...)
  │
  ▼
routing/classifier.py        classify intent {chitchat | qa | task | refuse}
  │
  ▼
routing/handler_registry.py  intent → handler / sub-graph
  │
  ▼
memory/ (load)               conversation window + recalled long-term context
  │
  ▼
agent/graph.py               LangGraph state machine
  │   ┌─────────────────────────────────────────────┐
  │   │  plan  → act  → observe  → (loop or finish)   │  agent/nodes.py
  │   │            │                                   │
  │   │            ▼                                   │
  │   │   agent/tools/{crm, web_search, code_search}   │
  │   └─────────────────────────────────────────────┘
  │            ▲
  │            │  every tool call + reasoning step is gated by ↓
  ▼            │
security/adrian_init.py      runtime defense harness (8 layers, see below)
  │
  ▼
memory/ (write)              append turn, cache answer, persist episode/entities
  │
  ▼
response  +  observability/{tracer, cost_tracker, feedback}
```

## The 8-layer runtime defense harness

Configured per agent in `security/contract.yaml`, enforced by `security/adrian_init.py`:

| # | Layer                       | Where            | What it does                                                        |
|---|-----------------------------|------------------|---------------------------------------------------------------------|
| 1 | Define the agent contract   | your config      | Scope, boundaries, enforcement mode.                                |
| 2 | Capture actions + reasoning | SDK (in-process) | Intercept tool calls, pair with reasoning, correlate per session.   |
| 3 | Scrub PII before it leaves  | SDK + backend    | Client-side regex (emails, phones, IDs) + server-side LLM sweep.    |
| 4 | Analyze the reasoning trace | backend          | Catch intent *before* the action runs.                              |
| 5 | Harden the analyser         | backend          | Sandboxed (no tools/MCP/internet); inputs spotlighted as untrusted. |
| 6 | Tier the verdict by severity| backend          | Multi-tier score (low → critical), per-agent action threshold.      |
| 7 | Choose the control mode     | SDK (in-process) | Audit · human-in-the-loop · block; tool calls gated pre-execution.  |
| 8 | Push alerts to channels     | backend          | Severity-gated Slack/Discord; payload = verdict + reasoning + action.|

> The blueprint names "Adrian" (`adrian-sdk`, Apache-2.0) as the harness. The repo
> keeps `security/adrian_init.py` provider-agnostic so you can swap it.

## Layers / ownership

| Layer            | What lives here                                       | Owns                       |
| ---------------- | ----------------------------------------------------- | -------------------------- |
| `app/`           | HTTP routes, config, schemas, lifecycle               | I/O contract               |
| `routing/`       | Intent classification + handler dispatch              | "what should run"          |
| `agent/`         | Graph, nodes, tools, prompts                          | Task-completing behavior   |
| `memory/`        | Short-term window, semantic cache, long-term store    | What the agent remembers   |
| `security/`      | Runtime defense harness + agent contract              | Safety / enforcement       |
| `observability/` | Tracing, cost, feedback                               | Visibility                 |
| `evaluation/`    | Golden set, eval runner, judges, results              | Quality bar                |

## Claude Code in the loop

- **`CLAUDE.md`** loads at session start and defines the contract above.
- **`.claude/rules/`** carves it into focused, scope-tagged rules.
- **`.claude/commands/`** captures repeatable workflows (`/review`, `/fix-issue`).
- **`.claude/skills/`** ships reusable expertise that auto-invokes on context match.
- **`.claude/agents/`** isolates risky review work (code-reviewer, security-auditor).
- **`.claude/hooks/`** runs deterministic checks at lifecycle events.
- **`.mcp.json`** wires in external tools (GitHub for `code_search`, Postgres, Slack).
