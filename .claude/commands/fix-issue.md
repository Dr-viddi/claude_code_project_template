---
name: fix-issue
description: End-to-end workflow to fix a GitHub issue - read, plan, implement, test, commit.
argument-hint: <issue-number>
---

# /fix-issue $ARGUMENTS

Resolve issue **#$ARGUMENTS** end-to-end.

Steps:

1. Fetch the issue via the GitHub MCP server. Read body, labels, and recent comments.
2. Use the `Explore` sub-agent to locate the relevant code paths.
3. Use the `Plan` sub-agent to draft an implementation plan. Present the plan to the
   user via `AskUserQuestion` before writing code.
4. Implement the fix on a feature branch named `fix/<issue-number>-<slug>`.
5. **Add a regression test** that reproduces the bug, then re-run the suite.
6. Run `make check` (lint + type + test). Iterate until green.
7. Commit with `fix: <summary> (#$ARGUMENTS)` and push to origin.
8. **Do not open a pull request unless the user explicitly asks.**
