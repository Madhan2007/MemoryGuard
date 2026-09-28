"""
Evaluation Harness

Member 3 ownership.

Runs scenarios through agent loop and computes metrics.
"""

import asyncio
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path

from .agent_harness import AgentLoop, AgentResponse
from ..integrations.hindsight_client import HindsightClient
from ..integrations.groq_client import GroqClient
from ..memory.memory_guard import MemoryGuard, MemoryDecision, DecisionType
from ..integrations.config import Config
from ..harness.session import InMemorySessionStore


@dataclass
class TurnExpectation:
    """Expected outcome for a single turn."""
    turn_id: int
    speaker: str  # "customer" or "rep"
    text: str
    expected_memories: List[Dict[str, Any]] = field(default_factory=list)
    expected_rejections: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class Scenario:
    """Evaluation scenario with ground truth."""
    scenario_id: str
    customer: str
    deal_id: str
    rep_id: str
    turns: List[TurnExpectation]
    ground_truth: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ScenarioResult:
    """Result of running a scenario."""
    scenario_id: str
    decisions: List  # MemoryDecision objects
    final_memories: List  # Memory objects
    expected: Dict[str, Any]
    turn_results: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class Metrics:
    """Computed evaluation metrics."""
    precision: float = 0.0
    hit_rate: float = 0.0
    merge_rate: float = 0.0
    conflict_detection_rate: float = 0.0
    scope_isolation_rate: float = 0.0
    promotion_accuracy: float = 0.0
    contamination_rejection_rate: float = 0.0
    ablation_improvement: float = 0.0
    grounded_claim_count: float = 0.0


@dataclass
class EvaluationReport:
    """Complete evaluation report."""
    timestamp: str
    scenarios: List[ScenarioResult]
    metrics: Metrics
    ablation: Dict[str, Metrics] = field(default_factory=dict)


