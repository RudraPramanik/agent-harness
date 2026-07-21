# Agents

## Purpose

Public v1 agent catalog, registration patterns, and provider dependency rules for AI Agent Studio.

## Requirements

### Requirement: V1 public agent catalog

The system SHALL ship a curated set of agents for the initial public demo, **pausing** advanced or dependency-heavy agents until explicitly enabled. Paused agents remain registered in code but are not loaded, listed, or invokable.

#### Scenario: Recommended v1 agents visible

- **WHEN** a user opens the Streamlit agent picker for the public demo
- **THEN** at minimum `chatbot` and `research-assistant` are available with `enabled=True`

#### Scenario: Advanced agents paused

- **WHEN** preparing the v1 public deployment
- **THEN** supervisor, command, bg-task, rag, knowledge-base, and github-mcp agents have `enabled=False` (paused) in `src/agents/agents.py`

#### Scenario: Paused agent not invokable

- **WHEN** a client calls `POST /{paused-agent-id}/stream` or `/invoke`
- **THEN** the API returns 404 with a clear message that the agent is paused

#### Scenario: Paused agent skipped at startup

- **WHEN** the FastAPI service starts
- **THEN** paused agents are not loaded via `load_agent()` and do not attach checkpointer/store

### Requirement: Default agent

The system SHALL default to `research-assistant` unless changed in `src/agents/agents.py` → `DEFAULT_AGENT`.

#### Scenario: Default on first load

- **WHEN** a user opens the chat UI without selecting an agent
- **THEN** `research-assistant` is the active agent (web search, weather, calculator)

### Requirement: Agent registration pattern

The system SHALL register every agent (enabled or paused) in `src/agents/agents.py` with an `enabled` flag and a welcome message in `src/branding.py` → `WELCOME_MESSAGES`.

#### Scenario: New agent added

- **WHEN** a developer adds `src/agents/my_agent.py`
- **THEN** they register it in `agents.py` with `enabled=True` or `enabled=False`, add a `WELCOME_MESSAGES` entry, and expose it via `POST /my-agent/stream` when enabled

#### Scenario: Re-enable paused agent

- **WHEN** an operator sets `enabled=True` for a paused agent in `agents.py` and redeploys
- **THEN** the agent appears in `/info`, loads at startup, and is selectable in the Streamlit picker without code changes elsewhere

### Requirement: Agent enablement metadata

Each agent registration SHALL include an `enabled: bool` field defaulting to `True` for new agents.

#### Scenario: Filter enabled agents for UI

- **WHEN** `GET /info` is called
- **THEN** only agents with `enabled=True` are returned in the agents list

#### Scenario: Helper functions respect enabled flag

- **WHEN** code calls `get_all_agent_info()` or `get_enabled_agent_ids()`
- **THEN** only enabled agents are included

### Requirement: Provider-gated enablement (optional)

Agents MAY declare optional `required_env` keys (e.g. `OPENAI_API_KEY`, `AWS_KB_ID`, `GITHUB_PAT`). When present, a startup helper MAY auto-enable agents whose requirements are satisfied.

#### Scenario: Auto-enable when deps present

- **WHEN** `rag-assistant` is paused but `OPENAI_API_KEY` is set and `./chroma_db` exists
- **THEN** the operator MAY call an optional `resolve_agent_enablement()` helper at startup to flip `enabled=True` without manual edits (opt-in, not default v1 behavior)

### Requirement: Provider dependencies per agent

The system SHALL document which agents require providers beyond Gemini.

#### Scenario: Gemini-only agents

- **WHEN** only `GOOGLE_API_KEY` is configured
- **THEN** `chatbot`, `research-assistant`, `interrupt-agent`, and `github-mcp-agent` (with `GITHUB_PAT`) are usable

#### Scenario: OpenAI-dependent features

- **WHEN** a user selects `rag-assistant` or enables voice STT/TTS
- **THEN** OpenAI API key (or code change to Google embeddings) is required; out of scope for v1 Gemini-only deploy

#### Scenario: AWS-dependent agent

- **WHEN** a user selects `knowledge-base-agent`
- **THEN** AWS Bedrock Knowledge Base credentials are required; not part of v1 free-tier deploy

### Requirement: Post-v1 agent roadmap

The system SHALL support iterative agent customization after deployment: **pause/enable catalog** → customize research assistant → add RAG docs → switch embeddings → add custom agent → production hardening.

#### Scenario: Custom agent as differentiator

- **WHEN** the platform is live and stable (week 2+)
- **THEN** operators add at least one custom agent module reflecting their product or domain and enable it via `enabled=True`
