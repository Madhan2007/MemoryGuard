# Solution Overview

## Status: PLANNED

## Core Concept

MemoryGuard is a Deal Intelligence Agent with:

1. **Persistent memory** through Hindsight
2. **MemoryGuard verification** — governance layer for memory admission
3. **Evidence/provenance** — full audit trail from source to decision
4. **Outcome memory** — records what happened after recommendations
5. **Learning from verified historical interactions** — future assistance improves

## Architecture Distinction

| Component | Role |
|-----------|------|
| **Hindsight** | Persistent memory, recall, storage, retrieval, and memory infrastructure |
| **MemoryGuard** | Governance, verification, and policy layer controlling which candidate memories are trusted and how they are handled |
| **Outcome Memory** | Evidence about whether an interaction, recommendation, or approach actually worked |
| **Learning** | Future recommendations become more informed by previously verified memories and outcomes |

## Memory vs Outcome vs Learning

| Concept | Definition | Example |
|---------|-----------|---------|
| **Memory** | What happened / what the customer said | "Customer prefers email communication" |
| **Outcome** | What happened after a recommendation or action | "ROI explanation received positive response" |
| **Learning** | Using verified historical context and outcomes in future assistance | Agent recalls positive ROI outcome when similar pricing objection arises |

## Flow

```
      SALES REPRESENTATIVE
              ↓
         DEAL AGENT
              ↓
      HINDSIGHT RECALL ← Persistent memory retrieval (project + common)
              ↓
      CONTEXT BUILDER  ← Relevant memories + outcomes injected
              ↓
         MAIN LLM     → Generates response
              ↓
        RESPONSE
              ↓
     CANDIDATE MEMORY  ← Memory candidates extracted from interaction
              ↓
       MEMORYGUARD     ← GOVERNANCE LAYER (core innovation)
     ┌────────┼────────┐
     ↓        ↓        ↓
  RETAIN    MERGE    REJECT
     ↓        ↓        ↓
     └────────┼────────┘
              ↓
         HINDSIGHT     ← Persist verified memories with metadata
              ↓
      PERSISTENT MEMORY
              ↓
       FUTURE RECALL
              ↓
   DEAL RECOMMENDATION ← Personalized, informed by verified history
              ↓
         OUTCOME       ← Record what happened
              ↓
      OUTCOME MEMORY   ← Candidate outcome → MemoryGuard → persist if supported
              ↓
      FUTURE LEARNING  ← Verified outcomes inform future assistance
```

## What MemoryGuard Adds

| Layer | Responsibility |
|-------|----------------|
| **Hindsight** | Persistent storage, semantic recall, deduplication, metadata |
| **MemoryGuard** | Admission control, contamination detection, merge policy, provenance, conflict resolution, scope management, outcome evidence validation |

## Key Principle

> **MemoryGuard does NOT replace Hindsight.** Hindsight provides memory capabilities (retain, recall, semantic search, deduplication). MemoryGuard provides **policy-level decisions** on what enters memory and how. MemoryGuard adds an explicit governance layer for evidence-grounded memory decisions.

## Verified Learning Loop

```
DEAL INTERACTION
        ↓
CANDIDATE MEMORY
        ↓
MEMORYGUARD VERIFICATION
        ↓
VERIFIED MEMORY
        ↓
HINDSIGHT
        ↓
FUTURE RECALL
        ↓
OUTCOME / FEEDBACK
        ↓
VERIFIED LEARNING
        ↓
BETTER FUTURE DEAL ASSISTANCE
```

1. Customer interaction happens
2. Agent generates a response/recommendation
3. Candidate memory is extracted
4. MemoryGuard evaluates the candidate
5. Supported memory is persisted through Hindsight
6. Later interaction recalls the memory
7. Agent uses the memory to make a recommendation
8. Outcome is recorded
9. Outcome becomes evidence for future recommendations
10. Future responses become more context-aware

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
| **REJECT** | Memory not admitted (not useful, contaminated, out of scope, unsupported causal claim) |
| **NEEDS_REVIEW** | Ambiguous case flagged for human review |

## Scope Strategy

Two persistent memory banks in Hindsight:
1. **Project Memory** — Deal-specific, team-shared (competitors, requirements, deal stage)
2. **Common/User Memory** — Rep-specific, personal (communication style, preferences)

**Combined Read View** — Agent queries both simultaneously for context building.

## Outcome Memory

Purpose: Record what happened after an important deal interaction or recommendation.

Example flow:
- **Customer objection**: "Your price is too high."
- **Agent approach**: "Use ROI justification."
- **Outcome**: "Customer responded positively."
- **Verified outcome memory**: "ROI-focused explanation received a positive response for this pricing objection."

> **Important**: The system must NOT automatically claim causality when the evidence does not support it. Outcome memory should distinguish what was observed from what the agent infers caused it.

---

**Status: PLANNED** — Architecture detailed in `ARCHITECTURE.md`.