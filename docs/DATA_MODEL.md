# Data Model

## Status: PLANNED

## Memory Record (Persisted in Hindsight)

### Required Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| `id` | string | Hindsight | Unique memory identifier (UUID) |
| `text` | string | MemoryGuard | Consolidated memory text |
| `memory_type` | enum | MemoryGuard | preference, requirement, objection, competitor, stakeholder, pricing, compliance, technical, decision, pattern |
| `scope` | enum | MemoryGuard | project, common |
| `decision` | enum | MemoryGuard | RETAIN, UPDATE, MERGE, REJECT, NEEDS_REVIEW |
| `confidence` | float | MemoryGuard | Decision confidence (0.0-1.0) |

### MemoryGuard Metadata (Required for Governance)

| Field | Type | Description |
|-------|------|-------------|
| `frequency` | int | Merge count + 1 (1 = first admission) |
| `evidence_count` | int | Number of distinct source quotes |
| `first_seen` | datetime | ISO timestamp of first supporting evidence |
| `last_seen` | datetime | ISO timestamp of latest supporting evidence |
| `source_type` | enum | conversation, document, email, crm_note |
| `source_id` | string | External reference (conversation ID, document ID) |
| `conversation_id` | string | Conversation UUID |
| `turn_id` | int | Turn number within conversation |
| `source_quote` | string | Exact quote from source (primary evidence) |
| `provenance` | JSON | Full provenance chain (see Provenance schema) |
| `conflicts` | array[string] | IDs of conflicting memories |
| `similar_memories` | array[string] | IDs of memories merged into this |
| `audit_id` | string | Unique audit trail ID (UUID) |

### Hindsight-Managed Fields

| Field | Type | Description |
|-------|------|-------------|
| `created_at` | datetime | Hindsight creation timestamp |
| `updated_at` | datetime | Hindsight last update timestamp |
| `embedding` | vector | Semantic embedding (managed by Hindsight) |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `tags` | array[string] | Compliance tags (SOC2, GDPR, etc.) |
| `stakeholder` | string | Associated stakeholder role |
| `deal_stage` | enum | Stage when memory created |
| `promotion_history` | array | Promotion events (common↔project) |
| `decay_score` | float | Current relevance after decay |

---

## Provenance Schema

```json
{
  "source_conversation_id": "conv-123",
  "source_turn_ids": [5, 12, 18],
  "source_quotes": [
    "We prefer email for deal communication",
    "I still prefer email for updates",
    "Please send everything via email"
  ],
  "extraction_method": "llm_extraction",
  "verifier_model": "openai/gpt-oss-120b",
  "verification_timestamp": "2026-02-20T14:30:00Z",
  "decision_chain": [
    {
      "step": "admission",
      "result": "PASS",
      "reason": "Actionable preference for deal communication"
    },
    {
      "step": "contamination",
      "result": "PASS",
      "reason": "All quotes directly support email preference"
    },
    {
      "step": "consolidation",
      "result": "MERGE",
      "target_memory_id": "mem-456",
      "reason": "Semantic duplicate: 3 quotes all indicate email preference"
    },
    {
      "step": "conflict_check",
      "result": "PASS",
      "reason": "No conflicting communication preferences"
    },
    {
      "step": "scope_assignment",
      "result": "PROJECT",
      "reason": "Deal-specific communication preference"
    }
  ]
}
```

---

## Decision Chain Steps

| Step | Purpose | Possible Results |
|------|---------|------------------|
| `admission` | Is memory useful? | PASS, FAIL (REJECT) |
| `reliability` | Is extraction reliable? | PASS, FAIL (NEEDS_REVIEW) |
| `relevance` | Deal-relevant? | PASS, FAIL (REJECT) |
| `contamination` | Grounded in source? | PASS, FAIL (REJECT) |
| `consolidation` | Similar to existing? | MERGE, NEW |
| `conflict_check` | Contradicts existing? | CONFLICT, PASS |
| `scope_assignment` | Project or common? | PROJECT, COMMON |
| `promotion_check` | Promote across scope? | PROMOTE, NO |

---

## Candidate Memory (Pre-Decision)

```python
@dataclass
class CandidateMemory:
    text: str
    memory_type: MemoryType
    confidence: float
    source_span: Optional[Tuple[int, int]]  # Char offsets in source
    extraction_metadata: Dict[str, Any]
```

---

## Verification Context

```python
@dataclass
class VerificationContext:
    deal_id: str
    rep_id: str
    conversation_id: str
    turn_id: int
    existing_memories: List[Memory]  # Retrieved for consolidation/conflict
    deal_stage: DealStage
    customer_name: str
```

---

## Evaluation Metrics (Member 3)

| Metric | Type | Target |
|--------|------|--------|
| Memory Precision | % | TARGET: >85% |
| Retrieval Hit Rate | % | TARGET: >90% |
| Consolidation/Merge Rate | % | TARGET: >70% of duplicates |
| Conflict Detection Rate | % | TARGET: >95% |
| Scope Isolation Rate | % | TARGET: 100% |
| Promotion Accuracy | % | TARGET: >80% |
| Contamination Rejection Rate | % | TARGET: >90% |
| Ablation Improvement | % | TARGET: >15% vs no-MemoryGuard |
| Grounded Claim Count | count | TARGET: 100% of retained |

> **Note**: All metrics labeled TARGET until measured.

---

## Scenario Data Schema (Member 3)

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
        {"text": "Customer prefers email communication", "decision": "RETAIN", "scope": "project"}
      ]
    },
    {
      "turn_id": 5,
      "speaker": "customer",
      "text": "I still prefer email for updates.",
      "expected_memories": [
        {"text": "Customer prefers email communication", "decision": "MERGE", "scope": "project", "target_memory_id": "mem-001"}
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

## Field Classification

| Category | Fields |
|----------|--------|
| **Required** | id, text, memory_type, scope, decision, confidence |
| **MemoryGuard Metadata** | frequency, evidence_count, first_seen, last_seen, source_type, source_id, conversation_id, turn_id, source_quote, provenance, conflicts, similar_memories, audit_id |
| **Calculated** | frequency, evidence_count, first_seen, last_seen, decay_score |
| **Provider (Hindsight)** | created_at, updated_at, embedding |
| **MemoryGuard Governance** | decision, confidence, provenance, conflicts, similar_memories, audit_id, scope, memory_type |

---

**Status: PLANNED** — Implementation in `src/memory/schema.py`.