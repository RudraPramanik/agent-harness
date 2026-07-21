## Context

Today all 10 agents in `src/agents/agents.py` are always loaded at startup, listed in `GET /info`, and shown in the Streamlit picker. The merged `openspec/specs/agents/spec.md` says v1 should hide advanced agents, but the implementation still registers everything. Operators want to **pause** agents (keep code, skip runtime cost) and flip them back on with minimal edits.

The LLM layer already supports multiple providers via `settings.model_post_init()` — keys add models to `AVAILABLE_MODELS`. NVIDIA NIM exposes an OpenAI-compatible REST API (`https://integrate.api.nvidia.com/v1`), which maps to the existing `COMPATIBLE_*` env vars and `OpenAICompatibleName` without new dependencies.

## Goals / Non-Goals

**Goals:**

- Pause v1 agents via an `enabled` flag on the existing `Agent` dataclass
- Filter enabled agents in `get_all_agent_info()`, startup `load_agent()` loop, and invoke/stream guards
- Re-enable an agent by setting `enabled=True` in one place (`agents.py`)
- Document NVIDIA NIM + multi-provider `.env` pattern
- Set explicit `DEFAULT_MODEL=gemini-2.0-flash` guidance when multiple keys exist

**Non-Goals:**

- Deleting agent modules or changing route patterns (`/{agent_id}/stream` stays)
- Per-agent default LLM assignment (e.g. research on Gemini, safeguard on Groq) — future change
- Dedicated `Provider.NVIDIA` enum — use compatible API first
- Auto-unpause by default (optional helper only)

## Decisions

### 1. `enabled` flag on `Agent` dataclass (not a separate dict)

**Choice:** Extend the existing dataclass:

```python
@dataclass
class Agent:
    description: str
    graph_like: AgentGraphLike
    enabled: bool = True
    required_env: frozenset[str] = frozenset()  # optional, for future auto-unpause
```

**Alternatives considered:**

| Approach | Pros | Cons |
|----------|------|------|
| Remove from `agents` dict | Simplest filter | Loses registration; hard to re-enable; breaks import graph |
| Separate `PAUSED_AGENTS` set | One-line toggle | Two sources of truth; easy to drift |
| **`enabled` on dataclass** | Single registry; self-documenting; one-line re-enable | Slightly more fields |

**Rationale:** Matches user request to pause, not remove. All metadata stays co-located.

### 2. v1 pause defaults

| Agent | v1 `enabled` | Reason |
|-------|-------------|--------|
| `chatbot` | `True` | Core demo |
| `research-assistant` | `True` | Default agent |
| `interrupt-agent` | `False` | Optional; enable when demoing HITL |
| All others | `False` | Extra providers or LangGraph demos |

Re-enable example — one line change:

```python
"interrupt-agent": Agent(..., enabled=True),
```

### 3. API behavior for paused agents

**Choice:** Return `404 Not Found` with body `"Agent '{id}' is paused"` when invoke/stream targets a paused agent. `get_agent()` raises `KeyError`-like error converted to HTTP 404 in route handlers.

**Startup:** Loop only enabled agents:

```python
for a in get_all_agent_info():  # already filtered
    await load_agent(a.key)
```

Lazy agents (GitHub MCP) skip init entirely when paused — saves startup time.

### 4. NVIDIA NIM via existing compatible provider

**Choice:** Document in `.env.example`:

```env
GOOGLE_API_KEY=...                    # primary default
DEFAULT_MODEL=gemini-2.0-flash        # explicit — avoids OpenAI precedence bug

# Optional: NVIDIA NIM (free tier ~40 RPM)
COMPATIBLE_BASE_URL=https://integrate.api.nvidia.com/v1
COMPATIBLE_API_KEY=nvapi-...
COMPATIBLE_MODEL=meta/llama-3.1-8b-instruct
```

User selects `openai-compatible` in Streamlit Settings to try NIM per session.

**Alternatives considered:**

- New `NVIDIA_API_KEY` + `Provider.NVIDIA` — cleaner naming but more code (models enum, settings branch, llm.py branch, tests)
- OpenRouter routing to NIM — adds latency/cost; user already has direct NIM key

**Rationale:** Zero new Provider code for v1; NIM is OpenAI-compatible by design.

### 5. Multi-provider default model fix

**Choice:** Recommend (and test) setting `DEFAULT_MODEL=gemini-2.0-flash` explicitly in deploy docs when `GOOGLE_API_KEY` + other keys coexist. No settings.py reorder in this change unless a one-line comment suffices.

**Follow-up (not this change):** Per-agent model defaults or provider-aware routing.

### 6. Optional `resolve_agent_enablement()` helper

Small function in `agents.py`:

```python
def resolve_agent_enablement() -> None:
    """Opt-in: auto-enable agents when required_env keys are set."""
    for agent_id, agent in agents.items():
        if agent.required_env and all(os.environ.get(k) for k in agent.required_env):
            agent.enabled = True
```

Called from `lifespan` only if `AUTO_ENABLE_AGENTS=true` env is set. Default off for predictable v1 behavior.

## Architecture (after change)

```
agents.py                          service.py                    streamlit
┌──────────────────┐              ┌─────────────────┐           ┌──────────────┐
│ Agent(enabled=…) │──register───▶│ load enabled    │──/info───▶│ picker shows │
│ 10 agents total  │              │ only at startup │           │ enabled only │
│ 2-3 enabled v1   │              │ 404 if paused   │           └──────────────┘
└──────────────────┘              └─────────────────┘
         │
         │ enabled=False → skip load_agent, no MCP init
         ▼
   source modules unchanged on disk
```

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Direct API calls to paused agent IDs | 404 with clear message; document paused list |
| Tests reference paused agents | Tests use `get_agent()` with explicit enable or test fixtures |
| NIM 40 RPM exceeded under load | Document as dev/test provider; keep Gemini as production default |
| Multiple keys → wrong default model | Mandate explicit `DEFAULT_MODEL` in deploy env |
| `WELCOME_MESSAGES` for paused agents | Keep entries; used when re-enabled |

## Migration Plan

1. Implement `enabled` flag + v1 defaults in `agents.py`
2. Filter `get_all_agent_info()`; guard `get_agent()` for paused
3. Update service lifespan + route error handling
4. Update `.env.example` and README NIM section
5. Run pytest; deploy Render with unchanged env (Gemini-only still works)
6. Rollback: set all `enabled=True` or revert commit

## Open Questions

1. Include `interrupt-agent` in v1 active set? (Currently spec says paused; flip one flag to enable.)
2. Add `AUTO_ENABLE_AGENTS` in v1 or defer to week-2 RAG work?
3. Per-agent LLM routing — separate change when NIM is used for specific agents only?
