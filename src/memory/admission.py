"""
MemoryGuard Admission Policy

Member 1 ownership.

Implements admission rules (R29-R31) for filtering candidate memories.
"""

from dataclasses import dataclass
from typing import List, Set
from .memory_guard import CandidateMemory, VerificationContext, RuleResult, RuleCategory
from .rules import Rule, rule


@rule("R29", "Utility Threshold", RuleCategory.ADMISSION)
class UtilityThresholdRule(Rule):
    """R29: Reject non-actionable polite phrases and filler."""
    
    # Polite phrases that don't constitute actionable memories
    POLITE_PHRASES: Set[str] = {
        "thanks for the call",
        "thank you for the call",
        "good talking to you",
        "nice speaking with you",
        "have a nice day",
        "have a good day",
        "goodbye",
        "bye",
        "talk soon",
        "speak soon",
        "thanks",
        "thank you",
    }
    
    def __init__(self):
        self.polite_phrases = self.POLITE_PHRASES.copy()
    
    async def evaluate(
        self,
        candidate: CandidateMemory,
        source: str,
        context: VerificationContext,
        existing: List
    ) -> RuleResult:
        text_lower = candidate.text.lower().strip()
        
        # Check for polite phrases
        for phrase in self.polite_phrases:
            if phrase in text_lower:
                return RuleResult(
                    rule_id=self.rule_id,
                    rule_name=self.rule_name,
                    passed=False,
                    reason=f"Polite phrase detected: '{phrase}' - not actionable",
                    metadata={"matched_phrase": phrase}
                )
        
        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            passed=True,
            reason="Candidate contains actionable content",
            metadata={}
        )


@rule("R30", "Deal Relevance", RuleCategory.ADMISSION)
class DealRelevanceRule(Rule):
    """R30: Memory must relate to active deal or rep pattern."""
    
    async def evaluate(
        self,
        candidate: CandidateMemory,
        source: str,
        context: VerificationContext,
        existing: List
    ) -> RuleResult:
        # TODO: Implement deal relevance check
        # Check if memory relates to deal_id, customer, or known rep patterns
        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            passed=True,
            reason="Assumed relevant to current context",
            metadata={}
        )


@rule("R31", "Actionability", RuleCategory.ADMISSION)
class ActionabilityRule(Rule):
    """R31: Memory should enable actionable agent behavior."""
    
    ACTIONABLE_TYPES = {
        "preference", "requirement", "objection", 
        "competitor", "stakeholder", "pricing",
        "compliance", "technical", "decision"
    }
    
    NON_ACTIONABLE_TYPES = {"pattern"}
    
    async def evaluate(
        self,
        candidate: CandidateMemory,
        source: str,
        context: VerificationContext,
        existing: List
    ) -> RuleResult:
        if candidate.memory_type.value in self.NON_ACTIONABLE_TYPES:
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                passed=False,
                reason=f"Memory type '{candidate.memory_type.value}' is not actionable",
                metadata={"memory_type": candidate.memory_type.value}
            )
        
        if candidate.memory_type.value in self.ACTIONABLE_TYPES:
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                passed=True,
                reason=f"Memory type '{candidate.memory_type.value}' is actionable",
                metadata={"memory_type": candidate.memory_type.value}
            )
        
        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            passed=True,
            reason="Assumed actionable",
            metadata={}
        )


class AdmissionPolicy:
    """High-level admission policy orchestrator."""
    
    def __init__(self):
        self.rules = [
            UtilityThresholdRule(),
            DealRelevanceRule(),
            ActionabilityRule(),
        ]
    
    async def evaluate_all(
        self,
        candidate: CandidateMemory,
        source: str,
        context: VerificationContext,
        existing: List
    ) -> List[RuleResult]:
        """Run all admission rules."""
        results = []
        for rule in self.rules:
            result = await rule.evaluate(candidate, source, context, existing)
            results.append(result)
        return results
    
    def should_reject(self, results: List[RuleResult]) -> bool:
        """Check if any admission rule failed (early reject)."""
        return any(not r.passed for r in results if r.rule_id in ["R29", "R30", "R31"])


__all__ = [
    "UtilityThresholdRule",
    "DealRelevanceRule", 
    "ActionabilityRule",
    "AdmissionPolicy",
]