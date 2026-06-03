# evaluation/eval_runner.py
#
# Intention:
#   Single entry point for both offline and online evaluation (replaces the split
#   offline_eval / online_monitor scripts). Offline mode replays the golden set
#   pre-merge and in CI; online mode samples live traffic. Both write tracked,
#   per-experiment history into `evaluation/results/<experiment>/<date>/`.
#
# What this file should contain:
#   - `load_golden()` - read `evaluation/golden_dataset.json`.
#   - `run_offline(experiment)` - replay the golden set through the agent, score each
#     item with the judges in `evaluation/judges/`, write a report under results/.
#   - `run_online(sample_rate)` - subsample production traces, re-score, append to
#     the same results history so offline and online are comparable.
#   - A CLI (`argparse`) with `offline` / `online` subcommands so it can run from
#     `make eval` and from a scheduled CI/cron job.
#   - CI gate: fail if the golden-set score regresses beyond the threshold in
#     `.claude/rules/testing.md`.
#
# Example (commented):
#
#   GOLDEN = Path(__file__).parent / "golden_dataset.json"
#   RESULTS = Path(__file__).parent / "results"
#
#   def run_offline(experiment: str) -> None: ...
#   def run_online(sample_rate: float = 0.01) -> None: ...
#
#   if __name__ == "__main__":
#       # python -m evaluation.eval_runner offline --experiment baseline
#       ...
