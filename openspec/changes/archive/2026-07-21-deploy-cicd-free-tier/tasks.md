## 1. Neon Postgres

- [ ] 1.1 Create Neon project and database at neon.tech
- [ ] 1.2 Copy `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` (use pooled host if available)

## 2. Render API deploy

- [ ] 2.1 Connect GitHub repo `RudraPramanik/agent-harness` on render.com
- [ ] 2.2 New Web Service: Docker, `docker/Dockerfile.service`, port 8080
- [ ] 2.3 Set Render env vars: `GOOGLE_API_KEY`, `DEFAULT_MODEL=gemini-2.0-flash`, `DATABASE_TYPE=postgres`, all `POSTGRES_*`, `AUTH_SECRET`, `HOST=0.0.0.0`, `PORT=8080`
- [ ] 2.4 Deploy and verify `curl https://<service>.onrender.com/health` and `/info`

## 3. Streamlit Community Cloud (free tier)

- [ ] 3.1 Sign up at share.streamlit.io and connect GitHub
- [ ] 3.2 New app: repo `RudraPramanik/agent-harness`, main file `src/streamlit_app.py`, Python 3.12
- [ ] 3.3 Set Secrets TOML: `AGENT_URL`, `AUTH_SECRET` (match Render), `PYTHONPATH=src`
- [ ] 3.4 Deploy and verify chat works at `https://<app>.streamlit.app`
- [x] 3.5 If dependency install fails, add root `requirements.txt` for Streamlit Cloud

## 4. CI/CD (GitHub Actions)

- [ ] 4.1 Confirm `test.yml` passes on push to `main` (run locally after fixing Google creds collection errors, or verify on GitHub after push)
- [x] 4.2 Optional: add `RENDER_DEPLOY_HOOK_URL` GitHub secret and workflow step to trigger Render deploy after CI
- [x] 4.3 Optional: add `.streamlit/secrets.toml.example` documenting required secrets (no real values)

## 5. Documentation and verification

- [x] 5.1 Update README Production deploy section with env var tables and Streamlit steps
- [ ] 5.2 Production smoke test: API health, Streamlit load, end-to-end chat, thread persistence after refresh, 401 without auth
- [x] 5.3 Document cold-start wake procedure in README

## 6. OpenSpec closure

- [x] 6.1 Run `openspec validate deploy-cicd-free-tier`
- [ ] 6.2 Archive change after deploy is live (`/opsx:archive`)
