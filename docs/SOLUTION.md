# Solution Overview

## Status: PLANCED

## Core Concept

MemoryGuard sits between the **AI Agent** and **Persistent Memory (Hindsight)** as a governance layer.

## Flow

```
┌─────────────┐
│    USER     │  Sales rep interacts with customer
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    AGENT    │  Main LLM generates response + candidate memory
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  HINDSIGHT  │  Recall relevant memories (project + common)
│   RECALL    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   CONTEXT   │  Build prompt with retrieved memories
│   BUILDER   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  MAIN LLM   │  Generate response
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  CANDIDATE  │  Extract memory candidates from interaction
│  MEMORY     │
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌──────────────────────────────┐
│ MEMORYGUARD │────▶│        DECISION ENGINE       │
│  GOVERNANCE │     │  • Admission (useful?)       │
└──────┬──────┘     │  • Reliability (grounded?)   │
       │           │  • Relevance (deal-relevant?)│
       ▼           │  • Contamination (supported?)│
┌─────────────┐     │  • Conflict (contradicts?) │
│   DECISION  │     │  • Scope (project/common?) │
│             │     │  • Consolidation (merge?)  │
│ RETAIN      │     │  • Provenance (traceable?) │
│ UPDATE      │     └──────────────────────────────┘
│ MERGE       │
│ REJECT      │
│ NEEDS_REVIEW│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  HINDSIGHT  │  Persist verified memories with metadata
│  RETAIN/    │  • Project bank (deal-scoped)
│  MERGE      │  • Common bank (user-scoped)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  FUTURE     │  Next interaction: recall → context → personalized
│  RETRIEVAL  │
└─────────────┘
```

## What MemoryGuard Adds

| Layer | Responsibility |
|-------|----------------|
| **Hindsight** | Persistent storage, semantic recall, deduplication, metadata |
| **MemoryGuard** | Admission control, contamination detection, merge policy, provenance, conflict resolution, scope management |

## Key Principle

> **MemoryGuard does NOT replace Hindsight.** Hindsight provides memory capabilities (retain, recall, semantic search, deduplication). MemoryGuard provides **policy-level decisions** on what enters memory and how.

## MERGE as Policy Decision

When MemoryGuard decides **MERGE**:
- It determines the new memory corresponds to an existing memory
- It decides the merge is appropriate (semantic equivalence)
- It specifies what evidence supports the decision
- It defines how provenance should be preserved (all source quotes retained)
- Hindsight executes the physical merge; MemoryGuard authors the policy

## Decisions

| Decision | Meaning |
|----------|---------|
| **RETAIN** | New memory admitted as-is |
| **UPDATE** | Existing memory updated with new information |
| **MERGE** | Semantically similar memories consolidated |
| **REJECT** | Memory not admitted (not useful, contaminated, out of scope) |
| **NEEDS_REVIEW** | Ambiguous case flagged for human review |

## Scope Strategy

Two persistent memory banks in Hindsight:
1. **Project Memory** — Deal-specific, team-shared (competitors, requirements, deal stage)
2. **Common/User Memory** — Rep-specific, personal (communication style, preferences)

**Combined Read View** — Agent queries both simultaneously for context building.

---

**Status: PLANNED** — Architecture detailed in `ARCHITECTURE.md`.