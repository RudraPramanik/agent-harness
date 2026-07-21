## Why

Branding is partially configured: the product name and UI copy exist, but GitHub links still point to placeholder values (`YOUR_USERNAME/ai-agent-studio`) while the actual remote is `RudraPramanik/agent-harness`. Author attribution is inconsistent across `branding.py`, `README.md`, `pyproject.toml`, and `LICENSE`. Broken source links in the Streamlit sidebar and mismatched metadata block publish readiness (BLUEPRINT Phase 1).

## What Changes

- Set real `GITHUB_OWNER` and `GITHUB_REPO` in `src/branding.py` to match `git remote` (`RudraPramanik/agent-harness`).
- Resolve author identity: pick one canonical author (or co-authors) and align `branding.py`, `README.md`, `pyproject.toml`, and `LICENSE`.
- Add `AUTHOR_LINK` (GitHub profile or LinkedIn) so the Streamlit footer renders a clickable credit.
- Update `.github/workflows/deploy.yml` repo gate from `YOUR_USERNAME/ai-agent-studio` to `RudraPramanik/agent-harness`.
- Align README author line with `branding.py` (currently README says Rudra Pramanik, branding says Niloy Dey).
- Trim `WELCOME_MESSAGES` to match v1 public agents only (`chatbot`, `research-assistant`, optional `interrupt-agent`) — optional cleanup, not blocking.
- Add live deploy URLs to README when deployment exists (placeholder section until then).

## Capabilities

### New Capabilities

- `branding`: Product identity, GitHub links, author attribution, and UI-facing copy requirements across `branding.py`, README, and workflows.

### Modified Capabilities

- _(none — main specs not yet archived from `project-blueprint-vision`)_

## Impact

| Layer | Impact |
|-------|--------|
| **Streamlit UI** | Sidebar title, tagline, GitHub source links, author footer — all read from `branding.py` |
| **README** | Author credit, repo URL, future live URLs |
| **pyproject.toml** | Package metadata authors field |
| **LICENSE** | Copyright holder line |
| **CI/Deploy** | `deploy.yml` repo gate condition |
| **FastAPI / Agents** | No API changes; agent registry trim is separate |

### Non-goals

- Renaming the GitHub repo from `agent-harness` to `ai-agent-studio` (can do later; this change matches current remote).
- Custom logo/screenshots in README (nice-to-have).
- Deploying to production (separate change).