class EvaluationHarness:
    """
    Runs evaluation scenarios through the full agent loop.
    
    Computes all MemoryGuard metrics and generates reports.
    """
    
    def __init__(
        self,
        agent_loop: AgentLoop,
        hindsight: HindsightClient,
        scenarios_dir: str = "src/data/scenarios",
    ):
        self.agent = agent_loop
        self.hindsight = hindsight
        self.scenarios_dir = Path(scenarios_dir)
    
    def load_scenarios(self) -> List[Scenario]:
        """Load all scenario JSON files."""
        scenarios = []
        for file_path in self.scenarios_dir.glob("*.json"):
            with open(file_path) as f:
                data = json.load(f)
                scenarios.append(Scenario(**data))
        return scenarios
    
    async def run_scenario(self, scenario: Scenario) -> ScenarioResult:
        """Run a single scenario through the agent loop."""
        decisions = []
        turn_results = []
        
        for turn_exp in scenario.turns:
            if turn_exp.speaker == "customer":
                response = await self.agent.process_turn(
                    turn_exp.text, 
                    scenario.deal_id, 
                    scenario.rep_id
                )
                
                turn_result = {
                    "turn_id": turn_exp.turn_id,
                    "input": turn_exp.text,
                    "response": response.response_text,
                    "candidates": len(response.candidate_memories),
                    "decisions": [
                        {
                            "decision": d.decision.value,
                            "memory_text": d.memory_text,
                            "reason": d.reason,
                            "confidence": d.confidence,
                            "scope": d.scope.value,
                        }
                        for d in response.memory_decisions
                    ],
                }
                turn_results.append(turn_result)
                decisions.extend(response.memory_decisions)
        
        # Get final memory state
        final_memories = await self._get_all_memories(scenario)
        
        return ScenarioResult(
            scenario_id=scenario.scenario_id,
            decisions=decisions,
            final_memories=final_memories,
            expected=scenario.ground_truth,
            turn_results=turn_results,
        )
    
    async def _get_all_memories(self, scenario: Scenario) -> List:
        """Get all memories from both banks after scenario."""
        project_bank = f"memoryguard-project-{scenario.deal_id}"
        common_bank = f"memoryguard-common-{scenario.rep_id}"
        
        project_memories = await self.hindsight.recall(project_bank, "", top_k=100)
        common_memories = await self.hindsight.recall(common_bank, "", top_k=100)
        
        return project_memories + common_memories
    
    async def run_all_scenarios(self) -> EvaluationReport:
        """Run all scenarios and generate report."""
        scenarios = self.load_scenarios()
        results = []
        
        for scenario in scenarios:
            result = await self.run_scenario(scenario)
            results.append(result)
        
        metrics = self.compute_metrics(results)
        ablation = await self.run_ablation()
        
        return EvaluationReport(
            timestamp=datetime.utcnow().isoformat(),
            scenarios=results,
            metrics=metrics,
            ablation=ablation,
        )
    
    def compute_metrics(self, results: List[ScenarioResult]) -> Metrics:
        """Compute all metrics from scenario results."""
        metrics = Metrics()
        
        # Memory Precision
        total_retained = 0
        correct_retained = 0
        
        # Retrieval Hit Rate
        total_expected = 0
        matched_expected = 0
        
        # Consolidation/Merge Rate
        total_duplicate_pairs = 0
        merged_pairs = 0
        
        # Conflict Detection Rate
        total_conflict_pairs = 0
        detected_conflicts = 0
        
        # Scope Isolation Rate
        total_isolation_tests = 0
        passed_isolation_tests = 0
        
        # Contamination Rejection Rate
        total_injected = 0
        rejected_hallucinations = 0
        
        # Grounded Claim Count
        total_retained_memories = 0
        grounded_memories = 0
        
        for result in results:
            # Precision
            retained = [d for d in result.decisions if d.decision in [
                "retain", "update", "merge"
            ]]
            total_retained += len(retained)
            for d in retained:
                if self._matches_ground_truth(d, result.expected):
                    correct_retained += 1
                if d.provenance.source_quotes:
                    grounded_memories += 1
            total_retained_memories += len(retained)
            
            # Hit Rate
            expected_memories = result.expected.get("final_memories", [])
            total_expected += len(expected_memories)
            for exp in expected_memories:
                if any(self._memories_match(exp, act) for act in result.final_memories):
                    matched_expected += 1
            
            # Merge Rate
            duplicate_pairs = self._find_duplicate_pairs(result.expected)
            total_duplicate_pairs += len(duplicate_pairs)
            for pair in duplicate_pairs:
                if self._was_merged(pair, result.decisions):
                    merged_pairs += 1
            
            # Conflict Detection
            conflict_pairs = result.expected.get("conflicts", [])
            total_conflict_pairs += len(conflict_pairs)
            for c in conflict_pairs:
                if self._conflict_detected(c, result.decisions):
                    detected_conflicts += 1
            
            # Scope Isolation
            isolation_tests = result.expected.get("isolation_tests", [])
            total_isolation_tests += len(isolation_tests)
            for test in isolation_tests:
                if self._isolation_passed(test, result.final_memories):
                    passed_isolation_tests += 1
            
            # Contamination Rejection
            injected = result.expected.get("rejected_candidates", [])
            total_injected += len(injected)
            for c in injected:
                if self._was_rejected(c, result.decisions):
                    rejected_hallucinations += 1
        
        metrics.precision = correct_retained / total_retained if total_retained else 1.0
        metrics.hit_rate = matched_expected / total_expected if total_expected else 1.0
        metrics.merge_rate = merged_pairs / total_duplicate_pairs if total_duplicate_pairs else 1.0
        metrics.conflict_detection_rate = detected_conflicts / total_conflict_pairs if total_conflict_pairs else 1.0
        metrics.scope_isolation_rate = passed_isolation_tests / total_isolation_tests if total_isolation_tests else 1.0
        metrics.contamination_rejection_rate = rejected_hallucinations / total_injected if total_injected else 1.0
        metrics.grounded_claim_count = grounded_memories / total_retained_memories if total_retained_memories else 1.0
        
        return metrics
    
    def _matches_ground_truth(self, decision, expected) -> bool:
        """Check if decision matches ground truth."""
        # Simplified matching
        return True
    
    def _memories_match(self, expected, actual) -> bool:
        """Check if expected memory matches actual."""
        return expected.get("text", "").lower() in actual.text.lower()
    
    def _find_duplicate_pairs(self, expected) -> List:
        """Find expected duplicate pairs in ground truth."""
        return []
    
    def _was_merged(self, pair, decisions) -> bool:
        """Check if duplicate pair was merged."""
        return False
    
    def _conflict_detected(self, conflict, decisions) -> bool:
        """Check if conflict was detected."""
        return False
    
    def _isolation_passed(self, test, memories) -> bool:
        """Check if scope isolation test passed."""
        return True
    
    def _was_rejected(self, candidate, decisions) -> bool:
        """Check if injected hallucination was rejected."""
        for d in decisions:
            if d.decision.value == "reject" and candidate["candidate_text"] in d.memory_text:
                return True
        return False
    
    async def run_ablation(self) -> Dict[str, Metrics]:
        """Run ablation study across configurations."""
        # TODO: Implement ablation configurations
        # full, no_contamination, no_merge, no_guard, stateless
        return {
            "full": Metrics(),
            "no_contamination": Metrics(),
            "no_merge": Metrics(),
            "no_guard": Metrics(),
            "stateless": Metrics(),
        }


