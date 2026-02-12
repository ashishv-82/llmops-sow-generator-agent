"""
Evaluation tests for SOW compliance review accuracy.

Tests the accuracy of compliance issue detection across
multiple scenarios with varying complexity.
"""

import pytest
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.agent.tools.compliance import (
    check_mandatory_clauses_v2,
    check_prohibited_terms,
    check_sla_requirements
)
from tests.evals.metrics import (
    issue_detection_accuracy,
    false_positive_rate,
    score_accuracy
)


@pytest.fixture
def eval_cases():
    """Load SOW review evaluation cases."""
    cases_file = Path(__file__).parent / "eval_datasets" / "sow_review_cases.json"
    with open(cases_file) as f:
        return json.load(f)


@pytest.mark.slow
def test_compliance_review_accuracy(eval_cases):
    """
    Test compliance review accuracy across multiple scenarios.
    
   This test:
    1. Reviews SOWs for compliance
    2. Compares detected issues with expected issues
    3. Calculates precision, recall, and false positive rate
    4. Asserts minimum accuracy threshold is met
    """
    results = []
    
    for case in eval_cases:
        sow_text = case["sow_text"]
        product = case["product"]
        client_tier = case["client_tier"]
        
        # Run compliance checks
        mandatory_result = check_mandatory_clauses_v2.invoke({
            "sow_text": sow_text,
            "product": product,
            "client_tier": client_tier
        })
        
        prohibited_result = check_prohibited_terms.invoke({
            "sow_text": sow_text
        })
        
        sla_result = check_sla_requirements.invoke({
            "sow_text": sow_text,
            "product": product,
            "client_tier": client_tier
        })
        
        # Collect all detected issues
        detected_issues = []
        
        # Extract issues from mandatory clauses check
        if mandatory_result.get("missing_clauses"):
            for clause in mandatory_result["missing_clauses"]:
                detected_issues.append({
                    "category": "Mandatory Clause",
                    "severity": "HIGH",
                    "description": f"Missing: {clause}"
                })
        
        # Extract issues from prohibited terms check
        if prohibited_result.get("violations"):
            for violation in prohibited_result["violations"]:
                detected_issues.append({
                    "category": "Prohibited Term",
                    "severity": "HIGH",
                    "description": f"Found: {violation['term']}"
                })
        
        # Extract issues from SLA check
        if not sla_result.get("compliant", True):
            for issue in sla_result.get("issues", []):
                detected_issues.append({
                    "category": "SLA",
                    "severity": "HIGH",
                    "description": issue
                })
        
        # Calculate compliance score (simple scoring: 100 - 20 per issue, min 0)
        detected_score = max(0, 100 - len(detected_issues) * 20)
        
        # Evaluate against expected results
        expected_issues = case["expected_issues"]
        accuracy_metrics = issue_detection_accuracy(detected_issues, expected_issues)
        fp_rate = false_positive_rate(detected_issues, expected_issues)
        score_ok = score_accuracy(detected_score, case["expected_score_range"])
        
        test_passed = (
            accuracy_metrics["f1_score"] >= 0.7 and  # F1 score threshold
            fp_rate <= 0.3 and  # Max 30% false positives
            score_ok  # Score within expected range
        )
        
        result = {
            "test_id": case["test_id"],
            "description": case["description"],
            "precision": accuracy_metrics["precision"],
            "recall": accuracy_metrics["recall"],
            "f1_score": accuracy_metrics["f1_score"],
            "false_positive_rate": fp_rate,
            "score_correct": score_ok,
            "detected_score": detected_score,
            "pass": test_passed
        }
        results.append(result)
        
        # Print individual test results
        status = "✓ PASS" if test_passed else "✗ FAIL"
        print(f"\n{status} {case['test_id']}: {case['description']}")
        print(f"  F1: {accuracy_metrics['f1_score']:.1%}, " +
              f"Precision: {accuracy_metrics['precision']:.1%}, " +
              f"Recall: {accuracy_metrics['recall']:.1%}")
        print(f"  FP Rate: {fp_rate:.1%}, Score: {detected_score} " +
              f"(expected: {case['expected_score_range']})")
    
    # Calculate aggregate metrics
    pass_rate = sum(r["pass"] for r in results) / len(results)
    avg_f1 = sum(r["f1_score"] for r in results) / len(results)
    avg_precision = sum(r["precision"] for r in results) / len(results)
    avg_recall = sum(r["recall"] for r in results) / len(results)
    avg_fp_rate = sum(r["false_positive_rate"] for r in results) / len(results)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"Compliance Review Evaluation Summary")
    print(f"{'='*60}")
    print(f"Total tests: {len(results)}")
    print(f"Pass rate: {pass_rate:.1%}")
    print(f"Average F1 score: {avg_f1:.1%}")
    print(f"Average precision: {avg_precision:.1%}")
    print(f"Average recall: {avg_recall:.1%}")
    print(f"Average false positive rate: {avg_fp_rate:.1%}")
    
    # Assert minimum quality threshold
    assert pass_rate >= 0.6, (
        f"Compliance review pass rate {pass_rate:.1%} is below 60% threshold. "
        f"This indicates accuracy issues with compliance detection logic."
    )
    
    assert avg_f1 >= 0.7, (
        f"Average F1 score {avg_f1:.1%} is below 70% threshold. "
        f"Consider improving issue detection precision and recall."
    )
