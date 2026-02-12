"""
FastAPI main application.

Provides REST API for SOW Generator.
"""

import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import routers
from src.api.routes import research_router, sow_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="SOW Generator API",
    description="AI-powered Statement of Work generation and review",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS middleware for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "*"],  # Streamlit default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(sow_router)
app.include_router(research_router)


# Exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions gracefully."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions gracefully."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "details": str(exc)},
    )


# Health check endpoint
@app.get("/health")
@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "sow-generator-api",
        "version": "1.0.0",
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "SOW Generator API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "health": "/health",
    }


# API info endpoint
@app.get("/api/v1/info")
async def api_info():
    """API information and capabilities."""
    return {
        "version": "v1",
        "endpoints": {
            "sow": {
                "create": "POST /api/v1/sow/create",
                "review": "POST /api/v1/sow/review",
            },
            "research": {
                "client": "POST /api/v1/research/client",
                "product": "POST /api/v1/research/product",
            },
        },
        "features": [
            "SOW generation with quick draft or production quality",
            "Compliance review with severity-based findings",
            "Client research from CRM and historical data",
            "Product research from knowledge base",
        ],
    }
