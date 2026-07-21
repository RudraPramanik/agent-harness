## Why

Branding is done locally, but the app is not yet live. The next milestone is a working CI/CD path and a $0/month deployment: FastAPI on Render, Postgres on Neon, Streamlit on Community Cloud. Operators need a single spec for which environment variables go where, how GitHub Actions fits in, and the exact Streamlit free-tier deploy steps — without re-reading the full BLUEPRINT.

## What Changes

- Document and implement the **recommended free-tier deploy stack** (Render + Neon + Streamlit Cloud).
- Add a **deployment env var matrix** per hosted service (API, UI, database).
- Replace or supplement the Azure-focused `deploy.yml` with a **Render-friendly CI/CD** path (test on push; optional deploy hook).
- Add **Streamlit Cloud** setup: `src/streamlit_app.py`, secrets TOML, `PYTHONPATH`, dependency detection.
- Add a **`.streamlit/secrets.toml.example`** or document secrets in README / deploy guide.
- Optionally add `requirements.txt` or ensure Streamlit Cloud can install from `pyproject.toml`.

## Capabilities

### New Capabilities

- `deployment`: Free-tier production topology, per-service environment variables, smoke-test checklist, operational constraints (cold starts, auth).
- `cicd`: GitHub Actions test pipeline, optional CD to Render via deploy hook, secrets required in GitHub.

### Modified Capabilities

- _(none in `openspec/specs/` yet for deployment — `project-blueprint-vision` delta not archived)_

## Impact

| Layer | Impact |
|-------|--------|
| **FastAPI (Render)** | Env: `GOOGLE_API_KEY`, `DEFAULT_MODEL`, `DATABASE_TYPE`, `POSTGRES_*`, `AUTH_SECRET`, `HOST`, `PORT` |
| **Streamlit Cloud** | Secrets: `AGENT_URL`, `AUTH_SECRET`; optional `PYTHONPATH=src` |
| **Neon Postgres** | Connection vars consumed by Render API only |
| **GitHub Actions** | `test.yml` unchanged; new or updated deploy workflow for Render hook |
| **Docs** | README deploy section, env reference |

### Non-goals

- Azure production deploy (keep existing workflow optional, not v1 path).
- Custom domain / Cloudflare (later).
- Auto-deploy Streamlit Cloud from GitHub Actions (Streamlit deploys on git push natively).
- Paid hosting or SLA guarantees.
