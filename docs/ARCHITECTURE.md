# System Architecture

## Status: PLANNED

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER (Sales Rep)                               │
└─────────────────────────────────┬───────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AGENT HARNESS (Member 2)                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        AGENT LOOP                                    │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │ HINDSIGHT   │─▶│  CONTEXT    │─▶│  MAIN LLM   │─▶│ RESPONSE  │  │   │
│  │  │  RECALL     │  │  BUILDER    │  │  (Groq)     │  │  TO USER  │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  │        ▲                                                          │   │
│  │        │                                                          │   │
│  │  ┌─────┴─────┐  ┌─────────────┐  ┌─────────────┐                  │   │
│  │  │ CANDIDATE │─▶│ MEMORYGUARD │─▶│   DECISION  │                  │   │
│  │  │  MEMORY   │  │  (Member 1) │  │             │                  │   │
│  │  └───────────┘  └─────────────┘  └──────┬──────┘                  │   │
│  │                                          │                         │   │
│  └──────────────────────────────────────────┼─────────────────────────┘   │
│                                             │                             │
└─────────────────────────────────────────────┼─────────────────────────────┘
                                              │
                                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MEMORYGUARD CORE (Member 1)                         │
│  ┌──────────┐ ┌────────────┐ ┌─────────────┐ ┌──────────┐ ┌────────────┐  │
│  │ ADMISSION│ │CONSOLIDATION│ │CONTAMINATION│ │PROVENANCE│ │ CONFLICTS  │  │
│  └────┬─────┘ └─────┬──────┘ └──────┬──────┘ └────┬─────┘ └─────┬──────┘  │
│       │             │               │             │           │          │
│       └─────────────┼───────────────┼─────────────┼───────────┘          │
│                     ▼               ▼             ▼                      │
│            ┌──────────────────────────────────────────────────┐         │
│            │              DECISION ENGINE                      │         │
│            │  Input: candidate_memory, source_text, context    │         │
│            │  Output: MemoryDecision {decision, reason, ...}   │         │
│            └──────────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────────────────────┘
                                              │
                                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         HINDSIGHT INTEGRATION (Member 2)                    │
│  ┌────────────────────────┐  ┌────────────────────────────────────────┐   │
│  │  PROJECT MEMORY BANK   │  │       COMMON/USER MEMORY BANK          │   │
│  │  (Deal-scoped)         │  │       (Rep-scoped)                     │   │
│  │  HINDSIGHT_PROJECT_    │  │       HINDSIGHT_COMMON_                │   │
│  │  BANK=memoryguard-     │  │       BANK=memoryguard-                │   │
│  │  project-{deal_id}     │  │       common-{rep_id}                  │   │
│  └────────────────────────┘  └────────────────────────────────────────┘   │
│           │                                                         │       │
│           └─────────────────────┬─────────────────────────────────────┘       │
│                                 ▼                                             │
│                    ┌─────────────────────────┐                               │
│                    │    COMBINED READ VIEW   │  ← Agent queries both        │
│                    │  (project + common)     │                               │
│                    └─────────────────────────┘                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Component Ownership

| Component | Owner | Path |
|-----------|-------|------|
| Agent Harness / Loop | Member 2 | `src/harness/agent_harness.py` |
| Hindsight Client | Member 2 | `src/integrations/hindsight_client.py` |
| Groq/LLM Client | Member 2 | `src/integrations/groq_client.py` |
| Configuration | Member 2 | `src/integrations/config.py` |
| MemoryGuard Core | Member 1 | `src/memory/memory_guard.py` |
| Admission Policy | Member 1 | `src/memory/admission.py` |
| Consolidation/Merge | Member 1 | `src/memory/consolidation.py` |
| Contamination Detection | Member 1 | `src/memory/contamination.py` |
| Provenance | Member 1 | `src/memory/provenance.py` |
| Conflict Handling | Member 1 | `src/memory/conflicts.py` |
| Scope Management | Member 1 | `src/memory/scopes.py` |
| Promotion Policy | Member 1 | `src/memory/promotion.py` |
| Rules Engine | Member 1 | `src/memory/rules.py` |
| Schema/Decision Types | Member 1 | `src/memory/schema.py` |
| Evaluation Harness | Member 3 | `src/harness/eval_harness.py` |
| Test Scenarios | Member 3 | `src/data/scenarios/*.json` |
| Streamlit UI | Member 4 | `src/ui/main.py` |
| UI Components | Member 4 | `src/ui/components/*.py` |

