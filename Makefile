.PHONY: install run run-prod test lint typecheck format check eval clean

install:
	pip install -e ".[dev]"

run:
	docker compose -f deploy/docker-compose.yml up --build

run-prod:
	docker compose -f deploy/docker-compose.yml -f deploy/docker-compose.prod.yml up -d

# Run the API locally without Docker (offline: EchoLLM + in-memory + audit harness).
serve:
	uvicorn app.main:app --reload --port 8000

test:
	pytest -q

lint:
	ruff check .

typecheck:
	mypy app agent memory routing security evaluation observability

format:
	ruff check --fix .
	black .

check: lint typecheck test

eval:
	python -m evaluation.eval_runner offline --experiment baseline

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
