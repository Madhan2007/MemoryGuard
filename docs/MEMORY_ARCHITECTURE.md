# Memory Architecture

## Status: PLANNED

## Overview

MemoryGuard uses a **two-bank persistent memory strategy** with a **combined read view**.

> **Critical**: This is NOT three persistent databases. There are exactly two persistent memory banks in Hindsight. The combined read is a query-time merge.

## Bank 1: Project Memory

### Purpose
Deal-specific memory shared across the deal team.

### Scope
Single deal/customer engagement.

### Bank Identifier
```
HINDSIGHT_PROJECT_BANK=memoryguard-project-{deal_id}
```

### Contents
| Category | Examples |
|----------|----------|
| Requirements | "Needs SOC2 compliance", "Must integrate with Salesforce" |
| Objections | "Price too high", "Missing SSO feature" |
| Competitors | "Evaluating Gong", "Prefers Chorus" |
| Stakeholders | "CTO is champion", "Procurement blocks" |
| Pricing | "Budget $50K/year", "Quarterly billing required" |
| Compliance | "GDPR required", "Data residency EU" |
| Deal Stage | "Stage: Negotiation", "Close date: Q2" |

### Ownership
- **Write**: Any team member on the deal (via their agent)
- **Read**: All team members on the deal
- **Governance**: MemoryGuard evaluates all writes

### Lifecycle
- Created at deal initiation
- Active during deal (30-90 days)
- Archived after close (won/lost)
- Retention: 2 years for compliance

## Bank 2: Common/User Memory

### Purpose
Sales rep's personal preferences and cross-deal patterns.

### Scope
Individual sales representative.

### Bank Identifier
```
HINDSIGHT_COMMON_BANK=memoryguard-common-{rep_id}
```

### Contents
| Category | Examples |
|----------|----------|
| Communication Style | "Prefers email over calls", "Sends summary after each meeting" |
| Personal Patterns | "Always asks about implementation timeline", "Emphasizes ROI" |
| Cross-Deal Learnings | "Healthcare deals need HIPAA", "Enterprise needs SSO" |
| Tool Preferences | "Uses Notion for notes", "Shares slides via Google Drive" |

### Ownership
- **Write**: Only the rep's agent
- **Read**: Only the rep's agent
- **Governance**: MemoryGuard evaluates all writes

### Lifecycle
- Created at rep onboarding
- Persistent across deals
- Evolves with rep's career
- Portable if rep changes teams

## Combined Read View

### Purpose
Single query interface for the agent to retrieve relevant context.

### Implementation
```python
def combined_recall(query: str, deal_id: str, rep_id: str, top_k: int = 10):
    project_results = hindsight.recall(
        bank=f"memoryguard-project-{deal_id}",
        query=query,
        top_k=top_k
    )
    common_results = hindsight.recall(
        bank=f"memoryguard-common-{rep_id}",
        query=query,
        top_k=top_k
    )
    # Merge, deduplicate, re-rank
    return merge_and_rank(project_results, common_results, top_k)
```

### Ranking Factors
1. **Relevance** (semantic similarity to query)
2. **Recency** (more recent memories ranked higher)
3. **Frequency** (memories with higher evidence_count)
4. **Scope Priority** (project memories slightly preferred for deal-specific queries)
5. **Decision Confidence** (high-confidence memories preferred)

### Deduplication
- If same memory exists in both banks (rare), keep project version
- Merge based on content similarity > 0.9
- Preserve all provenance from both sources

## Memory Flow Summary

```
┌─────────────────────────────────────────────────────────────┐
│                     WRITE PATH                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Candidate Memory                                           │
│       │                                                     │
│       ▼                                                     │
│  MemoryGuard Decision                                       │
│       │                                                     │
│       ├─▶ RETAIN/UPDATE/MERGE → Project Bank (deal-scoped) │
│       │                                                     │
│       └─▶ RETAIN/UPDATE/MERGE → Common Bank (rep-scoped)   │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                     READ PATH                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Query (from Agent)                                         │
│       │                                                     │
│       ▼                                                     │
│  Recall from Project Bank  +  Recall from Common Bank      │
│       │                                                     │
│       └──────────▶ Merge & Rank ──────────────▶ Context    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Hindsight Integration Details

### Retain Operation
```python
hindsight.retain(
    bank="memoryguard-project-acme",
    memory="Customer prefers email communication",
    metadata={
        "memory_type": "preference",
        "scope": "project",
        "decision": "MERGE",
        "confidence": 0.92,
        "frequency": 3,
        "evidence_count": 3,
        "first_seen": "2026-01-15T10:00:00Z",
        "last_seen": "2026-02-20T14:30:00Z",
        "source_type": "conversation",
        "source_id": "conv-123",
        "conversation_id": "conv-123",
        "turn_id": "turn-5",
        "source_quote": "I still prefer email for updates",
        "provenance": {...},
        "audit_id": "audit-456"
    }
)
```

### Recall Operation
```python
results = hindsight.recall(
    bank="memoryguard-project-acme",
    query="communication preference",
    top_k=5,
    filters={"memory_type": "preference"}
)
```

### Metadata Fields (Hindsight + MemoryGuard)

| Field | Source | Description |
|-------|--------|-------------|
| `id` | Hindsight | Unique memory identifier |
| `text` | MemoryGuard | Consolidated memory text |
| `memory_type` | MemoryGuard | preference, requirement, objection, competitor, stakeholder, pricing, compliance, technical, decision, pattern |
| `scope` | MemoryGuard | project, common |
| `decision` | MemoryGuard | RETAIN, UPDATE, MERGE, REJECT, NEEDS_REVIEW |
| `confidence` | MemoryGuard | 0.0-1.0 verification confidence |
| `frequency` | MemoryGuard | Merge count + 1 |
| `evidence_count` | MemoryGuard | Number of source quotes |
| `first_seen` | MemoryGuard | ISO timestamp of first evidence |
| `last_seen` | MemoryGuard | ISO timestamp of latest evidence |
| `source_type` | MemoryGuard | conversation, document, email, crm_note |
| `source_id` | MemoryGuard | External reference ID |
| `conversation_id` | MemoryGuard | Conversation UUID |
| `turn_id` | MemoryGuard | Turn number within conversation |
| `source_quote` | MemoryGuard | Exact quote supporting memory |
| `provenance` | MemoryGuard | Full provenance chain (JSON) |
| `conflicts` | MemoryGuard | List of conflicting memory IDs |
| `similar_memories` | MemoryGuard | List of merged memory IDs |
| `audit_id` | MemoryGuard | Unique audit trail ID |
| `created_at` | Hindsight | Hindsight creation timestamp |
| `updated_at` | Hindsight | Hindsight last update timestamp |

## Scope Isolation Rules

1. **Project memories never leak to other deals** — Bank per deal
2. **Common memories never leak to other reps** — Bank per rep
3. **Cross-bank contamination prevented** — MemoryGuard validates scope on write
4. **Combined read is query-time only** — No persistent third bank

## Promotion Policy

Memories can be **promoted** from common → project (or vice versa) when:
- A personal pattern becomes deal-relevant (common → project)
- A deal-specific learning generalizes (project → common)

Promotion requires:
- Explicit MemoryGuard decision (PROMOTE)
- Provenance preserved from original bank
- New audit_id for promotion event

---

**Status: PLANNED** — See `src/memory/scopes.py` for implementation.