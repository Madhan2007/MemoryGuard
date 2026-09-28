# Member 3 - Day 1 Tasks

## Status: PLANNED

## Goal

Foundation: Scenario data, ground truth, test skeletons.

---

## Task 1: ACME Scenario (`src/data/scenarios/acme.json`)

### Scenario: Communication Preference Consolidation
**Purpose**: Test MERGE/consolidation behavior

### Deliverables
- [ ] 10-15 turns of realistic conversation
- [ ] Customer repeats "prefer email" 3+ times with variations
- [ ] Ground truth: single consolidated memory with frequency=3, evidence_count=3
- [ ] Expected decisions per turn: RETAIN → MERGE → MERGE
- [ ] Source quotes preserved exactly

### Turn Structure
```json
{
  "turn_id": 1,
  "speaker": "customer",
  "text": "We prefer email for deal communication.",
  "expected_memories": [
    {"text": "Customer prefers email communication", "decision": "RETAIN", "scope": "project"}
  ]
}
```

---

## Task 2: GLOBEX Scenario (`src/data/scenarios/globex.json`)

### Scenario: Competitor Context Scope Isolation
**Purpose**: Test project memory isolation

### Deliverables
- [ ] Deal-specific competitor mentions (Gong, Chorus)
- [ ] Ground truth: memories only in `memoryguard-project-globex`
- [ ] Verification: zero leakage to other project banks
- [ ] Common bank unaffected

---

## Task 3: NORTHWIND Scenario (`src/data/scenarios/northwind.json`)

### Scenario: Contamination Detection (Hero Feature)
**Purpose**: Test REJECT of unsupported/hallucinated memory

### Deliverables
- [ ] Turn: "We are evaluating SOC2 compliance."
- [ ] Injected LLM candidate: "SOC2 is mandatory before purchase."
- [ ] Ground truth: REJECT with reason "Candidate memory not supported by source statement"
- [ ] Source quote: "We are evaluating SOC2 compliance."
- [ ] This is the CONTAMINATION HERO MOMENT

---

## Task 4: INITECH Scenario (`src/data/scenarios/initech.json`)

### Scenario: Conflict Resolution
**Purpose**: Test contradiction detection and temporal resolution

### Deliverables
- [ ] Turn 2: "SOC2 is not required for us right now."
- [ ] Turn 8: "Actually, SOC2 is now required due to new policy."
- [ ] Ground truth: CONFLICT detected, resolved to UPDATE with change note
- [ ] Both memories linked via `conflicts` field

---

## Task 5: UMBRELLA Scenario (`src/data/scenarios/umbrella.json`)

### Scenario: Freshness / Lifecycle
**Purpose**: Test decay, recency weighting, lifecycle

### Deliverables
- [ ] Turn 1 (Day 1): "I like getting SMS reminders."
- [ ] Turn 20 (Day 60): No SMS mention
- [ ] Turn 25 (Day 75): "Actually, just email is fine."
- [ ] Ground truth: Explicit change overrides; decay reduces old memory relevance

---

## Task 6: Test Skeletons

### Files
- [ ] `tests/test_admission.py` — R29-R31 tests
- [ ] `tests/test_consolidation.py` — R5-R9, R32-R33 tests
- [ ] `tests/test_contamination.py` — R1-R4, R34 tests
- [ ] `tests/test_provenance.py` — R2, R28 tests
- [ ] `tests/test_scope.py` — R15-R19 tests
- [ ] `tests/test_conflicts.py` — R10-R14 tests
- [ ] `tests/test_promotion.py` — R20-R24 tests
- [ ] `tests/test_integration.py` — End-to-end

### Pattern
```python
def test_unsupported_memory_is_rejected():
    """
    TODO:
    Give source text: "We are evaluating SOC2"
    Give candidate: "SOC2 is mandatory before purchase"
    Assert decision == REJECT
    Assert reason contains "not supported"
    """
    pass
```

---

## Task 7: Evaluation Harness Skeleton (`src/harness/eval_harness.py`)

### Deliverables
- [ ] `Scenario` dataclass loader
- [ ] `EvaluationHarness.run_scenario()` — runs turns through agent
- [ ] `EvaluationHarness.run_all_scenarios()` — batch execution
- [ ] `compute_metrics()` — precision, hit rate, merge rate, etc.
- [ ] Output: JSON report + markdown summary

---

## Dependencies on Other Members

| Need From | Artifact | Deadline |
|-----------|----------|----------|
| Member 1 | `MemoryDecision` schema | Day 1 Morning |
| Member 2 | `AgentLoop.process_turn()` | Day 2 Morning |
| Member 2 | `HindsightClient` for inspection | Day 2 Morning |

## Expected Commits

```
feat(data): add acme scenario with ground truth
feat(data): add globex scenario with ground truth
feat(data): add northwind scenario with ground truth
feat(data): add initech scenario with ground truth
feat(data): add umbrella scenario with ground truth
test(memory): add admission test skeletons
test(memory): add consolidation test skeletons
test(memory): add contamination test skeletons
feat(eval): add evaluation harness skeleton
```

## Handoff Requirements

**To Member 1 (Core)**:
- Failing test cases for each rule
- Expected decision format for scenarios

**To Member 2 (Backend)**:
- Scenario runner interface needs
- Direct memory inspection API needs

**To Member 4 (UI)**:
- Scenario data for demo scripting
- Expected hero moments for visualization

---

**Status: PLANNED** — Start Day 1 Morning.