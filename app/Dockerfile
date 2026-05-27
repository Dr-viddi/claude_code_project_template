# app/Dockerfile
#
# Intention:
#   Container image for the API service. Built by `docker compose build` (local)
#   and by the `deploy` skill (release). Should be slim, reproducible, and run
#   as a non-root user in production.
#
# What this file should contain:
#   - A slim Python base image matching `requires-python` in `pyproject.toml`.
#   - Standard env: `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUNBUFFERED=1`,
#     `PIP_NO_CACHE_DIR=1`.
#   - Copy `pyproject.toml` first, install deps, then copy the source - this
#     keeps the dependency layer cached across code changes.
#   - Expose the API port (8000 by convention).
#   - CMD using `uvicorn` (or `gunicorn -k uvicorn.workers.UvicornWorker` for prod).
#
# Example (commented; remove the leading '#' to activate):
#
# FROM python:3.11-slim
# ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
# WORKDIR /srv
# COPY pyproject.toml ./
# RUN pip install --upgrade pip && pip install -e .
# COPY app ./app
# COPY observability ./observability
# EXPOSE 8000
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
