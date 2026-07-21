# Branding

## Purpose

Product identity and GitHub links for AI Agent Studio. Personal owner/credit lines are intentionally omitted from the UI and docs.

## Requirements

### Requirement: Product identity in UI

The system SHALL display **AI Agent Studio** as the product name with icon ✨ and the configured tagline in the Streamlit UI, sourced from `src/branding.py`.

#### Scenario: App title in browser and sidebar

- **WHEN** a user opens the Streamlit app
- **THEN** the page title and sidebar header show `APP_TITLE` and `APP_ICON` from `branding.py`

### Requirement: Valid GitHub source links

The system SHALL link to the actual published GitHub repository, not placeholder values.

#### Scenario: Source code link works

- **WHEN** a user clicks "View the source code" in the Streamlit sidebar
- **THEN** the link resolves to `https://github.com/RudraPramanik/agent-harness` (matching `git remote origin`)

#### Scenario: Architecture image link works

- **WHEN** a user views the architecture diagram link in the sidebar
- **THEN** the GitHub raw URL uses the correct `GITHUB_OWNER` and `GITHUB_REPO`

### Requirement: No personal owner credits in UI or docs

The system SHALL NOT display personal owner names, author footers, or modification credit lines in the Streamlit UI, README body, or package metadata.

#### Scenario: No author footer in UI

- **WHEN** a user opens the Streamlit sidebar
- **THEN** no "Built by" author caption is shown

#### Scenario: No personal credits in README

- **WHEN** a reader opens `README.md`
- **THEN** no Author line, repository attribution line, or license footer credit bullets appear

#### Scenario: No authors in package metadata

- **WHEN** inspecting `pyproject.toml`
- **THEN** no `authors` field lists a personal name

### Requirement: Deploy workflow repo gate

The Azure deploy workflow SHALL only run for the actual repository, not placeholder values.

#### Scenario: Deploy workflow gated correctly

- **WHEN** code is pushed to `RudraPramanik/agent-harness`
- **THEN** `.github/workflows/deploy.yml` condition `github.repository == 'RudraPramanik/agent-harness'` allows the workflow to run (if Azure deploy is enabled)

### Requirement: Upstream license copyright

The LICENSE SHALL retain Joshua Carroll (2024) as the copyright holder per the upstream MIT license.

#### Scenario: LICENSE copyright

- **WHEN** inspecting `LICENSE`
- **THEN** the copyright line is `Copyright (c) 2024 Joshua Carroll`
