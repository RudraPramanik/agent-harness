## 1. Agent enablement model

- [x] 1.1 Add `enabled: bool = True` (and optional `required_env: frozenset[str]`) to the `Agent` dataclass in `src/agents/agents.py`
- [x] 1.2 Set v1 defaults: `chatbot` and `research-assistant` enabled; all other agents `enabled=False`
- [x] 1.3 Update `get_all_agent_info()` to return only enabled agents
- [x] 1.4 Add `get_agent()` guard that raises a clear error when the agent exists but is paused (e.g. `AgentPausedError` or `KeyError` with distinct message)
- [x] 1.5 Add optional `resolve_agent_enablement()` helper and `AUTO_ENABLE_AGENTS` env gate (default off)

## 2. Service integration

- [x] 2.1 Confirm service lifespan only loads enabled agents (via filtered `get_all_agent_info()`)
- [x] 2.2 Return HTTP 404 with `"Agent '{id}' is paused"` when invoke/stream targets a paused agent
- [x] 2.3 Verify `GET /info` returns only enabled agents and unchanged models list

## 3. Multi-provider and NVIDIA NIM docs

- [x] 3.1 Add NVIDIA NIM example block to `.env.example` (`COMPATIBLE_BASE_URL`, `COMPATIBLE_API_KEY`, `COMPATIBLE_MODEL`)
- [x] 3.2 Document explicit `DEFAULT_MODEL=gemini-2.0-flash` when multiple provider keys are set (README or docs/BLUEPRINT.md)
- [x] 3.3 Add brief NIM free-tier note (~40 RPM) recommending Gemini for production default

## 4. Tests

- [x] 4.1 Test `get_all_agent_info()` excludes paused agents
- [x] 4.2 Test `get_agent()` on paused agent raises expected error
- [x] 4.3 Test service lifespan skips paused agents (extend `tests/service/test_service_lifespan.py`)
- [x] 4.4 Test invoke/stream returns 404 for paused agent ID
- [x] 4.5 Run full `pytest` and fix any tests that assumed all 10 agents were active

## 5. Verification

- [x] 5.1 Local smoke: start API + Streamlit; confirm picker shows only `chatbot` and `research-assistant`
- [x] 5.2 Re-enable one paused agent (`interrupt-agent` → `enabled=True`); confirm it appears after restart without other code changes
- [x] 5.3 Optional: configure NIM compatible vars; confirm `openai-compatible` appears in model picker alongside Gemini
