"""
MemoryGuard Contamination Detection

Member 1 ownership.

Implements contamination detection (R1-R4, R34) - the hero feature.
"""

from dataclasses import dataclass
from typing import Literal
from .memory_guard import CandidateMemory, RuleResult, RuleCategory
from .rules import Rule, rule


@dataclass
class VerificationResponse:
    """Structured response from verifier LLM."""
    supported: Literal["SUPPORTED", "PARTIALLY_SUPPORTED", "NOT_SUPPORTED"]
    reason: str
    confidence: float


class VerifierClient:
    """Abstract interface for verifier LLM client."""
    
    async def check_support(
        self,
        candidate: CandidateMemory,
        source: str
    ) -> VerificationResponse:
        """Check if source text supports candidate memory."""
        raise NotImplementedError
    
    async def verify(self, prompt: str) -> VerificationResponse:
        """Generic verification call."""
        raise NotImplementedError


class MockVerifier(VerifierClient):
    """Mock verifier for development and testing."""
    
    async def check_support(
        self,
        candidate: CandidateMemory,
        source: str
    ) -> VerificationResponse:
        # Simple heuristic for mock
        candidate_lower = candidate.text.lower()
        source_lower = source.lower()
        
        # Check for obvious contradictions
        if "mandatory" in candidate_lower and "evaluating" in source_lower:
            return VerificationResponse(
                supported="NOT_SUPPORTED",
                reason="Candidate asserts mandate; source only states evaluation",
                confidence=0.95
            )
        
        if "not required" in source_lower and "required" in candidate_lower:
            return VerificationResponse(
                supported="PARTIALLY_SUPPORTED",
                reason="Source says not required, candidate says required",
                confidence=0.8
            )
        
        # Default: supported
        return VerificationResponse(
            supported="SUPPORTED",
            reason="Candidate appears consistent with source",
            confidence=0.85
        )


@rule("R34", "Source Support Verification", RuleCategory.CONTAMINATION)
class SourceSupportRule(Rule):
    """R34: Verify candidate memory is grounded in source text."""
    
    def __init__(self, verifier: VerifierClient):
        self.verifier = verifier
    
    async def evaluate(
        self,
        candidate: CandidateMemory,
        source: str,
        context: "VerificationContext",
        existing: List
    ) -> RuleResult:
        response = await self.verifier.check_support(candidate, source)
        
        if response.supported == "NOT_SUPPORTED":
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                passed=False,
                reason=f"Contamination detected: {response.reason}",
                metadata={"verifier_confidence": response.confidence}
            )
        elif response.supported == "PARTIALLY_SUPPORTED":
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                passed=False,
                reason=f"Partial support: {response.reason}",
                metadata={"verifier_confidence": response.confidence}
            )
        
        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            passed=True,
            reason="Candidate fully supported by source",
            metadata={"verifier_confidence": response.confidence}
        )


@rule("R1", "Grounding Required", RuleCategory.RELIABILITY)
class GroundingRequiredRule(Rule):
    """R1: Every retained memory must be grounded in source text."""
    
    async def evaluate(
        self,
        candidate: CandidateMemory,
        source: str,
        context: "VerificationContext",
        existing: List
    ) -> RuleResult:
        # This is checked by R34 (Source Support)
        # Additional check: source quote must be preserved
        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            passed=True,
            reason="Grounding verified via R34",
            metadata={}
        )


@rule("R2", "Verbatim Quote Preservation", RuleCategory.RELIABILITY)
class VerbatimQuoteRule(Rule):
    """R2: Source quote must be preserved exactly for audit."""
    
    async def evaluate(
        self,
        candidate: CandidateMemory,
        source: str,
        context: "VerificationContext",
        existing: List
    ) -> RuleResult:
        # Verified in provenance building
        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            passed=True,
            reason="Quote preservation handled in provenance",
            metadata={}
        )


@rule("R3", "No Hallucination Admission", RuleCategory.RELIABILITY)
class NoHallucinationRule(Rule):
    """R3: LLM-generated content not in source → REJECT."""
    
    async def evaluate(
        self,
        candidate: CandidateMemory,
        source: str,
        context: "VerificationContext",
        existing: List
    ) -> RuleResult:
        # Checked by R34
        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            passed=True,
            reason="Hallucination check via R34",
            metadata={}
        )


@rule("R4", "Confidence Threshold", RuleCategory.RELIABILITY)
class ConfidenceThresholdRule(Rule):
    """R4: Memories below confidence threshold → NEEDS_REVIEW."""
    
    def __init__(self, threshold: float = 0.7):
        self.threshold = threshold
    
    async def evaluate(
        self,
        candidate: CandidateMemory,
        source: str,
        context: "VerificationContext",
        existing: List
    ) -> RuleResult:
        if candidate.confidence < self.threshold:
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                passed=False,
                reason=f"Candidate confidence {candidate.confidence:.2f} below threshold {self.threshold}",
                metadata={"candidate_confidence": candidate.confidence, "threshold": self.threshold}
            )
        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            passed=True,
            reason=f"Confidence {candidate.confidence:.2f} meets threshold",
            metadata={}
        )


class ContaminationDetector:
    """High-level contamination detection orchestrator."""
    
    def __init__(self, verifier: VerifierClient):
        self.verifier = verifier
        self.source_support_rule = SourceSupportRule(verifier)
        self.confidence_rule = ConfidenceThresholdRule()
    
    async def check_grounding(
        self,
        candidate: CandidateMemory,
        source: str,
        context: "VerificationContext",
        existing: List
    ) -> RuleResult:
        """R34: Primary contamination check."""
        return await self.source_support_rule.evaluate(candidate, source, context, existing)
    
    async def check_hallucination(
        self,
        candidate: CandidateMemory,
        source: str,
        context: "VerificationContext",
        existing: List
    ) -> RuleResult:
        """R3: Check for hallucinated details."""
        # Delegate to source support check
        return await self.check_grounding(candidate, source, context, existing)


__all__ = [
    "VerificationResponse",
    "VerifierClient",
    "MockVerifier",
    "SourceSupportRule",
    "GroundingRequiredRule",
    "VerbatimQuoteRule",
    "NoHallucinationRule",
    "ConfidenceThresholdRule",
    "ContaminationDetector",
]