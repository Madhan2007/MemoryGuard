# Member 2 - Day 1 Tasks

## Status: PLANNED

## Goal

Foundation: Hindsight client, LLM clients, config, basic agent loop skeleton.

---

## Task 1: Configuration System (`config.py`)

### Deliverables
- [ ] `Config` class with Pydantic BaseSettings
- [ ] All required env vars (GROQ_API_KEY, HINDSIGHT_API_KEY, etc.)
- [ ] Model config (MAIN_MODEL, VERIFIER_MODEL, temperatures, tokens)
- [ ] Hindsight config (API key, base URL, bank IDs)
- [ ] Validation: fail fast if required vars missing
- [ ] No defaults for secrets
- [ ] Singleton pattern for app-wide access

### Acceptance
- `Config()` raises clear error if `.env` missing required vars
- All model params configurable
- Type-safe access throughout codebase

---

## Task 2: Groq/LLM Client (`groq_client.py`)

### Deliverables
- [ ] `GroqClient` class with async methods
- [ ] `call_main_llm(messages)` — response generation
- [ ] `call_verifier_llm(messages)` — structured output for verification
- [ ] Model fallback chain (config-driven)
- [ ] Retry logic (3 attempts, exponential backoff)
- [ ] Structured output parsing with Pydantic validation
- [ ] Mock mode for development (`MOCK_LLM=true`)
- [ ] Token usage tracking

### Acceptance
- Main LLM returns text response
- Verifier LLM returns validated JSON
- Falls back to next model on failure
- Works with mock mode

---

## Task 3: Hindsight Client (`hindsight_client.py`)

### Deliverables
- [ ] `HindsightClient` class
- [ ] `recall(bank_id, query, top_k, filters)` — semantic search
- [ ] `retain(bank_id, memory, metadata, merge_policy)` — store/update
- [ ] `create_bank(bank_id)` — idempotent bank creation
- [ ] `get_memory(memory_id)` — direct retrieval
- [ ] Bank ID helpers: `project_bank(deal_id)`, `common_bank(rep_id)`
- [ ] Retry logic + circuit breaker
- [ ] Mock mode for development (`MOCK_HINDSIGHT=true`)

### Acceptance
- Recalls memories from both banks
- Retains with full MemoryGuard metadata
- Handles bank-not-found gracefully
- Works with mock mode

---

## Task 4: Agent Harness Skeleton (`agent_harness.py`)

### Deliverables
- [ ] `AgentLoop` class
- [ ] `process_turn(user_input, deal_id, rep_id)` method
- [ ] Flow: Recall → Context Build → Main LLM → Candidate → MemoryGuard → Retain
- [ ] Dependency injection for HindsightClient, GroqClient, MemoryGuard
- [ ] Session integration
- [ ] Basic error handling

### Acceptance
- Single turn processes without errors
- Calls all components in correct order
- Returns `AgentResponse` with all fields

---

## Task 5: Session Management (`session.py`)

### Deliverables
- [ ] `Session` class — conversation state
- [ ] `ConversationHistory` — turn storage
- [ ] `turn_id` management
- [ ] Context window management (token budget)
- [ ] Serialization for persistence

### Acceptance
- Tracks multi-turn conversations
- Provides history for context building
- Manages token limits

---

## Task 6: Structured Logging (`logger.py`)

### Deliverables
- [ ] `setup_logging()` — JSON formatter, Rich handler
- [ ] Correlation IDs for request tracing
- [ ] Log levels: DEBUG, INFO, WARNING, ERROR
- [ ] Structured fields: component, deal_id, rep_id, turn_id
- [ ] No secrets in logs
- [ ] Performance timing decorators

### Acceptance
- Logs are parseable JSON
- Request traces work across components
- No API keys in output

---

## Dependencies on Other Members

| Need From | Artifact | Deadline |
|-----------|----------|----------|
| Member 1 | `MemoryGuard.verify()` interface (can mock) | Day 1 EOD |
| Member 1 | `MemoryDecision` schema | Day 1 Morning |
| Member 3 | Scenario format (for integration test) | Day 2 Morning |

## Expected Commits

```
feat(config): add pydantic settings with validation
feat(integrations): add groq client with fallback
feat(integrations): add hindsight client with mock mode
feat(harness): add agent loop skeleton
feat(harness): add session management
feat(harness): add structured logging
```

## Handoff Requirements

**To Member 1 (Core)**:
- Working `VerifierClient` implementation
- `Config` with `VERIFIER_MODEL`

**To Member 3 (Eval)**:
- `AgentLoop.process_turn()` for scenario runner
- `HindsightClient` for direct memory inspection

**To Member 4 (UI)**:
- `AgentLoop.process_turn()` API
- `AgentResponse` structure
- Demo-ready error handling

---

**Status: PLANNED** — Start Day 1 Morning.