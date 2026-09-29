import asyncio
import json
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.harness.agent_harness import agent_loop
from src.memory.schema import DecisionType


async def run_scenario(scenario_path: str):
    with open(scenario_path) as f:
        scenario = json.load(f)

    print(f"\n{'='*60}")
    print(f"SCENARIO: {scenario['scenario_id'].upper()} - {scenario['customer']}")
    print(f"{'='*60}")

    deal_id = scenario['deal_id']
    rep_id = scenario['rep_id']

    for turn in scenario['turns']:
        print(f"\n--- Turn {turn['turn_id']} ({turn['speaker']}) ---")
        print(f"Input: {turn['text']}")

        result = await agent_loop.process_turn(
            user_input=turn['text'],
            deal_id=deal_id,
            rep_id=rep_id,
            turn_id=turn['turn_id'],
            customer_name=scenario['customer'],
        )

        print(f"Agent: {result.answer[:200]}...")

        if result.memory_decisions:
            print(f"\n  Memory Decisions:")
            for dec in result.memory_decisions:
                badge = dec.decision.value.upper()
                print(f"    [{badge}] {dec.memory_text}")
                print(f"         Reason: {dec.reason}")
                print(f"         Scope: {dec.scope.value}, Confidence: {dec.confidence:.2f}")
                if dec.verification_status:
                    print(f"         Verification: {dec.verification_status.value}")
                if dec.merge_instruction:
                    print(f"         MERGE -> target: {dec.merge_instruction.target_memory_id[:8]}...")
        else:
            print("  No memory candidates extracted")

        if result.retrieved_memories:
            print(f"  Recalled {len(result.retrieved_memories)} memories")

    print(f"\n{'='*60}")
    print(f"SCENARIO COMPLETE: {scenario['scenario_id'].upper()}")
    print(f"{'='*60}\n")


async def main():
    print("MEMORYGUARD DEMO - Running All 5 Scenarios")
    print("=" * 60)

    scenarios_dir = Path(__file__).parent.parent / "scenarios"
    scenario_files = [
        "acme.json",
        "northwind.json",
        "globex.json",
        "initech.json",
        "umbrella.json",
    ]

    for sf in scenario_files:
        await run_scenario(str(scenarios_dir / sf))

    print("\n" + "="*60)
    print("ALL 5 SCENARIOS COMPLETE")
    print("="*60)
    print("HERO MOMENTS:")
    print("1. ACME: Consolidation - 'prefer email' x3 -> MERGE freq=3")
    print("2. NORTHWIND: Contamination - 'SOC2 mandatory' REJECTED")
    print("3. GLOBEX: Scope Isolation - Competitors stay in project")
    print("4. INITECH: Conflict - Salesforce -> HubSpot UPDATE")
    print("5. UMBRELLA: Lifecycle - SAML -> OIDC UPDATE, stakeholder change")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())