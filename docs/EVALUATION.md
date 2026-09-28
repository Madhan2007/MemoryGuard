# Evaluation Framework

## Status: PLANNED

## Overview

Member 3 owns evaluation across 5 business scenarios with defined metrics.

## Five Business Scenarios

### 1. ACME — Communication Preference Consolidation (MERGE)

**Scenario**: Repeated communication preference across conversations.
```
Turn 1: "I prefer email."
Turn 5: "Please send updates through email."
Turn 12: "Email is best for me."
```

**Purpose**: Test MERGE/consolidation behavior
**Expected**:
- Turn 1: RETAIN (frequency=1)
- Turn 5: MERGE into existing (frequency=2, evidence_count=2)
- Turn 12: MERGE (frequency=3, evidence_count=3)
- Final memory: "Customer prefers email communication"

**Ground Truth**: Single consolidated memory with frequency=3, 3 quotes, correct timestamps

---

### 2. GLOBEX — Competitor Context Scope Isolation

**Scenario**: Competitor information belongs to one deal only.
```
Deal: Globex
Turn 3: "We're also evaluating Gong for conversation intelligence."
Turn 7: "Chorus is another option we're looking at."
```

**Purpose**: Test scope isolation (project memory)
**Expected**:
- Memories stored in `memoryguard-project-globex`
- Same memories NOT retrievable from `memoryguard-project-acme`
- Common bank unaffected

**Ground Truth**: Project-scoped memories only; zero leakage to other projects

---

### 3. NORTHWIND — Contamination Detection (Hero Feature)

**Scenario**: Customer evaluates SOC2; LLM hallucinates "mandatory".
```
Turn 4: "We are evaluating SOC2 compliance."
LLM Candidate: "SOC2 is mandatory before purchase."
```

**Purpose**: Test contamination detection (REJECT unsupported)
**Expected**:
- Source: "We are evaluating SOC2"
- Candidate: "SOC2 is mandatory before purchase"
- Decision: REJECT
- Reason: "Candidate memory not supported by source statement"

**Ground Truth**: REJECT with correct contamination reason

---

### 4. INITECH — Conflict Resolution

**Scenario**: Customer changes mind on requirement.
```
Turn 2: "SOC2 is not required for us right now."
Turn 8: "Actually, SOC2 is now required due to new policy."
```

**Purpose**: Test conflict detection and temporal resolution
**Expected**:
- Turn 2: RETAIN "SOC2 not required" (with timestamp)
- Turn 8: CONFLICT detected with mem-1
- Resolution: UPDATE to "SOC2 now required" with change note
- Both memories linked via `conflicts` field

**Ground Truth**: Conflict detected, resolved to latest explicit statement

---

### 5. UMBRELLA — Freshness / Lifecycle

**Scenario**: Old minor preference no longer recent.
```
Turn 1 (Day 1): "I like getting SMS reminders."
Turn 20 (Day 60): No mention of SMS.
Turn 25 (Day 75): "Actually, just email is fine."
```

**Purpose**: Test decay, recency weighting, lifecycle
**Expected**:
- Turn 1: RETAIN "Prefers SMS reminders" (frequency=1)
- Turn 25: CONFLICT with SMS preference
- Resolution: UPDATE to "Prefers email only" (explicit change)
- Old SMS memory: decayed relevance, flagged as superseded

**Ground Truth**: Explicit change overrides; decay reduces old memory relevance

---

## Evaluation Metrics

| Metric | Definition | Target | Measurement |
|--------|------------|--------|-------------|
| Memory Precision | % of retained memories that are correct/useful | TARGET: >85% | Human eval on retained set |
| Retrieval Hit Rate | % of relevant memories retrieved for query | TARGET: >90% | Query test set vs ground truth |
| Consolidation/Merge Rate | % of semantic duplicates correctly merged | TARGET: >70% | Duplicate pairs in scenarios |
| Conflict Detection Rate | % of explicit contradictions detected | TARGET: >95% | Conflict pairs in scenarios |
| Scope Isolation Rate | % of project memories correctly isolated | TARGET: 100% | Cross-project query tests |
| Promotion Accuracy | % of correct common/project promotions | TARGET: >80% | Promotion test cases |
| Contamination Rejection Rate | % of unsupported candidates rejected | TARGET: >90% | Hallucination injection tests |
| Ablation Improvement | % improvement vs no-MemoryGuard baseline | TARGET: >15% | A/B on agent response quality |
| Grounded Claim Count | % of retained memories with source quote | TARGET: 100% | Audit trail verification |

