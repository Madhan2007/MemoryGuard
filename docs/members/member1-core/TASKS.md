# Member 1 - Day 1-3 Tasks (Memory Core & Governance)

## Status: COMPLETED & VALIDATED

## Goal

Foundation & Production: Schema, 34 governance rules engine, RapidFuzz C-level consolidation, contradiction & contamination shields, provenance audit.

---

## Task 1: Schema Definition (`src/memory/schema.py`)

### Deliverables
- [x] `MemoryCandidate` (source text, span, category, confidence, deal/rep scope)
- [x] `VerificationContext` / `EvaluationContext` dataclass
- [x] `Scope` / `ScopeInfo` enums/classes (`project` vs `common`)
- [x] `MemoryDecision` model with all fields (`decision`, `reason`, `memory_id`, `provenance`, `confidence`)
- [x] `DecisionType` enum (RETAIN, UPDATE, MERGE, REJECT, NEEDS_REVIEW)
- [x] `SourceEvidence`, `Provenance`, `MergeInstruction`
- [x] `MemoryType` / `MemoryCategory` enum (preference, requirement, objection, competitor, stakeholder, pricing, compliance, technical, decision, pattern)
- [x] `ConflictInfo`, `ConflictType`, `ChangeType`

### Acceptance
- [x] All types match `docs/API_CONTRACTS.md`
- [x] Pydantic v2 models with validation
- [x] Serialization to/from JSON works

---

## Task 2: Rules Engine Framework (`src/memory/rules.py` & `src/memory/memory_guard.py`)

### Deliverables
- [x] `Rule` base class / protocol
- [x] `RuleResult` dataclass (pass/fail, reason, metadata)
- [x] `RulesEngine` class with sequential deterministic evaluation pipeline
- [x] Rule registry covering all 34 rules
- [x] Rule categories: admission, reliability, relevance, contamination, consolidation, conflict, scope, lifecycle, security

### Acceptance
- [x] All 34 rules cataloged and enforced
- [x] Returns ordered results with reasons
- [x] Extensible for new rules

---

## Task 3: MemoryGuard Decision Engine (`src/memory/memory_guard.py`)

### Deliverables
- [x] `MemoryGuard` class with `verify()` method
- [x] Deterministic-first hybrid pipeline:
  1. Instant Programmatic Admission (<5 chars, polite filler)
  2. RapidFuzz Pre-Filter (composite token set + weighted ratio >= 85.0)
  3. Contradiction & Polarity Shield
  4. Contamination Shield
  5. PydanticAI Verifier Runtime
- [x] Audit ID generation (`audit_id` with UUIDv4)
- [x] Fail-safe fallback to `NEEDS_REVIEW`

### Acceptance
- [x] `verify()` returns typed `MemoryDecision` for any input
- [x] All rule categories invoked in deterministic order
- [x] Structured logging of each step

---

## Task 4: Admission Policy (`src/memory/admission.py`)

### Rules Implemented
- **R29**: Utility Threshold — Reject polite phrases ("thanks", "good talking")
- **R30**: Deal Relevance — Must relate to active deal or rep pattern
- **R31**: Actionability — Must enable future agent behavior

### Deliverables
- [x] `AdmissionPolicy` class
- [x] `assess_utility(candidate, context) -> RuleResult`
- [x] `check_deal_relevance(candidate, context) -> RuleResult`
- [x] `assess_actionability(candidate, context) -> RuleResult`
- [x] Keyword lists for polite phrases
- [x] Unit tests for each rule

### Acceptance
- [x] "Thanks for the call" → REJECT
- [x] "We need SOC2" → PASS
- [x] "I prefer email" → PASS

---

## Task 5: RapidFuzz Consolidation & Merging (`src/memory/consolidation.py`)

### Deliverables
- [x] `RapidFuzzMatcher` with composite score calculation:
  `max(fuzz.token_set_ratio, fuzz.weighted_ratio)`
- [x] Threshold filtering (`>= 85.0`)
- [x] Evidence count & frequency reinforcement
- [x] Timestamp tracking and last_seen updates

---

## Task 6: Contradiction & Lifecycle Management (`src/memory/conflicts.py` & `promotion.py`)

### Deliverables
- [x] Direct contradiction detection (`required` vs `not required`)
- [x] Temporal override resolution (newer evidence supersedes older)
- [x] Exponential decay function: $e^{-\Delta t / \text{half\_life}}$
- [x] Evidence-based half-life adjustment (30 days single mention vs 90 days reinforced)
- [x] Cross-scope promotion from project to common bank (Rule R24)

---

## Task 7: Unit Test Suite (`tests/unit/test_memory_guard.py`)

### Deliverables
- [x] 100% test pass rate across all memory guard unit tests
- [x] 10 unit test cases for admission, merge, contamination, decay, and provenance