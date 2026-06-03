# Deployment

Compose files live in `deploy/`: `docker-compose.yml` (dev) and
`docker-compose.prod.yml` (production overlay - GPU, health checks, non-root,
resource limits). The `deploy` skill (`.claude/skills/deploy/`) drives releases.

## Local

```bash
cp .env.example .env       # then fill in API keys (incl. the harness key)
docker compose -f deploy/docker-compose.yml up --build
```

- API: http://localhost:8000
- Postgres: localhost:5432
- Redis: localhost:6379
- Frontend (if you keep it): http://localhost:8501

`docker compose -f deploy/docker-compose.yml down -v` to wipe volumes.

## Production

Use the `/deploy` skill or follow these steps manually:

1. Ensure `make check` and `make eval` both pass.
2. Confirm the agent contract (`security/contract.yaml`) is set to the intended
   `control_mode` for prod (usually `human_in_the_loop` or `block`, not `audit`).
3. Bump version in `pyproject.toml` and add a `CHANGELOG.md` entry.
4. Build, tag, push:
   ```bash
   docker compose -f deploy/docker-compose.yml build
   docker tag <repo>/app:latest <repo>/app:<version>
   docker push <repo>/app:<version> <repo>/app:latest
   ```
5. Tag the release:
   ```bash
   git tag -a v<version> -m "v<version>"
   git push origin v<version>
   ```
6. Roll out with the prod overlay:
   ```bash
   docker compose -f deploy/docker-compose.yml -f deploy/docker-compose.prod.yml up -d
   ```
7. Smoke test - see `.claude/skills/deploy/deploy-config.md`.

## Configuration

All configuration is environment-variable driven (`app/config.py`). The variables
listed in `.env.example` cover the full surface, including the runtime defense
harness key and alert webhook URLs referenced by `security/contract.yaml`.
