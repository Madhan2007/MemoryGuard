# Member 2: Hindsight + Backend + Agent Harness

## Status: PLANNED

## Purpose

Integrate Hindsight persistent memory, LLM providers, and build the agent harness that orchestrates the full conversation loop.

## Owner

**Member 2** — Hindsight + Backend Engineer

## Responsibilities

- Hindsight client (`hindsight_client.py`)
- Groq/LLM client (`groq_client.py`)
- Configuration system (`config.py`)
- Agent harness (`agent_harness.py`)
- Session management (`session.py`)
- Structured logging (`logger.py`)
- Outcome capture pipeline
- Environment configuration
- Integration testing
- Error handling & retry logic

### Outcome Capture Pipeline

The backend supports the full learning flow:

```
run_turn()
    ↓
recall()                  ← Hindsight retrieval (project + common)
    ↓
agent_response()          ← Main LLM generates response
    ↓
candidate_memory()        ← Extract memory candidates
    ↓
memoryguard.verify()      ← Governance decision
    ↓
persist()                 ← Hindsight retain
    ↓
optional outcome capture  ← Record what happened
    ↓
outcome verification      ← MemoryGuard validates outcome claim
    ↓
persist verified outcome  ← Hindsight retain (if supported)
```

> **Important**: The backend does NOT decide policy. Member 2 executes MemoryGuard’s decision.

## Files Owned

```
src/integrations/
├── __init__.py
├── hindsight_client.py   # Hindsight SDK wrapper
├── groq_client.py        # Main + Verifier LLM clients
└── config.py             # Pydantic settings

src/harness/
├── __init__.py
├── agent_harness.py      # Main agent loop
├── session.py            # Conversation state
├── logger.py             # Structured JSON logging
└── eval_harness.py       # Shared with Member 3
```

## Dependencies

- **Input**: User message, deal_id, rep_id
- **Output**: AgentResponse (response + decisions + recalled memories)
- **Consumes**: Member 1's `MemoryGuard.verify()`
- **Provides**: `AgentLoop.process_turn()` for Member 4 UI
- **Provides**: `HindsightClient` for Member 3 eval

## Interfaces

### AgentLoop (for Member 4)
```python
async def process_turn(
    user_input: str,
    deal_id: str,
    rep_id: str
) -> AgentResponse
```

### HindsightClient (for Member 3)
```python
async def recall(bank_id: str, query: str, top_k: int) -> List[Memory]
async def retain(bank_id: str, memory: str, metadata: MemoryMetadata) -> Memory
```

### Contract
Defined in `docs/API_CONTRACTS.md` and `docs/CROSS_MEMBER_CONTRACTS.md`

## How to Run

```bash
# Start agent (for UI)
python scripts/run_app.py

# Run integration tests
pytest tests/test_integration.py -v

# Type check
mypy src/integrations/ src/harness/

# Lint
ruff check src/integrations/ src/harness/
```

## How to Test

- Unit tests with mocked Hindsight/LLM
- Integration tests with real APIs (or mock mode)
- Member 3's evaluation harness runs full scenarios

## Definition of Done

- [ ] Hindsight recall/retain working for both banks
- [ ] Agent loop processes turns end-to-end
- [ ] MemoryGuard integrated in loop
- [ ] Error handling + retries + circuit breaker
- [ ] Structured logging operational
- [ ] Config validates all required vars at startup
- [ ] Mock mode works for demo reliability

## What Not To Modify

- ❌ `src/memory/*` — Member 1 owns
- ❌ `src/ui/*` — Member 4 owns
- ❌ `src/data/scenarios/*` — Member 3 owns
- ❌ `docs/members/member1-core/*` — Member 1 owns
- ❌ `docs/members/member3-data-eval/*` — Member 3 owns
- ❌ `docs/members/member4-ui-demo/*` — Member 4 owns

## Related Documentation

- `docs/members/member2-backend/DESIGN.md` — Architecture details
- `docs/members/member2-backend/API.md` — Internal APIs
- `docs/members/member2-backend/HINDSIGHT.md` — Integration details
- `docs/members/member2-backend/MODELS.md` — Model configuration
- `docs/members/member2-backend/ENVIRONMENT.md` — Env vars
- `docs/members/member2-backend/ERROR_HANDLING.md` — Error strategy
- `docs/members/member2-backend/TESTING.md` — Test strategy
- `docs/HINDSIGHT_INTEGRATION.md` — Shared Hindsight doc
- `docs/MODEL_CONFIGURATION.md` — Model config
- `docs/API_CONTRACTS.md` — Contracts

## Current Status

**Status: PLANNED** — Day 1: Hindsight setup, LLM config, basic agent loop