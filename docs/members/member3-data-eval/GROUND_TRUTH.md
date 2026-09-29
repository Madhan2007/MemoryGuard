# Member 3 - Ground Truth Guide

## Status: IMPLEMENTED & VERIFIED

## Purpose

Define how ground truth annotations are created and validated for each scenario.

## Annotation Principles

1. **Explicit over inferred** — Only annotate what customer explicitly said
2. **One memory per semantic concept** — Consolidate at annotation level
3. **Exact quotes** — Preserve verbatim source text
4. **Scope assignment** — Project vs common at annotation time
5. **Decision labels** — RETAIN, MERGE, REJECT, UPDATE, NEEDS_REVIEW

## Annotation Format

```json
{
  "turn_id": 5,
  "source_text": "Please send updates through email.",
  "annotations": [
    {
      "memory_text": "Customer prefers email communication",
      "memory_type": "preference",
      "scope": "project",
      "decision": "MERGE",
      "target_memory_id": "mem-001",
      "reason": "Semantic duplicate of turn 1 preference",
      "evidence_quote": "Please send updates through email."
    }
  ]
}
```

## Memory Types

| Type | Description | Examples |
|------|-------------|----------|
| `preference` | Communication, process preferences | "prefer email", "weekly calls" |
| `requirement` | Functional/technical needs | "need SOC2", "API integration" |
| `objection` | Concerns, blockers | "price too high", "missing SSO" |
| `competitor` | Competitor mentions | "evaluating Gong", "prefer Chorus" |
| `stakeholder` | People, roles | "CTO is champion", "procurement blocks" |
| `pricing` | Budget, pricing constraints | "budget $50K", "quarterly billing" |
| `compliance` | Regulatory requirements | "GDPR required", "HIPAA" |
| `technical` | Technical specifications | "needs REST API", "on-prem only" |
| `decision` | Explicit decisions made | "chose us", "rejected competitor" |
| `pattern` | Rep behavioral patterns | "sends summaries", "asks timeline" |

## Decision Labels

| Label | When to Use |
|-------|-------------|
| `RETAIN` | First occurrence of a memory |
| `MERGE` | Semantic duplicate of existing memory |
| `UPDATE` | Explicit change/contradiction of existing |
| `REJECT` | Not useful, contaminated, out of scope |
| `NEEDS_REVIEW` | Ambiguous, low confidence |

## Scope Rules

| Scope | Criteria |
|-------|----------|
| `project` | Deal-specific: requirements, competitors, stakeholders, deal-stage info |
| `common` | Rep-specific: communication style, personal patterns, cross-deal learnings |

## Contamination Annotation

For injected hallucinations:
```json
{
  "turn_id": 4,
  "source_text": "We are evaluating SOC2 compliance.",
  "injected_candidate": "SOC2 is mandatory before purchase.",
  "annotation": {
    "decision": "REJECT",
    "reason": "Candidate asserts mandate; source only states evaluation",
    "contamination_type": "HALLUCINATION"
  }
}
```

## Conflict Annotation

```json
{
  "turn_id": 8,
  "source_text": "Actually, SOC2 is now required due to new policy.",
  "annotations": [
    {
      "memory_text": "SOC2 is now required due to new policy",
      "decision": "UPDATE",
      "conflicts_with": "mem-soc2-not-required",
      "conflict_type": "CONTRADICTION",
      "resolution": "TEMPORAL_OVERRIDE",
      "change_note": "Explicit customer change indicated by 'now required'"
    }
  ]
}
```

## Validation Checklist

Per scenario:
- [ ] Every turn annotated
- [ ] Every expected memory has exact source quote
- [ ] Scope assignments consistent
- [ ] Decision labels match rules
- [ ] Conflicts bidirectional (both memories reference each other)
- [ ] Merged memories have all source quotes
- [ ] Rejected candidates have contamination reason
- [ ] No orphan memories (every memory traced to turn)

## Inter-Annotator Agreement (Future)

- Two annotators per scenario
- Cohen's kappa > 0.8 target
- Disagreements resolved by third reviewer

---

**Status: PLANNED** — Applied to all 5 scenarios.