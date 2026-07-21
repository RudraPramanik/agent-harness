## Context

Audit of branding state (2026-07-21):

| File | Status | Issue |
|------|--------|-------|
| `src/branding.py` | **Partial** | `GITHUB_OWNER=YOUR_USERNAME`, `GITHUB_REPO=ai-agent-studio`; `AUTHOR_LINK` empty; `AUTHOR_NAME=Niloy Dey` |
| `README.md` | **Partial** | Author = Rudra Pramanik (mismatch); no live deploy URLs |
| `pyproject.toml` | **Done** | `name=ai-agent-studio`, `authors=Niloy Dey` |
| `LICENSE` | **Partial** | Copyright Rudra Pramanik (mismatch with branding.py) |
| `deploy.yml` | **Not done** | Still `YOUR_USERNAME/ai-agent-studio` |
| `git remote` | **Actual** | `RudraPramanik/agent-harness` |

Streamlit (`src/streamlit_app.py`) correctly imports all branding constants — fixing `branding.py` automatically fixes the UI.

## Goals / Non-Goals

**Goals:**

- One source of truth: `src/branding.py` drives UI; other files align to it.
- Working GitHub links in Streamlit sidebar.
- Consistent author across all metadata files.
- Deploy workflow matches real repo.

**Non-Goals:**

- Renaming GitHub repo to `ai-agent-studio`.
- Adding custom logo/media assets.
- Trimming agent registry (separate task in `project-blueprint-vision`).

## Decisions

### 1. Match git remote, not blueprint placeholder

**Decision:** Set `GITHUB_OWNER=RudraPramanik`, `GITHUB_REPO=agent-harness`.

**Rationale:** `git remote -v` shows `agent-harness`. Links must work today.

**Alternative:** Rename repo to `ai-agent-studio` on GitHub — deferred; would require remote update everywhere.

### 2. Resolve author identity (needs user input)

**Decision:** Align all files to one canonical author. Current candidates:

- `branding.py` + `pyproject.toml` → **Niloy Dey**
- `README.md` + `LICENSE` → **Rudra Pramanik**

**Recommendation:** Pick the primary owner. If Niloy Dey is the current maintainer, update README and LICENSE. If Rudra Pramanik owns the fork, update `branding.py` and `pyproject.toml`. Co-authorship in README is acceptable: "Niloy Dey, Rudra Pramanik".

### 3. AUTHOR_LINK

**Decision:** Set to `https://github.com/RudraPramanik` or personal profile URL.

**Rationale:** Streamlit only renders clickable footer when `AUTHOR_LINK` is non-empty.

### 4. deploy.yml update

**Decision:** Change line 15 to `github.repository == 'RudraPramanik/agent-harness'`.

**Rationale:** Workflow currently never runs on the real repo.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Wrong author chosen | Confirm with repo owner before `/opsx:apply` |
| Repo renamed later | Update `branding.py` + `deploy.yml` in one commit |
| README deploy URLs stale | Add "Coming soon" or omit until Phase 4 deploy |

## Migration Plan

1. Confirm canonical author name(s) with repo owner.
2. Update `src/branding.py` (GitHub owner/repo, author, link).
3. Align `README.md`, `pyproject.toml`, `LICENSE`.
4. Update `deploy.yml` repo gate.
5. Local smoke test: open Streamlit, verify title, links, author footer.
6. Archive change to merge branding spec.

## Open Questions

- **Who is the canonical author?** Niloy Dey, Rudra Pramanik, or both?
- **Should the repo be renamed** from `agent-harness` to `ai-agent-studio` on GitHub?
- **AUTHOR_LINK target:** GitHub profile, LinkedIn, or personal site?
