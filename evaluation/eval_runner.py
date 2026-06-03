# evaluation/eval_runner.py
#
# Purpose
#   Single entry point for both offline and online evaluation. Offline replays
#   `golden_dataset.json` through the agent and scores each item with the judges
#   in `judges/`. Online samples production traffic. Both write tracked,
#   per-experiment history into `results/<experiment>/<date>/`.
#
# When you want a file like this
#   Any agent past prototype. Without evals, prompt and tool changes are
#   guesswork: did I improve it, or did I just like the first example I checked?
#
# Why it matters
#   - A non-zero exit code on regression lets CI gate merges - the only sane
#     way to enforce a quality bar across a team.
#   - Tracked results in `results/<experiment>/<date>/` give you the
#     before/after diff for every PR that touches prompts.
#   - Offline + online share scorers, so a problem caught in production maps
#     cleanly back to a golden-set repro.
#
# What goes in it
#   - `load_golden()` - read evaluation/golden_dataset.json.
#   - `run_offline(experiment)` - boot the same agent prod uses, loop over the
#     dataset, score each item, write a report + summary into results/.
#   - `run_online(sample_rate)` - subsample production traces, re-score, append
#     to the same history so offline/online are comparable.
#   - An argparse CLI with `offline` / `online` subcommands so `make eval` and
#     scheduled jobs both call the same code.
#   - CI gate: exit non-zero if golden-set scores regress beyond the threshold
#     in .claude/rules/testing.md.
#
# Example (commented)
#
#   def run_offline(experiment: str) -> int:
#       data = load_golden()
#       rows = asyncio.run(_run_items(data["items"]))
#       out_dir = RESULTS / experiment / date.today().isoformat()
#       out_dir.mkdir(parents=True, exist_ok=True)
#       (out_dir / "report.json").write_text(json.dumps(rows, indent=2))
#       passed = sum(r["passed"] for r in rows)
#       return 0 if passed == len(rows) else 1
#
#   if __name__ == "__main__":
#       sys.exit(main())   # python -m evaluation.eval_runner offline --experiment baseline