## Data Flow Details

### 1. Recall Phase (Start of Turn)
```
Agent Harness
    │
    ├─▶ HindsightClient.recall(project_bank, query, top_k)
    ├─▶ HindsightClient.recall(common_bank, query, top_k)
    │
    ▼
Combine results → deduplicate by content → rank by relevance/recency
    │
    ▼
Context Builder → inject into system prompt
```

### 2. Generation Phase
```
Main LLM (MAIN_MODEL)
    │
    ├─▶ Response to user
    ├─▶ Candidate memories (structured extraction)
    │
    ▼
MemoryGuard.verify(candidate, source_text, context, scope)
```

### 3. Governance Phase (MemoryGuard)
```
MemoryGuard.verify()
    │
    ├─▶ Admission.check_usefulness(candidate, context)
    ├─▶ Contamination.check_grounding(candidate, source_text)
    ├─▶ Consolidation.find_similar(candidate, existing_memories)
    ├─▶ Conflicts.detect(candidate, existing_memories)
    ├─▶ Scopes.determine(candidate, context)
    ├─▶ Provenance.build(candidate, source_text, context)
    │
    ▼
Decision Engine → MemoryDecision
```

### 4. Persist Phase
```
if decision in [RETAIN, UPDATE, MERGE]:
    HindsightClient.retain(
        bank=scope.bank,
        memory=decision.memory_text,
        metadata=decision.provenance,
        merge_policy=decision.merge_instruction
    )
```

## Memory Bank Strategy

### Project Memory Bank
- **Scope**: Single deal/customer
- **Shared**: Team members on the deal
- **Contents**: Requirements, objections, competitors, stakeholders, deal stage, pricing
- **Lifecycle**: Deal duration + archive
- **Bank ID**: `memoryguard-project-{deal_id}`

### Common/User Memory Bank
- **Scope**: Individual sales rep
- **Private**: Not shared across reps
- **Contents**: Communication preferences, personal style, recurring patterns
- **Lifecycle**: Rep tenure
- **Bank ID**: `memoryguard-common-{rep_id}`

### Combined Read View
- Agent queries both banks simultaneously
- Results merged, deduplicated, ranked
- No third persistent bank created

## Configuration Flow

```
.env → Config (pydantic-settings) → Injected into all clients
     ├─▶ MAIN_MODEL, VERIFIER_MODEL
     ├─▶ HINDSIGHT_API_KEY, HINDSIGHT_BASE_URL
     ├─▶ HINDSIGHT_PROJECT_BANK, HINDSIGHT_COMMON_BANK
     └─▶ GROQ_API_KEY
```

## Error Handling Strategy

| Layer | Strategy |
|-------|----------|
| Hindsight Client | Retry with exponential backoff (3 attempts), circuit breaker |
| LLM Client | Retry with fallback model, structured output validation |
| MemoryGuard | Deterministic fallback rules if verifier fails |
| Agent Harness | Graceful degradation: proceed with empty context if recall fails |

## Observability

- Structured JSON logging (Member 2: `src/harness/logger.py`)
- Decision audit trail (Member 1: provenance)
- Evaluation metrics (Member 3: `src/harness/eval_harness.py`)
- UI decision panel (Member 4: `src/ui/components/decision_panel.py`)

---

**Status: PLANNED** — Implementation begins Day 1.