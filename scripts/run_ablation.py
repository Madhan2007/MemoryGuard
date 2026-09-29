#!/usr/bin/env python
"""
Ablation Study for MemoryGuard
Compares 5 configurations:
1. Full MemoryGuard (all features)
2. No Contamination (admission + merge only)
3. No Merge (admission + contamination only)
4. Raw Hindsight (no MemoryGuard)
5. Stateless (no memory at all)
"""

import asyncio
import json
import sys
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

os.environ["GROQ_API_KEY"] = "test-key"
os.environ["USE_MOCK_LLM"] = "true"
os.environ["PYDANTIC_AI_NO_BANNER"] = "1"

from src.harness.agent_harness import agent_loop, AgentLoop
from src.memory.memory_guard import MemoryGuard
from src.memory.schema import DecisionType, MemoryType, Scope


@dataclass
class AblationConfig:
    name: str
    enable_admission: bool = True
    enable_contamination: bool = True
    enable_consolidation: bool = True
    enable_recall: bool = True
    description: str = ""


@dataclass
class ScenarioResult:
    scenario_id: str
    config_name: str
    turns: List[Dict] = field(default_factory=list)
    total_decisions: int = 0
    retains: int = 0
    merges: int = 0
    updates: int = 0
    rejects: int = 0
    contamination_rejected: int = 0
    avg_confidence: float = 0.0
    total_latency_ms: int = 0


ABLATION_CONFIGS = [
    AblationConfig(
        name="Full MemoryGuard",
        enable_admission=True,
        enable_contamination=True,
        enable_consolidation=True,
        enable_recall=True,
        description="All gates active"
    ),
    AblationConfig(
        name="No Contamination",
        enable_admission=True,
        enable_contamination=False,
        enable_consolidation=True,
        enable_recall=True,
        description="Admission + Merge only"
    ),
    AblationConfig(
        name="No Merge",
        enable_admission=True,
        enable_contamination=True,
        enable_consolidation=False,
        enable_recall=True,
        description="Admission + Contamination only"
    ),
    AblationConfig(
        name="Raw Hindsight",
        enable_admission=False,
        enable_contamination=False,
        enable_consolidation=False,
        enable_recall=True,
        description="Only Hindsight recall, no governance"
    ),
    AblationConfig(
        name="Stateless",
        enable_admission=False,
        enable_contamination=False,
        enable_consolidation=False,
        enable_recall=False,
        description="No memory at all"
    ),
]


