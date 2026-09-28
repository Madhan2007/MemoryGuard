# Cross-Member Contracts

## Status: PLANNED

## Contract 1: MemoryGuard → Backend

### Interface
```python
# src/memory/memory_guard.py
async def verify(
    candidate_memory: CandidateMemory,
    source_text: str,
    context: VerificationContext,
    scope: Scope
) -> MemoryDecision
```

### Input (Backend → MemoryGuard)
| Field | Type | Required |
|-------|------|----------|
| `candidate_memory.text` | string | Yes |
| `candidate_memory.memory_type` | enum | Yes |
| `candidate_memory.confidence` | float | Yes |
| `source_text` | string | Yes |
| `context.deal_id` | string | Yes |
| `context.rep_id` | string | Yes |
| `context.conversation_id` | string | Yes |
| `context.turn_id` | int | Yes |
| `context.existing_memories` | List[Memory] | Yes |
| `context.deal_stage` | enum | Yes |
| `scope` | ScopeInfo | Yes |

### Output (MemoryGuard → Backend)
| Field | Type | Required |
|-------|------|----------|
| `decision` | DecisionType | Yes |
| `memory_text` | string | Yes |
| `reason` | string | Yes |
| `confidence` | float | Yes |
| `scope` | Scope | Yes |
| `source_evidence` | List[SourceEvidence] | Yes |
| `provenance` | Provenance | Yes |
| `similar_memories` | List[MemoryRef] | If MERGE |
| `conflicts` | List[ConflictInfo] | If conflict |
| `audit_id` | string | Yes |
| `merge_instruction` | MergeInstruction | If MERGE/UPDATE |

### Versioning
- v1: Current schema
- Breaking changes: Major version bump, all members notified
- Additive changes: Minor version, backward compatible

### Owner
- **Producer**: Member 1
- **Consumer**: Member 2

---

## Contract 2: Backend → UI

### Interface
```python
# src/harness/agent_harness.py
async def process_turn(
    user_input: str,
    deal_id: str,
    rep_id: str
) -> AgentResponse
```

### Output (Backend → UI)
```python
@dataclass
class AgentResponse:
    response_text: str                    # Agent's reply to user
    candidate_memories: List[CandidateMemory]  # What LLM extracted
    memory_decisions: List[MemoryDecision]     # MemoryGuard decisions
    recalled_memories: List[Memory]            # Context used
    turn_metadata: TurnMetadata                # Timing, tokens, etc.
```

### UI Requirements
- Display `response_text` in chat
- Show `memory_decisions` in decision panel
- Visualize `provenance` in provenance component
- Show `recalled_memories` as memory cards
- Compare `candidate_memories` vs `memory_decisions` (before/after)

### Versioning
- Same as Contract 1
- UI must handle missing optional fields gracefully

### Owner
- **Producer**: Member 2
- **Consumer**: Member 4

---

## Contract 3: Evaluation → Core

### Interface
```python
# src/harness/eval_harness.py
async def run_scenario(scenario: Scenario) -> ScenarioResult
```

### Input (Evaluation → Core/Backend)
- Scenario JSON (turns, expected outcomes)
- Ground truth memories
- Injected hallucinations for contamination test

### Output (Core/Backend → Evaluation)
- Actual decisions per turn
- Actual final memories
- Latency, token usage
- Error traces

### Metrics Computed (Member 3)
- Precision, recall, F1 per scenario
- Merge rate, contamination rejection rate
- Scope isolation verification
- Ablation comparisons

### Owner
- **Producer**: Member 2 (agent), Member 1 (decisions)
- **Consumer**: Member 3

---

## Contract 4: Backend → Evaluation

### Interface
```python
# Evaluation needs access to:
# - AgentLoop for scenario execution
# - HindsightClient for direct memory inspection
# - MemoryGuard for unit testing decisions
```

### Member 2 Provides
- `AgentLoop` with `process_turn()`
- `HindsightClient` with `recall()`, `retain()`, `get_memory()`
- Test fixtures for isolated unit tests

### Member 3 Consumes
- Writes `EvaluationHarness` using above
- Creates scenario runners
- Generates metrics

### Owner
- **Producer**: Member 2
- **Consumer**: Member 3

---

## Contract 5: All Modules → Configuration

### Interface
```python
# src/integrations/config.py
config = Config()  # Singleton, validated at startup
```

### Required Variables (All Modules)
| Variable | Modules Using |
|----------|---------------|
| `GROQ_API_KEY` | Member 1 (verifier), Member 2 (LLM) |
| `HINDSIGHT_API_KEY` | Member 2 |
| `HINDSIGHT_BASE_URL` | Member 2 |
| `HINDSIGHT_PROJECT_BANK` | Member 2 |
| `HINDSIGHT_COMMON_BANK` | Member 2 |
| `MAIN_MODEL` | Member 1, Member 2 |
| `VERIFIER_MODEL` | Member 1 |
| `LOG_LEVEL` | All |

### Validation Rules
- Fail fast at startup if required vars missing
- No defaults for secrets
- Type validation via Pydantic

### Owner
- **Producer**: Member 2 (config.py)
- **Consumer**: All members

---

## Contract Enforcement

### CI Checks
- Schema validation for all contracts
- Type checking across module boundaries
- Integration test on PR to `develop`

### Breaking Change Process
1. Propose in `docs/DECISIONS.md`
2. Update all affected contracts
3. Coordinate with all consumers
4. Version bump + migration guide

---

**Status: PLANNED** — Contracts frozen Day 1 EOD.