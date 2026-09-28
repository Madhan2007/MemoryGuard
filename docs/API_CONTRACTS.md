# API Contracts

## Status: PLANNED

## Canonical Interface

### MemoryGuard.verify()

**Primary entry point for all memory governance decisions.**

```python
def verify(
    candidate_memory: CandidateMemory,
    source_text: str,
    context: VerificationContext,
    scope: Scope
) -> MemoryDecision:
    """
    Evaluate a candidate memory for admission to persistent storage.

    Args:
        candidate_memory: The memory proposed by the LLM
        source_text: Original source text (conversation turn, document, etc.)
        context: Current deal/rep context for relevance assessment
        scope: Target memory scope (project or common)

    Returns:
        MemoryDecision with decision, reasoning, and metadata
    """
```

---

## Data Structures

### CandidateMemory

```python
@dataclass
class CandidateMemory:
    text: str                           # Proposed memory text
    memory_type: MemoryType             # preference, requirement, objection, etc.
    confidence: float                   # LLM's self-assessed confidence (0.0-1.0)
    source_span: Optional[SourceSpan]   # Character offsets in source_text
    metadata: Dict[str, Any]            # Additional extraction metadata
```

### VerificationContext

```python
@dataclass
class VerificationContext:
    deal_id: str                        # Current deal identifier
    rep_id: str                         # Sales rep identifier
    conversation_id: str                # Conversation UUID
    turn_id: int                        # Turn number
    existing_memories: List[Memory]     # Relevant existing memories for consolidation/conflict
    deal_stage: DealStage               # discovery, demo, negotiation, close
    customer_name: str                  # Customer/account name
```

### Scope

```python
class Scope(Enum):
    PROJECT = "project"      # Deal-scoped, team-shared
    COMMON = "common"        # Rep-scoped, private

@dataclass
class ScopeInfo:
    scope: Scope
    bank_id: str             # Hindsight bank identifier
    deal_id: Optional[str]   # Required for PROJECT
    rep_id: Optional[str]    # Required for COMMON
```

### MemoryDecision

```python
@dataclass
class MemoryDecision:
    decision: DecisionType                # RETAIN, UPDATE, MERGE, REJECT, NEEDS_REVIEW
    memory_text: str                      # Final memory text (may be merged/updated)
    reason: str                           # Human-readable explanation
    confidence: float                     # Decision confidence (0.0-1.0)
    scope: Scope                          # Assigned scope
    source_evidence: List[SourceEvidence] # Supporting source quotes
    provenance: Provenance                # Full provenance chain
    similar_memories: List[MemoryRef]     # Memories considered for merge
    conflicts: List[ConflictInfo]         # Detected conflicts
    audit_id: str                         # Unique audit trail ID
    merge_instruction: Optional[MergeInstruction]  # For Hindsight
```

### DecisionType

```python
class DecisionType(Enum):
    RETAIN = "retain"           # New memory admitted as-is
    UPDATE = "update"           # Existing memory updated
    MERGE = "merge"             # Consolidated with similar memory
    REJECT = "reject"           # Not admitted
    NEEDS_REVIEW = "needs_review"  # Ambiguous, flag for human
```

### SourceEvidence

```python
@dataclass
class SourceEvidence:
    quote: str                          # Exact source quote
    conversation_id: str
    turn_id: int
    source_type: SourceType
    source_id: str
    timestamp: datetime
```

### Provenance

```python
@dataclass
class Provenance:
    source_conversation_id: str
    source_turn_ids: List[int]
    source_quotes: List[str]
    extraction_method: str              # "llm_extraction", "rule_based"
    verifier_model: str                 # Model used for verification
    verification_timestamp: datetime
    decision_chain: List[DecisionStep]  # Step-by-step decision log
```

### MergeInstruction

```python
@dataclass
class MergeInstruction:
    target_memory_id: str               # Existing memory to merge into
    merge_strategy: MergeStrategy       # APPEND, REPLACE, SYNTHESIZE
    preserve_provenance: bool = True    # Always true for MVP
    new_frequency: int
    new_evidence_count: int
    new_first_seen: datetime
    new_last_seen: datetime
```

---

## Hindsight Client Interface

### Recall

```python
async def recall(
    bank_id: str,
    query: str,
    top_k: int = 10,
    filters: Optional[Dict[str, Any]] = None,
    min_score: float = 0.0
) -> List[Memory]:
    """
    Semantic recall from Hindsight memory bank.
    """
```

### Retain

```python
async def retain(
    bank_id: str,
    memory: str,
    metadata: MemoryMetadata,
    merge_policy: Optional[MergePolicy] = None
) -> Memory:
    """
    Store or update memory in Hindsight.

    If merge_policy provided, Hindsight handles deduplication.
    MemoryGuard provides policy-level merge_instruction.
    """
```

### MemoryMetadata (Hindsight)

```python
@dataclass
class MemoryMetadata:
    # MemoryGuard fields
    memory_type: str
    scope: str
    decision: str
    confidence: float
    frequency: int
    evidence_count: int
    first_seen: datetime
    last_seen: datetime
    source_type: str
    source_id: str
    conversation_id: str
    turn_id: int
    source_quote: str
    provenance: Dict
    conflicts: List[str]
    similar_memories: List[str]
    audit_id: str

    # Hindsight fields (managed by Hindsight)
    created_at: datetime
    updated_at: datetime
```

---

## Agent Harness Interface

### AgentLoop

```python
class AgentLoop:
    async def process_turn(
        self,
        user_input: str,
        deal_id: str,
        rep_id: str
    ) -> AgentResponse:
        """
        Single conversation turn processing.
        """
```

### AgentResponse

```python
@dataclass
class AgentResponse:
    response_text: str
    candidate_memories: List[CandidateMemory]
    memory_decisions: List[MemoryDecision]
    recalled_memories: List[Memory]
```

---

## Configuration Interface

```python
class Config(BaseSettings):
    # LLM
    MAIN_MODEL: str = "openai/gpt-oss-20b"
    VERIFIER_MODEL: str = "openai/gpt-oss-120b"
    GROQ_API_KEY: str

    # Hindsight
    HINDSIGHT_API_KEY: str
    HINDSIGHT_BASE_URL: str
    HINDSIGHT_PROJECT_BANK: str
    HINDSIGHT_COMMON_BANK: str

    # Thresholds
    ADMISSION_CONFIDENCE_THRESHOLD: float = 0.7
    MERGE_SIMILARITY_THRESHOLD: float = 0.85
    CONTAMINATION_THRESHOLD: float = 0.8
    CONFIDENCE_THRESHOLD: float = 0.7

    class Config:
        env_file = ".env"
```

---

## Contract Rules

1. **Never change** `MemoryDecision` structure without version bump and all-member coordination
2. **Never change** `verify()` signature without updating all callers
3. **Scope** is determined by MemoryGuard, not caller
4. **Provenance** is mandatory for all non-REJECT decisions
5. **Audit ID** must be unique (UUID4)
6. **Confidence** must be 0.0-1.0
7. **Source evidence** must include exact quotes

---

**Status: PLANNED** — Implementation in `src/memory/schema.py` and `src/memory/memory_guard.py`.