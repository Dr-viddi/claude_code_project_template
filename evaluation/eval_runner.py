"""Offline + online evaluation entry point.

Offline replays golden_dataset.json through the agent and scores each item with the
judges; results are written to evaluation/results/<experiment>/<date>/. Online mode
is a stub seam for sampling production traffic. Exit code is non-zero if any item
regresses below its min_score, so CI can gate on it.

    python -m evaluation.eval_runner offline --experiment baseline
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from datetime import date
from pathlib import Path

from agent.graph import Agent
from app.config import get_settings
from app.models import ChatRequest, Message
from evaluation.judges import RelevanceJudge

ROOT = Path(__file__).parent
GOLDEN = ROOT / "golden_dataset.json"
RESULTS = ROOT / "results"


def load_golden() -> dict:
    return json.loads(GOLDEN.read_text(encoding="utf-8"))


async def _run_items(items: list[dict]) -> list[dict]:
    agent = Agent.build(get_settings())
    judge = RelevanceJudge()
    rows: list[dict] = []
    for item in items:
        resp = await agent.ainvoke(
            ChatRequest(messages=[Message(role="user", content=item["query"])])
        )
        verdict = judge.score(resp.answer, item.get("expected_keywords", []))
        score = float(verdict["score"])  # type: ignore[arg-type]
        rows.append(
            {
                "id": item["id"],
                "score": score,
                "min_score": item.get("min_score", 0.0),
                "passed": score >= item.get("min_score", 0.0),
                "answer": resp.answer,
                "tools_used": resp.tools_used,
                "rationale": verdict["rationale"],
            }
        )
    return rows


def run_offline(experiment: str) -> int:
    data = load_golden()
    rows = asyncio.run(_run_items(data["items"]))

    out_dir = RESULTS / experiment / date.today().isoformat()
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "report.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")

    passed = sum(r["passed"] for r in rows)
    print(f"[eval:{experiment}] {passed}/{len(rows)} passed -> {out_dir}")
    for r in rows:
        flag = "ok " if r["passed"] else "FAIL"
        print(f"  {flag} {r['id']} score={r['score']} ({r['rationale']})")
    return 0 if passed == len(rows) else 1


def run_online(sample_rate: float) -> int:
    print(f"[eval:online] sampling {sample_rate:.1%} of traffic - wire to your trace store")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="eval_runner")
    sub = parser.add_subparsers(dest="mode", required=True)
    off = sub.add_parser("offline")
    off.add_argument("--experiment", default="baseline")
    on = sub.add_parser("online")
    on.add_argument("--sample-rate", type=float, default=0.01)

    args = parser.parse_args(argv)
    if args.mode == "offline":
        return run_offline(args.experiment)
    return run_online(args.sample_rate)


if __name__ == "__main__":
    sys.exit(main())
