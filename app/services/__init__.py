# Package marker for `app.services`.
#
# Services are where the workflow lives - pipeline orchestration, caching,
# conversation memory, query rewriting and routing. They coordinate components,
# agents, and security guards. Route handlers in `app/main.py` should delegate
# to a service rather than implementing logic inline.
