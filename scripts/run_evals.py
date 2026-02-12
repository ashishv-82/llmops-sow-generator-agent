#!/usr/bin/env python3
"""
Run LLM evaluation suite and generate report.

Usage:
    python scripts/run_evals.py
    python scripts/run_evals.py --output reports/eval_results.json
    python scripts/run_evals.py --compare-baseline baselines/v1.0.0.json
    python scripts/run_evals.py --save-baseline
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description="Run LLM evaluation suite")
    parser.add_argument(
        "--output",
        default="reports/eval_results.json",
        help="Output file for evaluation results"
    )
    parser.add_argument(
        "--compare-baseline",
        help="Baseline file to compare against"
    )
    parser.add_argument(
        "--save-baseline",
        action="store_true",
        help="Save results as new baseline"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output"
    )
    args = parser.parse_args()
    
    print("="*60)
    print("LLM Evaluation Suite")
    print("="*60)
    
    # Ensure output directory exists
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Run pytest with verbose output and capture results
    pytest_args = [
        "tests/evals/",
        "-v" if args.verbose else "-q",
        "--tb=short",
        "-m", "slow",  # Run only slow/eval tests
        f"--junit-xml={output_path.parent}/junit.xml"
    ]
    
    print(f"\nRunning evaluations...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest"] + pytest_args,
        capture_output=not args.verbose
    )
    
    # Parse results (simplified - in production would use pytest-json-report)
    eval_results = {
        "timestamp": datetime.now().isoformat(),
        "exit_code": result.returncode,
        "passed": result.returncode == 0,
        "command": " ".join(pytest_args)
    }
    
    # Save results
    with open(output_path, 'w') as f:
        json.dump(eval_results, f, indent=2)
    
    print(f"\n✓ Results saved to: {output_path}")
    
    # Compare to baseline if requested
    if args.compare_baseline:
        baseline_path = Path(args.compare_baseline)
        if baseline_path.exists():
            compare_results(output_path, baseline_path)
        else:
            print(f"⚠ Baseline file not found: {baseline_path}")
    
    # Save as new baseline if requested
    if args.save_baseline:
        save_baseline(output_path)
    
    return result.returncode


def compare_results(current_path: Path, baseline_path: Path):
    """Compare current results to baseline and highlight changes."""
    print(f"\n{'='*60}")
    print("Regression Analysis")
    print(f"{'='*60}")
    
    with open(current_path) as f:
        current = json.load(f)
    with open(baseline_path) as f:
        baseline = json.load(f)
    
    print(f"\nBaseline: {baseline_path.name} ({baseline.get('timestamp', 'unknown')})")
    print(f"Current:  {current_path.name} ({current.get('timestamp', 'unknown')})")
    
    current_passed = current.get("passed", False)
    baseline_passed = baseline.get("passed", False)
    
    if current_passed and not baseline_passed:
        print("\n✓ IMPROVEMENT: Tests now passing (were failing in baseline)")
    elif not current_passed and baseline_passed:
        print("\n✗ REGRESSION: Tests now failing (were passing in baseline)")
    elif current_passed:
        print("\n✓ STATUS: All tests passing (same as baseline)")
    else:
        print("\n✗ STATUS: Tests failing (same as baseline)")


def save_baseline(results_path: Path):
    """Save current results as a new baseline."""
    baseline_dir = Path("baselines")
    baseline_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    baseline_path = baseline_dir / f"baseline_{timestamp}.json"
    
    # Copy results to baseline
    with open(results_path) as f:
        results = json.load(f)
    
    with open(baseline_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Also save as "latest" baseline
    latest_path = baseline_dir / "baseline_latest.json"
    with open(latest_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Baseline saved to: {baseline_path}")
    print(f"✓ Latest baseline: {latest_path}")


if __name__ == "__main__":
    sys.exit(main())
