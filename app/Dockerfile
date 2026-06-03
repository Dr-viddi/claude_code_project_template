# API + agent image. Build context is the repo root (see deploy/docker-compose.yml).
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /srv

# Runtime packages the agent needs (evaluation/ and tests/ are dev-only, omitted).
COPY pyproject.toml README.md ./
COPY app ./app
COPY agent ./agent
COPY memory ./memory
COPY routing ./routing
COPY security ./security
COPY observability ./observability

# Install the package + its runtime deps. (For faster rebuilds you can split this
# into a cached "deps only" layer; kept simple here.)
RUN pip install --upgrade pip && pip install .

# Non-root.
RUN useradd --uid 10001 --no-create-home appuser
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
