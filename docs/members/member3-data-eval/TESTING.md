# Member 3 - Testing Strategy

## Status: IMPLEMENTED & VERIFIED

## Test Organization

```
tests/
├── test_admission.py         # R29-R31 tests
├── test_consolidation.py     # R5-R9, R32-R33 tests
├── test_contamination.py     # R1-R4, R34 tests
├── test_provenance.py        # R2, R28 tests
├── test_scope.py             # R15-R19 tests
├── test_conflicts.py         # R10-R14 tests
├── test_promotion.py         # R20-R24 tests
├── test_integration.py       # End-to-end
└── test_evaluation.py        # Evaluation harness tests
```

## Test Patterns by Module

### Admission Tests (`test_admission.py`)
```python
# R29: Utility Threshold
def test_polite_phrases_rejected():
    # Source: "Thanks for the call"
    # Candidate: "Thanks for the call"
    # Expected: REJECT

# R30: Deal Relevance
def test_irrelevant_memory_rejected():
    # Candidate about unrelated topic
    # Expected: REJECT

# R31: Actionability
def test_actionable_memories_admitted():
    # Candidate: "We need SOC2"
    # Type: COMPLIANCE
    # Expected: PASS
```

### Consolidation Tests (`test_consolidation.py`)
```python
# R5: Frequency Tracking
def test_frequency_increments_on_merge():
    # Merge 3 times
    # Expected: frequency=4

# R6: Evidence Count
def test_evidence_count_matches_sources():
    # 3 distinct quotes
    # Expected: evidence_count=3

# R7: First/Last Seen
def test_timestamps_span_correctly():
    # First turn 1, last turn 12
    # Expected: correct timestamps

# R8: Semantic Similarity
def test_similar_memories_merged():
    # "prefer email" + "email is best"
    # Expected: MERGE

# R9: Merge Preserves Provenance
def test_merged_memory_has_all_quotes():
    # Merge preserves all source quotes
    # Expected: all quotes in provenance

# R32: Merge Transparency
def test_merge_reason_generated():
    # Reason explains why merge
    # Expected: reason string

# R33: No Silent Overwrites
def test_update_creates_audit_entry():
    # UPDATE creates audit trail
    # Expected: audit_id present
```

### Contamination Tests (`test_contamination.py`)
```python
# R1: Grounding Required
def test_unsupported_memory_rejected():
    # Source: "evaluating SOC2"
    # Candidate: "SOC2 mandatory"
    # Expected: REJECT

# R2: Verbatim Quote
def test_source_quote_preserved_exact():
    # Quote matches source exactly
    # Expected: exact match

# R3: No Hallucination
def test_hallucinated_detail_rejected():
    # Source: "budget tight"
    # Candidate: "budget $50K"
    # Expected: REJECT

# R4: Confidence Threshold
def test_low_confidence_needs_review():
    # Verifier confidence < 0.7
    # Expected: NEEDS_REVIEW

# R34: Source Support
def test_unsupported_candidate_rejected():
    # NORTHWIND scenario
    # Expected: REJECT with correct reason
```

### Provenance Tests (`test_provenance.py`)
```python
# R2: Verbatim Quote
def test_provenance_includes_exact_quotes():
    # Provenance.source_quotes exact

# R28: Audit Immutable
def test_audit_immutable():
    # Audit chain append-only
    # Expected: hash chain valid
```

### Scope Tests (`test_scope.py`)
```python
# R15: Project Isolation
def test_project_memory_isolated():
    # Acme memories not in Globex
    # Expected: 0 cross-leakage

# R16: Common Privacy
def test_common_memory_private():
    # Rep A patterns not visible to Rep B
    # Expected: 0 cross-rep leakage

# R17: Scope Assignment
def test_scope_assigned_on_admission():
    # Every memory has scope
    # Expected: scope in {project, common}

# R18: Cross-Scope Prevention
def test_wrong_scope_rejected():
    # Personal pref to project bank
    # Expected: REJECT

# R19: Combined Read Only
def test_no_third_persistent_bank():
    # Only 2 banks exist
    # Expected: 2 banks
```

### Conflict Tests (`test_conflicts.py`)
```python
# R10: Contradiction Detection
def test_contradiction_detected():
    # "not required" vs "now required"
    # Expected: CONFLICT

# R11: Temporal Resolution
def test_explicit_change_updates_memory():
    # "now required" wins
    # Expected: UPDATE with change_note

# R12: Explicit vs Implicit
def test_explicit_change_priority():
    # Explicit customer change > agent inference
    # Expected: explicit wins

# R13: Stakeholder Isolation
def test_stakeholder_differences_not_conflicts():
    # Champion vs Procurement diff prefs
    # Expected: both retained, no conflict

# R14: Conflict Flagging
def test_conflict_flagged_not_overwritten():
    # conflicts field populated
    # Expected: conflict reference
```

### Promotion Tests (`test_promotion.py`)
```python
# R20: Recency Weighting
def test_recent_memories_ranked_higher():
    # Recent memory > old in recall
    # Expected: correct ranking

# R21: Decay Function
def test_decay_reduces_relevance():
    # 90-day half-life
    # Expected: decay formula correct

# R22: Evidence-Based Decay
def test_single_evidence_faster_decay():
    # freq=1, evidence=1 → half_life=30
    # Expected: faster decay

# R23: Archive Not Delete
def test_memory_archived_not_deleted():
    # Decayed memories still exist
    # Expected: exists with low relevance

# R24: Promotion Criteria
def test_promotion_after_3_deals():
    # Pattern in 3+ deals → promote
    # Expected: promotion triggered
```

## Evaluation Tests (`test_evaluation.py`)

```python
async def test_scenario_acme_runs():
    result = await harness.run_scenario(acme_scenario)
    assert result.precision >= 0.5 * TARGET_PRECISION

async def test_scenario_northwind_contamination():
    result = await harness.run_scenario(northwind_scenario)
    assert result.contamination_rejection == 1.0

async def test_ablation_full_vs_no_guard():
    full = await harness.run_ablation("full")
    no_guard = await harness.run_ablation("no_guard")
    assert full.precision > no_guard.precision
```

## Fixtures

```python
# conftest.py
@pytest.fixture
def acme_scenario():
    with open("src/data/scenarios/acme.json") as f:
        return Scenario.parse_raw(f.read())

@pytest.fixture
def harness(agent_loop, hindsight):
    return EvaluationHarness(agent_loop, hindsight)
```

## Running Tests

```bash
# All unit tests
pytest tests/test_admission.py tests/test_consolidation.py tests/test_contamination.py \
       tests/test_provenance.py tests/test_scope.py tests/test_conflicts.py \
       tests/test_promotion.py -v

# Evaluation tests
pytest tests/test_evaluation.py -v

# Integration tests
pytest tests/test_integration.py -v

# With coverage
pytest tests/ --cov=src/memory --cov=src/harness --cov-report=term-missing
```

## CI Integration

```yaml
# .github/workflows/tests.yml
- name: Test Member 3 Evaluation
  run: |
    pytest tests/test_admission.py tests/test_consolidation.py tests/test_contamination.py \
           tests/test_provenance.py tests/test_scope.py tests/test_conflicts.py \
           tests/test_promotion.py tests/test_evaluation.py -v
    mypy src/data/ src/harness/ tests/
    ruff check src/data/ src/harness/ tests/
```

---

**Status: PLANNED** — Tests written alongside implementation.