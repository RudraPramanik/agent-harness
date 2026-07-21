## 1. Phase 1 — Make the repo yours (platform + agents)

- [ ] 1.1 Update `src/branding.py`: set `GITHUB_OWNER`, `GITHUB_REPO`, `AUTHOR_LINK`, and welcome messages for v1 agents
- [ ] 1.2 Update `README.md` with your repo URL, author, and (when ready) live deploy URLs
- [ ] 1.3 Update `pyproject.toml` authors/description if renaming the package identity
- [ ] 1.4 Create `.env` from `.env.example` with `GOOGLE_API_KEY`, `DEFAULT_MODEL=gemini-2.0-flash`, `AUTH_SECRET` (omit `OPENAI_API_KEY` for Gemini-only)
- [ ] 1.5 Trim `src/agents/agents.py` to v1 catalog: keep `chatbot`, `research-assistant`, optional `interrupt-agent`; remove or hide supervisor/command/bg-task/kb agents from public registry
- [ ] 1.6 Confirm `DEFAULT_AGENT` is `research-assistant` (or chosen v1 default)
- [ ] 1.7 Update `.github/workflows/deploy.yml` repo gate (`YOUR_USERNAME/ai-agent-studio` → your `owner/repo`) if using automated deploy later

## 2. Phase 2 — Local validation

- [ ] 2.1 Run `uv sync --frozen` and start API: `python src/run_service.py`
- [ ] 2.2 Start UI in second terminal: `streamlit run src/streamlit_app.py`
- [ ] 2.3 Smoke test: UI branding, agent list, Gemini chat, `GET /info`, `GET /health`
- [ ] 2.4 Optional: run `docker compose watch` with `DATABASE_TYPE=postgres` to match production stack
- [ ] 2.5 Run `pytest` and fix any failures before publishing

## 3. Phase 3 — Publish on GitHub

- [ ] 3.1 Pre-push audit: no secrets in git (`git status`, search for `API_KEY`, `SECRET`, `PASSWORD`)
- [ ] 3.2 Push branded code to your GitHub repository (`main` branch)
- [ ] 3.3 Verify `.github/workflows/test.yml` passes on push (lint, mypy, pytest, Docker build)

## 4. Phase 4 — Free-tier deployment (deployment spec)

- [ ] 4.1 Create Neon Postgres project; copy `POSTGRES_*` connection details
- [ ] 4.2 Deploy FastAPI on Render: Docker `docker/Dockerfile.service`, port 8080, set env vars (`GOOGLE_API_KEY`, `DEFAULT_MODEL`, `DATABASE_TYPE=postgres`, `POSTGRES_*`, `AUTH_SECRET`, `HOST`, `PORT`)
- [ ] 4.3 Verify Render API: `curl https://your-service.onrender.com/info` and `/health`
- [ ] 4.4 Deploy Streamlit on Streamlit Community Cloud: main file `src/streamlit_app.py`, Python 3.12
- [ ] 4.5 Set Streamlit secrets: `AGENT_URL` (Render URL), `AUTH_SECRET` (same as API); add `PYTHONPATH=src` if imports fail
- [ ] 4.6 Production smoke test: end-to-end chat, thread history after refresh, 401 on bad/missing auth
- [ ] 4.7 Add live URLs to README; document "wake API via `/health` before demos" for Render cold starts

## 5. Phase 5–6 — Post-launch customization (optional, week 2+)

- [ ] 5.1 Customize `research-assistant` prompt and tools (`src/agents/research_assistant.py`, `src/agents/tools.py`)
- [ ] 5.2 Add one custom agent: new module under `src/agents/`, register in `agents.py`, welcome in `branding.py`
- [ ] 5.3 Optional RAG: run `scripts/create_chroma_db.py`, configure `rag-assistant` (requires OpenAI embeddings or Google embedding migration in `tools.py`)
- [ ] 5.4 Optional: custom domain via Cloudflare DNS pointing to Render/Streamlit

## 6. Phase 7 — Operations and OpenSpec closure

- [ ] 6.1 Set up weekly Gemini API usage monitoring
- [ ] 6.2 Document key rotation procedure (`AUTH_SECRET`, API keys) in team runbook
- [ ] 6.3 Run `openspec validate project-blueprint-vision` and fix any spec issues
- [ ] 6.4 Archive this change (`/opsx:archive`) to merge specs into `openspec/specs/`
