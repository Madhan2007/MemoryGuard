"""
MemoryGuard Consolidation Engine

Member 1 ownership.

Implements merge/consolidation logic (R5-R9, R32-R33).
"""

from dataclasses import dataclass
from typing import List, Optional
from .memory_guard import CandidateMemory, Memory, MemoryType, MergeInstruction, RuleResult, RuleCategory
from .rules import Rule, rule


@rule("R8", "Semantic Similarity Threshold", RuleCategory.CONSOLIDATION)
class SimilarityThresholdRule(Rule):
    """R8: Merge when semantic similarity exceeds threshold."""
    
    def __init__(self, threshold: float = 0.85):
        self.threshold = threshold
    
    async def evaluate(
        self,
        candidate: CandidateMemory,
        source: str,
        context: "VerificationContext",
        existing: List[Memory]
    ) -> RuleResult:
        similar = await self.find_similar(candidate, existing)
        if similar:
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                passed=True,
                reason=f"Similar memory found (similarity >= {self.threshold})",
                metadata={"target_memory_id": similar.id, "similarity": self.threshold}
            )
        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            passed=True,
            reason="No similar memory found",
            metadata={}
        )
    
    async def find_similar(
        self,
        candidate: CandidateMemory,
        existing: List[Memory]
    ) -> Optional[Memory]:
        """Find semantically similar memory in existing list."""
        # TODO: Implement semantic similarity (embedding-based or LLM-based)
        for mem in existing:
            if mem.memory_type != candidate.memory_type:
                continue
            # Placeholder: exact text match for now
            if mem.text.lower() == candidate.text.lower():
                return mem
        return None


class ConsolidationEngine:
    """Handles memory consolidation and merge operations."""
    
    SIMILARITY_THRESHOLD = 0.85
    
    def __init__(self, similarity_threshold: float = 0.85):
        self.threshold = similarity_threshold
    
    async def find_similar(
        self,
        candidate: CandidateMemory,
        existing: List[Memory]
    ) -> Optional[Memory]:
        """Find semantically similar existing memory."""
        # TODO: Implement with embeddings or LLM-based similarity
        for mem in existing:
            if mem.memory_type != candidate.memory_type:
                continue
            similarity = self._semantic_similarity(candidate.text, mem.text)
            if similarity >= self.threshold:
                return mem
        return None
    
    def _semantic_similarity(self, text1: str, text2: str) -> float:
        """Compute semantic similarity between two texts."""
        # TODO: Implement with embeddings
        # Placeholder: simple word overlap
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 or not words2:
            return 0.0
        intersection = words1 & words2
        union = words1 | words2
        return len(intersection) / len(union)
    
    def build_merge_instruction(
        self,
        candidate: CandidateMemory,
        target: Memory
    ) -> MergeInstruction:
        """Build merge instruction for Hindsight."""
        return MergeInstruction(
            target_memory_id=target.id,
            merge_strategy="SYNTHESIZE",
            new_frequency=target.frequency + 1,
            new_evidence_count=target.evidence_count + 1,
            new_first_seen=target.first_seen,
        )
    
    def update_frequency(self, memory: Memory) -> Memory:
        """Increment frequency counter."""
        memory.frequency += 1
        return memory
    
    def increment_evidence(self, memory: Memory) -> Memory:
        """Increment evidence count."""
        memory.evidence_count += 1
        return memory
    
    def update_timestamps(self, memory: Memory) -> Memory:
        """Update last_seen timestamp."""
        memory.last_seen = __import__("datetime").datetime.utcnow()
        return memory
    
    def merge_provenance(self, target: Memory, candidate: CandidateMemory, source: str) -> Memory:
        """Merge provenance chains preserving all source quotes."""
        # TODO: Implement provenance merging
        # Should preserve all source quotes from both memories
        return target
    
    def build_merge_reason(self, candidate: CandidateMemory, target: Memory) -> str:
        """R32: Build transparent merge reason."""
        return f"Semantic duplicate: both indicate {candidate.memory_type.value}"
    
    def update_with_audit(self, memory: Memory, candidate: CandidateMemory) -> Memory:
        """R33: Update with audit trail (no silent overwrites)."""
        # TODO: Implement audit trail creation
        return memory


__all__ = [
    "SimilarityThresholdRule",
    "ConsolidationEngine",
]