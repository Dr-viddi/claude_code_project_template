# Testing

Scope: `tests/` and `evaluation/`.

## Philosophy

- **Tests verify code correctness, evals verify feature quality.** Both are required.
- Every bug fix gets a regression test before the fix lands.
- Every new prompt or retrieval change updates `evaluation/golden_dataset.json`.

## Layout

```
tests/
├── test_retrieval.py     # hybrid_retriever + reranker
├── test_cache.py         # semantic cache hit/miss
├── test_routing.py       # query router + adaptive router
└── conftest.py           # shared fixtures
```

## Conventions

- **Framework:** pytest.
- **Fixtures:** in `conftest.py`, scoped as narrowly as possible.
- **Naming:** `test_<unit>_<scenario>_<expected>`. Example:
  `test_reranker_empty_input_returns_empty_list`.
- **AAA structure:** Arrange / Act / Assert, with a blank line between sections.
- **Mock at the boundary.** Mock the LLM client, not your own services.
- **No network in unit tests.** Use VCR / recorded responses for HTTP.

## Coverage

- Library code: aim for 90%+ branch coverage.
- API routes: every status code path covered.
- Agents and prompts: covered via golden-dataset evals, not unit tests.

## Evaluation

- `evaluation/offline_eval.py` runs nightly against `golden_dataset.json` in CI.
- `evaluation/online_monitor.py` samples production traffic; results land in
  `evaluation/eval_results/<date>/`.
- A change must not regress the golden-set scores by more than 2% to merge.
