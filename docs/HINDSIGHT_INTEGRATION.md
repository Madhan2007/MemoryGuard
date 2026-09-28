# Hindsight Integration

## Status: PLANNED

## Why Hindsight is Mandatory

**Hackathon requirement**: "MANDATORY TECHNOLOGY: Hindsight"

Hindsight is the persistent memory backbone. Memory is stored and recalled across interactions. Hindsight supports project/common memory separation according to the existing architecture. MemoryGuard sits above the memory layer as policy/governance. Outcome memories can also be retained when properly supported.

## What Hindsight Does

| Capability | Description |
|------------|-------------|
| **Retain** | Store memories with metadata |
| **Recall** | Semantic retrieval (vector + keyword) |
| **Fact Extraction** | LLM-powered fact extraction from conversations |
| **Deduplication** | Built-in semantic deduplication |
| **Consolidation** | Automatic merging of similar memories |
| **Metadata** | Rich metadata support (custom fields) |
| **Memory Banks** | Multiple isolated memory namespaces |
| **Management** | Update, delete, list, export |

## What MemoryGuard Does

| Capability | Description |
|------------|-------------|
| **Admission Control** | Decide if memory should enter persistent storage |
| **Contamination Detection** | Verify memory grounded in source (hero feature) |
| **Merge Policy** | Policy-level consolidation decisions (not execution) |
| **Provenance** | Full audit trail from source to decision |
| **Conflict Handling** | Detect and manage contradictory memories |
| **Scope Management** | Project vs common bank assignment |
| **Promotion Policy** | Cross-scope memory promotion rules |
| **Lifecycle** | Decay, recency, archive policies |

## Critical Distinction

> **MemoryGuard does NOT replace Hindsight.**
>
> Hindsight already provides deduplication/consolidation. MemoryGuard's MERGE decision is a **policy-level consolidation decision** that tells Hindsight *what* to merge and *why*, with full provenance preservation. MemoryGuard adds an explicit governance layer for evidence-grounded memory decisions.

> Hindsight does NOT perform the MemoryGuard governance logic. MemoryGuard sits above Hindsight as the policy and verification layer.

## Memory Bank Strategy

### Two Persistent Banks (Hindsight)

```
┌─────────────────────────────────────────────────────────────┐
│  HINDSIGHT                                                    │
│  ┌─────────────────────────┐  ┌─────────────────────────┐   │
│  │ PROJECT MEMORY BANK     │  │ COMMON/USER MEMORY BANK │   │
│  │ memoryguard-project-    │  │ memoryguard-common-     │   │
│  │ {deal_id}               │  │ {rep_id}                │   │
│  └─────────────────────────┘  └─────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Bank Creation

```python
# Project bank (per deal)
project_bank = f"memoryguard-project-{deal_id}"
await hindsight.create_bank(project_bank)

# Common bank (per rep)
common_bank = f"memoryguard-common-{rep_id}"
await hindsight.create_bank(common_bank)
```

## Retain Flow

```
MemoryGuard Decision (MERGE)
        │
        ▼
┌───────────────────────┐
│ MemoryGuard builds    │
│ MergeInstruction      │
│  - target_memory_id   │
│  - merge_strategy     │
│  - new_frequency      │
│  - new_evidence_count │
│  - provenance         │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Hindsight Client      │
│ retain()              │
│  - bank_id            │
│  - memory_text        │
│  - metadata           │
│  - merge_policy       │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Hindsight executes    │
│ physical merge        │
│ (vector update,       │
│  metadata merge)      │
└───────────────────────┘
```

### Retain Parameters

```python
await hindsight_client.retain(
    bank_id="memoryguard-project-acme",
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
        "turn_id": 5,
        "source_quote": "I still prefer email for updates",
        "provenance": {...},
        "conflicts": [],
        "similar_memories": ["mem-001", "mem-002"],
        "audit_id": "audit-789"
    },
    merge_policy=MergePolicy(
        target_id="mem-001",
        strategy="APPEND_PROVENANCE"
    )
)
```

## Recall Flow

```
Agent Query
    │
    ▼
┌───────────────────────┐
│ Hindsight Client      │
│ recall() x2           │
│  - project bank       │
│  - common bank        │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Merge & Rank          │
│  - Deduplicate        │
│  - Re-rank by         │
│    relevance, recency,│
│    frequency          │
└───────────┬───────────┘
            │
            ▼
      Context for LLM
```

### Recall Parameters

```python
project_results = await hindsight_client.recall(
    bank_id="memoryguard-project-acme",
    query="communication preference",
    top_k=10,
    filters={"memory_type": "preference"},
    min_score=0.3
)

