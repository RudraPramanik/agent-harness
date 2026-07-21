## 1. Resolve author identity (blocking)

- [x] 1.1 Confirm canonical author: Niloy Dey, Rudra Pramanik, or co-authors
- [x] 1.2 Decide `AUTHOR_LINK` URL (GitHub profile recommended)

## 2. Update src/branding.py (UI source of truth)

- [x] 2.1 Set `GITHUB_OWNER = "RudraPramanik"`
- [x] 2.2 Set `GITHUB_REPO = "agent-harness"`
- [x] 2.3 Set `AUTHOR_NAME` to confirmed canonical author
- [x] 2.4 Set `AUTHOR_LINK` to profile URL (non-empty for clickable footer)

## 3. Align metadata files

- [x] 3.1 Update `README.md` author line to match `branding.py`
- [x] 3.2 Update `pyproject.toml` authors if needed
- [x] 3.3 Update `LICENSE` copyright line to match (keep upstream MIT terms)
- [x] 3.4 Add repo URL to README if missing: `https://github.com/RudraPramanik/agent-harness`

## 4. Fix CI/deploy config

- [x] 4.1 Update `.github/workflows/deploy.yml` line 15: `RudraPramanik/agent-harness`

## 5. Verification

- [x] 5.1 Run `streamlit run src/streamlit_app.py` — verify title, tagline, welcome message
- [x] 5.2 Click "View the source code" — must open `github.com/RudraPramanik/agent-harness`
- [x] 5.3 Verify author footer shows clickable link when `AUTHOR_LINK` is set
- [x] 5.4 Grep repo for `YOUR_USERNAME` — should return zero hits in production files

## 6. Optional cleanup

- [ ] 6.1 Trim `WELCOME_MESSAGES` to v1 agents only (when agent registry is trimmed)
- [ ] 6.2 Add live Streamlit/Render URLs to README after deployment

## 7. Remove personal owner/credit lines

- [x] 7.1 Remove `AUTHOR_NAME` and `AUTHOR_LINK` from `src/branding.py`
- [x] 7.2 Remove "Built by" author footer from `src/streamlit_app.py`
- [x] 7.3 Remove author, repository, and attribution bullets from `README.md`
- [x] 7.4 Remove `authors` from `pyproject.toml`
- [x] 7.5 Restore `LICENSE` to upstream Joshua Carroll copyright only
