# Makefile
#
# Intention:
#   The one place to look for "how do I do X in this repo?" Every common task
#   - install, run, test, lint, type-check, eval - is a make target. CI calls
#   these targets too, so local and CI stay in sync.
#
# What this file should declare (suggested targets):
#   - install   : pip install -e ".[dev]"
#   - run       : docker compose up --build
#   - test      : pytest
#   - lint      : ruff check .
#   - typecheck : mypy app observability evaluation
#   - format    : ruff check --fix . && black .
#   - check     : lint + typecheck + test           (called from CI and pre-push)
#   - eval      : python -m evaluation.offline_eval
#   - clean     : remove caches and build artifacts
#
# Tabs, not spaces, in recipe lines.
#
# Example (commented; remove the leading '#' to activate):
#
# .PHONY: install run test lint typecheck check eval format clean
#
# install:
# 	pip install -e ".[dev]"
#
# run:
# 	docker compose up --build
#
# test:
# 	pytest
#
# lint:
# 	ruff check .
#
# typecheck:
# 	mypy app observability evaluation
#
# format:
# 	ruff check --fix .
# 	black .
#
# check: lint typecheck test
#
# eval:
# 	python -m evaluation.offline_eval
#
# clean:
# 	rm -rf .pytest_cache .mypy_cache .ruff_cache build dist *.egg-info
# 	find . -type d -name __pycache__ -exec rm -rf {} +
