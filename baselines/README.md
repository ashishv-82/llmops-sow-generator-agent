# Baselines Directory

This directory stores baseline evaluation results for regression detection.

Baselines are JSON files containing evaluation metrics from previous runs. When running evaluations with `scripts/run_evals.py --compare-baseline`, the current results are compared against a baseline to detect performance regressions or improvements.

## Files

- `baseline_latest.json` - Most recent baseline (automatically updated with `--save-baseline`)
- `baseline_YYYYMMDD_HHMMSS.json` - Timestamped baselines

## Usage

```bash
# Run evals and save as baseline
python scripts/run_evals.py --save-baseline

# Compare current run to latest baseline
python scripts/run_evals.py --compare-baseline baselines/baseline_latest.json
```
