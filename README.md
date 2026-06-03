# Claude Code Project Template

A **scaffold** for production AI **agent** projects developed with **Claude Code**
as the primary AI pair-programmer. It combines two best-practice blueprints:

- **The Claude Code project anatomy** - a `CLAUDE.md` "project brain" and a
  `.claude/` directory holding settings, rules, commands, skills, sub-agents and hooks.
- **The production-agent architecture** - an agent core (state-machine graph,
  nodes, tools, prompts), memory, routing, an 8-layer runtime defense harness,
  evaluation with judges, observability, and deploy configs.

> **This is not a runnable project.** Every source file is a comment-only stub
> that describes its *intent*, *what it should contain*, and a commented example.
> Copy this repo, rename it, then fill in the stubs to start building.

Clone it, rename it, run `/init` inside Claude Code to refresh `CLAUDE.md`
against your actual code, and replace the stub comments with real implementations.

---

## What's in the box

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
│   ├── graph.py              #   state machine (plan → act → observe)
│   ├── nodes.py              #   individual graph nodes
│   ├── tools/                #   crm, web_search, code_search (MCP)
│   └── prompts/              #   versioned system + per-intent templates
├── memory/                   # conversation (window), semantic_cache, long_term
├── routing/                  # intent classifier + handler registry
├── security/                 # Runtime defense harness
│   ├── adrian_init.py        #   two-line wrap of the agent (8 layers)
│   └── contract.yaml         #   agent contract: scope, thresholds, control mode
├── evaluation/               # golden_dataset, eval_runner, judges/, results/
├── observability/            # tracer, feedback, cost_tracker
├── data/                     # raw → processed → index config
├── tests/                    # test_agent, test_tools, test_security, test_routing
├── deploy/                   # docker-compose (dev) + docker-compose.prod (GPU, hardened)
├── docs/                     # architecture, API reference, deployment
├── scripts/                  # seed, migrate, healthcheck (optional helpers)
├── frontend/                 # optional UI, containerized separately
├── pyproject.toml
└── README.md
```

See `docs/architecture.md` for a full walkthrough.

## The runtime defense harness

`security/` wraps the agent in an always-on harness that gates tool calls and
reasoning *before* they execute. The 8 layers (configured in `contract.yaml`):

1. **Define the agent contract** - scope, boundaries, enforcement mode.
2. **Capture actions + reasoning** - intercept tool calls, pair with reasoning, correlate per session.
3. **Scrub PII before it leaves** - client-side regex + server-side LLM sweep.
4. **Analyze the reasoning trace** - catch intent before the action runs.
5. **Harden the analyser** - sandboxed (no tools/MCP/internet), inputs spotlighted as untrusted.
6. **Tier the verdict by severity** - low → critical, per-agent action threshold.
7. **Choose the control mode** - audit · human-in-the-loop · block.
8. **Push alerts to channels** - severity-gated Slack/Discord routing.

> The harness in the blueprint is "Adrian" (`adrian-sdk`), a specific third-party
> product. `security/adrian_init.py` is written as a **provider-agnostic seam** -
> wire in that SDK, another runtime-defense product, or your own implementation.

## Getting started

```bash
# 1. Use this repo as a GitHub template, then clone your new project
git clone <your-new-repo>
cd <your-new-repo>

# 2. Copy local override stubs
cp CLAUDE.local.md.example CLAUDE.local.md
cp .claude/settings.local.json.example .claude/settings.local.json

# 3. Open in Claude Code
claude
```

Inside the Claude Code session:

- Edit `CLAUDE.md` to describe your project (name, purpose, stack).
- Walk each stub file. Each explains its intended role and includes a commented
  example. Replace the comments with real code as you implement.
- Run `/init` once you have meaningful code so Claude can regenerate `CLAUDE.md`
  from the live tree.
- Use `/review` and `/fix-issue` (in `.claude/commands/`) for repeatable workflows.

## Conventions

- **`CLAUDE.md` is the contract.** Update it whenever architecture or workflow rules change.
- **`.claude/rules/*.md`** are scoped, modular conventions - prefer adding a new rule file over
  bloating `CLAUDE.md`.
- **Hooks block what shouldn't happen** (e.g. `validate-bash.sh` rejects dangerous commands).
- **Sub-agents own isolated context.** Use them for code review, security audits, or any task
  whose results you don't want clogging the main window.
- **MCP servers** live in `.mcp.json` - committed so the whole team shares the same external tools.
- **The agent contract (`security/contract.yaml`) is reviewed like code.** Changes to the agent's
  guardrails go through PR review.
