## Why

AI Agent Studio is a fork of agent-service-toolkit with strong technical foundations but no formal product specification tying together what we are building, for whom, and how we get from local dev to a live public deployment. `docs/BLUEPRINT.md` describes a phased plan; this change captures that vision as OpenSpec requirements so future work (branding, deployment, agent curation) is spec-driven and traceable.

## What Changes

- Establish the **product vision**: a branded, publicly deployable LangGraph agent platform on free-tier infrastructure.
- Define **baseline capabilities** for platform architecture, deployment, and agent catalog — not implementation of every phase yet.
- Document **non-goals** for v1 (enterprise SLA, paid hosting, full RAG without OpenAI embeddings).
- Provide a phased roadmap (local → GitHub → Render/Neon/Streamlit Cloud → agent customization) as the implementation sequence.
- No breaking API or code changes in this change — this is a planning/specification artifact only.

## Capabilities

### New Capabilities

- `platform`: Core product identity, two-service architecture (FastAPI + Streamlit), LLM provider strategy (Gemini-first), memory backends, and auth model.
- `deployment`: Free-tier production stack (Render API, Streamlit Cloud UI, Neon Postgres), env configuration, verification checklists, and operational constraints (cold starts, secrets hygiene).
- `agents`: Public v1 agent catalog, default agent selection, and rules for adding or hiding agents.

### Modified Capabilities

- _(none — `openspec/specs/` is empty; this is the first baseline spec)_

## Impact

| Layer | Impact |
|-------|--------|
| **Agents** | Defines which agents ship in v1 (`chatbot`, `research-assistant`, optional `interrupt-agent`); others hidden until needed |
| **FastAPI** | Auth via `AUTH_SECRET`, Postgres memory in production, streaming endpoints unchanged |
| **Streamlit** | Branding from `src/branding.py`, `AGENT_URL` + `AUTH_SECRET` for production |
| **Infra** | Render + Neon + Streamlit Cloud; Docker via `docker/Dockerfile.service` |
| **Docs** | `docs/BLUEPRINT.md` remains the operational guide; OpenSpec specs become the behavioral source of truth |

### Non-goals (v1)

- Production SLA or always-on API without cold starts (Render free tier sleeps).
- Gemini-only RAG (embeddings still require OpenAI or a future code change).
- Voice STT/TTS in production without OpenAI keys.
- Azure / paid hosting path (optional later via `deploy.yml`).
- Documenting or back-filling specs for every existing agent implementation detail.
