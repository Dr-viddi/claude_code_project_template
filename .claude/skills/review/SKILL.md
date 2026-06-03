---
name: review
description: Reusable code-review expertise. Auto-invoked when the user asks Claude to review a diff, PR, or set of staged changes. Also exposed as the /review slash command.
---

# Review Skill

Apply this skill whenever the task involves evaluating code quality on an existing
diff. It is the same logic the `/review` slash command runs, but auto-invoked when
the task context matches (keywords: "review", "look over", "feedback on this PR").

## What to check

1. **Correctness** - bugs, edge cases, off-by-ones, race conditions.
2. **Style** - `.claude/rules/code-style.md` compliance.
3. **Tests** - is the change tested? Does it regress existing tests?
4. **Architecture** - does it respect the layering described in `CLAUDE.md`?
5. **Security** - if `security/`, `agent/tools/`, `routing/`, or any auth path changed,
   escalate to the `security-auditor` sub-agent.
6. **Observability** - new agent nodes/tools need tracing via `observability/tracer.py`.

## Output format

A numbered list. Each item: severity (blocker / major / minor / nit), file:line, brief
description, suggested fix.

## When to fork into a sub-agent

If the diff is larger than ~500 lines or spans multiple subsystems, fork into the
`code-reviewer` sub-agent (own context window). For diffs touching `security/` or
`agent/tools/`, always also fork into `security-auditor`.
