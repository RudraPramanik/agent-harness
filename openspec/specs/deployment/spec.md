# Deployment

## Purpose

Free-tier production deployment for AI Agent Studio: Neon Postgres, Render FastAPI API, and Streamlit Community Cloud UI at $0/month.

## Requirements

### Requirement: Free-tier three-service topology

The system SHALL be deployable at $0/month using Neon (Postgres), Render (FastAPI API), and Streamlit Community Cloud (UI).

#### Scenario: API on Render

- **WHEN** the FastAPI service is deployed with `docker/Dockerfile.service` on Render port 8080
- **THEN** `/health` and `/info` return success over HTTPS

#### Scenario: UI on Streamlit Cloud

- **WHEN** Streamlit Cloud runs `src/streamlit_app.py` from the connected GitHub repo
- **THEN** users reach a public `*.streamlit.app` URL that proxies chat to the API

#### Scenario: Memory on Neon

- **WHEN** Render env vars point to Neon with `DATABASE_TYPE=postgres`
- **THEN** conversation threads persist across API redeploys

### Requirement: Render API environment variables

The FastAPI service on Render SHALL be configured with minimum variables: `GOOGLE_API_KEY`, `DEFAULT_MODEL`, `DATABASE_TYPE=postgres`, all `POSTGRES_*`, `AUTH_SECRET`, `HOST=0.0.0.0`, `PORT=8080`.

#### Scenario: Gemini-only production API

- **WHEN** deploying v1 public demo
- **THEN** `OPENAI_API_KEY` is omitted so Gemini is the default provider

#### Scenario: Auth enabled

- **WHEN** `AUTH_SECRET` is set on Render
- **THEN** unauthenticated API requests return 401

### Requirement: Streamlit Cloud secrets

The Streamlit app on Community Cloud SHALL read configuration from Streamlit Secrets (TOML): `AGENT_URL`, `AUTH_SECRET`, and optionally `PYTHONPATH=src`.

#### Scenario: Streamlit connects to production API

- **WHEN** a user opens the Streamlit app
- **THEN** `AgentClient` uses `AGENT_URL` and sends `Authorization: Bearer <AUTH_SECRET>`

#### Scenario: Import path on Streamlit Cloud

- **WHEN** deploy fails with `ModuleNotFoundError` for `branding` or `client`
- **THEN** operator adds `PYTHONPATH = "src"` to Streamlit secrets

### Requirement: Neon Postgres credentials on API only

Neon database credentials SHALL be configured only on the Render API service, not on Streamlit Cloud.

#### Scenario: Neon pooled connection

- **WHEN** Neon offers a pooled connection host
- **THEN** `POSTGRES_HOST` uses the pooled endpoint for better free-tier behavior

### Requirement: Environment configuration

The system SHALL document required environment variables in `.env.example` and load them via pydantic-settings (`src/core/settings.py`).

#### Scenario: Secrets not in git

- **WHEN** a developer configures API keys or passwords
- **THEN** values live in `.env` (gitignored) or host secret panels, never committed

### Requirement: Pre- and post-deploy verification

The system SHALL define smoke tests before and after going live.

#### Scenario: Pre-deploy local check

- **WHEN** running locally before deploy
- **THEN** `pytest` passes and optional Docker compose smoke test succeeds

#### Scenario: Post-deploy production check

- **WHEN** deploy is complete
- **THEN** `curl <AGENT_URL>/health` returns 200, Streamlit loads without connection errors, end-to-end Gemini chat works, thread history survives refresh, and unauthorized requests are rejected

### Requirement: Free-tier operational constraints

The system SHALL document Render cold starts and SQLite unsuitability on Render.

#### Scenario: Cold start before demo

- **WHEN** Render API has been idle ~15 minutes
- **THEN** operator hits `/health` ~1 minute before demo to wake the service

#### Scenario: No SQLite on Render

- **WHEN** `DATABASE_TYPE=sqlite` on Render
- **THEN** conversation data is lost on redeploy (not acceptable for production)
