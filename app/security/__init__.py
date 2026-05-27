# Package marker for `app.security`.
#
# Three guard layers: input (user -> service), content (retrieved docs -> prompt),
# output (model -> client). Every change touching this directory must run the
# `security-auditor` sub-agent before merge - see `CLAUDE.md` workflow rule #5.
