"""
MemoryGuard Conflict Handling

Member 1 ownership.

Implements contradiction detection and resolution (R10-R14).
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from .memory_guard import CandidateMemory, Memory, RuleResult, RuleCategory, ConflictInfo, ConflictType, ChangeType
from .rules import Rule, rule


@rule("R10", "Direct Contradiction Detection", RuleCategory.CONFLICT)
class ContradictionDetectionRule(Rule):
    """R10: Detect when new memory contradicts existing."""
    
    async def evaluate(
        self,
        candidate: CandidateMemory,
        source: str,
        context: "VerificationContext",
        existing: List[Memory]
    ) -> RuleResult:
        conflicts = await self.detect_contradictions(candidate, existing)
        if conflicts:
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                passed=False,  # Flag as conflict, not pass/fail
                reason=f"Contradiction detected with {len(conflicts)} existing memory(s)",
                metadata={"conflicts": [c.conflicting_memory_id for c in conflicts]}
            )
        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            passed=True,
            reason="No contradictions detected",
            metadata={}
        )
    
    async def detect_contradictions(
        self,
        candidate: CandidateMemory,
        existing: List[Memory]
    ) -> List[ConflictInfo]:
        """Detect contradictions between candidate and existing memories."""
        conflicts = []
        # TODO: Implement semantic contradiction detection
        # For now, simple keyword-based detection
        candidate_lower = candidate.text.lower()
        
        contradiction_pairs = [
            ("required", "not required"),
            ("required", "optional"),
            ("mandatory", "not mandatory"),
            ("prefer", "don't prefer"),
            ("like", "dislike"),
            ("yes", "no"),
        ]
        
        for mem in existing:
            if mem.memory_type != candidate.memory_type:
                continue
            
            mem_lower = mem.text.lower()
            for pos, neg in contradiction_pairs:
                if pos in candidate_lower and neg in mem_lower:
                    conflicts.append(ConflictInfo(
                        conflicting_memory_id=mem.id,
                        conflict_type=ConflictType.CONTRADICTION,
                        resolution=None
                    ))
                elif neg in candidate_lower and pos in mem_lower:
                    conflicts.append(ConflictInfo(
                        conflicting_memory_id=mem.id,
                        conflict_type=ConflictType.CONTRADICTION,
                        resolution=None
                    ))
        
        return conflicts


@rule("R11", "Temporal Conflict Resolution", RuleCategory.CONFLICT)
class TemporalResolutionRule(Rule):
    """R11: Newer explicit information overrides older."""
    
    async def evaluate(
        self,
        candidate: CandidateMemory,
        source: str,
        context: "VerificationContext",
        existing: List[Memory]
    ) -> RuleResult:
        # This rule provides resolution guidance, doesn't pass/fail
        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            passed=True,
            reason="Temporal resolution applied if conflicts exist",
            metadata={}
        )
    
    def resolve_temporal(
        self,
        old_memory: Memory,
        new_candidate: CandidateMemory
    ) -> "ConflictResolution":
        """Resolve temporal contradiction: newer explicit wins."""
        # Check for explicit change indicators
        change_indicators = ["now", "changed", "updated", "new policy", "recently"]
        source_lower = new_candidate.text.lower()
        
        is_explicit = any(indicator in source_lower for indicator in change_indicators)
        
        if is_explicit:
            return ConflictResolution(
                strategy="TEMPORAL_OVERRIDE",
                winner="new",
                reason="Explicit customer change indicated",
                change_note=f"Explicit change from '{old_memory.text}' to '{new_candidate.text}'"
            )
        else:
            return ConflictResolution(
                strategy="FLAG_FOR_REVIEW",
                winner=None,
                reason="Implicit change, needs human review",
                change_note=None
            )


@rule("R12", "Implicit vs Explicit Change", RuleCategory.CONFLICT)
class ExplicitChangeRule(Rule):
    """R12: Distinguish explicit customer change from agent inference."""
    
    async def evaluate(
        self,
        candidate: CandidateMemory,
        source: str,
        context: "VerificationContext",
        existing: List[Memory]
    ) -> RuleResult:
        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            passed=True,
            reason="Explicit change classification applied during conflict resolution",
            metadata={}
        )
    
    def classify_change_type(
        self,
        old_memory: Memory,
        new_candidate: CandidateMemory
    ) -> ChangeType:
        """Classify whether change is explicit or implicit."""
        explicit_indicators = [
            "now", "changed", "updated", "new policy", 
            "recently", "actually", "correction"
        ]
        source_lower = new_candidate.text.lower()
        
        if any(indicator in source_lower for indicator in explicit_indicators):
            return ChangeType.EXPLICIT
        return ChangeType.IMPLICIT


@rule("R13", "Stakeholder Conflict Isolation", RuleCategory.CONFLICT)
class StakeholderIsolationRule(Rule):
    """R13: Different stakeholders may have different preferences - not conflicts."""
    
    async def evaluate(
        self,
        candidate: CandidateMemory,
        source: str,
        context: "VerificationContext",
        existing: List[Memory]
    ) -> RuleResult:
        # Check if contradiction is due to different stakeholders
        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            passed=True,
            reason="Stakeholder context checked during conflict resolution",
            metadata={}
        )
    
    def check_stakeholder_context(
        self,
        candidate: CandidateMemory,
        existing: List[Memory]
    ) -> bool:
        """Check if apparent contradiction is actually stakeholder difference."""
        # TODO: Implement stakeholder extraction from source/metadata
        return False


@rule("R14", "Conflict Memory Flagging", RuleCategory.CONFLICT)
class ConflictFlaggingRule(Rule):
    """R14: Conflicted memories flagged, not silently overwritten."""
    
    async def evaluate(
        self,
        candidate: CandidateMemory,
        source: str,
        context: "VerificationContext",
        existing: List[Memory]
    ) -> RuleResult:
        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            passed=True,
            reason="Conflict flagging applied in decision output",
            metadata={}
        )
    
    def flag_conflict(
        self,
        candidate: CandidateMemory,
        existing_memory: Memory
    ) -> ConflictInfo:
        """Create conflict info linking two memories."""
        return ConflictInfo(
            conflicting_memory_id=existing_memory.id,
            conflict_type=ConflictType.CONTRADICTION,
            resolution="PENDING_REVIEW"
        )


class ConflictDetector:
    """High-level conflict detection orchestrator."""
    
    def __init__(self):
        self.contradiction_rule = ContradictionDetectionRule()
        self.temporal_rule = TemporalResolutionRule()
        self.explicit_rule = ExplicitChangeRule()
        self.stakeholder_rule = StakeholderIsolationRule()
        self.flagging_rule = ConflictFlaggingRule()
    
    async def detect_contradictions(
        self,
        candidate: CandidateMemory,
        existing: List[Memory]
    ) -> List[ConflictInfo]:
        """Detect all contradictions with existing memories."""
        # Use a temporary context for rule evaluation
        from .memory_guard import VerificationContext
        temp_context = VerificationContext(
            deal_id="temp",
            rep_id="temp",
            conversation_id="temp",
            turn_id=0
        )
        
        result = await self.contradiction_rule.evaluate(candidate, "", temp_context, existing)
        if not result.passed and result.metadata.get("conflicts"):
            # Convert metadata to ConflictInfo objects
            return [
                ConflictInfo(conflicting_memory_id=mid, conflict_type=ConflictType.CONTRADICTION)
                for mid in result.metadata["conflicts"]
            ]
        return []
    
    async def classify_and_resolve(
        self,
        old_memory: Memory,
        new_candidate: CandidateMemory
    ) -> "ConflictResolution":
        """Classify change type and determine resolution."""
        change_type = self.explicit_rule.classify_change_type(old_memory, new_candidate)
        return self.temporal_rule.resolve_temporal(old_memory, new_candidate)


@dataclass
class ConflictResolution:
    """Resolution strategy for a conflict."""
    strategy: str  # TEMPORAL_OVERRIDE, FLAG_FOR_REVIEW, KEEP_BOTH
    winner: Optional[str]  # "old", "new", None
    reason: str
    change_note: Optional[str]


__all__ = [
    "ContradictionDetectionRule",
    "TemporalResolutionRule",
    "ExplicitChangeRule",
    "StakeholderIsolationRule",
    "ConflictFlaggingRule",
    "ConflictDetector",
    "ConflictResolution",
]