from pydantic_ai import Agent
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from src.integrations.hindsight_client import hindsight_client, HindsightMemory
from src.integrations.groq_client import groq_client
from src.memory.memory_guard import memory_guard
from src.memory.schema import (
    CandidateMemory,
    VerificationContext,
    MemoryDecision,
    TurnResult,
    MemoryType,
    Scope,
    SourceEvidence,
    DecisionType,
)
from src.config import settings, get_project_bank, get_common_bank, get_pydantic_ai_model
import json
import logging
import time
import uuid
import os
from datetime import datetime

logger = logging.getLogger(__name__)

USE_MOCK = os.getenv("USE_MOCK_LLM", "true").lower() == "true"

MAIN_AGENT_PROMPT = """You are a Deal Intelligence Agent helping a sales representative.

You have access to verified deal memories from previous interactions. Use these to personalize your response.

RECALLED MEMORIES:
{memories}

CURRENT DEAL: {deal_id}
CUSTOMER: {customer_name}
DEAL STAGE: {deal_stage}

INSTRUCTIONS:
- Provide a helpful, personalized response to the sales rep
- Reference relevant memories naturally (e.g., "Based on our previous discussion...")
- If no relevant memories, acknowledge this is a new conversation
- Be concise and actionable
- Do NOT make up facts not in memories

RESPONSE FORMAT: Provide your response as a natural language answer."""

CANDIDATE_EXTRACTION_PROMPT = """Extract potential memories from this interaction.

USER INPUT: {user_input}
AGENT RESPONSE: {agent_response}
DEAL CONTEXT: {deal_id}, {customer_name}, Stage: {deal_stage}

Extract actionable memories that would be useful for future deal interactions. Focus on:
- Customer preferences (communication, process)
- Requirements and constraints
- Objections raised
- Competitors mentioned
- Stakeholder information
- Pricing/compliance/technical details
- Decisions made

Return JSON with this structure:
{{
  "candidates": [
    {{
      "text": "memory text",
      "memory_type": "preference|requirement|objection|competitor|stakeholder|pricing|compliance|technical|decision|pattern",
      "confidence": 0.0-1.0
    }}
  ]
}}

Only extract memories that are specific, actionable, and grounded in the conversation. Reject filler, pleasantries, or vague statements."""


class CandidateExtraction(BaseModel):
    candidates: List[CandidateMemory] = Field(default_factory=list)


