# Package marker for `evaluation.judges`.
#
# Judges score a single agent output along one dimension. `eval_runner.py` applies
# the relevant judges to each golden-set item (offline) and to sampled traces
# (online). Keep each judge small, single-purpose, and independently testable.
#
# Typical judges:
#   relevance_judge.py    - did the answer address the question?
#   faithfulness_judge.py - is the answer grounded in retrieved/tool evidence?
#   safety_judge.py       - did the output respect the security contract?
#   tool_choice_judge.py  - did the agent pick appropriate tools?
#
# A judge may be programmatic (regex/metric) or LLM-as-judge. LLM judges should use
# a fixed model + temperature 0 so scores are reproducible across runs.
