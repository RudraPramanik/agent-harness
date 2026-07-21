# Delta for Agents

## ADDED Requirements

### Requirement: V1 public agent catalog

The system SHALL ship a curated set of agents for the initial public demo, hiding advanced or dependency-heavy agents until explicitly enabled.

#### Scenario: Recommended v1 agents visible

- **WHEN** a user opens the Streamlit agent picker for the public demo
- **THEN** at minimum `chatbot` and `research-assistant` are available; `interrupt-agent` is optional

#### Scenario: Advanced agents hidden

- **WHEN** preparing the v1 public deployment
- **THEN** supervisor, command, bg-task, and other demo-only agents are removed from the `agents` dict in `src/agents/agents.py` or not promoted in the UI

### Requirement: Default agent

The system SHALL default to `research-assistant` unless changed in `src/agents/agents.py` → `DEFAULT_AGENT`.

#### Scenario: Default on first load

- **WHEN** a user opens the chat UI without selecting an agent
- **THEN** `research-assistant` is the active agent (web search, weather, calculator)

### Requirement: Agent registration pattern

The system SHALL register every exposed agent in `src/agents/agents.py` with a welcome message in `src/branding.py` → `WELCOME_MESSAGES`.

#### Scenario: New agent added

- **WHEN** a developer adds `src/agents/my_agent.py`
- **THEN** they register it in `agents.py`, add a `WELCOME_MESSAGES` entry, and expose it via `POST /my-agent/stream`

### Requirement: Provider dependencies per agent

The system SHALL document which agents require providers beyond Gemini.

#### Scenario: Gemini-only agents

- **WHEN** only `GOOGLE_API_KEY` is configured
- **THEN** `chatbot`, `research-assistant`, `interrupt-agent`, and `github-mcp-agent` (with `GITHUB_PAT`) are usable

#### Scenario: OpenAI-dependent features

- **WHEN** a user selects `rag-assistant` or enables voice STT/TTS
- **THEN** OpenAI API key (or code change to Google embeddings) is required; this is out of scope for v1 Gemini-only deploy

#### Scenario: AWS-dependent agent

- **WHEN** a user selects `knowledge-base-agent`
- **THEN** AWS Bedrock Knowledge Base credentials are required; not part of v1 free-tier deploy

### Requirement: Post-v1 agent roadmap

The system SHALL support iterative agent customization after deployment works, in priority order: trim catalog → customize research assistant → add RAG docs → switch embeddings to Google → add custom agent → production hardening.

#### Scenario: Custom agent as differentiator

- **WHEN** the platform is live and stable (week 2+)
- **THEN** operators add at least one custom agent module reflecting their product or domain
