# Deployment

This template ships with `docker-compose.yml` for local development and a
`deploy` skill (`.claude/skills/deploy/`) for production releases.

## Local

```bash
cp .env.example .env       # then fill in API keys
docker compose up --build
```

- API: http://localhost:8000
- Frontend: http://localhost:8501
- Postgres: localhost:5432
- Redis: localhost:6379

`docker compose down -v` to wipe volumes.

## Production

Use the `/deploy` skill or follow these steps manually:

1. Ensure `make check` and `make eval` both pass.
2. Bump version in `pyproject.toml` and add a `CHANGELOG.md` entry.
3. Build, tag, push:
   ```bash
   docker compose build
   docker tag <repo>/app:latest <repo>/app:<version>
   docker push <repo>/app:<version> <repo>/app:latest
   ```
4. Tag the release:
   ```bash
   git tag -a v<version> -m "v<version>"
   git push origin v<version>
   ```
5. Roll out via your orchestrator (Kubernetes / ECS / Fly / ...).
6. Smoke test - see `.claude/skills/deploy/deploy-config.md`.

## Configuration

All configuration is environment-variable driven (`app/config.py`). The variables
listed in `.env.example` cover the full surface.
