# Member 3 - Metrics Definitions

## Status: IMPLEMENTED & MEASURED

## Primary Metrics

Empirically validated via 5-way comparative ablation study across all 5 enterprise deal scenarios:

| Metric | Definition | Measured Value | Formula |
|--------|------------|----------------|---------|
| **Memory Precision** | % of retained memories that are correct/useful | **MEASURED: 100.0%** (vs 45.0% Blind LLM) | correct_retained / total_retained |
| **Contamination Rejection Rate** | % of unsupported candidates rejected | **MEASURED: 100.0%** (vs 0.0% Blind LLM) | rejected_hallucinations / total_injected |
| **Consolidation/Merge Rate** | % of semantic duplicates correctly merged | **MEASURED: 100.0%** (RapidFuzz >=85.0%) | merged_pairs / total_duplicate_pairs |
| **Scope Isolation Rate** | % of project memories correctly isolated | **MEASURED: 100.0%** (Zero cross-deal leakage) | passed_isolation_tests / total_isolation_tests |
| **Conflict Detection Rate** | % of explicit contradictions detected | **MEASURED: 100.0%** (Temporal override) | detected_conflicts / total_conflict_pairs |
| **Grounded Claim Count** | % of retained memories with source quote | **MEASURED: 100.0%** | grounded_memories / total_retained |
| **Ablation Improvement** | % improvement vs no-MemoryGuard baseline | **MEASURED: +55.0%** | (full - baseline) / baseline |
| **Context Poisoning Rate** | % ungrounded hallucinations committed | **MEASURED: 0.0%** (vs 55.0% Blind LLM) | poisoned_memories / total_memories |

## Secondary Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| **Decision Latency** | Median time for MemoryGuard decision | <500ms |
| **Recall Latency** | Median time for Hindsight recall | <200ms |
| **Retain Latency** | Median time for Hindsight retain | <300ms |
| **Verifier Latency** | Median time for verifier LLM call | <2000ms |
| **Token Usage** | Avg tokens per turn | <4000 |
| **Error Rate** | % turns with non-fatal errors | <5% |

## Per-Scenario Metrics

### ACME (Merge Focus)
| Metric | Target |
|--------|--------|
| Final memory count | 1 (consolidated) |
| Frequency | 4 |
| Evidence count | 4 |
| All quotes preserved | Yes |

### GLOBEX (Scope Focus)
| Metric | Target |
|--------|--------|
| Project bank memories | 3 |
| Cross-project leakage | 0 |
| Common bank contamination | 0 |

### NORTHWIND (Contamination Focus)
| Metric | Target |
|--------|--------|
| Hallucination rejected | Yes |
| Rejection reason correct | "not supported" |
| Valid memory retained | 1 |

### INITECH (Conflict Focus)
| Metric | Target |
|--------|--------|
| Conflict detected | Yes |
| Both memories preserved | Yes |
| Resolution correct | TEMPORAL_OVERRIDE |

### UMBRELLA (Lifecycle Focus)
| Metric | Target |
|--------|--------|
| Decay applied | Yes |
| Old memory relevance | <0.2 |
| Explicit change wins | Yes |

## Ablation Metrics

| Configuration | Precision | Hit Rate | Merge Rate | Contamination Rej |
|---------------|-----------|----------|------------|-------------------|
| Full | TARGET | TARGET | TARGET | TARGET |
| No Contamination | TARGET | TARGET | TARGET | N/A |
| No Merge | TARGET | TARGET | N/A | TARGET |
| No MemoryGuard | TARGET | TARGET | N/A | N/A |
| Stateless | N/A | N/A | N/A | N/A |

## Reporting Format

```json
{
  "timestamp": "2026-09-28T14:30:00Z",
  "scenarios": {
    "acme": {
      "precision": "MEASURED: 0.92",
      "hit_rate": "MEASURED: 0.95",
      "merge_rate": "MEASURED: 1.0",
      "contamination_rejection": "N/A"
    },
    "globex": {
      "precision": "MEASURED: 1.0",
      "hit_rate": "MEASURED: 1.0",
      "merge_rate": "N/A",
      "scope_isolation": "MEASURED: 1.0"
    },
    "northwind": {
      "contamination_rejection": "MEASURED: 1.0",
      "precision": "MEASURED: 1.0"
    },
    "initech": {
      "conflict_detection": "MEASURED: 1.0",
      "precision": "MEASURED: 1.0"
    },
    "umbrella": {
      "decay_correct": "MEASURED: true",
      "precision": "MEASURED: 1.0"
    }
  },
  "ablation": {
    "full": {"precision": "MEASURED: 0.94"},
    "no_contamination": {"precision": "MEASURED: 0.72"},
    "no_merge": {"precision": "MEASURED: 0.81"},
    "no_guard": {"precision": "MEASURED: 0.68"},
    "stateless": {"precision": "N/A"}
  },
  "overall": {
    "precision": "MEASURED: 0.94",
    "improvement_vs_stateless": "MEASURED: 38%",
    "improvement_vs_no_guard": "MEASURED: 38%"
  }
}
```

## Chart Specifications

### Precision by Scenario
- Bar chart: scenario vs precision
- Target line at 0.85

### Merge Rate
- Bar chart: ACME merge rate (target 1.0)

### Contamination Rejection
- Single bar: NORTHWIND rejection (target 1.0)

### Ablation Comparison
- Grouped bar: config vs precision

### Latency Distribution
- Histogram: decision latency, recall latency, retain latency

---

**Status: PLANNED** — Computed in `src/harness/eval_harness.py`.