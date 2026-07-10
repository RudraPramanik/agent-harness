# ✨ AI Agent Studio

**AI Agent Studio** is a LangGraph-based agent platform with a FastAPI backend and Streamlit chat UI. Run multi-agent workflows locally or deploy them to free-tier hosting.

**Author:** [Rudra Pramanik](https://github.com/RudraPramanik)  
**Based on:** [agent-service-toolkit](https://github.com/JoshuaC215/agent-service-toolkit) by Joshua Carroll (MIT)

> Replace `YOUR_USERNAME` above (and in `src/branding.py`) once your GitHub repository is created.

## Overview

- **LangGraph agents** — chat, research, RAG, supervisors, interrupts, MCP, and more
- **FastAPI service** — streaming and non-streaming HTTP endpoints
- **Streamlit UI** — branded chat interface with optional voice support
- **Docker Compose** — local stack with Postgres and hot reload

<img src="media/agent_architecture.png" width="600" alt="Architecture">

## Quickstart

### Python (Windows / macOS / Linux)

```sh
cp .env.example .env
# Set GOOGLE_API_KEY=... and DEFAULT_MODEL=gemini-2.0-flash
# (or OPENAI_API_KEY if you prefer OpenAI)

uv sync --frozen
# Windows: .\.venv\Scripts\Activate.ps1
# Unix: source .venv/bin/activate

python src/run_service.py
# Second terminal:
streamlit run src/streamlit_app.py
```

Open **http://localhost:8501** (UI) and **http://localhost:8080/redoc** (API).

### Docker

```sh
cp .env.example .env
# Set GOOGLE_API_KEY and DATABASE_TYPE=postgres (see .env.example)
docker compose watch
```

## Branding

Edit **`src/branding.py`** to control:

- App title, icon, and tagline
- GitHub repo URL for source links
- Author name and profile link
- Per-agent welcome messages in the UI

## Environment variables

See [`.env.example`](./.env.example). Minimum for a Gemini-first setup:

| Variable | Required |
|----------|----------|
| `GOOGLE_API_KEY` (or another provider key) | Yes |
| `DEFAULT_MODEL=gemini-2.0-flash` | Recommended |
| `DATABASE_TYPE=postgres` + `POSTGRES_*` | Recommended for Docker / production |
| `AUTH_SECRET` | Recommended for production |
| `AGENT_URL` | Set on Streamlit host (points to FastAPI) |

> If both `OPENAI_API_KEY` and `GOOGLE_API_KEY` are set, OpenAI is used as the default provider.

## Project layout

| Path | Purpose |
|------|---------|
| `src/agents/` | Agent definitions |
| `src/branding.py` | App branding and welcome messages |
| `src/service/` | FastAPI app |
| `src/streamlit_app.py` | Chat UI |
| `src/client/` | HTTP client for the API |

## Add or customize agents

1. Create a module under `src/agents/`
2. Register it in `src/agents/agents.py`
3. Add a welcome line in `src/branding.py` → `WELCOME_MESSAGES`
4. Invoke via `POST /{agent-name}/stream` or from the Streamlit sidebar

See [docs/RAG_Assistant.md](docs/RAG_Assistant.md) for RAG setup.

## Documentation

| Guide | Description |
|-------|-------------|
| [docs/BLUEPRINT.md](docs/BLUEPRINT.md) | Own the repo, publish, and deploy on free tier |
| [docs/RAG_Assistant.md](docs/RAG_Assistant.md) | ChromaDB RAG setup |
| [docs/GitHub_MCP_Agent.md](docs/GitHub_MCP_Agent.md) | GitHub MCP agent |
| [docs/Ollama.md](docs/Ollama.md) | Local LLM via Ollama |
| [docs/VertexAI.md](docs/VertexAI.md) | Google Vertex AI |

## Production deploy

Recommended free-tier path (see [docs/BLUEPRINT.md](docs/BLUEPRINT.md)):

1. Deploy **FastAPI** (`docker/Dockerfile.service`) to Render (or Fly.io / Railway)
2. Deploy **Streamlit** (`src/streamlit_app.py`) to Streamlit Community Cloud
3. Use **Neon** Postgres for conversation memory
4. Set matching `AGENT_URL` and `AUTH_SECRET` on the Streamlit side

## Development

```sh
uv sync --frozen
pre-commit install
pytest
```

## License

MIT — see [LICENSE](./LICENSE).

- Original work Copyright (c) 2024 Joshua Carroll
- Modifications Copyright (c) 2026 Niloy Dey
