# Delta for Branding

## ADDED Requirements

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

### Requirement: Consistent author attribution

The system SHALL use a single canonical author identity across `branding.py`, `README.md`, `pyproject.toml`, and `LICENSE`.

#### Scenario: Streamlit author footer

- **WHEN** `AUTHOR_LINK` is set in `branding.py`
- **THEN** the sidebar shows a clickable "Built by [Author Name](link)" caption

#### Scenario: README author matches branding

- **WHEN** a reader opens `README.md`
- **THEN** the author name matches `AUTHOR_NAME` in `branding.py`

#### Scenario: Package metadata matches branding

- **WHEN** inspecting `pyproject.toml` authors
- **THEN** the listed author matches `AUTHOR_NAME` in `branding.py`

### Requirement: Deploy workflow repo gate

The Azure deploy workflow SHALL only run for the actual repository, not placeholder values.

#### Scenario: Deploy workflow gated correctly

- **WHEN** code is pushed to `RudraPramanik/agent-harness`
- **THEN** `.github/workflows/deploy.yml` condition `github.repository == 'RudraPramanik/agent-harness'` allows the workflow to run (if Azure deploy is enabled)

### Requirement: Upstream attribution preserved

The system SHALL retain MIT attribution to agent-service-toolkit in README and upstream credit in LICENSE.

#### Scenario: README upstream credit

- **WHEN** a reader opens `README.md`
- **THEN** Joshua Carroll / agent-service-toolkit is credited as the upstream project