class AgentLoop:
    def __init__(self):
        if USE_MOCK:
            self.main_agent = None
            self.extraction_agent = None
            # Track which contamination candidates have been injected per deal
            self._contamination_injected: Dict[str, set] = {}
        else:
            self.main_agent = Agent(
                model=get_pydantic_ai_model(settings.MAIN_MODEL),
                system_prompt="You are a Deal Intelligence Agent.",
            )
            self.extraction_agent = Agent(
                model=get_pydantic_ai_model(settings.MAIN_MODEL),
                system_prompt="You extract structured memory candidates from conversations.",
                output_type=CandidateExtraction,
            )

    def _mock_extract_candidates(self, user_input: str, agent_response: str, deal_id: str) -> List[CandidateMemory]:
        """Mock candidate extraction for demo"""
        candidates = []
        text_lower = user_input.lower()
        
        # Initialize tracking for this deal
        if deal_id not in self._contamination_injected:
            self._contamination_injected[deal_id] = set()
        
        if "prefer email" in text_lower or "email" in text_lower:
            candidates.append(CandidateMemory(
                text="Customer prefers email communication",
                memory_type=MemoryType.PREFERENCE,
                confidence=0.95,
            ))
        elif "evaluating soc2" in text_lower or "soc2" in text_lower:
            candidates.append(CandidateMemory(
                text="Customer is evaluating SOC2 compliance",
                memory_type=MemoryType.COMPLIANCE,
                confidence=0.9,
            ))
            # Only inject contamination candidate ONCE per deal (first mention)
            if "soc2_contamination" not in self._contamination_injected[deal_id]:
                candidates.append(CandidateMemory(
                    text="SOC2 is mandatory before purchase",
                    memory_type=MemoryType.COMPLIANCE,
                    confidence=0.85,
                ))
                self._contamination_injected[deal_id].add("soc2_contamination")
        elif "hipaa" in text_lower:
            candidates.append(CandidateMemory(
                text="Customer requires HIPAA compliance",
                memory_type=MemoryType.COMPLIANCE,
                confidence=0.95,
            ))
        elif "gong" in text_lower or "chorus" in text_lower:
            candidates.append(CandidateMemory(
                text="Customer evaluating Gong and Chorus for conversation intelligence",
                memory_type=MemoryType.COMPETITOR,
                confidence=0.9,
            ))
        elif "integration" in text_lower or "api" in text_lower:
            candidates.append(CandidateMemory(
                text="Customer needs CRM integration",
                memory_type=MemoryType.TECHNICAL,
                confidence=0.85,
            ))
        elif "sso" in text_lower or "single sign" in text_lower:
            candidates.append(CandidateMemory(
                text="Customer requires SSO",
                memory_type=MemoryType.TECHNICAL,
                confidence=0.9,
            ))
        elif "price" in text_lower or "budget" in text_lower:
            candidates.append(CandidateMemory(
                text="Customer has budget constraints",
                memory_type=MemoryType.PRICING,
                confidence=0.8,
            ))
        elif "stakeholder" in text_lower or "champion" in text_lower or "blocker" in text_lower:
            candidates.append(CandidateMemory(
                text="New stakeholder identified",
                memory_type=MemoryType.STAKEHOLDER,
                confidence=0.85,
            ))
        
        return candidates

    def _serialize_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Convert datetime objects to ISO format strings for JSON serialization"""
        result = {}
        for k, v in metadata.items():
            if isinstance(v, datetime):
                result[k] = v.isoformat()
            elif isinstance(v, dict):
                result[k] = self._serialize_metadata(v)
            elif isinstance(v, list):
                result[k] = [self._serialize_metadata(item) if isinstance(item, dict) else item for item in v]
            else:
                result[k] = v
        return result

    async def process_turn(
        self,
        user_input: str,
        deal_id: str,
        rep_id: str,
        conversation_id: str = None,
        turn_id: int = 1,
        customer_name: str = "",
        deal_stage: str = "discovery",
    ) -> TurnResult:
        start_time = time.time()
        audit_id = str(uuid.uuid4())

        if conversation_id is None:
            conversation_id = f"conv-{deal_id}"

        # Step 1: Recall from Hindsight (both banks)
        query = f"{user_input} {deal_id} {customer_name}"
        recalled = await hindsight_client.recall_both(deal_id, rep_id, query, top_k=10)

        # Format memories for context
        memory_texts = []
        for m in recalled:
            scope_tag = m.metadata.get("scope", "unknown")
            freq = m.metadata.get("frequency", 1)
            memory_texts.append(f"[{scope_tag}] {m.text} (freq={freq})")

        memory_context = "\n".join(memory_texts) if memory_texts else "No prior memories recalled."

        # Step 2: Call main LLM for response
        prompt = MAIN_AGENT_PROMPT.format(
            memories=memory_context,
            deal_id=deal_id,
            customer_name=customer_name or deal_id,
            deal_stage=deal_stage,
        )

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input},
        ]
        response_text = await groq_client.call_main(messages)

        # Step 3: Extract candidate memories
        if USE_MOCK:
            candidate_memories = self._mock_extract_candidates(user_input, response_text, deal_id)
        else:
            extract_prompt = CANDIDATE_EXTRACTION_PROMPT.format(
                user_input=user_input,
                agent_response=response_text,
                deal_id=deal_id,
                customer_name=customer_name or deal_id,
                deal_stage=deal_stage,
            )
            try:
                extraction_result = await self.extraction_agent.run(extract_prompt)
                candidate_memories = extraction_result.output.candidates
            except Exception as e:
                logger.warning(f"Candidate extraction failed: {e}")
                candidate_memories = []

        # Step 4: Verify each candidate through MemoryGuard
        memory_decisions = []
        context = VerificationContext(
            deal_id=deal_id,
            rep_id=rep_id,
            conversation_id=conversation_id,
            turn_id=turn_id,
            existing_memories=[{
                "id": m.id,
                "text": m.text,
                "metadata": m.metadata,
            } for m in recalled],
            deal_stage=deal_stage,
            customer_name=customer_name or deal_id,
        )

        for candidate in candidate_memories:
            # Determine default scope from memory type
            default_scope = Scope.COMMON if candidate.memory_type == MemoryType.PATTERN else Scope.PROJECT

            decision = await memory_guard.verify(
                candidate=candidate,
                source_text=user_input,
                context=context,
                scope=default_scope,
            )
            memory_decisions.append(decision)

            # Step 5: Persist verified memories
            if decision.decision in (DecisionType.RETAIN, DecisionType.MERGE):
                target_bank = get_project_bank(deal_id) if decision.scope == Scope.PROJECT else get_common_bank(rep_id)

                now = datetime.utcnow()
                metadata = {
                    "memory_type": candidate.memory_type.value,
                    "scope": decision.scope.value,
                    "decision": decision.decision.value,
                    "confidence": decision.confidence,
                    "frequency": 1,
                    "evidence_count": len(decision.source_evidence),
                    "first_seen": now.isoformat(),
                    "last_seen": now.isoformat(),
                    "source_type": "conversation",
                    "source_id": conversation_id,
                    "conversation_id": conversation_id,
                    "turn_id": turn_id,
                    "source_quote": decision.source_evidence[0].quote if decision.source_evidence else user_input,
                    "provenance": decision.provenance.model_dump() if decision.provenance else {},
                    "conflicts": [c.conflicting_memory_id for c in decision.conflicts],
                    "similar_memories": [s.memory_id for s in decision.similar_memories],
                    "audit_id": decision.audit_id,
                }

                if decision.merge_instruction:
                    metadata["merge_policy"] = decision.merge_instruction.model_dump()

                # Serialize metadata for JSON
                metadata = self._serialize_metadata(metadata)

                await hindsight_client.retain(
                    bank_id=target_bank,
                    text=decision.memory_text,
                    metadata=metadata,
                    merge_policy=decision.merge_instruction.model_dump() if decision.merge_instruction else None,
                )

        latency_ms = int((time.time() - start_time) * 1000)

        return TurnResult(
            answer=response_text,
            retrieved_memories=[{
                "id": m.id,
                "text": m.text,
                "score": m.score,
                "metadata": m.metadata,
            } for m in recalled],
            candidate_memories=candidate_memories,
            memory_decisions=memory_decisions,
            audit_id=audit_id,
            latency_ms=latency_ms,
        )


agent_loop = AgentLoop()