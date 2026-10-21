#!/usr/bin/env python3
"""
Global Economic Forecast Engine - Main FastAPI Application
AI-Powered Macroeconomic Intelligence & Forecasting Platform
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import routers
from app.api.routes import macro_api, forecasting_api, risk_api, news_api, country_api, sector_api
from app.db.database import DatabaseManager, get_db
from app.ingestion.data_ingestion import DataIngestionEngine
from app.analytics.correlation_analysis import CorrelationAnalyzer

# Global state for long-running processes
data_ingestion_engine = None
correlation_analyzer = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management"""
    global data_ingestion_engine, correlation_analyzer
    
    logger.info("Starting GEFE - Global Economic Forecast Engine")
    
    # Initialize database connection
    db_manager = await DatabaseManager.get_instance()
    await db_manager.initialize()
    
    # Initialize data ingestion engine
    data_ingestion_engine = DataIngestionEngine()
    await data_ingestion_engine.start_ingestion()
    
    # Initialize analytics engines
    correlation_analyzer = CorrelationAnalyzer()
    await correlation_analyzer.initialize()
    
    logger.info("GEFE initialized successfully")
    
    yield
    
    # Cleanup on shutdown
    logger.info("Shutting down GEFE services...")
    if data_ingestion_engine:
        await data_ingestion_engine.stop_ingestion()
    if correlation_analyzer:
        await correlation_analyzer.cleanup()
    await db_manager.close()


# Create FastAPI application
app = FastAPI(
    title="Global Economic Forecast Engine",
    description="AI-Powered Macroeconomic Intelligence & Forecasting Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(macro_api.router, prefix="/api/v1/macro", tags=["Macro Economics"])
app.include_router(forecasting_api.router, prefix="/api/v1/forecast", tags=["Forecasting"])
app.include_router(risk_api.router, prefix="/api/v1/risk", tags=["Risk Analysis"])
app.include_router(news_api.router, prefix="/api/v1/news", tags=["News Intelligence"])
app.include_router(country_api.router, prefix="/api/v1/country", tags=["Country Analysis"])
app.include_router(sector_api.router, prefix="/api/v1/sector", tags=["Sector Forecasts"])


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "GEFE",
        "version": "1.0.0"
    }


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc: Exception):
    """Handle unhandled exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        workers=4
    )
