# Data Module

## Purpose

Business scenario data, fixtures, annotations, and ground truth for evaluation.

## Owner

**Member 3** — Data + Evaluation Engineer

## Structure

```
src/data/
├── scenarios/        # 5 business scenarios (JSON)
├── fixtures/         # Test fixtures
├── annotations/      # Human annotations
└── ground_truth/     # Ground truth for evaluation
```

## Scenarios

| Scenario | Focus | Hero Feature |
|----------|-------|--------------|
| ACME | Communication preference consolidation | MERGE |
| GLOBEX | Competitor context scope isolation | Scope isolation |
| NORTHWIND | Contamination detection | REJECT (hero) |
| INITECH | Conflict resolution | CONFLICT → UPDATE |
| UMBRELLA | Freshness / lifecycle | Decay |

---

**Status: PLANNED** — JSON files created with ground truth.