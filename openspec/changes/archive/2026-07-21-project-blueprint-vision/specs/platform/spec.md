# Delta for Platform

## ADDED Requirements

### Requirement: Product identity

The system SHALL present itself as **AI Agent Studio** — a branded LangGraph agent platform with a FastAPI backend and Streamlit chat UI, forked from agent-service-toolkit with upstream MIT attribution preserved.

#### Scenario: Branding is centralized

- **WHEN** a developer customizes the product name, tagline, or author links
- **THEN** changes are made in `src/branding.py` and reflected in the Streamlit UI and README

#### Scenario: Upstream attribution

- **WHEN** the project is published or distributed
- **THEN** README and LICENSE retain credit to agent-service-toolkit (Joshua Carroll, MIT)

### Requirement: Two-service architecture

The system SHALL split into two independently deployable services: a FastAPI agent service and a Streamlit chat UI, communicating over HTTP with optional auth.

#### Scenario: API service role

- **WHEN** a client invokes an agent via `POST /{agent-name}/stream` or non-streaming endpoints
- **THEN** the FastAPI service (`src/run_service.py`) runs the LangGraph agent, manages memory, and returns responses

#### Scenario: UI service role

- **WHEN** a user opens the Streamlit app (`src/streamlit_app.py`)
- **THEN** the UI displays branding, agent picker, and chat, proxying requests to the API via `src/client/`

### Requirement: Gemini-first LLM strategy

The system SHALL use Google Gemini as the default LLM provider for v1 public deployment, configured via `GOOGLE_API_KEY` and `DEFAULT_MODEL=gemini-2.0-flash`.

#### Scenario: Gemini-only local dev

- **WHEN** only `GOOGLE_API_KEY` is set (no `OPENAI_API_KEY`)
- **THEN** chatbot, research-assistant, interrupt-agent, and supervisor agents work without OpenAI

#### Scenario: OpenAI takes precedence when both keys set

- **WHEN** both `OPENAI_API_KEY` and `GOOGLE_API_KEY` are set
- **THEN** OpenAI is used as the default provider (documented pitfall; v1 deploy should omit OpenAI key)

### Requirement: Conversation memory

The system SHALL support SQLite for local development and Postgres for production, selected via `DATABASE_TYPE`.

#### Scenario: Local SQLite memory

- **WHEN** `DATABASE_TYPE=sqlite` and the API is running locally
- **THEN** conversation threads persist in `checkpoints.db` across restarts on the same machine

#### Scenario: Production Postgres memory

- **WHEN** `DATABASE_TYPE=postgres` with valid `POSTGRES_*` credentials (e.g. Neon)
- **THEN** conversation history survives API redeploys and is shared across instances

### Requirement: API authentication

The system SHALL protect the FastAPI service in production using a shared `AUTH_SECRET` between the API and Streamlit client.

#### Scenario: Authenticated request

- **WHEN** `AUTH_SECRET` is set on the API and Streamlit sends matching credentials
- **THEN** agent endpoints accept requests

#### Scenario: Unauthorized request rejected

- **WHEN** `AUTH_SECRET` is set on the API but the client sends no or wrong secret
- **THEN** the API returns 401 Unauthorized
