"""
MemoryGuard Rules Engine

Member 1 ownership.

Implements the 34 MemoryGuard rules as composable, testable components.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum

from .memory_guard import CandidateMemory, VerificationContext, Memory, RuleResult, RuleCategory


class Rule(ABC):
    """Base protocol for all MemoryGuard rules."""
    
    rule_id: str
    rule_name: str
    category: RuleCategory
    
    @abstractmethod
    async def evaluate(
        self,
        candidate: CandidateMemory,
        source: str,
        context: VerificationContext,
        existing: List[Memory]
    ) -> RuleResult:
        """Evaluate the rule against a candidate memory."""
        pass


class RulesEngine:
    """Registry and executor for all MemoryGuard rules."""
    
    def __init__(self):
        self.rules: Dict[str, Rule] = {}
    
    def register(self, rule: Rule) -> None:
        """Register a rule by its ID."""
        self.rules[rule.rule_id] = rule
    
    def get_rule(self, rule_id: str) -> Optional[Rule]:
        """Get a rule by ID."""
        return self.rules.get(rule_id)
    
    async def evaluate_all(
        self,
        candidate: CandidateMemory,
        source: str,
        context: VerificationContext,
        existing: List[Memory]
    ) -> List[RuleResult]:
        """Evaluate all registered rules in order."""
        results = []
        for rule in self.rules.values():
            result = await rule.evaluate(candidate, source, context, existing)
            results.append(result)
        return results
    
    async def evaluate_category(
        self,
        category: RuleCategory,
        candidate: CandidateMemory,
        source: str,
        context: VerificationContext,
        existing: List[Memory]
    ) -> List[RuleResult]:
        """Evaluate only rules of a specific category."""
        results = []
        for rule in self.rules.values():
            if rule.category == category:
                result = await rule.evaluate(candidate, source, context, existing)
                results.append(result)
        return results


def rule(rule_id: str, name: str, category: RuleCategory):
    """Decorator to register a rule class."""
    def decorator(cls):
        cls.rule_id = rule_id
        cls.rule_name = name
        cls.category = category
        return cls
    return decorator


# TODO: Implement all 34 rules as individual classes
# Example pattern:
#
# @rule("R29", "Utility Threshold", RuleCategory.ADMISSION)
# class UtilityThresholdRule(Rule):
#     async def evaluate(self, candidate, source, context, existing):
#         # Implementation
#         pass
#
# @rule("R34", "Source Support Verification", RuleCategory.CONTAMINATION)
# class SourceSupportRule(Rule):
#     async def evaluate(self, candidate, source, context, existing):
#         # Implementation
#         pass

# Rule ID to Category Mapping
RULE_CATEGORIES = {
    "R1": RuleCategory.RELIABILITY,
    "R2": RuleCategory.RELIABILITY,
    "R3": RuleCategory.RELIABILITY,
    "R4": RuleCategory.RELIABILITY,
    "R5": RuleCategory.CONSOLIDATION,
    "R6": RuleCategory.CONSOLIDATION,
    "R7": RuleCategory.CONSOLIDATION,
    "R8": RuleCategory.CONSOLIDATION,
    "R9": RuleCategory.CONSOLIDATION,
    "R10": RuleCategory.CONFLICT,
    "R11": RuleCategory.CONFLICT,
    "R12": RuleCategory.CONFLICT,
    "R13": RuleCategory.CONFLICT,
    "R14": RuleCategory.CONFLICT,
    "R15": RuleCategory.SCOPE,
    "R16": RuleCategory.SCOPE,
    "R17": RuleCategory.SCOPE,
    "R18": RuleCategory.SCOPE,
    "R19": RuleCategory.SCOPE,
    "R20": RuleCategory.LIFECYCLE,
    "R21": RuleCategory.LIFECYCLE,
    "R22": RuleCategory.LIFECYCLE,
    "R23": RuleCategory.LIFECYCLE,
    "R24": RuleCategory.LIFECYCLE,
    "R25": RuleCategory.SECURITY,
    "R26": RuleCategory.SECURITY,
    "R27": RuleCategory.SECURITY,
    "R28": RuleCategory.SECURITY,
    "R29": RuleCategory.ADMISSION,
    "R30": RuleCategory.ADMISSION,
    "R31": RuleCategory.ADMISSION,
    "R32": RuleCategory.CONSOLIDATION,
    "R33": RuleCategory.CONSOLIDATION,
    "R34": RuleCategory.CONTAMINATION,
}

__all__ = [
    "Rule",
    "RulesEngine",
    "rule",
    "RULE_CATEGORIES",
]