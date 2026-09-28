"""
MemoryGuard Promotion Policy

Member 1 ownership.

Implements cross-scope promotion and lifecycle (R20-R24).
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from .memory_guard import Memory, Scope, RuleResult, RuleCategory
from .rules import Rule, rule


@rule("R20", "Recency Weighting", RuleCategory.LIFECYCLE)
class RecencyWeightingRule(Rule):
    """R20: Recent memories weighted higher in retrieval."""
    
    async def evaluate(
        self,
        candidate: "CandidateMemory",
        source: str,
        context: "VerificationContext",
        existing: List[Memory]
    ) -> RuleResult:
        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            passed=True,
            reason="Recency weighting applied at retrieval time",
            metadata={}
        )


@rule("R21", "Decay Function", RuleCategory.LIFECYCLE)
class DecayFunctionRule(Rule):
    """R21: Old, unreinforced memories decay in relevance."""
    
    def __init__(self, half_life_days: int = 90):
        self.half_life = half_life_days
    
    async def evaluate(
        self,
        candidate: "CandidateMemory",
        source: str,
        context: "VerificationContext",
        existing: List[Memory]
    ) -> RuleResult:
        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            passed=True,
            reason=f"Decay function configured (half-life: {self.half_life} days)",
            metadata={"half_life_days": self.half_life}
        )
    
    def apply_decay(self, memory: Memory) -> float:
        """Calculate decay score for a memory."""
        days_since = (datetime.utcnow() - memory.last_seen).days
        if days_since <= 0:
            return 1.0
        import math
        return math.exp(-days_since / self.half_life)


@rule("R22", "Minimum Evidence for Retention", RuleCategory.LIFECYCLE)
class MinimumEvidenceRule(Rule):
    """R22: Memories with single evidence decay faster."""
    
    async def evaluate(
        self,
        candidate: "CandidateMemory",
        source: str,
        context: "VerificationContext",
        existing: List[Memory]
    ) -> RuleResult:
        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            passed=True,
            reason="Evidence-based decay applied in retrieval ranking",
            metadata={}
        )
    
    def adjust_decay_by_evidence(self, memory: Memory, base_half_life: int = 90) -> int:
        """Adjust half-life based on evidence count and frequency."""
        if memory.evidence_count == 1 and memory.frequency == 1:
            return 30  # Faster decay for single evidence
        return base_half_life


@rule("R23", "Archive vs Delete", RuleCategory.LIFECYCLE)
class ArchiveNotDeleteRule(Rule):
    """R23: Memories never deleted; archived with decayed relevance."""
    
    async def evaluate(
        self,
        candidate: "CandidateMemory",
        source: str,
        context: "VerificationContext",
        existing: List[Memory]
    ) -> RuleResult:
        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            passed=True,
            reason="Archive policy: memories decay but never deleted",
            metadata={}
        )


@rule("R24", "Promotion Criteria", RuleCategory.LIFECYCLE)
class PromotionCriteriaRule(Rule):
    """R24: Common→Project promotion when pattern appears in 3+ deals."""
    
    def __init__(self, promotion_threshold: int = 3):
        self.threshold = promotion_threshold
    
    async def evaluate(
        self,
        candidate: "CandidateMemory",
        source: str,
        context: "VerificationContext",
        existing: List[Memory]
    ) -> RuleResult:
        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            passed=True,
            reason=f"Promotion criteria: {self.threshold}+ deals for common→project",
            metadata={"promotion_threshold": self.threshold}
        )


@dataclass
class PromotionDecision:
    """Decision about cross-scope promotion."""
    should_promote: bool
    from_scope: "Scope"
    to_scope: "Scope"
    reason: str
    trigger: str  # "deal_threshold", "explicit_request", "pattern_recognition"


class PromotionPolicy:
    """Manages cross-scope promotion policies."""
    
    def __init__(self, promotion_threshold: int = 3):
        self.threshold = promotion_threshold
        self.criteria_rule = PromotionCriteriaRule(promotion_threshold)
    
    def evaluate_promotion(
        self,
        memory: "Memory",
        context: "VerificationContext"
    ) -> PromotionDecision:
        """Evaluate if memory should be promoted across scopes."""
        # Common → Project: pattern appears in multiple deals
        if memory.scope == "common":
            deal_count = self._count_deal_occurrences(memory)
            if deal_count >= self.threshold:
                return PromotionDecision(
                    should_promote=True,
                    from_scope="common",
                    to_scope="project",
                    reason=f"Pattern observed in {deal_count} deals (threshold: {self.threshold})",
                    trigger="deal_threshold"
                )
        
        # Project → Common: deal-specific learning generalizes
        if memory.scope == "project":
            if self._is_generalizable_pattern(memory):
                return PromotionDecision(
                    should_promote=True,
                    from_scope="project",
                    to_scope="common",
                    reason="Deal-specific learning generalized to rep pattern",
                    trigger="pattern_recognition"
                )
        
        return PromotionDecision(
            should_promote=False,
            from_scope=memory.scope,
            to_scope=memory.scope,
            reason="Promotion criteria not met",
            trigger="none"
        )
    
    def _count_deal_occurrences(self, memory: "Memory") -> int:
        """Count how many deals this pattern appears in."""
        # TODO: Query Hindsight across project banks
        return 0
    
    def _is_generalizable_pattern(self, memory: "Memory") -> bool:
        """Check if deal-specific memory represents a generalizable pattern."""
        # TODO: Implement pattern recognition
        return False
    
    def apply_recency_weight(self, memories: List["Memory"]) -> List["Memory"]:
        """R20: Apply recency weighting to retrieval results."""
        # Sort by last_seen descending
        return sorted(memories, key=lambda m: m.last_seen, reverse=True)
    
    def apply_decay(self, memories: List["Memory"]) -> List["Memory"]:
        """R21-R22: Apply decay function and filter."""
        decay_rule = DecayFunctionRule()
        min_evidence_rule = MinimumEvidenceRule()
        
        scored = []
        for mem in memories:
            decay_score = decay_rule.apply_decay(mem)
            half_life = min_evidence_rule.adjust_decay_by_evidence(mem)
            # Adjust decay based on evidence
            if mem.evidence_count == 1 and mem.frequency == 1:
                decay_score *= 0.5  # Additional penalty
            
            if decay_score > 0.1:  # Minimum relevance threshold
                scored.append((mem, decay_score))
        
        # Sort by decay score descending
        scored.sort(key=lambda x: x[1], reverse=True)
        return [mem for mem, score in scored]


__all__ = [
    "RecencyWeightingRule",
    "DecayFunctionRule",
    "MinimumEvidenceRule",
    "ArchiveNotDeleteRule",
    "PromotionCriteriaRule",
    "PromotionPolicy",
    "PromotionDecision",
]