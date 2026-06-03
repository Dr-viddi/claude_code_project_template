# Makefile
#
# Purpose
#   The one place to look for "how do I do X in this repo?" Every common task -
#   install, run, test, lint, type-check, eval - is a make target. CI calls the
#   same targets, so local and CI stay in sync.
#
# When you want a file like this
#   Every project. Even a 3-target Makefile (`install`, `test`, `check`)
#   eliminates a class of "what's the command again?" friction.
#
# Why it matters
#   - One command per task means contributors run `make check` instead of
#     remembering "ruff check . && black --check . && mypy app && pytest".
#   - CI and local invocations converge on the same definitions - if local
#     passes, CI passes (and vice versa).
#   - `make help` (if you add it) doubles as inline docs.
#
# What goes in it (typical targets)
#   - install   : pip install -e ".[dev]"
#   - serve     : run the API locally without Docker
#   - run       : docker compose -f deploy/docker-compose.yml up --build
#   - run-prod  : docker compose -f deploy/docker-compose.yml -f deploy/docker-compose.prod.yml up -d
#   - test      : pytest -q
#   - lint      : ruff check .
#   - typecheck : mypy app agent memory routing security evaluation observability
#   - format    : ruff check --fix . && black .
#   - check     : lint + typecheck + test       (CI + pre-push gate)
#   - eval      : python -m evaluation.eval_runner offline --experiment baseline
#   - clean     : remove caches and build artifacts
#
# Tabs, not spaces, in recipe lines.
#
# Example (commented; uncomment + edit)
#
# .PHONY: install serve run test lint typecheck format check eval clean
#
# install:
# 	pip install -e ".[dev]"
#
# serve:
# 	uvicorn app.main:app --reload --port 8000
#
# run:
# 	docker compose -f deploy/docker-compose.yml up --build
#
# test:
# 	pytest -q
#
# lint:
# 	ruff check .
#
# typecheck:
# 	mypy app agent memory routing security evaluation observability
#
# format:
# 	ruff check --fix .
# 	black .
#
# check: lint typecheck test
#
# eval:
# 	python -m evaluation.eval_runner offline --experiment baseline
#
# clean:
# 	rm -rf .pytest_cache .mypy_cache .ruff_cache build dist *.egg-info
# 	find . -type d -name __pycache__ -exec rm -rf {} +
