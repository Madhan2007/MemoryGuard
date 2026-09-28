# Member 3 - Evaluation Design

## Status: PLANNED

## Evaluation Harness Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    EvaluationHarness                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  load_scenarios()                                               │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │           for scenario in scenarios:                    │   │
│  │              result = run_scenario(scenario)            │   │
│  │              results.append(result)                     │   │
│  │                                                         │   │
│  │  run_scenario():                                       │   │
│  │    agent = AgentLoop(...)                              │   │
│  │    for turn in scenario.turns:                         │   │
│  │       response = agent.process_turn(...)               │   │
│  │       record_decisions(response)                       │   │
│  │    final_memories = hindsight.recall_all()             │   │
│  │    return ScenarioResult                               │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│  compute_metrics(results)                                       │
│       │                                                         │
│       ▼                                                         │
│  generate_report()                                              │
│       │                                                         │
│       ▼                                                         │
│  save_artifacts()                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components

### Scenario Runner
```python
class EvaluationHarness:
    def __init__(self, agent_loop: AgentLoop, hindsight: HindsightClient):
        self.agent = agent_loop
        self.hindsight = hindsight
    
    async def run_scenario(self, scenario: Scenario) -> ScenarioResult:
        decisions = []
        for turn in scenario.turns:
            if turn.speaker == "customer":
                response = await self.agent.process_turn(
                    turn.text, scenario.deal_id, scenario.rep_id
                )
                decisions.extend(response.memory_decisions)
        
        # Inspect final memory state
        final_memories = await self._get_all_memories(scenario)
        
        return ScenarioResult(
            scenario_id=scenario.scenario_id,
            decisions=decisions,
            final_memories=final_memories,
            expected=scenario.ground_truth
        )
    
    async def run_all_scenarios(self) -> EvaluationReport:
        scenarios = self.load_scenarios()
        results = []
        for scenario in scenarios:
            result = await self.run_scenario(scenario)
            results.append(result)
        
        metrics = self.compute_metrics(results)
        return EvaluationReport(results=results, metrics=metrics)
```

## Metrics Computation

### 1. Memory Precision
```python
def compute_precision(result: ScenarioResult) -> float:
    """% of retained memories that match ground truth."""
    retained = [d for d in result.decisions if d.decision in [RETAIN, UPDATE, MERGE]]
    correct = sum(1 for d in retained if matches_ground_truth(d, result.expected))
    return correct / len(retained) if retained else 1.0
```

### 2. Retrieval Hit Rate
```python
def compute_hit_rate(result: ScenarioResult) -> float:
    """% of expected memories found in final state."""
    expected = result.expected.final_memories
    actual = result.final_memories
    matched = sum(1 for exp in expected if any(matches(exp, act) for act in actual))
    return matched / len(expected) if expected else 1.0
```

### 3. Consolidation/Merge Rate
```python
def compute_merge_rate(result: ScenarioResult) -> float:
    """% of semantic duplicates correctly merged."""
    duplicate_pairs = find_duplicate_pairs(result.expected)
    merged = sum(1 for pair in duplicate_pairs if was_merged(pair, result.decisions))
    return merged / len(duplicate_pairs) if duplicate_pairs else 1.0
```

### 4. Conflict Detection Rate
```python
def compute_conflict_detection(result: ScenarioResult) -> float:
    """% of explicit contradictions detected."""
    conflict_pairs = result.expected.conflicts
    detected = sum(1 for c in conflict_pairs if conflict_detected(c, result.decisions))
    return detected / len(conflict_pairs) if conflict_pairs else 1.0
```

### 5. Scope Isolation Rate
```python
def compute_scope_isolation(result: ScenarioResult) -> float:
    """% of project memories correctly isolated."""
    if not result.expected.isolation_tests:
        return 1.0
    passed = sum(1 for t in result.expected.isolation_tests if test_passed(t, result.final_memories))
    return passed / len(result.expected.isolation_tests)
```

### 6. Contamination Rejection Rate
```python
def compute_contamination_rejection(result: ScenarioResult) -> float:
    """% of hallucinated candidates rejected."""
    injected = result.expected.rejected_candidates
    rejected = sum(1 for c in injected if was_rejected(c, result.decisions))
    return rejected / len(injected) if injected else 1.0
```

### 7. Ablation Improvement
```python
def compute_ablation(baseline: Metrics, variant: Metrics) -> float:
    """% improvement over baseline."""
    return (variant.precision - baseline.precision) / baseline.precision * 100
```

## Ablation Configurations

| Config | Description |
|--------|-------------|
| `full` | All MemoryGuard features |
| `no_contamination` | Admission + merge only |
| `no_merge` | Admission + contamination only |
| `no_guard` | Raw Hindsight (no MemoryGuard) |
| `stateless` | No memory at all |

## Report Generation

```python
def generate_report(report: EvaluationReport) -> str:
    return f"""
# Evaluation Report - {datetime.now().strftime('%Y-%m-%d')}

## Summary
| Scenario | Precision | Hit Rate | Merge Rate | Contamination Rejection |
|----------|-----------|----------|------------|------------------------|
{rows}

## Ablation
| Config | Precision | Hit Rate | Merge Rate |
|--------|-----------|----------|------------|
{ablation_rows}

## Per-Scenario Details
{scenario_details}

## Charts
![Precision](charts/precision.png)
![Merge Rate](charts/merge_rate.png)
![Contamination](charts/contamination.png)
"""
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

## Regression Testing

```python
# In CI
def test_regression():
    report = run_evaluation()
    assert report.metrics.precision >= 0.5 * TARGET_PRECISION
    assert report.metrics.contamination_rejection >= 0.5 * TARGET_CONTAMINATION
    # Thresholds increase over time
```

---

**Status: PLANNED** — Implementation in `src/harness/eval_harness.py`.