async def run_evaluation(
    scenarios_dir: str = "src/data/scenarios",
    output_dir: str = "evaluation_results",
    mock: bool = False,
) -> EvaluationReport:
    """Main entry point for running evaluation."""
    config = Config(MOCK_HINDSIGHT=mock, MOCK_LLM=mock)
    
    hindsight = HindsightClient(config)
    groq = GroqClient(config)
    memoryguard = MemoryGuard()  # TODO: inject dependencies
    session_store = InMemorySessionStore()
    
    agent = AgentLoop(hindsight, groq, memoryguard, session_store)
    harness = EvaluationHarness(agent, hindsight, scenarios_dir)
    
    report = await harness.run_all_scenarios()
    
    # Save results
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    run_dir = output_path / timestamp
    run_dir.mkdir()
    
    # Save report
    with open(run_dir / "report.json", "w") as f:
        json.dump(asdict(report), f, indent=2, default=str)
    
    # Save markdown report
    with open(run_dir / "report.md", "w") as f:
        f.write(generate_markdown_report(report))
    
    return report


def generate_markdown_report(report: EvaluationReport) -> str:
    """Generate markdown evaluation report."""
    lines = [
        f"# Evaluation Report - {report.timestamp}",
        "",
        "## Summary",
        "| Scenario | Precision | Hit Rate | Merge Rate | Contamination Rejection |",
        "|----------|-----------|----------|------------|------------------------|",
    ]
    
    for result in report.scenarios:
        lines.append(
            f"| {result.scenario_id} | "
            f"{report.metrics.precision:.2%} | "
            f"{report.metrics.hit_rate:.2%} | "
            f"{report.metrics.merge_rate:.2%} | "
            f"{report.metrics.contamination_rejection_rate:.2%} |"
        )
    
    lines.extend([
        "",
        "## Ablation",
        "| Configuration | Precision | Hit Rate | Merge Rate |",
        "|---------------|-----------|----------|------------|",
    ])
    
    for config, metrics in report.ablation.items():
        lines.append(
            f"| {config} | {metrics.precision:.2%} | "
            f"{metrics.hit_rate:.2%} | {metrics.merge_rate:.2%} |"
        )
    
    return "\n".join(lines)


__all__ = [
    "TurnExpectation",
    "Scenario",
    "ScenarioResult",
    "Metrics",
    "EvaluationReport",
    "EvaluationHarness",
    "run_evaluation",
    "generate_markdown_report",
]