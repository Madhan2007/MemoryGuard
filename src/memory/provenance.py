"""
MemoryGuard Provenance Chain

Member 1 ownership.

Builds full audit trail from source to decision.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
import hashlib
import json

from .memory_guard import CandidateMemory, VerificationContext, Provenance, DecisionStep, RuleResult


class ProvenanceBuilder:
    """Builds complete provenance chain for memory decisions."""
    
    def build(
        self,
        candidate: CandidateMemory,
        source: str,
        context: VerificationContext,
        rule_results: List[RuleResult],
        decision: "DecisionType",
        scope: "Scope"
    ) -> Provenance:
        """Build complete provenance chain."""
        audit_id = str(uuid.uuid4())
        
        # Extract source quote from candidate or source
        source_quote = self._extract_quote(source, candidate)
        
        # Build decision chain from rule results
        decision_chain = []
        for result in rule_results:
            decision_chain.append(DecisionStep(
                step=result.rule_id,
                result="PASS" if result.passed else "FAIL",
                reason=result.reason
            ))
        
        # Add final decision step
        decision_chain.append(DecisionStep(
            step="final_decision",
            result=decision.value.upper(),
            reason=f"Final decision: {decision.value}"
        ))
        
        return Provenance(
            source_conversation_id=context.conversation_id,
            source_turn_ids=[context.turn_id],
            source_quotes=[source_quote] if source_quote else [],
            extraction_method="llm_extraction",
            verifier_model="configured_verifier_model",  # TODO: get from config
            verification_timestamp=datetime.utcnow(),
            decision_chain=decision_chain,
            audit_id=audit_id
        )
    
    def _extract_quote(self, source: str, candidate: CandidateMemory) -> str:
        """Extract relevant quote from source text."""
        if candidate.source_span:
            start, end = candidate.source_span
            return source[start:end]
        # Fallback: return first sentence or first 200 chars
        sentences = source.split('.')
        if sentences:
            return sentences[0].strip() + '.'
        return source[:200]
    
    def merge_provenance(
        self,
        target_provenance: Provenance,
        candidate: CandidateMemory,
        source: str,
        rule_results: List[RuleResult]
    ) -> Provenance:
        """Merge provenance from candidate into target (for MERGE decisions)."""
        new_quote = self._extract_quote(source, candidate)
        
        merged = Provenance(
            source_conversation_id=target_provenance.source_conversation_id,
            source_turn_ids=target_provenance.source_turn_ids + [candidate.source_turn_id if hasattr(candidate, 'source_turn_id') else 0],
            source_quotes=target_provenance.source_quotes + [new_quote],
            extraction_method=target_provenance.extraction_method,
            verifier_model=target_provenance.verifier_model,
            verification_timestamp=datetime.utcnow(),
            decision_chain=target_provenance.decision_chain + [
                DecisionStep(
                    step=result.rule_id,
                    result="PASS" if result.passed else "FAIL",
                    reason=result.reason
                ) for result in rule_results
            ],
            audit_id=str(uuid.uuid4())
        )
        return merged
    
    def build_audit_hash(self, provenance: Provenance) -> str:
        """Build cryptographic hash for audit immutability (R28)."""
        # Create deterministic representation
        data = {
            "audit_id": provenance.audit_id,
            "source_conversation_id": provenance.source_conversation_id,
            "source_turn_ids": provenance.source_turn_ids,
            "source_quotes": provenance.source_quotes,
            "decision_chain": [
                {"step": s.step, "result": s.result, "reason": s.reason}
                for s in provenance.decision_chain
            ],
            "verification_timestamp": provenance.verification_timestamp.isoformat(),
        }
        serialized = json.dumps(data, sort_keys=True)
        return hashlib.sha256(serialized.encode()).hexdigest()
    
    def verify_audit_integrity(self, provenance: Provenance, expected_hash: str) -> bool:
        """Verify audit trail hasn't been tampered with (R28)."""
        computed = self.build_audit_hash(provenance)
        return computed == expected_hash


__all__ = [
    "ProvenanceBuilder",
]