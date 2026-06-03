# evaluation/judges/relevance_judge.py
#
# Intention:
#   Example judge. Scores how well an agent answer addresses the user's question.
#   Use it as the pattern for the other judges (faithfulness, safety, tool_choice).
#
# What this file should contain:
#   - A `RelevanceJudge` class with:
#       * Constructor taking the judge LLM client (fixed model, temperature 0) or a
#         programmatic scorer.
#       * An async `score(question, answer, context=None)` -> a float in [0, 1] plus
#         a short rationale string.
#   - A stable output schema (JSON mode) so `eval_runner.py` can aggregate scores.
#   - No dependency on the agent's own code - judges evaluate from the outside.
#
# Example (commented):
#
#   class RelevanceJudge:
#       name = "relevance"
#       def __init__(self, judge_llm): ...
#       async def score(self, question: str, answer: str, context: str | None = None) -> dict:
#           # returns {"score": 0.0..1.0, "rationale": "..."}
#           ...
