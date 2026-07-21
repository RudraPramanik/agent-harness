# Delta for Deployment

## ADDED Requirements

### Requirement: Free-tier production stack

The system SHALL be deployable at $0/month using Render (API), Streamlit Community Cloud (UI), and Neon (Postgres).

#### Scenario: API on Render

- **WHEN** the FastAPI service is deployed with `docker/Dockerfile.service` on Render port 8080
- **THEN** `/health` and `/info` endpoints are publicly reachable over HTTPS

#### Scenario: UI on Streamlit Cloud

- **WHEN** Streamlit Cloud runs `src/streamlit_app.py` with secrets `AGENT_URL` and `AUTH_SECRET`
- **THEN** users can chat with agents via the public Streamlit URL

#### Scenario: Persistent memory on Neon

- **WHEN** Render env vars point to Neon Postgres with `DATABASE_TYPE=postgres`
- **THEN** conversation threads survive API redeploys

### Requirement: Environment configuration

The system SHALL document all required environment variables in `.env.example` and load them via pydantic-settings (`src/core/settings.py`).

#### Scenario: Minimum Gemini deploy config

- **WHEN** deploying to production
- **THEN** operators set `GOOGLE_API_KEY`, `DEFAULT_MODEL`, `AUTH_SECRET`, `DATABASE_TYPE=postgres`, and `POSTGRES_*` on Render; `AGENT_URL` and `AUTH_SECRET` on Streamlit

#### Scenario: Secrets not in git

- **WHEN** a developer configures API keys or passwords
- **THEN** values live in `.env` (gitignored) or host secret panels, never committed

### Requirement: Pre-deploy verification

The system SHALL pass a defined smoke-test checklist before production is considered live.

#### Scenario: Local smoke test

- **WHEN** running locally with `python src/run_service.py` and `streamlit run src/streamlit_app.py`
- **THEN** UI loads with branding, agent list appears, chat works, `/info` and `/health` return success

#### Scenario: Production smoke test

- **WHEN** deployment is complete
- **THEN** API `/info` returns JSON, Streamlit loads without agent-connection errors, end-to-end Gemini chat works, thread history persists after refresh, and unauthorized requests are rejected

### Requirement: Operational constraints

The system SHALL document known free-tier limitations so operators can plan demos and ops.

#### Scenario: Render cold start

- **WHEN** the Render free-tier API has been idle ~15 minutes
- **THEN** the first request may take 30–60 seconds; operators wake the API via `/health` before demos

#### Scenario: SQLite not for production deploy

- **WHEN** `DATABASE_TYPE=sqlite` is used on Render
- **THEN** conversation data is lost on redeploy (acceptable for throwaway demos only)

### Requirement: CI on GitHub

The system SHALL run automated tests on push via `.github/workflows/test.yml` (lint, mypy, pytest, Docker build).

#### Scenario: CI passes before publish

- **WHEN** code is pushed to GitHub
- **THEN** the test workflow runs and must pass before the repo is considered publish-ready
