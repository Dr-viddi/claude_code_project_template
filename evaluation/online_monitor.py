# evaluation/online_monitor.py
#
# Intention:
#   Continuous quality monitor in production. Samples a configurable fraction of
#   live traffic, re-scores it against quality rubrics, and writes results back
#   into `eval_results/<date>/`. Surfaces drift the golden set won't catch.
#
# What this file should contain:
#   - A `sample_and_score(sample_rate)` function that:
#       * Pulls traces from the observability backend.
#       * Subsamples deterministically (so re-runs are reproducible).
#       * Scores each sampled response (LLM-as-judge or programmatic rubric).
#       * Aggregates into a daily report.
#   - A `__main__` block so it can run as a scheduled job (cron, k8s CronJob).
#
# Example (commented):
#
#   def sample_and_score(sample_rate: float = 0.01) -> None: ...
#   if __name__ == "__main__":
#       sample_and_score()
