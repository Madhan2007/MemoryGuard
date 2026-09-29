from src.memory.schema import (
    CandidateMemory,
    VerificationContext,
    MemoryDecision,
    DecisionType,
    MemoryType,
    Scope,
    ScopeInfo,
    SourceEvidence,
    Provenance,
    MergeInstruction,
    MergeStrategy,
    SupportState,
    MemoryRef,
)
from src.memory.contamination import check_grounding
from src.memory.consolidation import find_similar, check_merge
from src.memory.scopes import assign_scope
from src.config import settings
from typing import List, Dict, Any, Optional
import logging
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)


class MemoryGuard:
    def __init__(self):
        self.fuzzy_threshold = settings.FUZZY_MERGE_THRESHOLD

    async def verify(
        self,
        candidate: CandidateMemory,
        source_text: str,
        context: VerificationContext,
        scope: Scope,
    ) -> MemoryDecision:
        audit_id = str(uuid.uuid4())

        logger.info(f"MemoryGuard.verify: {candidate.text[:80]}... (audit={audit_id[:8]})")

        decision_chain = []

        # Gate 1: Admission (stub - always PASS for MVP)
        admission_result = await self._admission_gate(candidate, context)
        decision_chain.append(admission_result)
        if admission_result["result"] == "FAIL":
            assigned_scope = assign_scope(candidate, context, scope)
            return self._build_reject(candidate, context, assigned_scope, "Failed admission gate", audit_id, decision_chain)

        # Gate 2: Contamination / Grounding
        grounding_result = await check_grounding(candidate, source_text)
        decision_chain.append(grounding_result)
        if grounding_result["result"] == "FAIL":
            assigned_scope = assign_scope(candidate, context, scope)
            return self._build_reject(
                candidate, context, assigned_scope,
                f"Contamination: {grounding_result['reason']}",
                audit_id, decision_chain,
                verification_status=SupportState.UNSUPPORTED
            )

        # Gate 3: Consolidation / Similarity
        similar_memories = find_similar(candidate, context.existing_memories, self.fuzzy_threshold)
        merge_decision = check_merge(candidate, similar_memories, self.fuzzy_threshold)
        decision_chain.append(merge_decision)

        # Gate 4: Scope Assignment
        assigned_scope = assign_scope(candidate, context, scope)

        # Build final decision
        if merge_decision["should_merge"]:
            return self._build_merge(
                candidate, context, assigned_scope, merge_decision, source_text, audit_id, decision_chain
            )
        else:
            return self._build_retain(
                candidate, context, assigned_scope, source_text, audit_id, decision_chain
            )

    async def _admission_gate(self, candidate: CandidateMemory, context: VerificationContext) -> Dict[str, Any]:
        text = candidate.text.strip().lower()

        if len(text) < 5:
            return {"step": "admission", "result": "FAIL", "reason": "Too short"}

        filler_phrases = [
            "thanks for", "thank you", "good talking", "have a nice",
            "appreciate it", "nice to meet", "good call", "bye"
        ]
        for phrase in filler_phrases:
            if phrase in text:
                return {"step": "admission", "result": "FAIL", "reason": f"Filler phrase: {phrase}"}

        return {"step": "admission", "result": "PASS", "reason": "Actionable memory candidate"}

    def _build_retain(
        self,
        candidate: CandidateMemory,
        context: VerificationContext,
        scope: ScopeInfo,
        source_text: str,
        audit_id: str,
        decision_chain: List[Dict],
    ) -> MemoryDecision:
        now = datetime.utcnow()
        prov = Provenance(
            source_conversation_id=context.conversation_id,
            source_turn_ids=[context.turn_id],
            source_quotes=[source_text],
            verifier_model=settings.VERIFIER_MODEL,
            decision_chain=decision_chain,
        )
        return MemoryDecision(
            decision=DecisionType.RETAIN,
            memory_text=candidate.text,
            reason="New verified memory admitted",
            confidence=candidate.confidence,
            scope=scope.scope,
            source_evidence=[SourceEvidence(
                quote=source_text,
                conversation_id=context.conversation_id,
                turn_id=context.turn_id,
                source_id=context.conversation_id,
            )],
            provenance=prov,
            audit_id=audit_id,
            verification_status=SupportState.SUPPORTED,
        )

    def _build_merge(
        self,
        candidate: CandidateMemory,
        context: VerificationContext,
        scope: ScopeInfo,
        merge_decision: Dict,
        source_text: str,
        audit_id: str,
        decision_chain: List[Dict],
    ) -> MemoryDecision:
        target = merge_decision["target_memory"]
        target_quotes = target.get("metadata", {}).get("provenance", {}).get("source_quotes", [])
        all_quotes = target_quotes + [source_text]

        target_freq = target.get("metadata", {}).get("frequency", 1)
        target_evidence = target.get("metadata", {}).get("evidence_count", 1)
        target_first = target.get("metadata", {}).get("first_seen", datetime.utcnow().isoformat())

        now = datetime.utcnow()
        merge_inst = MergeInstruction(
            target_memory_id=target["id"],
            merge_strategy=MergeStrategy.APPEND_PROVENANCE,
            new_frequency=target_freq + 1,
            new_evidence_count=target_evidence + 1,
            new_first_seen=datetime.fromisoformat(target_first) if isinstance(target_first, str) else now,
            new_last_seen=now,
        )

        prov = Provenance(
            source_conversation_id=context.conversation_id,
            source_turn_ids=[context.turn_id],
            source_quotes=all_quotes,
            verifier_model=settings.VERIFIER_MODEL,
            decision_chain=decision_chain,
        )
        return MemoryDecision(
            decision=DecisionType.MERGE,
            memory_text=target["text"],
            reason=f"Merged with similar memory (similarity={merge_decision['similarity']:.2f})",
            confidence=candidate.confidence,
            scope=scope.scope,
            source_evidence=[SourceEvidence(
                quote=source_text,
                conversation_id=context.conversation_id,
                turn_id=context.turn_id,
                source_id=context.conversation_id,
            )],
            provenance=prov,
            similar_memories=[MemoryRef(
                memory_id=target["id"],
                text=target["text"],
                similarity=merge_decision["similarity"],
            )],
            audit_id=audit_id,
            merge_instruction=merge_inst,
            verification_status=SupportState.SUPPORTED,
        )

    def _build_reject(
        self,
        candidate: CandidateMemory,
        context: VerificationContext,
        scope: ScopeInfo,
        reason: str,
        audit_id: str,
        decision_chain: List[Dict],
        verification_status: SupportState = SupportState.UNSUPPORTED,
    ) -> MemoryDecision:
        prov = Provenance(
            source_conversation_id=context.conversation_id,
            source_turn_ids=[context.turn_id],
            source_quotes=[],
            verifier_model=settings.VERIFIER_MODEL,
            decision_chain=decision_chain,
        )
        return MemoryDecision(
            decision=DecisionType.REJECT,
            memory_text=candidate.text,
            reason=reason,
            confidence=0.0,
            scope=scope.scope,
            source_evidence=[],
            provenance=prov,
            audit_id=audit_id,
            verification_status=verification_status,
        )


memory_guard = MemoryGuard()