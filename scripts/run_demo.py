#!/usr/bin/env python3
"""
Run MemoryGuard demo scenario.
"""

import asyncio
import argparse
import sys
from pathlib import Path

# Add src to path
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root / "src"))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

from harness.agent_harness import AgentLoop
from integrations.hindsight_client import HindsightClient
from integrations.groq_client import GroqClient
from memory.memory_guard import MemoryGuard
from harness.session import InMemorySessionStore
from integrations.config import Config


# Demo messages for each scenario
DEMO_MESSAGES = {
    "acme": [
        "We prefer email for deal communication.",
        "I still prefer email for updates.",
        "We are evaluating SOC2 compliance.",
        "What should I send next?",
    ],
    "northwind": [
        "We are evaluating SOC2 compliance for our vendor requirements.",
        "What should I send next?",
    ],
    "initech": [
        "SOC2 is not required for us right now.",
        "Actually, SOC2 is now required due to new policy.",
    ],
    "globex": [
        "We're evaluating Gong for conversation intelligence.",
        "Chorus is another option we're looking at.",
    ],
    "umbrella": [
        "I like getting SMS reminders for meetings.",
        "Actually, just email is fine for reminders now.",
    ],
}

DEAL_IDS = {
    "acme": "deal-acme-001",
    "globex": "deal-globex-001",
    "northwind": "deal-northwind-001",
    "initech": "deal-initech-001",
    "umbrella": "deal-umbrella-001",
}

REP_IDS = {
    "acme": "rep-001",
    "globex": "rep-002",
    "northwind": "rep-003",
    "initech": "rep-004",
    "umbrella": "rep-005",
}


async def run_demo(scenario: str, speed: float = 1.0):
    """Run demo scenario."""
    if scenario not in DEMO_MESSAGES:
        print(f"Unknown scenario: {scenario}")
        return
    
    messages = DEMO_MESSAGES[scenario]
    deal_id = DEAL_IDS[scenario]
    rep_id = REP_IDS[scenario]
    
    print(f"\n🎬 Running {scenario.upper()} demo")
    print(f"Deal: {deal_id}, Rep: {rep_id}")
    print("=" * 50)
    
    # Initialize components
    config = Config(MOCK_HINDSIGHT=True, MOCK_LLM=True)
    hindsight = HindsightClient(Config(MOCK_HINDSIGHT=True, MOCK_LLM=True))
    groq = GroqClient(Config(MOCK_HINDSIGHT=True, MOCK_LLM=True))
    memoryguard = MemoryGuard()  # TODO: inject proper dependencies
    session_store = InMemorySessionStore()
    
    loop = AgentLoop(hindsight, groq, MemoryGuard(), InMemorySessionStore())
    
    for i, message in enumerate(messages):
        print(f"\n👤 User: {message}")
        
        response = await loop.process_turn(message, deal_id, rep_id)
        
        print(f"🤖 Agent: {response.response_text}")
        print(f"   Candidates: {len(response.candidate_memories)}")
        for d in response.memory_decisions:
            print(f"   🛡️ {d.decision.value.upper()}: {d.memory_text[:60]}... (conf: {d.confidence:.0%})")
        
        # Simulate typing delay
        await asyncio.sleep(1.0 / speed)
    
    print(f"\n✅ {scenario.upper()} demo complete!")


def main():
    parser = argparse.ArgumentParser(description="Run MemoryGuard demo")
    parser.add_argument(
        "--scenario",
        choices=["acme", "northwind", "initech", "globex", "umbrella"],
        default="acme",
        help="Demo scenario to run"
    )
    parser.add_argument(
        "--speed",
        type=float,
        default=1.0,
        help="Demo speed multiplier"
    )
    
    args = parser.parse_args()
    
    asyncio.run(run_demo(args.scenario, args.speed))


if __name__ == "__main__":
    main()