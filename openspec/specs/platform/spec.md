# Platform

## Purpose

Core product architecture for AI Agent Studio: two-service layout, Gemini-first LLM strategy, conversation memory, and API authentication.

## Requirements

### Requirement: Product identity

The system SHALL present itself as **AI Agent Studio** — a branded LangGraph agent platform with a FastAPI backend and Streamlit chat UI.

#### Scenario: Branding is centralized

- **WHEN** a developer customizes the product name, tagline, or GitHub links
- **THEN** changes are made in `src/branding.py` and reflected in the Streamlit UI and README

#### Scenario: Upstream license

- **WHEN** inspecting `LICENSE`
- **THEN** Joshua Carroll (2024) copyright is retained per upstream MIT license

### Requirement: Two-service architecture

The system SHALL split into two independently deployable services: a FastAPI agent service and a Streamlit chat UI, communicating over HTTP with optional auth.

#### Scenario: API service role

- **WHEN** a client invokes an agent via `POST /{agent-name}/stream` or non-streaming endpoints
- **THEN** the FastAPI service (`src/run_service.py`) runs the LangGraph agent, manages memory, and returns responses

#### Scenario: UI service role

- **WHEN** a user opens the Streamlit app (`src/streamlit_app.py`)
- **THEN** the UI displays branding, agent picker, and chat, proxying requests to the API via `src/client/`

### Requirement: Gemini-first LLM strategy

The system SHALL use Google Gemini as the **default** LLM provider for v1 public deployment, configured via `GOOGLE_API_KEY` and `DEFAULT_MODEL=gemini-2.0-flash`, while supporting **additional providers concurrently** when their API keys are configured.

#### Scenario: Gemini-only local dev

- **WHEN** only `GOOGLE_API_KEY` is set (no `OPENAI_API_KEY`)
- **THEN** chatbot, research-assistant, and interrupt-agent work without OpenAI

#### Scenario: OpenAI takes precedence when both keys set

- **WHEN** both `OPENAI_API_KEY` and `GOOGLE_API_KEY` are set and `DEFAULT_MODEL` is unset
- **THEN** OpenAI is used as the default provider (documented pitfall; v1 deploy should set `DEFAULT_MODEL` explicitly to Gemini)

#### Scenario: Explicit default model with multiple providers

- **WHEN** multiple provider keys are set and `DEFAULT_MODEL=gemini-2.0-flash` is explicit
- **THEN** Gemini is the default regardless of provider registration order

### Requirement: NVIDIA NIM via OpenAI-compatible API

The system SHALL support NVIDIA NIM as an LLM provider through the existing OpenAI-compatible configuration without a new Provider enum.

#### Scenario: NIM configured

- **WHEN** the operator sets `COMPATIBLE_BASE_URL=https://integrate.api.nvidia.com/v1`, `COMPATIBLE_API_KEY` (NVIDIA API key), and `COMPATIBLE_MODEL` (e.g. `meta/llama-3.1-8b-instruct`)
- **THEN** `openai-compatible` appears in `AVAILABLE_MODELS` and is selectable in the Streamlit LLM picker

#### Scenario: NIM rate limits documented

- **WHEN** using NVIDIA NIM free tier (~40 RPM)
- **THEN** operators are advised to set `DEFAULT_MODEL` to a NIM model only for dev/test or low-traffic agents; production default remains Gemini

### Requirement: Multi-provider model picker

The system SHALL expose all models from all configured providers in the Streamlit LLM selectbox via `GET /info` → `models`.

#### Scenario: Gemini and NIM both configured

- **WHEN** `GOOGLE_API_KEY` and `COMPATIBLE_*` (NIM) are both set
- **THEN** both Gemini models and `openai-compatible` appear in the model list; user can switch per session in Settings

#### Scenario: Per-request model override

- **WHEN** a user selects a model in Streamlit Settings
- **THEN** the chosen model is passed to the agent via `configurable.model` on each invoke/stream request

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
