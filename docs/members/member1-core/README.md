# Member 1: MemoryGuard Core

## Status: PLANNED

## Purpose

Build the decision engine that determines what the agent should remember. This is the core governance layer.

## Owner

**Member 1** — MemoryGuard Core Engineer

## Responsibilities

- MemoryGuard decision engine (`memory_guard.py`)
- Memory rules engine (`rules.py`)
- Memory schema & decision types (`schema.py`)
- Admission policy (`admission.py`)
- Consolidation/merge policy (`consolidation.py`)
- Contamination detection (`contamination.py`)
- Provenance chain (`provenance.py`)
- Conflict handling (`conflicts.py`)
- Scope management (`scopes.py`)
- Promotion policy (`promotion.py`)
- Core unit tests

## Files Owned

```
src/memory/
├── __init__.py
├── memory_guard.py      # Main verify() entry point
├── rules.py             # Rules engine (34 rules)
├── schema.py            # Pydantic models for all types
├── admission.py         # Admission policy (R29-R31)
├── consolidation.py     # Merge logic (R5-R9, R32-R33)
├── contamination.py     # Grounding verification (R1-R4, R34)
├── provenance.py        # Provenance chain, audit trail
├── conflicts.py         # Conflict detection/resolution (R10-R14)
├── scopes.py            # Scope assignment, isolation (R15-R19)
└── promotion.py         # Cross-scope promotion (R24)
```

## Dependencies

- **Input**: CandidateMemory, source_text, VerificationContext, Scope
- **Output**: MemoryDecision (defined in `schema.py`)
- **Consumes**: Verifier LLM (via Member 2's Groq client)
- **Consumed by**: Member 2 (Agent Harness)

## Interfaces

### Primary: `verify()`
```python
async def verify(
    candidate_memory: CandidateMemory,
    source_text: str,
    context: VerificationContext,
    scope: Scope
) -> MemoryDecision
```

### Contract
Defined in `docs/API_CONTRACTS.md` — **Frozen Day 1 EOD**

## How to Run

```bash
# Unit tests
pytest tests/test_memory_guard.py -v
pytest tests/test_admission.py -v
pytest tests/test_consolidation.py -v
pytest tests/test_contamination.py -v
pytest tests/test_provenance.py -v
pytest tests/test_scope.py -v
pytest tests/test_conflicts.py -v

# Type check
mypy src/memory/
```

## How to Test

- All 34 rules have test cases in `tests/`
- Run scenario tests via Member 3's eval harness
- Mock verifier LLM for deterministic tests

## Definition of Done

- [ ] All 34 rules implemented with passing tests
- [ ] `verify()` returns correct decisions for all 5 scenarios
- [ ] Provenance chain complete for every decision
- [ ] Decision contract stable (no breaking changes after Day 1)
- [ ] Type hints on all public functions
- [ ] Docstrings on all public classes/functions

## What Not To Modify

- ❌ `src/integrations/*` — Member 2 owns
- ❌ `src/harness/agent_harness.py` — Member 2 owns
- ❌ `src/ui/*` — Member 4 owns
- ❌ `src/data/scenarios/*` — Member 3 owns
- ❌ `docs/members/member2-backend/*` — Member 2 owns
- ❌ `docs/members/member3-data-eval/*` — Member 3 owns
- ❌ `docs/members/member4-ui-demo/*` — Member 4 owns

## Related Documentation

- `docs/members/member1-core/DESIGN.md` — Architecture details
- `docs/members/member1-core/API.md` — Internal APIs
- `docs/members/member1-core/RULES.md` — Rule implementations
- `docs/members/member1-core/TESTING.md` — Test strategy
- `docs/members/member1-core/DECISIONS.md` — Local decisions
- `docs/API_CONTRACTS.md` — External contract
- `docs/MEMORY_RULES.md` — All 34 rules specification
- `docs/DATA_MODEL.md` — Schema definitions

## Current Status

**Status: PLANNED** — Day 1: Schema, rules framework, admission policy