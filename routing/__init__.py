# Package marker for `routing`.
#
# Turns an incoming request into a decision about how to handle it:
#   classifier.py       - classify the user's intent
#   handler_registry.py - map an intent to the handler/sub-graph that serves it
#
# Routing runs before the agent loop commits to a plan, so cheap/known intents
# can short-circuit the expensive loop and unsafe intents can be refused early.
