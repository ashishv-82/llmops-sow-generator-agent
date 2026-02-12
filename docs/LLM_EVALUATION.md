# LLM Evaluation Framework

## Overview

This document describes the LLM evaluation framework for the SOW Generator Agent, including the types of evaluations performed, metrics used, results tracking, and optimization approach.

## Purpose

Traditional software testing validates that **code executes correctly**. LLM evaluation validates that **AI-generated content meets quality standards**. This framework provides:

1. **Quantitative metrics** for content quality
2. **Regression detection** when prompts or models change
3. **Baseline tracking** to measure improvements over time
4. **Automated quality gates** for CI/CD integration

---

## Evaluation Categories

### 1. SOW Generation Quality

**What we evaluate:** The quality of AI-generated Statements of Work

**Test cases:** 5 scenarios covering different industries and complexity levels
- Enterprise banking client (PCI-DSS, 99.9% SLA, migration)
- SMB fraud detection (basic implementation)
- Healthcare analytics (HIPAA compliance)
- Financial services (custom integrations)
- Edge case (minimal information)

**Metrics:**
- **Section Completeness** (40% weight): % of required sections present
  - Expected sections: Executive Summary, Scope, Deliverables, Timeline, SLA, Pricing, etc.
  - Target: ≥80% completeness
- **Keyword Coverage** (30% weight): % of expected technical/business keywords
  - Examples: "PCI-DSS", "99.9%", "uptime", "HIPAA", "encryption"
  - Target: ≥70% coverage
- **Format Compliance** (20% weight): Valid markdown structure with headers
  - Target: 100% compliance
- **Length Check** (10% weight): Appropriate word count (400-3000 words)
  - Target: Within specified range

**Overall Quality Score:** Weighted average of above metrics  
**Pass Threshold:** ≥70% quality score

