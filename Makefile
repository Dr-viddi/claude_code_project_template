.PHONY: install run test lint typecheck check eval format clean

install:
	pip install -e ".[dev]"

run:
	docker compose up --build

test:
	pytest

lint:
	ruff check .

typecheck:
	mypy app observability evaluation

format:
	ruff check --fix .
	black .

check: lint typecheck test

eval:
	python -m evaluation.offline_eval

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
