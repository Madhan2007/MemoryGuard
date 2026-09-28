# Member 3 - Scenarios Specification

## Status: PLANNED

## Scenario Format

```json
{
  "scenario_id": "acme",
  "customer": "Acme Corp",
  "deal_id": "deal-acme-001",
  "rep_id": "rep-001",
  "turns": [
    {
      "turn_id": 1,
      "speaker": "customer",
      "text": "We prefer email for deal communication.",
      "expected_memories": [
        {
          "text": "Customer prefers email communication",
          "decision": "RETAIN",
          "scope": "project",
          "memory_type": "preference"
        }
      ]
    }
  ],
  "ground_truth": {
    "final_memories": [...],
    "rejected_candidates": [...],
    "conflicts": [...]
  }
}
```

---

## ACME — Communication Preference Consolidation

**Focus**: MERGE/consolidation behavior (Rules R5-R9, R32-R33)

### Conversation Flow
| Turn | Speaker | Text | Expected Decision |
|------|---------|------|-------------------|
| 1 | Customer | "We prefer email for deal communication." | RETAIN |
| 3 | Rep | "Noted, I'll use email for updates." | RETAIN (rep pattern → common) |
| 5 | Customer | "Please send updates through email." | MERGE (freq=2) |
| 8 | Customer | "Email is best for me, I don't check Slack often." | MERGE (freq=3) |
| 12 | Customer | "Just email, please." | MERGE (freq=4) |

### Ground Truth Final Memories
```json
{
  "final_memories": [
    {
      "text": "Customer prefers email communication",
      "memory_type": "preference",
      "scope": "project",
      "decision": "MERGE",
      "frequency": 4,
      "evidence_count": 4,
      "first_seen": "turn_1",
      "last_seen": "turn_12",
      "source_quotes": [
        "We prefer email for deal communication.",
        "Please send updates through email.",
        "Email is best for me, I don't check Slack often.",
        "Just email, please."
      ]
    },
    {
      "text": "Rep uses email for customer updates",
      "memory_type": "pattern",
      "scope": "common",
      "decision": "RETAIN",
      "frequency": 1,
      "evidence_count": 1
    }
  ]
}
```

### Hero Moment
Turn 5: "Please send updates through email." → MERGE with frequency=2
Turn 12: "Just email, please." → MERGE with frequency=4

---

## GLOBEX — Competitor Context Scope Isolation

**Focus**: Project memory isolation (Rules R15-R19)

### Conversation Flow
| Turn | Speaker | Text | Expected Decision |
|------|---------|------|-------------------|
| 1 | Customer | "We're evaluating Gong for conversation intelligence." | RETAIN (project) |
| 3 | Customer | "Chorus is another option we're looking at." | RETAIN (project) |
| 5 | Customer | "We've also demoed Wingman but it's too expensive." | RETAIN (project) |

### Ground Truth
```json
{
  "final_memories": [
    {"text": "Customer evaluating Gong", "scope": "project", "deal_id": "deal-globex-001"},
    {"text": "Customer evaluating Chorus", "scope": "project", "deal_id": "deal-globex-001"},
    {"text": "Customer demoed Wingman, too expensive", "scope": "project", "deal_id": "deal-globex-001"}
  ],
  "isolation_tests": [
    {"query": "Gong", "expected_bank": "memoryguard-project-globex", "not_in": "memoryguard-project-acme"},
    {"query": "competitor", "expected_count": 3, "scope": "project_only"}
  ]
}
```

### Verification
- Query "Gong" from Acme project bank → 0 results
- Query "competitor" from Globex project bank → 3 results
- Common bank → 0 competitor memories

---

## NORTHWIND — Contamination Detection

**Focus**: Contamination rejection (Rules R1-R4, R34) — **HERO FEATURE**

### Conversation Flow
| Turn | Speaker | Text | Injected Candidate | Expected Decision |
|------|---------|------|-------------------|-------------------|
| 4 | Customer | "We are evaluating SOC2 compliance." | "SOC2 is mandatory before purchase." | REJECT |