**Files:**
- Dataset: [`tests/evals/eval_datasets/sow_creation_cases.json`](file:///Users/Ashish/GitHub%20Repos/llmops-sow-generator-agent/tests/evals/eval_datasets/sow_creation_cases.json)
- Test: [`tests/evals/test_sow_generation.py`](file:///Users/Ashish/GitHub%20Repos/llmops-sow-generator-agent/tests/evals/test_sow_generation.py)

---

### 2. Compliance Review Accuracy

**What we evaluate:** Accuracy of automated compliance issue detection

**Test cases:** 5 scenarios with varying compliance problems
- Clean SOW (no issues, should pass)
- Missing mandatory clause (liability)
- Prohibited terms ("unlimited liability")
- SLA violations (uptime below threshold)
- Multiple issues (combination)

**Metrics:**
- **Precision**: % of detected issues that are actually issues
  - Formula: True Positives / (True Positives + False Positives)
  - Target: ≥85%
- **Recall**: % of actual issues that were detected
  - Formula: True Positives / (True Positives + False Negatives)
  - Target: ≥85%
- **F1 Score**: Harmonic mean of precision and recall
  - Formula: 2 × (Precision × Recall) / (Precision + Recall)
  - Target: ≥70%
- **False Positive Rate**: % of detections that are incorrect
  - Target: ≤30%
- **Score Accuracy**: Compliance score within expected range
  - Target: 100% within ±20 points

**Pass Threshold:** F1 ≥70% AND FP Rate ≤30%

**Files:**
- Dataset: [`tests/evals/eval_datasets/sow_review_cases.json`](file:///Users/Ashish/GitHub%20Repos/llmops-sow-generator-agent/tests/evals/eval_datasets/sow_review_cases.json)
- Test: [`tests/evals/test_sow_review.py`](file:///Users/Ashish/GitHub%20Repos/llmops-sow-generator-agent/tests/evals/test_sow_review.py)

---

### 3. Research Tool Accuracy

**What we evaluate:** Accuracy and completeness of research tool outputs

**Test cases:** 6 scenarios covering different research tools
- CRM lookup (known client)
- CRM lookup (unknown client - error handling)
- Product KB search
- Opportunities retrieval
- Historical SOW search
- Compliance rules lookup

**Metrics:**
- **Field Coverage**: % of expected fields present in results
  - Target: ≥90%
- **Keyword Relevance**: % of expected keywords in results
  - Target: ≥70%
- **Error Handling**: Graceful handling of missing data
  - Target: No crashes, informative error messages

**Files:**
- Dataset: [`tests/evals/eval_datasets/research_cases.json`](file:///Users/Ashish/GitHub%20Repos/llmops-sow-generator-agent/tests/evals/eval_datasets/research_cases.json)

---

## Evaluation Infrastructure

### Metrics Module

[`tests/evals/metrics.py`](file:///Users/Ashish/GitHub%20Repos/llmops-sow-generator-agent/tests/evals/metrics.py) provides:

**Quality Metrics:**
- `section_completeness()` - SOW section coverage
- `keyword_coverage()` - Technical term presence
- `format_compliance()` - Markdown validation
- `length_check()` - Word count validation

**Accuracy Metrics:**
- `issue_detection_accuracy()` - Precision/recall/F1
- `false_positive_rate()` - Incorrect detection rate
- `severity_correctness()` - Severity level accuracy
- `score_accuracy()` - Score range validation

**Utilities:**
- `calculate_aggregate_metrics()` - Cross-test statistics
- `compare_to_baseline()` - Regression detection
- `generate_report()` - Export results

All metrics have unit tests: [`tests/evals/test_metrics.py`](file:///Users/Ashish/GitHub%20Repos/llmops-sow-generator-agent/tests/evals/test_metrics.py) (7/7 passing)

### Automation

[`scripts/run_evals.py`](file:///Users/Ashish/GitHub%20Repos/llmops-sow-generator-agent/scripts/run_evals.py) automates evaluation runs:

```bash
# Run evaluations
python scripts/run_evals.py

# Run and save as baseline
python scripts/run_evals.py --save-baseline

# Compare to baseline (detect regressions)
python scripts/run_evals.py --compare-baseline baselines/baseline_latest.json
```

**Features:**
- Automated pytest execution
- JSON result export
- Baseline comparison
- Regression flagging

---

## Current Status

### Infrastructure: ✅ Complete

- ✅ 16 evaluation test cases created
- ✅ Metrics module implemented (100% test coverage)
- ✅ Evaluation tests created (SOW generation, compliance review)
- ✅ Automation script ready
- ✅ Baseline tracking configured

### Baseline Results: 🔄 Pending Initial Run

**Status:** Infrastructure complete, awaiting first full evaluation run with real LLM

**Next Steps:**
1. Run initial evaluation: `python scripts/run_evals.py --save-baseline`
2. Analyze results and identify areas for improvement
3. Document baseline performance metrics
4. Establish performance targets

**Note:** Current tests use **mocked LLM responses** for validation. Production evaluation runs will use real AWS Bedrock calls.

---

## Optimization Approach

### When Evaluations Fail

Based on evaluation results, we can optimize the system through:

#### 1. Prompt Engineering (Most Common)

**If:** Section completeness is low (e.g., 60%)  
**Action:** Update prompts to explicitly request missing sections

**Example:**
```yaml
# Before
system_prompt: "Generate a professional SOW"

# After
system_prompt: |
  Generate a professional SOW with the following sections:
  1. Executive Summary
  2. Scope of Work
  3. Deliverables
  4. Timeline
  5. Service Level Agreement
  6. Pricing
  7. Security & Compliance
```

**Files to modify:** [`src/agent/prompts/system_prompt.yaml`](file:///Users/Ashish/GitHub%20Repos/llmops-sow-generator-agent/src/agent/prompts/system_prompt.yaml)

#### 2. Few-Shot Examples (For Complex Patterns)

**If:** Keyword coverage is low or format inconsistent  
**Action:** Add example SOWs to prompts

**Example:**
```yaml
examples:
  - input: "Banking client needing PCI-DSS compliance"
    output: |
      # Statement of Work: PCI-DSS Compliance Implementation
      
      ## Executive Summary
      Acme Bank requires PCI-DSS Level 1 compliance...
```

**Files to modify:** Add to [`src/agent/prompts/`](file:///Users/Ashish/GitHub%20Repos/llmops-sow-generator-agent/src/agent/prompts/)

#### 3. Retrieval Enhancement (For Accuracy Issues)

**If:** Generated content lacks technical details  
**Action:** Improve RAG retrieval or add more documentation

**Actions:**
- Index more historical SOWs
- Add product documentation to knowledge base
- Tune embedding model or chunk size

**Files to modify:** [`src/rag/indexer.py`](file:///Users/Ashish/GitHub%20Repos/llmops-sow-generator-agent/src/rag/indexer.py), RAG data files

#### 4. Tool Refinement (For Compliance Issues)

**If:** False positive rate is high (>30%)  
**Action:** Refine compliance detection logic

**Example:**
```python
# Before: Too strict, flags common terms
if "unlimited" in sow_text:
    flag_issue("Prohibited term: unlimited")

# After: More nuanced detection
if re.search(r"unlimited\s+(liability|responsibility)", sow_text):
    flag_issue("Prohibited term: unlimited liability")
```

**Files to modify:** [`src/agent/tools/compliance.py`](file:///Users/Ashish/GitHub%20Repos/llmops-sow-generator-agent/src/agent/tools/compliance.py)

#### 5. Model Selection (Last Resort)

**If:** All other optimizations fail to meet thresholds  
**Action:** Evaluate different LLM models

**Options:**
- More capable models (e.g., Claude 3.5 Sonnet vs Claude 3 Haiku)
- Specialized models (e.g., fine-tuned for legal/technical writing)
- Larger context windows (for longer SOWs)

**Files to modify:** [`src/agent/config.py`](file:///Users/Ashish/GitHub%20Repos/llmops-sow-generator-agent/src/agent/config.py) (model configuration)

### Iterative Improvement Process

```
1. Run Evaluation
   ↓
2. Analyze Results (which metrics failed?)
   ↓
3. Identify Root Cause (prompts? retrieval? logic?)
   ↓
4. Implement Fix (prompt tuning, code changes)
   ↓
5. Re-run Evaluation (compare to baseline)
   ↓
6. Save New Baseline (if improved)
   ↓
7. Repeat until thresholds met
```

---

## Fine-Tuning Status

### Current: ❌ No Fine-Tuning

We are using **prompt engineering** and **RAG** with pre-trained foundation models (AWS Bedrock Claude).

**Why no fine-tuning yet:**
- Foundation models (Claude 3.5 Sonnet) are very capable out-of-the-box
- Prompt engineering is faster and more cost-effective
- RAG provides domain-specific knowledge
- Fine-tuning requires large datasets and is expensive

### Future Considerations

**When fine-tuning might be needed:**
- Evaluation scores consistently <70% despite prompt optimization
- Need for highly specialized terminology or format
- Cost optimization (smaller fine-tuned model vs large foundation model)
- Regulatory requirements (on-prem model)

**Approach if fine-tuning needed:**
1. Collect high-quality training dataset (100+ SOW examples)
2. Evaluate fine-tuning vs continued prompt engineering
3. Use AWS Bedrock Custom Model Import or SageMaker
4. Re-run evaluations to validate improvement

---

## Regression Detection

### Baseline Tracking

Every evaluation run can be saved as a baseline:

```bash
python scripts/run_evals.py --save-baseline
```

This creates:
- `baselines/baseline_YYYYMMDD_HHMMSS.json` (timestamped)
- `baselines/baseline_latest.json` (always current)

### Detecting Regressions

Compare current run to baseline:

```bash
python scripts/run_evals.py --compare-baseline baselines/baseline_latest.json
```

**Output:**
- ✅ **Improvements:** Metrics better than baseline
- ⚠️ **Regressions:** Metrics worse than baseline (>5% degradation)
- ➡️ **Stable:** Metrics within ±5% of baseline

**Example:**
```
=== Regression Analysis ===
Baseline: baseline_20260212.json
Current:  eval_results.json

✓ IMPROVEMENT: section_completeness: 78% → 85% (+9%)
✗ REGRESSION: keyword_coverage: 82% → 71% (-13%)
➡️ STABLE: format_compliance: 100% → 100% (0%)
```

---

## Integration with CI/CD

### Recommended Workflow

```yaml
# .github/workflows/llm-eval.yml
name: LLM Evaluation

on:
  pull_request:
    branches: [main]
  schedule:
    - cron: "0 0 * * 0"  # Weekly

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Evaluations
        run: |
          python scripts/run_evals.py \
            --compare-baseline baselines/baseline_latest.json \
            --output reports/pr_eval.json
      
      - name: Check for Regressions
        run: |
          # Fail if regressions detected
          python scripts/check_regressions.py reports/pr_eval.json
```

**Benefits:**
- Catch quality regressions before merging
- Track LLM performance over time
- Automated quality gates

---

## Metrics Summary

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| SOW Section Completeness | ≥80% | Pending | 🔄 |
| SOW Keyword Coverage | ≥70% | Pending | 🔄 |
| SOW Format Compliance | 100% | Pending | 🔄 |
| SOW Pass Rate | ≥60% | Pending | 🔄 |
| Compliance Detection F1 | ≥70% | Pending | 🔄 |
| Compliance False Positive Rate | ≤30% | Pending | 🔄 |
| Research Field Coverage | ≥90% | Pending | 🔄 |

**Note:** First baseline run required to populate "Current" values.

---

## Next Steps

1. **Run Initial Baseline**
   ```bash
   python scripts/run_evals.py --save-baseline
   ```

2. **Analyze Results**
   - Review evaluation report
   - Identify failing metrics
   - Prioritize optimization areas

3. **Optimize System**
   - Update prompts for failing metrics
   - Enhance RAG for missing content
   - Refine compliance logic

4. **Track Improvements**
   - Re-run evaluations
   - Compare to baseline
   - Document changes in this file

5. **Integrate to CI/CD** (Phase 5)
   - Add GitHub Actions workflow
   - Set up automated regression checks
   - Configure alerts for quality issues

---

## References

- [Testing Framework Documentation](file:///Users/Ashish/GitHub%20Repos/llmops-sow-generator-agent/docs/TESTING.md)
- [Evaluation Metrics Source](file:///Users/Ashish/GitHub%20Repos/llmops-sow-generator-agent/tests/evals/metrics.py)
- [SOW Generation Eval](file:///Users/Ashish/GitHub%20Repos/llmops-sow-generator-agent/tests/evals/test_sow_generation.py)
- [Compliance Review Eval](file:///Users/Ashish/GitHub%20Repos/llmops-sow-generator-agent/tests/evals/test_sow_review.py)
- [Evaluation Runner Script](file:///Users/Ashish/GitHub%20Repos/llmops-sow-generator-agent/scripts/run_evals.py)

---

**Last Updated:** 2026-02-12  
**Status:** Infrastructure complete, awaiting initial evaluation run  
**Maintained By:** SOW Generator Team
