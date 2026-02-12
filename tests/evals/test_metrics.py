"""Tests for evaluation metrics."""
import pytest
from tests.evals.metrics import (
    section_completeness,
    keyword_coverage,
    format_compliance,
    length_check,
    issue_detection_accuracy,
    false_positive_rate,
    score_accuracy
)


def test_section_completeness():
    sow = "# SOW\n\n## Executive Summary\nContent\n\n## Scope of Work\nMore content"
    expected = ["Executive Summary", "Scope of Work", "Deliverables"]
    
    completeness = section_completeness(sow, expected)
    assert completeness == pytest.approx(2/3)  # 2 out of 3 sections found


def test_keyword_coverage():
    sow = "This SOW covers real-time payments with 99.9% uptime."
    keywords = ["real-time", "99.9%", "uptime", "blockchain"]
    
    coverage = keyword_coverage(sow, keywords)
    assert coverage == 0.75  # 3 out of 4 keywords found


def test_format_compliance():
    # Good SOW has headers, is long enough, has structure
    good_sow = """# Statement of Work

## Executive Summary
This is a paragraph.

## Scope of Work
Another paragraph here.

## Deliverables
Final paragraph content.
"""
    bad_sow = "Just one line of text"
    
    assert format_compliance(good_sow) is True
    assert format_compliance(bad_sow) is False


def test_length_check():
    sow = " ".join(["word"] * 600)
    
    assert length_check(sow, 500, 1000) is True
    assert length_check(sow, 700, 1000) is False
    assert length_check(sow, 100, 500) is False


def test_issue_detection_accuracy():
    detected = [
        {"category": "Mandatory Clause", "severity": "HIGH"},
        {"category": "SLA", "severity": "MEDIUM"}
    ]
    expected = [
        {"category": "Mandatory Clause", "severity": "HIGH"}
    ]
    
    accuracy = issue_detection_accuracy(detected, expected)
    
    assert accuracy["precision"] == 0.5  # 1 TP, 1 FP
    assert accuracy["recall"] == 1.0  # 1 TP, 0 FN


def test_false_positive_rate():
    detected = [
        {"category": "A", "severity": "HIGH"},
        {"category": "B", "severity": "MEDIUM"}
    ]
    expected = [
        {"category": "A", "severity": "HIGH"}
    ]
    
    fp_rate = false_positive_rate(detected, expected)
    assert fp_rate == 0.5  # 1 out of 2 is false positive


def test_score_accuracy():
    assert score_accuracy(75.0, (70, 80)) is True
    assert score_accuracy(85.0, (70, 80)) is False
    assert score_accuracy(65.0, (70, 80)) is False
