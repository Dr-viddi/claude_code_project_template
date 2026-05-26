"""Offline evaluation runner. Replays the golden dataset against the pipeline."""

from __future__ import annotations

import json
from pathlib import Path


GOLDEN = Path(__file__).parent / "golden_dataset.json"
RESULTS_DIR = Path(__file__).parent / "eval_results"


def load_golden() -> dict:
    return json.loads(GOLDEN.read_text())


def run() -> None:
    """Run the golden set through the pipeline and write per-item scores to RESULTS_DIR."""
    raise NotImplementedError


if __name__ == "__main__":
    run()
