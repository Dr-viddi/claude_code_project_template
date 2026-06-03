# evaluation/judges/relevance_judge.py
#
# Purpose
#   Example judge. Scores how well an agent answer addresses the user's
#   question. Use it as the pattern for the other judges (faithfulness, safety,
#   tool_choice).
#
# When you want a file like this
#   The first non-trivial agent eval. Start with one judge (relevance), prove
#   the eval loop works, then add more dimensions.
#
# Why it matters
#   - Programmatic judges (keyword coverage, regex, structured checks) are
#     deterministic, fast, and free - perfect for CI.
#   - LLM-as-judge variants give graded quality scores but need a pinned model +
#     temperature 0 for reproducibility.
#   - A common return shape (`{"score": float in [0,1], "rationale": str}`) lets
#     the eval runner aggregate across judges without per-judge plumbing.
#
# What goes in it
#   - A judge class with `name` and a `score(...)` method returning the common shape.
#   - Inputs depend on the judge: relevance needs the answer + expected
#     keywords; faithfulness needs the answer + retrieved context; safety
#     needs the answer + contract; tool_choice needs the tools_used + ground truth.
#   - No dependency on the agent's own code - judges evaluate from the outside.
#
# Example (commented)
#
#   class RelevanceJudge:
#       name = "relevance"
#       def score(self, answer: str, expected_keywords: list[str]) -> dict[str, object]:
#           if not expected_keywords:
#               return {"score": 1.0, "rationale": "no expected keywords"}
#           hits = [kw for kw in expected_keywords if kw.lower() in answer.lower()]
#           score = len(hits) / len(expected_keywords)
#           return {"score": round(score, 3), "rationale": f"matched {len(hits)}/{len(expected_keywords)}"}
