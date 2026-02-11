"""
SOW endpoints: creation and review.
"""

import time
import logging
from fastapi import APIRouter, Depends, HTTPException
from src.api.schemas import (
    SOWCreateRequest,
    SOWCreateResponse,
    SOWReviewRequest,
    SOWReviewResponse,
    ComplianceIssue,
)
from src.api.dependencies import get_sow_agent
from src.agent.core import SOWAgent
from src.agent.tools.compliance import (
    check_mandatory_clauses_v2,
    check_prohibited_terms,
    check_sla_requirements,
)
from src.agent.tools.research import search_compliance_kb
from src.api.audit import audit_endpoint

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/sow", tags=["SOW"])


@router.post("/create", response_model=SOWCreateResponse)
@audit_endpoint("sow_create")
async def create_sow(
    request: SOWCreateRequest,
    agent: SOWAgent = Depends(get_sow_agent),
):
    """
    Generate a Statement of Work.
    
    Quality modes:
    - quick: Fast generation (15s, $0.06, 1 LLM call)
    - production: High-quality with reflection (35s, $0.23, 3 LLM calls)
    """
    logger.info(f"Creating SOW for client={request.client_id}, product={request.product}")
    
    start_time = time.time()
    
    try:
        # Build agent query
        query_parts = [
            f"Generate a Statement of Work for client {request.client_id}",
            f"for product {request.product}.",
        ]
        
        if request.requirements:
            query_parts.append(f"Additional requirements: {request.requirements}")
        
        # Specify quality mode
        if request.quality_mode == "production":
            query_parts.append(
                "Use the production quality generation tool with reflection for highest quality."
            )
        else:
            query_parts.append("Use quick draft generation for speed.")
        
        query = " ".join(query_parts)
        
        # Call agent
        logger.info(f"Calling agent with quality_mode={request.quality_mode}")
        response = agent.run(query)
        
        generation_time = time.time() - start_time
        
        # Estimate cost and LLM calls based on mode
        if request.quality_mode == "production":
            cost_usd = 0.23
            llm_calls = 3
        else:
            cost_usd = 0.06
            llm_calls = 1
        
        return SOWCreateResponse(
            sow_text=response,
            metadata={
                "client_id": request.client_id,
                "product": request.product,
                "quality_mode": request.quality_mode,
            },
            generation_time_seconds=round(generation_time, 2),
            cost_usd=cost_usd,
            llm_calls=llm_calls,
            quality_mode=request.quality_mode,
        )
        
    except Exception as e:
        logger.error(f"Error generating SOW: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate SOW: {str(e)}",
        )


@router.post("/review", response_model=SOWReviewResponse)
@audit_endpoint("sow_review")
async def review_sow(request: SOWReviewRequest):
    """
    Review a Statement of Work for compliance.
    
    Checks:
    - Mandatory clauses presence
    - Prohibited terms
    - SLA requirements (if product specified)
    """
    logger.info(f"Reviewing SOW (length={len(request.sow_text)} chars)")
    
    try:
        issues = []
        
        # Get compliance rules if client tier provided
        compliance_rules = {}
        if request.product and request.client_tier:
            compliance_rules = search_compliance_kb.invoke({
                "product": request.product,
                "client_tier": request.client_tier,
            })
        
        # Check 1: Mandatory clauses
        if compliance_rules.get("mandatory_clauses"):
            # Tool expects List[str], but rules contain Dicts. Extract names.
            mandatory_clauses = compliance_rules["mandatory_clauses"]
            requirements = [
                c["name"] if isinstance(c, dict) else str(c)
                for c in mandatory_clauses
            ]
            
            logger.info(f"DEBUG: Extracted {len(requirements)} requirements from rules.")
            if requirements:
                logger.info(f"DEBUG: First requirement type: {type(requirements[0])} val: {requirements[0]}")
            
            clause_check = check_mandatory_clauses_v2.invoke({
                "sow_text": request.sow_text,
                "requirements": requirements,
            })
            
            for missing in clause_check.get("missing_clauses", []):
                issues.append(
                    ComplianceIssue(
                        severity="HIGH",
                        category="Mandatory Clause",
                        description=f"Missing required clause: {missing}",
                        suggestion=f"Add clause: {missing}",
                    )
                )
        
        # Check 2: Prohibited terms
        prohibited_check = check_prohibited_terms.invoke({
            "sow_text": request.sow_text
        })
        
        for finding in prohibited_check.get("findings", []):
            issues.append(
                ComplianceIssue(
                    severity="HIGH",
                    category="Prohibited Term",
                    description=f"Found prohibited term: '{finding['term']}'",
                    location=f"Near: {finding.get('context', 'N/A')}",
                    suggestion=f"Remove or replace: {finding['term']}",
                )
            )
        
        # Check 3: SLA requirements
        if request.product and compliance_rules.get("sla_requirements"):
            sla_check = check_sla_requirements.invoke({
                "sow_text": request.sow_text,
                "product": request.product,
                "client_tier": request.client_tier or "MEDIUM",
            })
            
            for finding in sla_check.get("findings", []):
                issues.append(
                    ComplianceIssue(
                        severity=finding.get("severity", "MEDIUM"),
                        category="SLA",
                        description=finding.get("issue", "SLA violation"),
                        location=finding.get("location", "SLA Section"),
                        suggestion=finding.get("suggestion", "Review SLA terms"),
                    )
                )
        
        # Calculate summary
        summary = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for issue in issues:
            summary[issue.severity] += 1
        
        # Calculate compliance score (0-100)
        total_issues = len(issues)
        high_issues = summary["HIGH"]
        medium_issues = summary["MEDIUM"]
        
        # Scoring: -20 per HIGH, -10 per MEDIUM, -5 per LOW
        score = 100 - (high_issues * 20 + medium_issues * 10 + summary["LOW"] * 5)
        score = max(0, min(100, score))  # Clamp to 0-100
        
        # Determine status
        if score >= 90:
            status = "PASS"
        elif score >= 70:
            status = "WARNING"
        else:
            status = "FAIL"
        
        return SOWReviewResponse(
            compliance_score=score,
            status=status,
            issues=issues,
            summary=summary,
        )
        
    except Exception as e:
        logger.error(f"Error reviewing SOW: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to review SOW: {str(e)}",
        )
