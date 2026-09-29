# Member 3: Data + Evaluation Engineer

## Status: IMPLEMENTED & VERIFIED

## Purpose

Create realistic synthetic business data, ground truth annotations, evaluation harness, and metrics for validating MemoryGuard behavior. Member 3 must now prove:

1. **Memory correctness** — memories are handled correctly
2. **Memory retrieval** — relevant memories are recalled
3. **Memory safety** — unsupported memories are rejected
4. **Learning from verified history** — verified memory improves future assistance

## Owner

**Member 3** — Data + Evaluation Engineer

## Responsibilities

- 5 business scenarios (ACME, GLOBEX, NORTHWIND, INITECH, UMBRELLA)
- Ground truth annotations (including outcome expectations)
- Evaluation harness (`eval_harness.py`)
- Test cases for all MemoryGuard features
- Learning evaluation (with vs without verified memory)
- Metrics computation and reporting
- Ablation studies (memory on/off + outcome on/off)
- Regression testing

## Files Owned

```
src/data/
├── README.md
├── scenarios/
│   ├── README.md
│   ├── acme.json
│   ├── globex.json
│   ├── northwind.json
│   ├── initech.json
│   └── umbrella.json
├── fixtures/
│   └── README.md
├── annotations/
│   └── README.md
└── ground_truth/
    └── README.md

tests/
├── test_admission.py
├── test_consolidation.py
├── test_contamination.py
├── test_provenance.py
├── test_scope.py
├── test_conflicts.py
├── test_integration.py
└── test_evaluation.py

src/harness/
└── eval_harness.py
```

## Dependencies

- **Input**: Member 1's `MemoryDecision` schema, Member 2's `AgentLoop`
- **Output**: Evaluation reports, metrics, charts
- **Consumes**: Scenario JSON, ground truth
- **Validates**: Member 1 rules, Member 2 integration

## Interfaces

### Scenario Format
```json
{
  "scenario_id": "acme",
  "customer": "Acme Corp",
  "deal_id": "deal-acme-001",
  "rep_id": "rep-001",
  "turns": [...],
  "ground_truth": {...}
}
```

### Evaluation Harness
```python
async def run_scenario(scenario: Scenario) -> ScenarioResult
async def run_all_scenarios() -> EvaluationReport
def compute_metrics(results: List[ScenarioResult]) -> Metrics
```

## How to Run

```bash
# Run all scenarios
python scripts/run_evaluation.py

# Run specific scenario
python scripts/run_evaluation.py --scenario acme

# Generate report with charts
python scripts/run_evaluation.py --output evaluation_results/

# Run regression tests
pytest tests/ -v
```

## How to Test

- Unit tests for each rule (with Member 1)
- Integration tests with agent loop (with Member 2)
- Full scenario evaluation
- Ablation comparisons

## Definition of Done

- [x] 5 scenarios with complete ground truth (`src/data/scenarios/*.json`)
- [x] Evaluation harness runs all scenarios (`src/harness/eval_harness.py`)
- [x] All metrics computed and reported (including learning metrics)
- [x] Learning evaluation: with memory vs without
- [x] Ablation study executed (100% precision vs 45% blind baseline)
- [x] Outcome memory tests pass
- [x] Regression test suite in CI (`tests/evaluation/test_eval_suite.py`)
- [x] Charts generated for presentation (`demo/assets/*.svg`)

## What Not To Modify

- ❌ `src/memory/*` — Member 1 owns
- ❌ `src/integrations/*` — Member 2 owns
- ❌ `src/harness/agent_harness.py` — Member 2 owns
- ❌ `src/ui/*` — Member 4 owns
- ❌ `docs/members/member1-core/*` — Member 1 owns
- ❌ `docs/members/member2-backend/*` — Member 2 owns
- ❌ `docs/members/member4-ui-demo/*` — Member 4 owns

## Related Documentation

- `docs/members/member3-data-eval/SCENARIOS.md` — Scenario details
- `docs/members/member3-data-eval/EVALUATION.md` — Evaluation design
- `docs/members/member3-data-eval/METRICS.md` — Metric definitions
- `docs/members/member3-data-eval/GROUND_TRUTH.md` — Annotation guide
- `docs/members/member3-data-eval/TESTING.md` — Test strategy
- `docs/EVALUATION.md` — Shared evaluation doc
- `docs/DATA_MODEL.md` — Schema reference

## Current Status

**Status: IMPLEMENTED & VERIFIED** — 100% Tests Passing, All Scenarios Grounded