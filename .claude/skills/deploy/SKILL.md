---
name: deploy
description: Reusable expertise for building, tagging, and shipping container images. Auto-invoked when the user mentions deploy, release, ship, or cut a version.
---

# Deploy Skill

Apply when the task involves shipping a new version of the app.

## Pre-flight

1. Confirm we are on the release branch and `git status` is clean.
2. `make check` is green.
3. `make eval` golden-set scores have not regressed.
4. `security/contract.yaml` `control_mode` is correct for the target env
   (not left on `audit` for production).
5. `CHANGELOG.md` has an entry for the new version.

## Steps

1. Bump the version in `pyproject.toml`.
2. Build images: `docker compose -f deploy/docker-compose.yml build`.
3. Tag: `docker tag <repo>/app:latest <repo>/app:<version>`.
4. Push: `docker push <repo>/app:<version>` and `:latest`.
5. Create a git tag: `git tag -a v<version> -m "v<version>"` then push.
6. **Stop.** Do not roll out automatically - hand off to a human for the actual deploy
   (prod overlay: `deploy/docker-compose.prod.yml`).

See `deploy-config.md` for environment-specific knobs.
