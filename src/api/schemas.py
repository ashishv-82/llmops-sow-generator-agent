"""
Pydantic schemas for API request and response models.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# ============================================================================
# SOW Creation Schemas
# ============================================================================

class SOWCreateRequest(BaseModel):
    """Request model for SOW creation."""
    
    client_id: str = Field(..., description="Client ID from CRM")
    product: str = Field(..., description="Product name")
    requirements: Optional[str] = Field(
        None, description="Additional requirements or customizations"
    )
    quality_mode: str = Field(
        "production",
        description="Generation mode: 'quick' (15s, $0.06) or 'production' (35s, $0.23)",
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "client_id": "CLIENT-001",
                "product": "Real-Time Payments",
                "requirements": "Include migration plan, 6-month timeline",
                "quality_mode": "production",
            }
        }


class SOWCreateResponse(BaseModel):
    """Response model for SOW creation."""
    
    sow_text: str = Field(..., description="Generated SOW content")
    metadata: Dict[str, Any] = Field(..., description="Generation metadata")
    generation_time_seconds: float = Field(..., description="Time taken to generate")
    cost_usd: float = Field(..., description="Estimated cost in USD")
    llm_calls: int = Field(..., description="Number of LLM calls made")
    quality_mode: str = Field(..., description="Mode used for generation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "sow_text": "# Statement of Work\n\n## Executive Summary...",
                "metadata": {
                    "client": "Acme Financial Services",
                    "product": "Real-Time Payments",
                    "generated_at": "2026-02-07T19:15:00Z",
                },
                "generation_time_seconds": 34.5,
                "cost_usd": 0.23,
                "llm_calls": 3,
                "quality_mode": "production",
            }
        }


# ============================================================================
# SOW Review Schemas
# ============================================================================

class SOWReviewRequest(BaseModel):
    """Request model for SOW compliance review."""
    
    sow_text: str = Field(..., description="SOW content to review")
    product: Optional[str] = Field(
        None, description="Product name for SLA validation"
    )
    client_tier: Optional[str] = Field(
        None, description="Client tier (HIGH/MEDIUM/LOW) for compliance rules"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "sow_text": "# Statement of Work\n\nAcme Corp...",
                "product": "Real-Time Payments",
                "client_tier": "HIGH",
            }
        }


class ComplianceIssue(BaseModel):
    """Individual compliance issue."""
    
    severity: str = Field(..., description="Severity: HIGH, MEDIUM, LOW")
    category: str = Field(..., description="Issue category")
    description: str = Field(..., description="Issue description")
    location: Optional[str] = Field(None, description="Location in document")
    suggestion: Optional[str] = Field(None, description="Suggested fix")


class SOWReviewResponse(BaseModel):
    """Response model for SOW review."""
    
    compliance_score: int = Field(..., description="Overall score (0-100)")
    status: str = Field(..., description="PASS, WARNING, or FAIL")
    issues: List[ComplianceIssue] = Field(..., description="List of issues found")
    summary: Dict[str, int] = Field(..., description="Issue count by severity")
    
    class Config:
        json_schema_extra = {
            "example": {
                "compliance_score": 85,
                "status": "WARNING",
                "issues": [
                    {
                        "severity": "HIGH",
                        "category": "SLA",
                        "description": "Missing uptime SLA (99.9% required)",
                        "location": "Section 3",
                        "suggestion": "Add uptime commitment: 99.9%",
                    }
                ],
                "summary": {"HIGH": 2, "MEDIUM": 1, "LOW": 0},
            }
        }


# ============================================================================
# Research Schemas
# ============================================================================

class ClientResearchRequest(BaseModel):
    """Request model for client research."""
    
    client_name: Optional[str] = Field(None, description="Client name (partial match)")
    client_id: Optional[str] = Field(None, description="Exact client ID")
    
    class Config:
        json_schema_extra = {
            "example": {"client_name": "Acme"}
        }


class ClientResearchResponse(BaseModel):
    """Response model for client research."""
    
    client_data: Dict[str, Any] = Field(..., description="Client information from CRM")
    opportunities: List[Dict[str, Any]] = Field(
        ..., description="Past opportunities"
    )
    historical_sows: List[Dict[str, Any]] = Field(
        ..., description="Historical SOWs"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "client_data": {
                    "id": "CLIENT-001",
                    "name": "Acme Financial Services",
                    "industry": "Banking",
                    "size": "Enterprise",
                },
                "opportunities": [
                    {"id": "OPP-001", "name": "Data Migration", "value": 1200000}
                ],
                "historical_sows": [
                    {"id": "SOW-001", "product": "Real-Time Payments", "year": 2023}
                ],
            }
        }


class ProductResearchRequest(BaseModel):
    """Request model for product research."""
    
    product_name: str = Field(..., description="Product name")
    
    class Config:
        json_schema_extra = {
            "example": {"product_name": "Real-Time Payments"}
        }


class ProductResearchResponse(BaseModel):
    """Response model for product research."""
    
    product_info: Dict[str, Any] = Field(..., description="Product details")
    features: List[str] = Field(..., description="Key features")
    requirements: Dict[str, Any] = Field(
        ..., description="Technical requirements"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "product_info": {
                    "name": "Real-Time Payments",
                    "category": "Banking",
                    "pricing_model": "Transaction-based",
                },
                "features": [
                    "Instant payment processing",
                    "24/7 availability",
                    "Multi-currency support",
                ],
                "requirements": {
                    "deployment": "Cloud or On-Premise",
                    "integration": "REST API or SDK",
                },
            }
        }


# ============================================================================
# Error Response
# ============================================================================

class ErrorResponse(BaseModel):
    """Standard error response."""
    
    error: str = Field(..., description="Error message")
    status_code: int = Field(..., description="HTTP status code")
    details: Optional[str] = Field(None, description="Additional details")
