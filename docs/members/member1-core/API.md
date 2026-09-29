# Member 1 - Internal API Reference

## Status: IMPLEMENTED & VERIFIED

## Public Interface

### MemoryGuard.verify()

```python
async def verify(
    candidate_memory: CandidateMemory,
    source_text: str,
    context: VerificationContext,
    scope: Scope
) -> MemoryDecision
```

**Parameters**:
- `candidate_memory`: Extracted memory from LLM
- `source_text`: Original conversation turn text
- `context`: Deal/rep context + existing memories
- `scope`: Target scope (determined by MemoryGuard)

**Returns**: `MemoryDecision` with all governance metadata

---

## Core Types (schema.py)

### CandidateMemory
```python
@dataclass
class CandidateMemory:
    text: str
    memory_type: MemoryType
    confidence: float
    source_span: Optional[Tuple[int, int]] = None
    extraction_metadata: Dict[str, Any] = field(default_factory=dict)
```

### VerificationContext
```python
@dataclass
class VerificationContext:
    deal_id: str
    rep_id: str
    conversation_id: str
    turn_id: int
    existing_memories: List[Memory] = field(default_factory=list)
    deal_stage: DealStage = DealStage.DISCOVERY
    customer_name: str = ""
```

### Scope / ScopeInfo
```python
class Scope(Enum):
    PROJECT = "project"
    COMMON = "common"

@dataclass
class ScopeInfo:
    scope: Scope
    bank_id: str
    deal_id: Optional[str] = None
    rep_id: Optional[str] = None
```

### MemoryDecision
```python
@dataclass
class MemoryDecision:
    decision: DecisionType
    memory_text: str
    reason: str
    confidence: float
    scope: Scope
    source_evidence: List[SourceEvidence]
    provenance: Provenance
    similar_memories: List[MemoryRef] = field(default_factory=list)
    conflicts: List[ConflictInfo] = field(default_factory=list)
    audit_id: str
    merge_instruction: Optional[MergeInstruction] = None
```

### DecisionType
```python
class DecisionType(Enum):
    RETAIN = "retain"
    UPDATE = "update"
    MERGE = "merge"
    REJECT = "reject"
    NEEDS_REVIEW = "needs_review"
```

### SourceEvidence
```python
@dataclass
class SourceEvidence:
    quote: str
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
    extraction_method: str
    verifier_model: str
    verification_timestamp: datetime
    decision_chain: List[DecisionStep]
```

### MergeInstruction
```python
@dataclass
class MergeInstruction:
    target_memory_id: str
    merge_strategy: MergeStrategy
    preserve_provenance: bool = True
    new_frequency: int
    new_evidence_count: int
    new_first_seen: datetime
    new_last_seen: datetime
```

### ConflictInfo
```python
@dataclass
class ConflictInfo:
    conflicting_memory_id: str
    conflict_type: ConflictType  # CONTRADICTION, STALE, STAKEHOLDER_DIFFERENCE
    resolution: Optional[ConflictResolution] = None
```

### MemoryRef
```python
@dataclass
class MemoryRef:
    memory_id: str
    similarity_score: float
    reason: str
```

---

## Rule Engine API

### RulesEngine
```python
class RulesEngine:
    def register(self, rule: Rule) -> None
    async def evaluate_all(
        self,
        candidate: CandidateMemory,
        source: str,
        context: VerificationContext,
        existing: List[Memory]
    ) -> List[RuleResult]
```

### Rule (Protocol)
```python
class Rule(Protocol):
    rule_id: str
    rule_name: str
    category: RuleCategory
    
    async def evaluate(
        self,
        candidate: CandidateMemory,
        source: str,
        context: VerificationContext,
        existing: List[Memory]
    ) -> RuleResult
```

### RuleResult
```python
@dataclass
class RuleResult:
    rule_id: str
    rule_name: str
    passed: bool
    reason: str
    metadata: Dict[str, Any] = field(default_factory=dict)
```

### RuleCategory
```python
class RuleCategory(Enum):
    ADMISSION = "admission"
    RELIABILITY = "reliability"
    RELEVANCE = "relevance"
    CONTAMINATION = "contamination"
    CONSOLIDATION = "consolidation"
    CONFLICT = "conflict"
    SCOPE = "scope"
    LIFECYCLE = "lifecycle"
    SECURITY = "security"
```

---

## Module APIs

### Admission (`admission.py`)
```python
class AdmissionPolicy:
    def assess_utility(self, candidate: CandidateMemory, context: VerificationContext) -> RuleResult
    def check_deal_relevance(self, candidate: CandidateMemory, context: VerificationContext) -> RuleResult
    def assess_actionability(self, candidate: CandidateMemory, context: VerificationContext) -> RuleResult
```

### Consolidation (`consolidation.py`)
```python
class ConsolidationEngine:
    def __init__(self, similarity_threshold: float = 0.85)
    async def find_similar(self, candidate: CandidateMemory, existing: List[Memory]) -> Optional[Memory]
    def build_merge_instruction(self, candidate: CandidateMemory, target: Memory) -> MergeInstruction
    def update_frequency(self, memory: Memory) -> Memory
    def merge_provenance(self, target: Memory, candidate: CandidateMemory, source: str) -> Memory
```

### Contamination (`contamination.py`)
```python
class ContaminationDetector:
    def __init__(self, verifier: VerifierClient)
    async def check_grounding(self, candidate: CandidateMemory, source: str) -> RuleResult
    async def check_hallucination(self, candidate: CandidateMemory, source: str) -> RuleResult
```

### Provenance (`provenance.py`)
```python
class ProvenanceBuilder:
    def build(
        self,
        candidate: CandidateMemory,
        source: str,
        context: VerificationContext,
        rule_results: List[RuleResult],
        decision: DecisionType
    ) -> Provenance
```

### Conflicts (`conflicts.py`)
```python
class ConflictDetector:
    async def detect_contradiction(self, candidate: CandidateMemory, existing: List[Memory]) -> List[ConflictInfo]
    def classify_change_type(self, old: Memory, new: CandidateMemory) -> ChangeType
    def resolve_temporal(self, old: Memory, new: CandidateMemory) -> ConflictResolution
```

### Scopes (`scopes.py`)
```python
class ScopeManager:
    def assign_scope(self, candidate: CandidateMemory, context: VerificationContext) -> Scope
    def validate_scope_assignment(self, candidate: CandidateMemory, scope: Scope, context: VerificationContext) -> RuleResult
    def enforce_isolation(self, bank_id: str, expected_scope: Scope) -> bool
```

### Promotion (`promotion.py`)
```python
class PromotionPolicy:
    def evaluate_promotion(self, memory: Memory, context: VerificationContext) -> PromotionDecision
    def check_promotion_criteria(self, memory: Memory) -> bool
```

---

## Verifier Client Protocol

```python
class VerifierClient(Protocol):
    async def verify(self, prompt: str) -> VerificationResponse
    
    async def check_support(
        self,
        candidate: CandidateMemory,
        source: str
    ) -> VerificationResponse
```

### VerificationResponse
```python
@dataclass
class VerificationResponse:
    supported: Literal["SUPPORTED", "PARTIALLY_SUPPORTED", "NOT_SUPPORTED"]
    reason: str
    confidence: float
```

---

## Error Types

```python
class MemoryGuardError(Exception): pass
class VerificationError(MemoryGuardError): pass
class VerifierUnavailableError(VerificationError): pass
class InvalidDecisionError(MemoryGuardError): pass
class SchemaValidationError(MemoryGuardError): pass
```

---

**Status: PLANNED** — Stable after Day 1 EOD.