## Why

The public v1 deploy still exposes all 10 registered agents, including demos that need extra providers (OpenAI embeddings, AWS Bedrock) or confuse first-time users. Operators want to **pause** advanced agents—not delete their code—so re-enabling them later is a one-line config change. Separately, the platform should document and support running **multiple LLM providers** (Gemini primary + NVIDIA NIM free tier) without ripping out the existing provider stack.

## What Changes

- Add an **`enabled` flag** (or equivalent pause list) to each agent in `src/agents/agents.py`; paused agents stay registered but are hidden from the UI, skipped at startup, and rejected at invoke/stream.
- Ship v1 with **active**: `chatbot`, `research-assistant`; **paused**: all others (including optional `interrupt-agent` until explicitly enabled).
- Expose only **enabled** agents via `GET /info` and Streamlit picker; keep welcome messages for paused agents in `branding.py` for when they are re-enabled.
- Document **NVIDIA NIM** as an OpenAI-compatible provider via existing `COMPATIBLE_*` env vars (no new Provider enum in v1).
- Document **multi-provider** setup: Gemini default + optional NIM/Groq/OpenAI keys; clarify default-model precedence when multiple keys are set.
- Optional per-agent **`required_env`** metadata so agents can auto-unpause when their dependencies are present (minimal helper, not mandatory for v1).

## Capabilities

### New Capabilities

_(none — behavior extends existing agent catalog and platform LLM strategy)_

### Modified Capabilities

- `agents`: Replace "remove from dict" with pause/enable model; define active vs paused v1 catalog and re-enable workflow.
- `platform`: Extend LLM strategy to cover multi-provider operation and NVIDIA NIM via OpenAI-compatible endpoint.

## Impact

| Layer | Change |
|-------|--------|
| `src/agents/agents.py` | `Agent` dataclass gains `enabled`; filter helpers; v1 pause list |
| `src/service/service.py` | Startup skips paused agents; invoke/stream returns 404 for paused |
| `src/streamlit_app.py` | No change if it already reads `/info` agents list |
| `src/branding.py` | Keep all `WELCOME_MESSAGES`; no deletion |
| `src/core/settings.py`, `.env.example` | Document NIM + multi-provider env pattern |
| `tests/agents/`, `tests/service/` | Coverage for paused-agent filtering and 404 behavior |
| Agent source modules | **Unchanged** — paused agents remain on disk |

**Non-goals (this change):**

- Deleting agent modules or routes architecture
- Full per-agent LLM routing (e.g. research-assistant on Gemini, safeguard on Groq) — document as follow-up
- Gemini-only RAG / embedding migration
- NVIDIA NIM as a dedicated Provider enum (use compatible API first)
