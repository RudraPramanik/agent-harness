# CI/CD

## Purpose

Continuous integration and optional deployment automation for AI Agent Studio via GitHub Actions, Render deploy hooks, and Streamlit Cloud auto-rebuild.

## Requirements

### Requirement: CI on every push and PR

The system SHALL run automated quality checks via `.github/workflows/test.yml` on push to `main` and on pull requests.

#### Scenario: Python CI matrix

- **WHEN** code is pushed to GitHub
- **THEN** ruff, mypy, and pytest run on Python 3.11, 3.12, and 3.13

#### Scenario: Docker integration test

- **WHEN** the test workflow runs
- **THEN** `docker/Dockerfile.service` and `docker/Dockerfile.app` build and integration tests run with `USE_FAKE_MODEL=true`

### Requirement: GitHub repository secrets for CI

The CI workflow SHALL run without production LLM or database secrets; only optional secrets such as `CODECOV_TOKEN` may be configured.

#### Scenario: CI passes without production secrets

- **WHEN** `CODECOV_TOKEN` is unset
- **THEN** tests still run; coverage upload may be skipped or fail non-blocking

### Requirement: CD to Render via deploy hook

The system SHALL support optional auto-deploy of the API to Render after CI passes on `main` via `.github/workflows/deploy-render.yml`.

#### Scenario: Render deploy hook

- **WHEN** `RENDER_DEPLOY_HOOK_URL` is set as a GitHub secret and main branch CI passes
- **THEN** a workflow step POSTs to the Render deploy hook to trigger API redeploy

#### Scenario: Manual Render deploy

- **WHEN** auto-deploy is not configured
- **THEN** operator deploys via Render dashboard connected to GitHub or manual deploy

### Requirement: Streamlit Cloud deploys from GitHub

Streamlit Community Cloud SHALL deploy the UI when the connected GitHub branch updates; no separate GitHub Actions job is required for the UI.

#### Scenario: Streamlit auto-redeploy

- **WHEN** `src/streamlit_app.py` or dependencies change on the connected branch
- **THEN** Streamlit Cloud rebuilds the app

#### Scenario: Streamlit app configuration

- **WHEN** creating the Streamlit Cloud app
- **THEN** main file path is `src/streamlit_app.py`, Python 3.12, repo `RudraPramanik/agent-harness`

### Requirement: Secrets never in git

The system SHALL NOT commit `.env`, Streamlit secrets, or API keys to the repository.

#### Scenario: Pre-push audit

- **WHEN** preparing to deploy
- **THEN** operator confirms no `API_KEY`, `SECRET`, or `PASSWORD` values are committed