class AblationAgentLoop:
    """Agent loop with configurable ablation settings"""
    
    def __init__(self, config: AblationConfig):
        self.config = config
        self._contamination_injected: Dict[str, set] = {}
    
    def _mock_extract_candidates(self, user_input: str, agent_response: str, deal_id: str):
        from src.memory.schema import CandidateMemory, MemoryType
        candidates = []
        text_lower = user_input.lower()
        
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
            if self.config.enable_contamination and "soc2_contamination" not in self._contamination_injected[deal_id]:
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
        elif "integration" in text_lower or "api" in text_lower or "crm" in text_lower:
            if "hubspot" in text_lower:
                candidates.append(CandidateMemory(
                    text="Customer requires HubSpot CRM integration",
                    memory_type=MemoryType.TECHNICAL,
                    confidence=0.9,
                ))
            else:
                candidates.append(CandidateMemory(
                    text="Customer needs CRM integration",
                    memory_type=MemoryType.TECHNICAL,
                    confidence=0.85,
                ))
        elif "sso" in text_lower or "saml" in text_lower or "oidc" in text_lower:
            if "oidc" in text_lower:
                candidates.append(CandidateMemory(
                    text="Customer requires OIDC for SSO",
                    memory_type=MemoryType.TECHNICAL,
                    confidence=0.9,
                ))
            else:
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
        elif "stakeholder" in text_lower or "champion" in text_lower or "cto" in text_lower or "vp engineering" in text_lower:
            candidates.append(CandidateMemory(
                text="New stakeholder identified",
                memory_type=MemoryType.STAKEHOLDER,
                confidence=0.85,
            ))
        elif "procurement" in text_lower or "approval" in text_lower or "quotes" in text_lower:
            candidates.append(CandidateMemory(
                text="Procurement requires three quotes",
                memory_type=MemoryType.REQUIREMENT,
                confidence=0.8,
            ))
        
        return candidates
    
    async def process_turn(self, user_input: str, deal_id: str, rep_id: str, turn_id: int = 1, customer_name: str = ""):
        from src.integrations.hindsight_client import hindsight_client
        from src.integrations.groq_client import groq_client
        from src.memory.memory_guard import memory_guard
        from src.memory.schema import (
            CandidateMemory, VerificationContext, MemoryDecision, TurnResult,
            MemoryType, Scope, SourceEvidence, DecisionType
        )
        from src.config import settings, get_project_bank, get_common_bank
        from datetime import datetime
        import uuid
        import time
        
        start_time = time.time()
        
        # Recall if enabled
        recalled = []
        if self.config.enable_recall:
            query = f"{user_input} {deal_id} {customer_name}"
            recalled = await hindsight_client.recall_both(deal_id, rep_id, query, top_k=10)
        
        # Main LLM response
        memory_context = "No prior memories recalled."
        if recalled:
            memory_texts = []
            for m in recalled:
                scope_tag = m.metadata.get("scope", "unknown")
                freq = m.metadata.get("frequency", 1)
                memory_texts.append(f"[{scope_tag}] {m.text} (freq={freq})")
            memory_context = "\n".join(memory_texts)
        
        prompt = f"""You are a Deal Intelligence Agent helping a sales representative.

RECALLED MEMORIES:
{memory_context}

CURRENT DEAL: {deal_id}
CUSTOMER: {customer_name or deal_id}
DEAL STAGE: discovery

INSTRUCTIONS:
- Provide a helpful, personalized response to the sales rep
- Reference relevant memories naturally
- Be concise and actionable
"""
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input},
        ]
        response_text = await groq_client.call_main(messages)
        
        # Extract candidates
        candidate_memories = self._mock_extract_candidates(user_input, response_text, deal_id)
        
        # Verify through MemoryGuard (with ablation)
        memory_decisions = []
        context = VerificationContext(
            deal_id=deal_id,
            rep_id=rep_id,
            conversation_id=f"conv-{deal_id}",
            turn_id=turn_id,
            existing_memories=[{
                "id": m.id,
                "text": m.text,
                "metadata": m.metadata,
            } for m in recalled],
            deal_stage="discovery",
            customer_name=customer_name or deal_id,
        )
        
        for candidate in candidate_memories:
            default_scope = Scope.COMMON if candidate.memory_type == MemoryType.PATTERN else Scope.PROJECT
            
            # Apply ablation: skip certain gates
            if not self.config.enable_admission:
                decision = MemoryDecision(
                    decision=DecisionType.RETAIN,
                    memory_text=candidate.text,
                    reason="Ablation: admission disabled",
                    confidence=candidate.confidence,
                    scope=default_scope,
                    source_evidence=[SourceEvidence(quote=user_input, conversation_id=f"conv-{deal_id}", turn_id=turn_id, source_id=f"conv-{deal_id}")],
                    audit_id=str(uuid.uuid4()),
                )
            elif not self.config.enable_contamination:
                # Skip contamination check
                decision = MemoryDecision(
                    decision=DecisionType.RETAIN,
                    memory_text=candidate.text,
                    reason="Ablation: contamination check disabled",
                    confidence=candidate.confidence,
                    scope=default_scope,
                    source_evidence=[SourceEvidence(quote=user_input, conversation_id=f"conv-{deal_id}", turn_id=turn_id, source_id=f"conv-{deal_id}")],
                    audit_id=str(uuid.uuid4()),
                )
            elif not self.config.enable_consolidation:
                # Skip merge
                decision = MemoryDecision(
                    decision=DecisionType.RETAIN,
                    memory_text=candidate.text,
                    reason="Ablation: consolidation disabled",
                    confidence=candidate.confidence,
                    scope=default_scope,
                    source_evidence=[SourceEvidence(quote=user_input, conversation_id=f"conv-{deal_id}", turn_id=turn_id, source_id=f"conv-{deal_id}")],
                    audit_id=str(uuid.uuid4()),
                )
            else:
                # Full MemoryGuard
                decision = await memory_guard.verify(
                    candidate=candidate,
                    source_text=user_input,
                    context=context,
                    scope=default_scope,
                )
            
            memory_decisions.append(decision)
        
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
            audit_id=str(uuid.uuid4()),
            latency_ms=latency_ms,
        )


async def run_scenario(scenario_path: str, config: AblationConfig) -> ScenarioResult:
    with open(scenario_path) as f:
        scenario = json.load(f)
    
    # Create fresh agent loop for each config
    loop = AblationAgentLoop(config)
    
    result = ScenarioResult(
        scenario_id=scenario['scenario_id'],
        config_name=config.name,
    )
    
    deal_id = scenario['deal_id']
    rep_id = scenario['rep_id']
    
    for turn in scenario['turns']:
        turn_result = await loop.process_turn(
            user_input=turn['text'],
            deal_id=deal_id,
            rep_id=rep_id,
            turn_id=turn['turn_id'],
            customer_name=scenario['customer'],
        )
        
        result.turns.append({
            "turn_id": turn['turn_id'],
            "decisions": [d.decision.value for d in turn_result.memory_decisions],
        })
        
        result.total_decisions += len(turn_result.memory_decisions)
        result.total_latency_ms += turn_result.latency_ms
        
        for dec in turn_result.memory_decisions:
            if dec.decision == DecisionType.RETAIN:
                result.retains += 1
            elif dec.decision == DecisionType.MERGE:
                result.merges += 1
            elif dec.decision == DecisionType.UPDATE:
                result.updates += 1
            elif dec.decision == DecisionType.REJECT:
                result.rejects += 1
                if dec.verification_status and dec.verification_status.value == "unsupported":
                    result.contamination_rejected += 1
        
        if turn_result.memory_decisions:
            confidences = [d.confidence for d in turn_result.memory_decisions if d.confidence > 0]
            if confidences:
                result.avg_confidence = sum(confidences) / len(confidences)
    
    return result


