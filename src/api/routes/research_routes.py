"""
Research endpoints: client and product information.
"""

import logging
from fastapi import APIRouter, HTTPException
from src.api.schemas import (
    ClientResearchRequest,
    ClientResearchResponse,
    ProductResearchRequest,
    ProductResearchResponse,
)
from src.agent.tools.research import (
    search_crm,
    search_opportunities,
    search_historical_sows,
    search_product_kb,
)
from src.api.audit import audit_endpoint

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/research", tags=["Research"])


@router.post("/client", response_model=ClientResearchResponse)
@audit_endpoint("research_client")
async def research_client(request: ClientResearchRequest):
    """
    Research client information.
    
    Retrieves:
    - Client data from CRM
    - Past opportunities
    - Historical SOWs
    """
    logger.info(f"Researching client: name={request.client_name}, id={request.client_id}")
    
    try:
        # Search CRM
        if request.client_id:
            # Direct lookup by ID
            client_data = search_crm.invoke({"client_name": request.client_id})
        elif request.client_name:
            # Search by name
            client_data = search_crm.invoke({"client_name": request.client_name})
        else:
            raise HTTPException(
                status_code=400,
                detail="Must provide either client_name or client_id",
            )
        
        if not client_data:
            raise HTTPException(
                status_code=404,
                detail=f"Client not found: {request.client_name or request.client_id}",
            )
        
        # Get opportunities
        opportunities = []
        if client_data.get("id"):
            opportunities = search_opportunities.invoke({
                "client_id": client_data["id"]
            })
        
        # Get historical SOWs
        historical_sows = []
        if client_data.get("id"):
            # Search for SOWs - this would use RAG retriever
            try:
                sow_results = search_historical_sows.invoke({
                    "client_id": client_data["id"],
                    "product": "",  # Get all products
                })
                
                # Format SOW results
                for sow in sow_results:
                    historical_sows.append({
                        "title": sow.get("metadata", {}).get("file_name", "Unknown"),
                        "product": sow.get("metadata", {}).get("product", "N/A"),
                        "year": sow.get("metadata", {}).get("year", "N/A"),
                    })
            except Exception as e:
                logger.warning(f"Could not retrieve historical SOWs: {e}")
                # Continue without SOWs
        
        return ClientResearchResponse(
            client_data=client_data,
            opportunities=opportunities,
            historical_sows=historical_sows,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error researching client: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to research client: {str(e)}",
        )


@router.post("/product", response_model=ProductResearchResponse)
@audit_endpoint("research_product")
async def research_product(request: ProductResearchRequest):
    """
    Research product information.
    
    Retrieves:
    - Product details from knowledge base
    - Features and capabilities
    - Technical requirements
    """
    logger.info(f"Researching product: {request.product_name}")
    
    try:
        # Search product KB
        product_info = search_product_kb.invoke({
            "product": request.product_name
        })
        
        if not product_info:
            raise HTTPException(
                status_code=404,
                detail=f"Product not found: {request.product_name}",
            )
        
        # Extract features from product info
        features = []
        if "features" in product_info:
            features = product_info["features"]
        elif "description" in product_info:
            # If no explicit features, extract from description
            features = [product_info["description"]]
        
        # Extract requirements
        requirements = {}
        if "technical_requirements" in product_info:
            requirements = product_info["technical_requirements"]
        if "deployment_model" in product_info:
            requirements["deployment"] = product_info["deployment_model"]
        
        return ProductResearchResponse(
            product_info={
                "name": product_info.get("name", request.product_name),
                "category": product_info.get("category", "N/A"),
                "pricing_model": product_info.get("pricing_model", "Contact Sales"),
            },
            features=features,
            requirements=requirements,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error researching product: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to research product: {str(e)}",
        )
