# Delta for Deployment

## ADDED Requirements

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

The FastAPI service on Render SHALL be configured with the following minimum variables:

| Variable | Required | Purpose |
|----------|----------|---------|
| `GOOGLE_API_KEY` | Yes | Gemini LLM (v1 default) |
| `DEFAULT_MODEL` | Yes | e.g. `gemini-2.0-flash` |
| `DATABASE_TYPE` | Yes | `postgres` in production |
| `POSTGRES_HOST` | Yes | Neon hostname |
| `POSTGRES_PORT` | Yes | `5432` |
| `POSTGRES_USER` | Yes | Neon user |
| `POSTGRES_PASSWORD` | Yes | Neon password |
| `POSTGRES_DB` | Yes | Neon database name |
| `AUTH_SECRET` | Yes | Shared bearer token with Streamlit |
| `HOST` | Yes | `0.0.0.0` |
| `PORT` | Yes | `8080` |

#### Scenario: Gemini-only production API

- **WHEN** deploying v1 public demo
- **THEN** `OPENAI_API_KEY` is omitted so Gemini is the default provider

#### Scenario: Auth enabled

- **WHEN** `AUTH_SECRET` is set on Render
- **THEN** unauthenticated API requests return 401

### Requirement: Streamlit Cloud secrets

The Streamlit app on Community Cloud SHALL read configuration from Streamlit Secrets (TOML), not from committed `.env` files.

| Secret / env | Required | Purpose |
|--------------|----------|---------|
| `AGENT_URL` | Yes | Public Render API URL, e.g. `https://your-service.onrender.com` |
| `AUTH_SECRET` | Yes | Same value as Render `AUTH_SECRET` |
| `PYTHONPATH` | If imports fail | Set to `src` so `branding`, `client`, `schema` resolve |

Example secrets TOML:

```toml
AGENT_URL = "https://your-agent-service.onrender.com"
AUTH_SECRET = "your-long-random-secret"
PYTHONPATH = "src"
```

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

### Requirement: Pre- and post-deploy verification

The system SHALL define smoke tests before and after going live.

#### Scenario: Pre-deploy local check

- **WHEN** running locally before deploy
- **THEN** `pytest` passes and `docker compose watch` smoke test succeeds (optional)

#### Scenario: Post-deploy production check

- **WHEN** deploy is complete
- **THEN** `curl <AGENT_URL>/health` returns 200, Streamlit loads without connection errors, chat works, thread history survives refresh

### Requirement: Free-tier operational constraints

The system SHALL document Render cold starts and SQLite unsuitability on Render.

#### Scenario: Cold start before demo

- **WHEN** Render API has been idle ~15 minutes
- **THEN** operator hits `/health` ~1 minute before demo to wake the service

#### Scenario: No SQLite on Render

- **WHEN** `DATABASE_TYPE=sqlite` on Render
- **THEN** conversation data is lost on redeploy (not acceptable for production)
