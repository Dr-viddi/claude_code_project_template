"""Example judge: keyword-coverage relevance score.

Programmatic and deterministic so evals run offline. Use it as the pattern for
LLM-as-judge variants (fixed model, temperature 0) - keep the same return shape:
``{"score": float in [0,1], "rationale": str}``.
"""

from __future__ import annotations


class RelevanceJudge:
    name = "relevance"

    def score(self, answer: str, expected_keywords: list[str]) -> dict[str, object]:
        if not expected_keywords:
            return {"score": 1.0, "rationale": "no expected keywords"}
        hay = answer.lower()
        hits = [kw for kw in expected_keywords if kw.lower() in hay]
        score = len(hits) / len(expected_keywords)
        return {
            "score": round(score, 3),
            "rationale": f"matched {len(hits)}/{len(expected_keywords)}: {hits}",
        }