> **Important**: All metrics labeled **TARGET** until actually measured. Change to **MEASURED** only after evaluation runs.

## Evaluation Harness

### Structure

```python
# src/harness/eval_harness.py
class EvaluationHarness:
    async def run_scenario(self, scenario: Scenario) -> ScenarioResult:
        """Run single scenario through full agent loop."""
        
    async def run_all_scenarios(self) -> EvaluationReport:
        """Run all 5 scenarios, aggregate metrics."""
        
    def compute_metrics(self, results: List[ScenarioResult]) -> Metrics:
        """Calculate all metrics from results."""
```

### Test Case Structure

```python
@dataclass
class TestCase:
    scenario_id: str
    turn_inputs: List[str]
    expected_decisions: List[ExpectedDecision]
    expected_final_memories: List[ExpectedMemory]
    expected_rejections: List[ExpectedRejection]

@dataclass
class ExpectedDecision:
    turn_id: int
    candidate_text: str
    expected_decision: DecisionType
    expected_reason_contains: str
```

### Running Evaluation

```bash
# Run all scenarios
python scripts/run_evaluation.py

# Run specific scenario
python scripts/run_evaluation.py --scenario acme

# Generate report
python scripts/run_evaluation.py --output evaluation_results/
```

## Regression Testing

- Each scenario = regression test
- Run on every PR to `develop`
- Fail if any metric drops below threshold
- Thresholds start at 50% of TARGET, increase over time

## Ablation Study

Compare:
1. **Full MemoryGuard** (all features)
2. **No Contamination** (admission + merge only)
3. **No Merge** (admission + contamination only)
4. **No MemoryGuard** (raw Hindsight only)
5. **No Memory** (stateless agent)

Measure: Response quality (human eval), Memory Precision, User satisfaction proxy

## Results Reporting

```markdown
# Evaluation Report - 2026-09-28

## Summary
| Scenario | Precision | Hit Rate | Merge Rate | Contamination Rejection |
|----------|-----------|----------|------------|------------------------|
| ACME     | MEASURED  | MEASURED | MEASURED   | MEASURED               |
| GLOBEX   | MEASURED  | MEASURED | MEASURED   | MEASURED               |
| NORTHWIND| MEASURED  | MEASURED | MEASURED   | MEASURED               |
| INITECH  | MEASURED  | MEASURED | MEASURED   | MEASURED               |
| UMBRELLA | MEASURED  | MEASURED | MEASURED   | MEASURED               |

## Ablation
| Configuration | Response Quality | Memory Precision |
|---------------|------------------|------------------|
| Full          | MEASURED         | MEASURED         |
| No Contam.    | MEASURED         | MEASURED         |
| No Merge      | MEASURED         | MEASURED         |
| Raw Hindsight | MEASURED         | MEASURED         |
| Stateless     | MEASURED         | N/A              |

## Charts
- Precision by scenario
- Merge frequency over turns
- Contamination rejection examples
- Scope isolation verification
```

## Artifacts

```
evaluation_results/
├── 2026-09-28_14-30-00/
│   ├── report.md
│   ├── metrics.json
│   ├── scenario_acme.json
│   ├── scenario_globex.json
│   ├── scenario_northwind.json
│   ├── scenario_initech.json
│   ├── scenario_umbrella.json
│   ├── ablation.json
│   └── charts/
│       ├── precision.png
│       ├── merge_rate.png
│       └── contamination.png
```

---

**Status: PLANNED** — Implementation in `src/harness/eval_harness.py` and `src/data/scenarios/`.