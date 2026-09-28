"""
MemoryGuard Scope Management

Member 1 ownership.

Implements scope assignment and isolation (R15-R19).
"""

from dataclasses import dataclass
from typing import Optional, List
from .memory_guard import CandidateMemory, Memory, Scope, ScopeInfo, RuleResult, RuleCategory
from .rules import Rule, rule


@rule("R15", "Project Scope Isolation", RuleCategory.SCOPE)
class ProjectIsolationRule(Rule):
    """R15: Deal memories never appear in other deals."""
    
    async def evaluate(
        self,
        candidate: CandidateMemory,
        source: str,
        context: "VerificationContext",
        existing: List[Memory]
    ) -> RuleResult:
        # This is enforced at Hindsight bank level
        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            passed=True,
            reason="Project isolation enforced at Hindsight bank level",
            metadata={}
        )


@rule("R16", "Common Scope Privacy", RuleCategory.SCOPE)
class CommonPrivacyRule(Rule):
    """R16: Rep's personal memories never visible to other reps."""
    
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
            reason="Common scope privacy enforced at Hindsight bank level",
            metadata={}
        )


@rule("R17", "Scope Assignment at Admission", RuleCategory.SCOPE)
class ScopeAssignmentRule(Rule):
    """R17: Every memory assigned scope at admission time."""
    
    async def evaluate(
        self,
        candidate: CandidateMemory,
        source: str,
        context: "VerificationContext",
        existing: List[Memory]
    ) -> RuleResult:
        scope = self.assign_scope(candidate, context)
        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            passed=True,
            reason=f"Scope assigned: {scope.value}",
            metadata={"assigned_scope": scope.value}
        )
    
    def assign_scope(
        self,
        candidate: CandidateMemory,
        context: "VerificationContext"
    ) -> "Scope":
        """Determine scope based on memory type and context."""
        # Project-scoped: deal-specific information
        project_types = {
            "requirement", "objection", "competitor", 
            "stakeholder", "pricing", "compliance", 
            "technical", "decision"
        }
        
        # Common-scoped: rep-specific patterns
        common_types = {"preference", "pattern"}
        
        if candidate.memory_type.value in project_types:
            return Scope.PROJECT
        elif candidate.memory_type.value in common_types:
            return Scope.COMMON
        
        # Default to project for deal-relevant, common for personal
        if context.deal_id and context.deal_id != "temp":
            return Scope.PROJECT
        return Scope.COMMON


@rule("R18", "Cross-Scope Contamination Prevention", RuleCategory.SCOPE)
class CrossScopePreventionRule(Rule):
    """R18: MemoryGuard rejects memories assigned wrong scope."""
    
    async def evaluate(
        self,
        candidate: CandidateMemory,
        source: str,
        context: "VerificationContext",
        existing: List[Memory]
    ) -> RuleResult:
        # Check if memory content matches assigned scope
        assigned_scope = ScopeAssignmentRule().assign_scope(candidate, context)
        
        # Example: personal preference shouldn't go to project bank
        if assigned_scope == Scope.PROJECT and candidate.memory_type.value == "preference":
            # Check if it's actually a deal-relevant preference
            deal_keywords = ["deal", "contract", "proposal", "negotiation", "pricing"]
            if not any(kw in candidate.text.lower() for kw in deal_keywords):
                return RuleResult(
                    rule_id=self.rule_id,
                    rule_name=self.rule_name,
                    passed=False,
                    reason="Personal preference assigned to project scope without deal relevance",
                    metadata={"suggested_scope": Scope.COMMON.value}
                )
        
        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            passed=True,
            reason="Scope assignment validated",
            metadata={}
        )


@rule("R19", "Combined Read Only", RuleCategory.SCOPE)
class CombinedReadOnlyRule(Rule):
    """R19: Combined view is query-time merge; no persistent third bank."""
    
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
            reason="Combined read is query-time only; two persistent banks",
            metadata={}
        )


class ScopeManager:
    """Manages scope assignment and validation."""
    
    def __init__(self, config: Optional["Config"] = None):
        self.config = config
        self.assignment_rule = ScopeAssignmentRule()
        self.validation_rule = CrossScopePreventionRule()
    
    def assign_scope(
        self,
        candidate: CandidateMemory,
        context: "VerificationContext"
    ) -> "Scope":
        """Assign scope to candidate memory."""
        return self.assignment_rule.assign_scope(candidate, context)
    
    def get_bank_id(self, scope: "Scope", context: "VerificationContext") -> str:
        """Get Hindsight bank ID for scope."""
        if scope == Scope.PROJECT:
            return f"memoryguard-project-{context.deal_id}"
        else:
            return f"memoryguard-common-{context.rep_id}"
    
    def validate_scope_assignment(
        self,
        candidate: CandidateMemory,
        scope: "Scope",
        context: "VerificationContext"
    ) -> RuleResult:
        """Validate scope assignment is appropriate."""
        from .memory_guard import VerificationContext
        temp_context = VerificationContext(
            deal_id=context.deal_id,
            rep_id=context.rep_id,
            conversation_id=context.conversation_id,
            turn_id=context.turn_id
        )
        return CrossScopePreventionRule().evaluate(candidate, "", temp_context, [])
    
    def enforce_project_isolation(self, bank_id: str, expected_scope: "Scope") -> bool:
        """Verify bank matches expected scope."""
        if expected_scope == Scope.PROJECT:
            return bank_id.startswith("memoryguard-project-")
        else:
            return bank_id.startswith("memoryguard-common-")
    
    def combined_read_query(
        self,
        query: str,
        deal_id: str,
        rep_id: str,
        top_k: int = 10
    ) -> dict:
        """Build combined read query parameters (not persistent)."""
        return {
            "project_bank": f"memoryguard-project-{deal_id}",
            "common_bank": f"memoryguard-common-{rep_id}",
            "query": query,
            "top_k": top_k
        }


__all__ = [
    "ProjectIsolationRule",
    "CommonPrivacyRule",
    "ScopeAssignmentRule",
    "CrossScopePreventionRule",
    "CombinedReadOnlyRule",
    "ScopeManager",
]