### Ground Truth
```json
{
  "rejected_candidates": [
    {
      "candidate_text": "SOC2 is mandatory before purchase",
      "source_text": "We are evaluating SOC2 compliance.",
      "expected_decision": "REJECT",
      "expected_reason_contains": "not supported",
      "contamination_type": "HALLUCINATION"
    }
  ],
  "final_memories": [
    {
      "text": "Customer evaluating SOC2 compliance",
      "memory_type": "compliance",
      "scope": "project",
      "decision": "RETAIN",
      "evidence_count": 1
    }
  ]
}
```

### Hero Moment Visualization
```
USER SOURCE: "We are evaluating SOC2 compliance."
CANDIDATE:   "SOC2 is mandatory before purchase."
MEMORYGUARD: REJECT
REASON:      "Candidate memory is not supported by the source statement."
```

---

## INITECH — Conflict Resolution

**Focus**: Contradiction detection and temporal resolution (Rules R10-R14)

### Conversation Flow
| Turn | Speaker | Text | Expected Decision |
|------|---------|------|-------------------|
| 2 | Customer | "SOC2 is not required for us right now." | RETAIN |
| 5 | Rep | "Understood, we'll focus on other requirements." | RETAIN (rep pattern) |
| 8 | Customer | "Actually, SOC2 is now required due to new policy." | CONFLICT → UPDATE |

### Ground Truth
```json
{
  "final_memories": [
    {
      "text": "SOC2 is now required due to new policy",
      "memory_type": "compliance",
      "scope": "project",
      "decision": "UPDATE",
      "conflicts": ["mem-soc2-not-required"],
      "change_note": "Explicit customer change: 'now required' overrides 'not required'"
    },
    {
      "text": "SOC2 was not required (superseded)",
      "memory_type": "compliance",
      "scope": "project",
      "decision": "RETAIN",
      "status": "superseded",
      "conflicts": ["mem-soc2-now-required"]
    }
  ],
  "conflicts": [
    {
      "memory_id": "mem-soc2-now-required",
      "conflicts_with": "mem-soc2-not-required",
      "conflict_type": "CONTRADICTION",
      "resolution": "TEMPORAL_OVERRIDE"
    }
  ]
}
```

---

## UMBRELLA — Freshness / Lifecycle

**Focus**: Decay, recency, lifecycle (Rules R20-R24)

### Conversation Flow
| Turn | Day | Speaker | Text | Expected Decision |
|------|-----|---------|------|-------------------|
| 1 | 1 | Customer | "I like getting SMS reminders for meetings." | RETAIN |
| 10 | 30 | Customer | "The project is going well." | (no memory) |
| 20 | 60 | Customer | "We're in final negotiations." | (no memory) |
| 25 | 75 | Customer | "Actually, just email is fine for reminders." | CONFLICT → UPDATE |

### Ground Truth
```json
{
  "final_memories": [
    {
      "text": "Customer prefers email for reminders",
      "memory_type": "preference",
      "scope": "project",
      "decision": "UPDATE",
      "conflicts": ["mem-sms-reminders"],
      "change_note": "Explicit change from SMS to email"
    },
    {
      "text": "Customer previously liked SMS reminders (superseded)",
      "memory_type": "preference",
      "scope": "project",
      "decision": "RETAIN",
      "status": "superseded",
      "decay_score": 0.15,
      "conflicts": ["mem-email-reminders"]
    }
  ],
  "lifecycle_tests": {
    "decay_applied": true,
    "old_memory_relevance": 0.15,
    "new_memory_relevance": 0.95
  }
}
```

---

## Cross-Scenario Tests

| Test | Description |
|------|-------------|
| Scope Isolation | ACME memories not in GLOBEX bank |
| Contamination | NORTHWIND rejection reason matches spec |
| Conflict | INITECH both memories preserved with link |
| Lifecycle | UMBRELLA decay score computed correctly |
| Merge Quality | ACME merged memory has all 4 quotes |

---

**Status: PLANNED** — Implementation in `src/data/scenarios/*.json`.