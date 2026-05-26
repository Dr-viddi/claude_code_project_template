"""Online monitor. Samples production traffic and scores it against quality rubrics."""

from __future__ import annotations


def sample_and_score(sample_rate: float = 0.01) -> None:
    """Tap a fraction of live requests, score them, push to RESULTS_DIR."""
    raise NotImplementedError


if __name__ == "__main__":
    sample_and_score()
