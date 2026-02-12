"""
Evaluation metrics for LLM-generated content.

Provides metrics for assessing:
- SOW generation quality (completeness, coverage, format)
- Compliance review accuracy (precision, recall, false positives)
- Research retrieval accuracy
"""

import re
from typing import List, Dict, Any, Tuple
from collections import defaultdict


# ====================
# SOW Generation Metrics
# ====================

def section_completeness(generated_sow: str, expected_sections: List[str]) -> float:
    """
    Calculate what percentage of expected sections are present in the SOW.
    
    Args:
        generated_sow: The generated SOW text
        expected_sections: List of required section names
        
    Returns:
        Float between 0 and 1 representing completeness
    """
    if not expected_sections:
        return 1.0
    
    # Normalize SOW text for matching
    sow_lower = generated_sow.lower()
    
    found_sections = 0
    for section in expected_sections:
        # Check if section appears as a header (## Section Name or # Section Name)
        section_pattern = re.escape(section.lower())
        if re.search(rf'#+ *{section_pattern}', sow_lower):
            found_sections += 1
    
    return found_sections / len(expected_sections)


def keyword_coverage(generated_sow: str, expected_keywords: List[str]) -> float:
    """
    Calculate what percentage of expected keywords appear in the SOW.
    
    Args:
        generated_sow: The generated SOW text
        expected_keywords: List of keywords that should appear
        
    Returns:
        Float between 0 and 1 representing keyword coverage
    """
    if not expected_keywords:
        return 1.0
    
    sow_lower = generated_sow.lower()
    found_keywords = sum(1 for kw in expected_keywords if kw.lower() in sow_lower)
    
    return found_keywords / len(expected_keywords)


def format_compliance(generated_sow: str) -> bool:
    """
    Check if SOW follows basic markdown formatting rules.
    
    Checks for:
    - At least one header (# or ##)
    - Reasonable structure (headers, paragraphs)
    - No egregious formatting issues
    
    Args:
        generated_sow: The generated SOW text
        
    Returns:
        True if format is compliant, False otherwise
    """
    if not generated_sow or len(generated_sow.strip()) < 100:
        return False
    
    # Check for headers
    has_headers = bool(re.search(r'^#+\s+.+$', generated_sow, re.MULTILINE))
    
    # Check for reasonable paragraph structure (not all one line)
    lines = generated_sow.strip().split('\n')
    has_paragraphs = len(lines) > 5
    
    # Basic structural check - not requiring empty lines since they might be in the test
    return has_headers and has_paragraphs


def length_check(generated_sow: str, min_words: int, max_words: int) -> bool:
    """
    Check if SOW length is within acceptable range.
    
    Args:
        generated_sow: The generated SOW text
        min_words: Minimum acceptable word count
        max_words: Maximum acceptable word count
        
    Returns:
        True if length is acceptable, False otherwise
    """
    word_count = len(generated_sow.split())
    return min_words <= word_count <= max_words


# ====================
# Compliance Review Metrics
# ====================

def issue_detection_accuracy(
    detected_issues: List[Dict[str, Any]], 
    expected_issues: List[Dict[str, Any]]
) -> Dict[str, float]:
    """
    Calculate precision and recall for issue detection.
    
    Args:
        detected_issues: List of issues found by the system
        expected_issues: List of ground-truth issues
        
    Returns:
        Dict with precision, recall, and f1_score
    """
    if not expected_issues:
        # If no issues expected, precision is 1.0 if none detected
        precision = 1.0 if not detected_issues else 0.0
        return {"precision": precision, "recall": 1.0, "f1_score": precision}
    
    if not detected_issues:
        # If issues expected but none detected, recall is 0
        return {"precision": 0.0, "recall": 0.0, "f1_score": 0.0}
    
    # Match issues by category and severity
    expected_set = {(issue["category"], issue["severity"]) for issue in expected_issues}
    detected_set = {(issue.get("category", ""), issue.get("severity", "")) for issue in detected_issues}
    
    true_positives = len(expected_set & detected_set)
    false_positives = len(detected_set - expected_set)
    false_negatives = len(expected_set - detected_set)
    
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score
    }


def false_positive_rate(
    detected_issues: List[Dict[str, Any]], 
    expected_issues: List[Dict[str, Any]]
) -> float:
    """
    Calculate false positive rate.
    
    Args:
        detected_issues: List of issues found by the system
        expected_issues: List of ground-truth issues
        
    Returns:
        Float representing false positive rate
    """
    if not detected_issues:
        return 0.0
    
    expected_set = {(issue["category"], issue["severity"]) for issue in expected_issues}
    detected_set = {(issue.get("category", ""), issue.get("severity", "")) for issue in detected_issues}
    
    false_positives = len(detected_set - expected_set)
    return false_positives / len(detected_issues)