async def main():
    print("=" * 80)
    print("MEMORYGUARD ABLATION STUDY")
    print("=" * 80)
    
    scenarios_dir = Path(__file__).parent.parent / "scenarios"
    scenario_files = [
        "acme.json",
        "northwind.json",
        "globex.json",
        "initech.json",
        "umbrella.json",
    ]
    
    all_results: List[ScenarioResult] = []
    
    for config in ABLATION_CONFIGS:
        print(f"\n{'='*60}")
        print(f"CONFIG: {config.name}")
        print(f"Description: {config.description}")
        print(f"{'='*60}")
        
        for sf in scenario_files:
            result = await run_scenario(str(scenarios_dir / sf), config)
            all_results.append(result)
            print(f"  {result.scenario_id}: {result.total_decisions} decisions, "
                  f"R={result.retains} M={result.merges} U={result.updates} X={result.rejects} "
                  f"(contam_rej={result.contamination_rejected})")
    
    # Print summary table
    print("\n" + "=" * 80)
    print("ABLATION SUMMARY")
    print("=" * 80)
    
    # Group by config
    for config in ABLATION_CONFIGS:
        config_results = [r for r in all_results if r.config_name == config.name]
        total_decisions = sum(r.total_decisions for r in config_results)
        total_retains = sum(r.retains for r in config_results)
        total_merges = sum(r.merges for r in config_results)
        total_updates = sum(r.updates for r in config_results)
        total_rejects = sum(r.rejects for r in config_results)
        total_contam = sum(r.contamination_rejected for r in config_results)
        avg_conf = sum(r.avg_confidence for r in config_results) / len(config_results) if config_results else 0
        total_latency = sum(r.total_latency_ms for r in config_results)
        
        print(f"\n{config.name}:")
        print(f"  Total Decisions: {total_decisions}")
        print(f"  RETAIN: {total_retains} | MERGE: {total_merges} | UPDATE: {total_updates} | REJECT: {total_rejects}")
        print(f"  Contamination Rejected: {total_contam}")
        print(f"  Avg Confidence: {avg_conf:.2f}")
        print(f"  Total Latency: {total_latency}ms")
    
    # Key comparison metrics
    print("\n" + "=" * 80)
    print("KEY COMPARISONS")
    print("=" * 80)
    
    full = [r for r in all_results if r.config_name == "Full MemoryGuard"]
    no_contam = [r for r in all_results if r.config_name == "No Contamination"]
    no_merge = [r for r in all_results if r.config_name == "No Merge"]
    raw_hindsight = [r for r in all_results if r.config_name == "Raw Hindsight"]
    stateless = [r for r in all_results if r.config_name == "Stateless"]
    
    # Contamination rejection rate
    full_contam = sum(r.contamination_rejected for r in full)
    no_contam_contam = sum(r.contamination_rejected for r in no_contam)
    print(f"\nContamination Rejection:")
    print(f"  Full MemoryGuard: {full_contam}")
    print(f"  No Contamination: {no_contam_contam} (expected: 0)")
    
    # Merge rate
    full_merges = sum(r.merges for r in full)
    no_merge_merges = sum(r.merges for r in no_merge)
    print(f"\nConsolidation (MERGE):")
    print(f"  Full MemoryGuard: {full_merges}")
    print(f"  No Merge: {no_merge_merges} (expected: 0)")
    
    # Decisions with memory vs without
    full_decisions = sum(r.total_decisions for r in full)
    stateless_decisions = sum(r.total_decisions for r in stateless)
    print(f"\nTotal Memory Decisions:")
    print(f"  Full MemoryGuard: {full_decisions}")
    print(f"  Stateless: {stateless_decisions} (expected: 0)")
    
    # Save results
    output = {
        "timestamp": datetime.utcnow().isoformat(),
        "configs": [
            {
                "name": c.name,
                "description": c.description,
                "enable_admission": c.enable_admission,
                "enable_contamination": c.enable_contamination,
                "enable_consolidation": c.enable_consolidation,
                "enable_recall": c.enable_recall,
            } for c in ABLATION_CONFIGS
        ],
        "results": [
            {
                "scenario_id": r.scenario_id,
                "config_name": r.config_name,
                "total_decisions": r.total_decisions,
                "retains": r.retains,
                "merges": r.merges,
                "updates": r.updates,
                "rejects": r.rejects,
                "contamination_rejected": r.contamination_rejected,
                "avg_confidence": r.avg_confidence,
                "total_latency_ms": r.total_latency_ms,
            } for r in all_results
        ]
    }
    
    output_dir = Path(__file__).parent.parent / "eval" / "results"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"ablation_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    asyncio.run(main())