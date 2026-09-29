from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime
from enum import Enum
import uuid


class DecisionType(str, Enum):
    RETAIN = "retain"
    UPDATE = "update"
    MERGE = "merge"
    REJECT = "reject"
    NEEDS_REVIEW = "needs_review"


class MemoryType(str, Enum):
    PREFERENCE = "preference"
    REQUIREMENT = "requirement"
    OBJECTION = "objection"
    COMPETITOR = "competitor"
    STAKEHOLDER = "stakeholder"
    PRICING = "pricing"
    COMPLIANCE = "compliance"
    TECHNICAL = "technical"
    DECISION = "decision"
    PATTERN = "pattern"
    OUTCOME = "outcome"
    OTHER = "other"


class Scope(str, Enum):
    PROJECT = "project"
    COMMON = "common"


class MergeStrategy(str, Enum):
    APPEND_PROVENANCE = "append_provenance"
    REPLACE = "replace"
    SYNTHESIZE = "synthesize"


class SupportState(str, Enum):
    SUPPORTED = "supported"
    PARTIALLY_SUPPORTED = "partially_supported"
    UNSUPPORTED = "unsupported"
    CONTRADICTED = "contradicted"


class SourceType(str, Enum):
    CONVERSATION = "conversation"
    DOCUMENT = "document"
    EMAIL = "email"
    CRM_NOTE = "crm_note"


class OutcomeType(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"


class SourceSpan(BaseModel):
    start: int
    end: int


class SourceEvidence(BaseModel):
    quote: str
    conversation_id: str
    turn_id: int
    source_type: SourceType = SourceType.CONVERSATION
    source_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class Provenance(BaseModel):
    source_conversation_id: str
    source_turn_ids: List[int]
    source_quotes: List[str]
    extraction_method: str = "llm_extraction"
    verifier_model: str
    verification_timestamp: datetime = Field(default_factory=datetime.utcnow)
    decision_chain: List[Dict[str, Any]] = Field(default_factory=list)


class MergeInstruction(BaseModel):
    target_memory_id: str
    merge_strategy: MergeStrategy = MergeStrategy.APPEND_PROVENANCE
    preserve_provenance: bool = True
    new_frequency: int
    new_evidence_count: int
    new_first_seen: datetime
    new_last_seen: datetime


class ConflictInfo(BaseModel):
    conflicting_memory_id: str
    conflict_type: str
    description: str
    resolution: Optional[str] = None


class MemoryRef(BaseModel):
    memory_id: str
    text: str
    similarity: float


class CandidateMemory(BaseModel):
    text: str
    memory_type: MemoryType
    confidence: float = Field(ge=0.0, le=1.0)
    source_span: Optional[SourceSpan] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class VerificationContext(BaseModel):
    deal_id: str
    rep_id: str
    conversation_id: str
    turn_id: int
    existing_memories: List[Dict[str, Any]] = Field(default_factory=list)
    deal_stage: str = "discovery"
    customer_name: str = ""


class ScopeInfo(BaseModel):
    scope: Scope
    bank_id: str
    deal_id: Optional[str] = None
    rep_id: Optional[str] = None


class MemoryDecision(BaseModel):
    decision: DecisionType
    memory_text: str
    reason: str
    confidence: float = Field(ge=0.0, le=1.0)
    scope: Scope
    source_evidence: List[SourceEvidence] = Field(default_factory=list)
    provenance: Optional[Provenance] = None
    similar_memories: List[MemoryRef] = Field(default_factory=list)
    conflicts: List[ConflictInfo] = Field(default_factory=list)
    audit_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    merge_instruction: Optional[MergeInstruction] = None
    verification_status: Optional[SupportState] = None


class TurnResult(BaseModel):
    answer: str
    retrieved_memories: List[Dict[str, Any]] = Field(default_factory=list)
    candidate_memories: List[CandidateMemory] = Field(default_factory=list)
    memory_decisions: List[MemoryDecision] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    outcome_candidates: List[Dict[str, Any]] = Field(default_factory=list)
    audit_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    latency_ms: int = 0