common_results = await hindsight_client.recall(
    bank_id="memoryguard-common-rep-001",
    query="communication preference",
    top_k=10,
    filters={"memory_type": "preference"},
    min_score=0.3
)
```

## Metadata Mapping

### MemoryGuard → Hindsight Metadata

| MemoryGuard Field | Hindsight Field | Notes |
|-------------------|-----------------|-------|
| `memory_type` | `metadata.memory_type` | Enum string |
| `scope` | `metadata.scope` | "project" or "common" |
| `decision` | `metadata.decision` | DecisionType value |
| `confidence` | `metadata.confidence` | Float 0-1 |
| `frequency` | `metadata.frequency` | Int |
| `evidence_count` | `metadata.evidence_count` | Int |
| `first_seen` | `metadata.first_seen` | ISO datetime |
| `last_seen` | `metadata.last_seen` | ISO datetime |
| `source_type` | `metadata.source_type` | Enum string |
| `source_id` | `metadata.source_id` | String |
| `conversation_id` | `metadata.conversation_id` | UUID string |
| `turn_id` | `metadata.turn_id` | Int |
| `source_quote` | `metadata.source_quote` | String (primary) |
| `provenance` | `metadata.provenance` | JSON object |
| `conflicts` | `metadata.conflicts` | Array of memory IDs |
| `similar_memories` | `metadata.similar_memories` | Array of memory IDs |
| `audit_id` | `metadata.audit_id` | UUID string |

### Hindsight-Managed (Not Set by MemoryGuard)

| Field | Description |
|-------|-------------|
| `created_at` | Set by Hindsight on first retain |
| `updated_at` | Updated by Hindsight on each retain |
| `embedding` | Computed by Hindsight |

## Scope Enforcement

### Write Path
- MemoryGuard **assigns scope** in decision
- Hindsight client writes to **correct bank only**
- Cross-scope writes **rejected** by MemoryGuard (R18)

### Read Path
- Agent queries **both banks** simultaneously
- Results **merged at query time**
- **No third persistent bank** created

## Deduplication Interaction

### Hindsight's Built-in Deduplication
- Semantic similarity detection
- Automatic merge on retain (if enabled)
- Vector-level consolidation

### MemoryGuard's Policy Layer
- **Decides** if merge appropriate (semantic + contextual)
- **Preserves all provenance** from both memories
- **Tracks frequency, evidence_count, timestamps**
- **Instructs Hindsight** via `merge_policy` parameter

### Division of Labor

| Task | Owner |
|------|-------|
| Vector similarity search | Hindsight |
| Semantic equivalence judgment | MemoryGuard (with verifier LLM) |
| Provenance preservation | MemoryGuard (policy) + Hindsight (execution) |
| Frequency/evidence tracking | MemoryGuard |
| Physical vector merge | Hindsight |

## Error Handling

| Scenario | Handling |
|----------|----------|
| Hindsight API timeout | Retry 3x with exponential backoff |
| Bank not found | Auto-create (idempotent) |
| Merge conflict (concurrent) | Retry with fresh recall |
| Metadata too large | Chunk provenance, store reference |
| Quota exceeded | Fallback to local cache, queue for sync |

## Configuration

```python
# Environment variables
HINDSIGHT_API_KEY=...
HINDSIGHT_BASE_URL=https://api.hindsight.example.com
HINDSIGHT_PROJECT_BANK=memoryguard-project-{deal_id}
HINDSIGHT_COMMON_BANK=memoryguard-common-{rep_id}

# Client config
class HindsightConfig:
    timeout: 30.0
    max_retries: 3
    retry_backoff: 2.0
    circuit_breaker_threshold: 5
```

---

## Outcome Memory Support

Outcome memories are persisted through Hindsight using the same bank strategy:
- **Project bank**: Deal-specific outcomes (e.g., "ROI explanation received positive response for Acme")
- **Common bank**: Rep-level outcome patterns (when promoted from 3+ deals)

Outcome memories are stored with the same metadata structure, with additional outcome fields:
- `outcome_type`: positive, negative, neutral, mixed
- `outcome_text`: What happened
- `outcome_evidence`: Source evidence supporting the outcome
- `outcome_timestamp`: When observed

> **Important**: Hindsight stores outcome memories as data. MemoryGuard validates that outcome claims are evidence-grounded before they are persisted.

---

**Status: PLANNED** — Implementation in `src/integrations/hindsight_client.py`.