# Package marker for `evaluation`.
#
# Golden-dataset replay (offline) + production-traffic sampling (online), scored
# by judges in `judges/`. Tracked history per experiment lands under `results/`.
#
# Why it lives next to (not inside) `tests/`: evals measure FEATURE QUALITY
# (does this answer satisfy the user?); tests measure CODE CORRECTNESS (does
# this function do what it claims?). Both matter; they need different
# infrastructure.
