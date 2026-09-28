# Member 1 - Day 1 Tasks

## Status: PLANNED

## Goal

Foundation: Schema, rules engine, basic verifier interface.

---

## Task 1: Schema Definition (`schema.py`)

### Deliverables
- [ ] `CandidateMemory` dataclass
- [ ] `VerificationContext` dataclass
- [ ] `Scope` / `ScopeInfo` enums/classes
- [ ] `MemoryDecision` dataclass with all fields
- [ ] `DecisionType` enum (RETAIN, UPDATE, MERGE, REJECT, NEEDS_REVIEW)
- [ ] `SourceEvidence`, `Provenance`, `MergeInstruction`
- [ ] `MemoryType` enum (preference, requirement, objection, competitor, stakeholder, pricing, compliance, technical, decision, pattern)
- [ ] `ConflictInfo`, `MemoryRef`

### Acceptance
- All types match `docs/API_CONTRACTS.md`
- Pydantic v2 models with validation
- Serialization to/from JSON works

---

## Task 2: Rules Engine Framework (`rules.py`)

### Deliverables
- [ ] `Rule` base class / protocol
- [ ] `RuleResult` dataclass (pass/fail, reason, metadata)
- [ ] `RulesEngine` class with `evaluate_all()` method
- [ ] Rule registry (decorator-based registration)
- [ ] Rule categories: admission, reliability, relevance, contamination, consolidation, conflict, scope, lifecycle, security

### Acceptance
- Can register 34 rules by number
- Returns ordered results with reasons
- Extensible for new rules

---

## Task 3: MemoryGuard Skeleton (`memory_guard.py`)

### Deliverables
- [ ] `MemoryGuard` class with `verify()` method
- [ ] Dependency injection for verifier client
- [ ] Orchestration: admission → reliability → relevance → contamination → consolidation → conflict → scope → promotion
- [ ] Decision aggregation logic
- [ ] Audit ID generation (UUID4)
- [ ] Error handling with fallback to NEEDS_REVIEW

### Acceptance
- `verify()` returns `MemoryDecision` for any input
- All rule categories invoked in order
- Structured logging of each step

---

## Task 4: Admission Policy (`admission.py`)

### Rules to Implement
- **R29**: Utility Threshold — Reject polite phrases ("thanks", "good talking")
- **R30**: Deal Relevance — Must relate to active deal or rep pattern
- **R31**: Actionability — Must enable future agent behavior

### Deliverables
- [ ] `AdmissionPolicy` class
- [ ] `assess_utility(candidate, context) -> RuleResult`
- [ ] `check_deal_relevance(candidate, context) -> RuleResult`
- [ ] `assess_actionability(candidate, context) -> RuleResult`
- [ ] Keyword lists for polite phrases (configurable)
- [ ] Unit tests for each rule

### Acceptance
- "Thanks for the call" → REJECT
- "We need SOC2" → PASS
- "I prefer email" → PASS

---

## Task 5: Basic Verifier Interface

### Deliverables
- [ ] `VerifierClient` protocol (abstraction over LLM)
- [ ] Structured prompt template for verification
- [ ] JSON response parsing with Pydantic validation
- [ ] Retry logic (3 attempts)
- [ ] Fallback: rule-based verification if LLM fails

### Acceptance
- Can call verifier with candidate + source
- Returns structured result (supported/unsupported/partial)
- Graceful degradation

---

## Task 6: Unit Test Skeletons

### Files
- [ ] `tests/test_memory_guard.py`
- [ ] `tests/test_admission.py`
- [ ] `tests/test_rules.py`

### Pattern
```python
def test_utility_threshold_rejects_polite_phrases():
    """
    TODO:
    Give candidate: "Thanks for the call"
    Give context: deal context
    Assert decision == REJECT
    Assert reason contains "polite"
    """
    pass
```

---

## Dependencies on Other Members

| Need From | Artifact | Deadline |
|-----------|----------|----------|
| Member 2 | `VerifierClient` implementation (Groq) | Day 1 EOD |
| Member 2 | `Config` with `VERIFIER_MODEL` | Day 1 Morning |
| Member 3 | Scenario data format (for test fixtures) | Day 1 EOD |

## Expected Commits

```
feat(memory): add schema types
feat(memory): add rules engine framework
feat(memory): add memory_guard skeleton
feat(memory): add admission policy
feat(memory): add verifier interface
test(memory): add admission test skeletons
```

## Handoff Requirements

**To Member 2 (Backend)**:
- Stable `MemoryDecision` schema
- Working `verify()` interface (can be mocked)
- Documented input/output types

**To Member 3 (Eval)**:
- Test fixtures for admission rules
- Expected decision format for scenarios

---

**Status: PLANNED** — Start Day 1 Morning.