def severity_correctness(
    detected_issues: List[Dict[str, Any]], 
    expected_issues: List[Dict[str, Any]]
) -> float:
    """
    Calculate percentage of issues with correct severity.
    
    Args:
        detected_issues: List of issues found by the system
        expected_issues: List of ground-truth issues
        
    Returns:
        Float between 0 and 1 representing severity accuracy
    """
    if not expected_issues or not detected_issues:
        return 0.0
    
    # Match by category, check severity
    expected_dict = {issue["category"]: issue["severity"] for issue in expected_issues}
    detected_dict = {issue.get("category", ""): issue.get("severity", "") for issue in detected_issues}
    
    correct_severity = 0
    for category, expected_sev in expected_dict.items():
        if detected_dict.get(category) == expected_sev:
            correct_severity += 1
    
    return correct_severity / len(expected_issues)


def score_accuracy(actual_score: float, expected_range: Tuple[float, float]) -> bool:
    """
    Check if compliance score is within expected range.
    
    Args:
        actual_score: Compliance score from the system
        expected_range: Tuple of (min, max) expected score
        
    Returns:
        True if score is within range, False otherwise
    """
    min_score, max_score = expected_range
    return min_score <= actual_score <= max_score


# ====================
# Research Metrics
# ====================

def retrieval_accuracy(results: List[Dict[str, Any]], expected_fields: List[str]) -> float:
    """
    Calculate what percentage of expected fields are present in results.
    
    Args:
        results: List of retrieved results
        expected_fields: List of fields that should be present
        
    Returns:
        Float between 0 and 1 representing field coverage
    """
    if not expected_fields:
        return 1.0
    
    if not results:
        return 0.0
    
    # Check first result for field presence
    first_result = results[0] if isinstance(results, list) else results
    
    found_fields = sum(1 for field in expected_fields if field in first_result)
    return found_fields / len(expected_fields)


def relevance_score(results: List[Dict[str, Any]], expected_keywords: List[str]) -> float:
    """
    Calculate relevance of results based on keyword presence.
    
    Args:
        results: List of retrieved results
        expected_keywords: Keywords that indicate relevance
        
    Returns:
        Float between 0 and 1 representing relevance
    """
    if not expected_keywords or not results:
        return 0.0
    
    # Combine all result content
    combined_content = " ".join(str(v) for r in results for v in r.values()).lower()
    
    matching_keywords = sum(1 for kw in expected_keywords if kw.lower() in combined_content)
    return matching_keywords / len(expected_keywords)


# ====================
# Aggregate Metrics
# ====================

def calculate_aggregate_metrics(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate aggregate statistics across multiple test results.
    
    Args:
        results: List of individual test results
        
    Returns:
        Dict with aggregate metrics (mean, min, max, pass rate)
    """
    if not results:
        return {}
    
    aggregates = defaultdict(list)
    
    for result in results:
        for key, value in result.items():
            if isinstance(value, (int, float, bool)):
                aggregates[key].append(float(value))
    
    summary = {}
    for metric, values in aggregates.items():
        summary[metric] = {
            "mean": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
            "count": len(values)
        }
    
    # Calculate overall pass rate if "pass" field exists
    if "pass" in aggregates:
        summary["pass_rate"] = sum(aggregates["pass"]) / len(aggregates["pass"])
    
    return summary


def compare_to_baseline(
    current_results: Dict[str, Any], 
    baseline_results: Dict[str, Any],
    threshold: float = 0.05
) -> Dict[str, Any]:
    """
    Compare current results to baseline and flag regressions.
    
    Args:
        current_results: Current evaluation metrics
        baseline_results: Baseline metrics to compare against
        threshold: Acceptable degradation threshold (default 5%)
        
    Returns:
        Dict with comparison results and regression flags
    """
    comparison = {
        "regressions": [],
        "improvements": [],
        "stable": []
    }
    
    for metric in baseline_results:
        if metric not in current_results:
            continue
        
        baseline_val = baseline_results[metric].get("mean", baseline_results[metric])
        current_val = current_results[metric].get("mean", current_results[metric])
        
        if isinstance(baseline_val, (int, float)) and isinstance(current_val, (int, float)):
            delta = current_val - baseline_val
            pct_change = (delta / baseline_val * 100) if baseline_val != 0 else 0
            
            result = {
                "metric": metric,
                "baseline": baseline_val,
                "current": current_val,
                "delta": delta,
                "pct_change": pct_change
            }
            
            if delta < -threshold:
                comparison["regressions"].append(result)
            elif delta > threshold:
                comparison["improvements"].append(result)
            else:
                comparison["stable"].append(result)
    
    comparison["has_regressions"] = len(comparison["regressions"]) > 0
    
    return comparison


def generate_report(results: Dict[str, Any], output_path: str) -> None:
    """
    Generate HTML or JSON report from evaluation results.
    
    Args:
        results: Evaluation results dictionary
        output_path: Path to save report
    """
    import json
    from pathlib import Path
    
    output_file = Path(output_path)
    
    if output_file.suffix == ".json":
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
    else:
        # Simple text report
        with open(output_file, 'w') as f:
            f.write("# Evaluation Report\n\n")
            for section, data in results.items():
                f.write(f"## {section}\n")
                f.write(f"{json.dumps(data, indent=2)}\n\n")
