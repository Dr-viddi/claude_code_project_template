# app/Dockerfile
#
# Purpose
#   Container image for the API + agent service. Built by deploy/docker-compose.yml
#   (dev) and the deploy skill (release). Should be slim, reproducible, and run
#   as non-root in production.
#
# When you want a file like this
#   Any service you'll deploy as a container. Even single-developer projects
#   benefit from a Dockerfile - reproducibility across machines pays back fast.
#
# Why it matters
#   - Layer ordering (deps before source) caches the heavy install across code
#     changes - the difference between a 5-second and a 5-minute rebuild.
#   - Non-root + dropped capabilities is the cheapest container hardening you
#     can do, and most security scanners check for it.
#   - Build context = repo root (the compose file sets `context: ..`), so the
#     Dockerfile can copy every package the agent needs.
#
# What goes in it
#   - Slim Python base image matching requires-python in pyproject.toml.
#   - Standard env: PYTHONDONTWRITEBYTECODE=1, PYTHONUNBUFFERED=1, PIP_NO_CACHE_DIR=1.
#   - Copy pyproject.toml first, install deps, THEN copy source.
#   - Copy every runtime package: app/, agent/, memory/, routing/, security/,
#     observability/.
#   - Non-root user.
#   - EXPOSE the API port.
#   - CMD using uvicorn (or gunicorn+uvicorn workers for prod).
#
# Example (commented; uncomment to use as starting point)
#
# FROM python:3.11-slim
# ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
# WORKDIR /srv
# COPY pyproject.toml README.md ./
# RUN pip install --upgrade pip && pip install .
# COPY app ./app
# COPY agent ./agent
# COPY memory ./memory
# COPY routing ./routing
# COPY security ./security
# COPY observability ./observability
# RUN useradd --uid 10001 --no-create-home appuser
# USER appuser
# EXPOSE 8000
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
