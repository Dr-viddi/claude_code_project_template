# Makefile
#
# Intention:
#   The one place to look for "how do I do X in this repo?" Every common task is a
#   make target, and CI calls these same targets so local and CI stay in sync.
#
# What this file should declare (suggested targets):
#   - install   : pip install -e ".[dev]"
#   - run       : docker compose -f deploy/docker-compose.yml up --build
#   - run-prod  : docker compose -f deploy/docker-compose.yml -f deploy/docker-compose.prod.yml up -d
#   - test      : pytest
#   - lint      : ruff check .
#   - typecheck : mypy app agent memory routing security evaluation observability
#   - format    : ruff check --fix . && black .
#   - check     : lint + typecheck + test            (called from CI and pre-push)
#   - eval      : python -m evaluation.eval_runner offline --experiment baseline
#   - clean     : remove caches and build artifacts
#
# Tabs, not spaces, in recipe lines.
#
# Example (commented; remove the leading '#' to activate):
#
# .PHONY: install run run-prod test lint typecheck check eval format clean
#
# install:
# 	pip install -e ".[dev]"
#
# run:
# 	docker compose -f deploy/docker-compose.yml up --build
#
# run-prod:
# 	docker compose -f deploy/docker-compose.yml -f deploy/docker-compose.prod.yml up -d
#
# test:
# 	pytest
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
