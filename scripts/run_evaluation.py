#!/usr/bin/env python3
"""
Run MemoryGuard evaluation.
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Add src to path
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root / "src"))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

from harness.eval_harness import run_evaluation


async def main():
    parser = argparse.ArgumentParser(description="Run MemoryGuard evaluation")
    parser.add_argument(
        "--scenario",
        choices=["acme", "globex", "northwind", "initech", "umbrella", "all"],
        default="all",
        help="Scenario to evaluate"
    )
    parser.add_argument(
        "--output",
        default="evaluation_results",
        help="Output directory for results"
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Run in mock mode (no API calls)"
    )
    parser.add_argument(
        "--charts",
        action="store_true",
        help="Generate charts"
    )
    
    args = parser.parse_args()
    
    print("📊 Running MemoryGuard Evaluation")
    print("=" * 50)
    
    report = await run_evaluation(
        scenarios_dir="src/data/scenarios",
        output_dir=args.output,
        mock=args.mock,
    )
    
    print(f"\n✅ Evaluation complete!")
    print(f"Results saved to: {args.output}/")
    
    # Print summary
    print(f"\nOverall Metrics:")
    print(f"  Precision: {report.metrics.precision:.1%}")
    print(f"  Hit Rate: {report.metrics.hit_rate:.1%}")
    print(f"  Merge Rate: {report.metrics.merge_rate:.1%}")
    print(f"  Contamination Rejection: {report.metrics.contamination_rejection_rate:.1%}")
    print(f"  Scope Isolation: {report.metrics.scope_isolation_rate:.1%}")


if __name__ == "__main__":
    asyncio.run(main())