# Testing

Scope: `tests/` and `evaluation/`.

## Philosophy

- **Tests verify code correctness, evals verify feature quality.** Both are required.
- Every bug fix gets a regression test before the fix lands.
- Every new prompt, tool, or routing change updates `evaluation/golden_dataset.json`.

## Layout

```
tests/
├── test_agent.py        # agent graph, nodes, memory integration
├── test_tools.py        # agent/tools: validation, timeouts, contracts
├── test_security.py     # harness wiring + contract.yaml parsing/gating
├── test_routing.py      # intent classifier + handler registry
└── conftest.py          # shared fixtures (fake_llm, fake_redis, fake_deps, ...)
```

## Conventions

- **Framework:** pytest.
- **Fixtures:** in `conftest.py`, scoped as narrowly as possible.
- **Naming:** `test_<unit>_<scenario>_<expected>`. Example:
  `test_classifier_smalltalk_returns_chitchat`.
- **AAA structure:** Arrange / Act / Assert, with a blank line between sections.
- **Mock at the boundary.** Mock the LLM client and the harness backend, not your
  own nodes/services.
- **No network in unit tests.** Use VCR / recorded responses for HTTP.

## Coverage

- Library code: aim for 90%+ branch coverage.
- API routes: every status code path covered.
- Agent behavior and prompts: covered via golden-dataset evals + judges, not unit tests.
- Security: contract parsing and gating logic are unit-tested; the vendor backend is mocked.

## Evaluation

- `evaluation/eval_runner.py offline` runs nightly against `golden_dataset.json` in CI.
- `evaluation/eval_runner.py online` samples production traffic.
- Judges in `evaluation/judges/` score each item; results land in
  `evaluation/results/<experiment>/<date>/`.
- A change must not regress the golden-set scores by more than 2% to merge.
