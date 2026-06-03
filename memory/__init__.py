# Package marker for `memory`.
#
# Everything the agent remembers, across three time horizons:
#   conversation.py   - short-term: a sliding window of the current session
#   semantic_cache.py - mid-term: a repeat-query cache to skip redundant work
#   long_term.py      - long-term: episodic memory + an entity store across sessions
#
# Memory is read at the start of a turn (to assemble context) and written at the
# end (to persist what was learned). The agent graph in `agent/graph.py` owns the
# read/write points.
