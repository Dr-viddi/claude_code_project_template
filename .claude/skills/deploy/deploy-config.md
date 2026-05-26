# Deploy Configuration

Environment-specific knobs referenced by the `deploy` skill.

## Environments

| Env       | Cluster           | Registry                  | Promotion gate         |
| --------- | ----------------- | ------------------------- | ---------------------- |
| `dev`     | `<dev-cluster>`   | `<registry>/<project>`    | merge to `main`        |
| `staging` | `<stg-cluster>`   | `<registry>/<project>`    | manual approval        |
| `prod`    | `<prd-cluster>`   | `<registry>/<project>`    | tag `vX.Y.Z` + sign-off |

## Required secrets

- `REGISTRY_USER`, `REGISTRY_PASSWORD`
- `KUBECONFIG_<env>`
- `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` (whichever the app uses)

## Smoke tests after deploy

- `GET /healthz` returns 200.
- `GET /readyz` returns 200 within 30s of pod start.
- One end-to-end query through `/v1/chat` returns under the SLO (p95 < 3s).
