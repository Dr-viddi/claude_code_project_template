# app/Dockerfile
#
# Intention:
#   Container image for the API + agent service. Built by the deploy/ compose files
#   and by the `deploy` skill. Slim, reproducible, runs as non-root in production.
#
# What this file should contain:
#   - A slim Python base image matching `requires-python` in `pyproject.toml`.
#   - Standard env: PYTHONDONTWRITEBYTECODE=1, PYTHONUNBUFFERED=1, PIP_NO_CACHE_DIR=1.
#   - Copy `pyproject.toml` first, install deps, THEN copy source - keeps the
#     dependency layer cached across code changes.
#   - Copy every runtime package the agent needs:
#       app/  agent/  memory/  routing/  security/  observability/
#   - Expose the API port (8000).
#   - CMD using uvicorn (or gunicorn+uvicorn workers for prod).
#
# Build context is the repo ROOT (the deploy/ compose files set `context: ..`).
#
# Example (commented; remove the leading '#' to activate):
#
# FROM python:3.11-slim
# ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
# WORKDIR /srv
# COPY pyproject.toml ./
# RUN pip install --upgrade pip && pip install -e .
# COPY app ./app
# COPY agent ./agent
# COPY memory ./memory
# COPY routing ./routing
# COPY security ./security
# COPY observability ./observability
# EXPOSE 8000
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
