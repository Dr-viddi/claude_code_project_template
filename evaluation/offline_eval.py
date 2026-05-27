# evaluation/offline_eval.py
#
# Intention:
#   Nightly (and pre-merge) evaluation pass. Replays every item in
#   `evaluation/golden_dataset.json` through the live pipeline, scores the
#   output against the expected criteria, and writes a per-run report to
#   `evaluation/eval_results/<date>/`.
#
# What this file should contain:
#   - `load_golden()` helper that reads `golden_dataset.json`.
#   - `run()` orchestrator that:
#       * Boots the pipeline (the same one production uses).
#       * Iterates the dataset, collecting answers + per-stage timings.
#       * Computes metrics (keyword recall, semantic similarity, faithfulness,
#         citation coverage, latency, cost).
#       * Writes a JSON report + a Markdown summary into `eval_results/<date>/`.
#   - A `__main__` block so it can be invoked via `python -m evaluation.offline_eval`
#     or `make eval`.
#   - CI should fail the build if the golden-set score regresses by more than
#     the threshold defined in `.claude/rules/testing.md`.
#
# Example (commented):
#
#   GOLDEN = Path(__file__).parent / "golden_dataset.json"
#   RESULTS_DIR = Path(__file__).parent / "eval_results"
#   def run() -> None: ...
#   if __name__ == "__main__":
#       run()
