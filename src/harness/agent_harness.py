"""
Agent Harness - Main Agent Loop

Member 2 ownership.

Orchestrates the full conversation turn processing:
Recall → Context Build → Main LLM → Candidate → MemoryGuard → Retain
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

from ..integrations.hindsight_client import HindsightClient
from ..integrations.groq_client import GroqClient
from ..memory.memory_guard import (
    MemoryGuard, 
    CandidateMemory, 
    VerificationContext, 
    MemoryDecision,
    Memory,
    Scope,
    DecisionType,
    MemoryType,
)
from ..integrations.config import Config
from .session import Session, SessionStore, InMemorySessionStore
from .logger import get_logger

logger = get_logger(__name__)


@dataclass
class TurnMetadata:
    """Metadata about a conversation turn."""
    turn_id: int
    latency_ms: float
    tokens_used: int
    memories_recalled: int
    candidates_extracted: int
    decisions_made: int


@dataclass
class ChatMessage:
    """Chat message for UI/history."""
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class AgentResponse:
    """Complete response from agent turn processing."""
    response_text: str
    candidate_memories: List[CandidateMemory]
    memory_decisions: List[MemoryDecision]
    recalled_memories: List[Memory]
    turn_metadata: TurnMetadata
    chat_message: ChatMessage
    errors: List[str] = field(default_factory=list)


class AgentLoop:
    """
    Main agent conversation loop.
    
    Processes each user turn through the full pipeline:
    1. Recall relevant memories from Hindsight
    2. Build context with retrieved memories
    3. Generate response with Main LLM
    4. Extract candidate memories from response
    5. Verify each candidate with MemoryGuard
    6. Persist accepted memories to Hindsight
    7. Return response to user
    """
    
    def __init__(
        self,
        hindsight: HindsightClient,
        groq: GroqClient,
        memoryguard: MemoryGuard,
        session_store: SessionStore,
        config: Optional[Config] = None,
    ):
        self.hindsight = hindsight
        self.groq = groq
        self.memoryguard = memoryguard
        self.sessions = session_store
        self.config = config or Config()
    
    async def process_turn(
        self,
        user_input: str,
        deal_id: str,
        rep_id: str
    ) -> AgentResponse:
        """
        Process a single conversation turn.
        
        Args:
            user_input: User's message
            deal_id: Current deal identifier
            rep_id: Sales rep identifier
            
        Returns:
            AgentResponse with response and metadata
        """
        start_time = datetime.utcnow()
        turn_id = 0
        
        try:
            # Get or create session
            session = await self.sessions.get_or_create(deal_id, rep_id)
            turn_id = session.turn_count + 1
            
            # Add user message to session
            session.add_turn("user", user_input)
            
            # 1. RECALL PHASE
            recalled_memories = await self._recall_memories(
                user_input, deal_id, rep_id
            )
            
            # 2. CONTEXT BUILD
            messages = self._build_context_messages(session, recalled_memories)
            
            # 3. GENERATION PHASE
            llm_start = datetime.utcnow()
            response_text = await self.groq.call_main_llm(messages)
            llm_latency = (datetime.utcnow() - llm_start).total_seconds() * 1000
            
            # 4. CANDIDATE EXTRACTION
            candidates = self._extract_candidates(response_text, session, user_input)
            
            # 5. GOVERNANCE PHASE
            decisions = []
            for candidate in candidates:
                context = self._build_verification_context(
                    candidate, session, deal_id, rep_id, turn_id
                )
                scope = self._determine_scope(candidate, context)
                
                decision = await self.memoryguard.verify(
                    candidate, user_input, context, scope
                )
                decisions.append(decision)
                
                # 6. PERSIST DECISION
                if decision.decision in [DecisionType.RETAIN, DecisionType.UPDATE, DecisionType.MERGE]:
                    await self._persist_decision(decision, deal_id, rep_id)
            
            # 7. UPDATE SESSION
            session.add_turn("assistant", response_text)
            
            # Build response
            turn_metadata = TurnMetadata(
                turn_id=turn_id,
                latency_ms=(datetime.utcnow() - start_time).total_seconds() * 1000,
                tokens_used=0,  # TODO: Track from LLM response
                memories_recalled=len(recalled_memories),
                candidates_extracted=len(candidates),
                decisions_made=len(decisions),
            )
            
            chat_message = ChatMessage(
                role="assistant",
                content=response_text,
                timestamp=datetime.utcnow(),
                metadata={
                    "turn_id": turn_id,
                    "latency_ms": turn_metadata.latency_ms,
                    "candidates": len(candidates),
                    "decisions": [d.decision.value for d in decisions],
                }
            )
            
            logger.info(
                "turn_processed",
                deal_id=deal_id,
                rep_id=rep_id,
                turn=turn_id,
                latency_ms=turn_metadata.latency_ms,
                candidates=len(candidates),
                decisions=[d.decision.value for d in decisions],
            )
            
            return AgentResponse(
                response_text=response_text,
                candidate_memories=candidates,
                memory_decisions=decisions,
                recalled_memories=recalled_memories,
                turn_metadata=turn_metadata,
                chat_message=chat_message,
            )
            
        except Exception as e:
            logger.error("turn_processing_failed", deal_id=deal_id, rep_id=rep_id, error=str(e))
            return AgentResponse(
                response_text="I apologize, but I encountered an error processing your message. Please try again.",
                candidate_memories=[],
                memory_decisions=[],
                recalled_memories=[],
                turn_metadata=TurnMetadata(
                    turn_id=turn_id,
                    latency_ms=(datetime.utcnow() - start_time).total_seconds() * 1000,
                    tokens_used=0,
                    memories_recalled=0,
                    candidates_extracted=0,
                    decisions_made=0,
                ),
                chat_message=ChatMessage(
                    role="assistant",
                    content="Error occurred",
                    timestamp=datetime.utcnow(),
                ),
                errors=[str(e)],
            )
    
    async def _recall_memories(
        self, 
        query: str, 
        deal_id: str, 
        rep_id: str
    ) -> List[Memory]:
        """Recall relevant memories from both project and common banks."""
        project_bank = self.hindsight.project_bank(deal_id)
        common_bank = self.hindsight.common_bank(rep_id)
        
        # Parallel recall
        project_task = self.hindsight.recall(project_bank, query, top_k=10)
        common_task = self.hindsight.recall(common_bank, query, top_k=10)
        
        project_memories, common_memories = await asyncio.gather(
            project_task, common_task, return_exceptions=True
        )
        
        # Handle exceptions
        if isinstance(project_memories, Exception):
            logger.warning("project_recall_failed", deal_id=deal_id, error=str(project_memories))
            project_memories = []
        if isinstance(common_memories, Exception):
            logger.warning("common_recall_failed", rep_id=rep_id, error=str(common_memories))
            common_memories = []
        
        # Merge and rank
        return self._merge_and_rank(project_memories, common_memories)
    
    def _merge_and_rank(
        self, 
        project: List[Memory], 
        common: List[Memory]
    ) -> List[Memory]:
        """Merge memories from both banks, deduplicate, and rank."""
        all_memories = project + common
        
        # Deduplicate by content similarity
        deduped = self._deduplicate(all_memories)
        
        # Rank by: relevance, recency, frequency, scope priority
        ranked = sorted(deduped, key=self._ranking_key, reverse=True)
        
        return ranked[:10]
    
    def _deduplicate(self, memories: List[Memory]) -> List[Memory]:
        """Remove duplicate memories by content similarity."""
        unique = []
        for mem in memories:
            is_dup = False
            for existing in unique:
                if self._text_similarity(mem.text, existing.text) > 0.9:
                    is_dup = True
                    break
            if not is_dup:
                unique.append(mem)
        return unique
    
    def _text_similarity(self, text1: str, text2: str) -> float:
        """Simple text similarity (placeholder for embeddings)."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 or not words2:
            return 0.0
        return len(words1 & words2) / len(words1 | words2)
    
    def _ranking_key(self, mem: Memory) -> tuple:
        """Ranking key for memory retrieval."""
        # Higher is better: relevance, recency, frequency, project priority
        recency = mem.metadata.get("last_seen", "")
        frequency = mem.metadata.get("frequency", 1)
        is_project = 1 if mem.metadata.get("scope") == "project" else 0
        return (1.0, recency, frequency, is_project)  # Simplified
    
    def _build_context_messages(
        self, 
        session: "Session", 
        recalled_memories: List[Memory]
    ) -> List[Dict[str, str]]:
        """Build LLM messages with context from recalled memories."""
        messages = []
        
        # System prompt with memories
        if recalled_memories:
            memory_context = "\n".join([
                f"- {m.text} (source: {m.metadata.get('source_quote', 'N/A')[:100]})"
                for m in recalled_memories[:5]
            ])
            system_prompt = f"""You are a sales assistant with access to verified customer memories.
            
Relevant customer context:
{memory_context}

Use this context to personalize your responses. Be natural and conversational."""
        else:
            system_prompt = """You are a sales assistant. Be helpful and professional."""
        
        messages.append({"role": "system", "content": system_prompt})
        
        # Add conversation history
        for turn in session.get_history(max_turns=10):
            messages.append({"role": turn.role, "content": turn.content})
        
        return messages
    
    def _extract_candidates(
        self, 
        response: str, 
        session: "Session",
        source_text: str
    ) -> List[CandidateMemory]:
        """Extract candidate memories from LLM response."""
        # TODO: Implement structured extraction from LLM
        # For now, simple heuristic extraction
        candidates = []
        
        # Simple heuristic: look for key phrases indicating memories
        memory_indicators = [
            ("prefer", MemoryType.PREFERENCE),
            ("require", MemoryType.REQUIREMENT),
            ("need", MemoryType.REQUIREMENT),
            ("objection", MemoryType.OBJECTION),
            ("competitor", MemoryType.COMPETITOR),
            ("evaluating", MemoryType.COMPETITOR),
            ("budget", MemoryType.PRICING),
            ("price", MemoryType.PRICING),
            ("compliance", MemoryType.COMPLIANCE),
            ("SOC2", MemoryType.COMPLIANCE),
            ("technical", MemoryType.TECHNICAL),
            ("decision", MemoryType.DECISION),
            ("stakeholder", MemoryType.STAKEHOLDER),
        ]
        
        response_lower = response.lower()
        for indicator, mem_type in memory_indicators:
            if indicator in response_lower:
                # Find the sentence containing the indicator
                sentences = response.split('.')
                for sent in sentences:
                    if indicator in sent.lower():
                        candidates.append(CandidateMemory(
                            text=sent.strip(),
                            memory_type=mem_type,
                            confidence=0.7,
                        ))
                        break
        
        return candidates
    
    def _build_verification_context(
        self,
        candidate: CandidateMemory,
        session: "Session",
        deal_id: str,
        rep_id: str,
        turn_id: int
    ) -> VerificationContext:
        """Build context for MemoryGuard verification."""
        # Recall existing memories for consolidation/conflict checks
        existing = []  # TODO: Recall similar memories
        
        return VerificationContext(
            deal_id=deal_id,
            rep_id=rep_id,
            conversation_id=session.conversation_id,
            turn_id=turn_id,
            existing_memories=existing,
            deal_stage="discovery",  # TODO: Track deal stage
            customer_name="Customer",
        )
    
    def _determine_scope(
        self, 
        candidate: CandidateMemory, 
        context: VerificationContext
    ) -> "ScopeInfo":
        """Determine memory scope (delegated to MemoryGuard)."""
        from ..memory.scopes import ScopeManager
        scope_manager = ScopeManager()
        scope = scope_manager.assign_scope(candidate, context)
        return scope_manager.get_bank_id(scope, context)
    
    async def _persist_decision(
        self, 
        decision: MemoryDecision, 
        deal_id: str, 
        rep_id: str
    ):
        """Persist MemoryGuard decision to Hindsight."""
        scope = decision.scope
        bank_id = (
            self.hindsight.project_bank(deal_id) 
            if scope == Scope.PROJECT 
            else self.hindsight.common_bank(rep_id)
        )
        
        metadata = {
            "memory_type": decision.memory_text,  # TODO: extract from decision
            "scope": scope.value,
            "decision": decision.decision.value,
            "confidence": decision.confidence,
            "frequency": decision.merge_instruction.new_frequency if decision.merge_instruction else 1,
            "evidence_count": decision.merge_instruction.new_evidence_count if decision.merge_instruction else 1,
            "first_seen": decision.merge_instruction.new_first_seen.isoformat() if decision.merge_instruction else datetime.utcnow().isoformat(),
            "last_seen": decision.merge_instruction.new_last_seen.isoformat() if decision.merge_instruction else datetime.utcnow().isoformat(),
            "source_type": "conversation",
            "source_id": context.conversation_id if 'context' in locals() else "unknown",
            "conversation_id": context.conversation_id if 'context' in locals() else "unknown",
            "turn_id": context.turn_id if 'context' in locals() else 0,
            "source_quote": decision.source_evidence[0].quote if decision.source_evidence else "",
            "provenance": {
                "source_conversation_id": decision.provenance.source_conversation_id,
                "source_turn_ids": decision.provenance.source_turn_ids,
                "source_quotes": decision.provenance.source_quotes,
                "extraction_method": decision.provenance.extraction_method,
                "verifier_model": decision.provenance.verifier_model,
                "verification_timestamp": decision.provenance.verification_timestamp.isoformat(),
                "decision_chain": [
                    {"step": s.step, "result": s.result, "reason": s.reason}
                    for s in decision.provenance.decision_chain
                ],
            },
            "conflicts": [c.conflicting_memory_id for c in decision.conflicts],
            "similar_memories": [m.memory_id for m in decision.similar_memories],
            "audit_id": decision.audit_id,
        }
        
        merge_policy = None
        if decision.merge_instruction:
            merge_policy = MergePolicy(
                target_id=decision.merge_instruction.target_memory_id,
                strategy=decision.merge_instruction.merge_strategy,
            )
        
        await self.hindsight.retain(bank_id, decision.memory_text, metadata, merge_policy)


__all__ = [
    "AgentLoop",
    "AgentResponse",
    "TurnMetadata",
    "ChatMessage",
]