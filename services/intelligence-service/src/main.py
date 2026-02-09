"""
Intelligence Service - Main FastAPI Application
Handles all ML/AI endpoints for ProjectMind
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from loguru import logger
import sys

from src.config.settings import settings
from src.api.v1.endpoints import predictions, skills, simulations, sentiment, health, insights
from src.api import conversation_routes
from src.ml.models.timeline_predictor import TimelinePredictor

# Configure logging
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level=settings.LOG_LEVEL
)
logger.add(
    "logs/intelligence_service.log",
    rotation="500 MB",
    retention="10 days",
    level="INFO"
)

# Global state for ML models
ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info("🚀 Starting Intelligence Service...")
    
    # Load ML models on startup
    try:
        logger.info("Loading ML models...")
        ml_models['timeline_predictor'] = TimelinePredictor()
        
        # Try to load pre-trained models
        try:
            ml_models['timeline_predictor'].load(f"{settings.ML_MODEL_PATH}/timeline_model.pkl")
            logger.success("✅ Loaded pre-trained timeline model")
        except FileNotFoundError:
            logger.warning("⚠️  No pre-trained timeline model found, using heuristics")
        
        logger.success("✅ All ML models loaded successfully")
    except Exception as e:
        logger.error(f"❌ Error loading ML models: {e}")
    
    yield
    
    # Cleanup on shutdown
    logger.info("🛑 Shutting down Intelligence Service...")
    ml_models.clear()

# Create FastAPI app
app = FastAPI(
    title="ProjectMind Intelligence Service",
    description="AI/ML Engine for project intelligence and predictions",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.SERVICE_NAME,
        "version": "1.0.0",
        "models_loaded": list(ml_models.keys())
    }

@app.get("/")
async def root():
    """Root endpoint with service info"""
    return {
        "service": "Intelligence Service",
        "description": "AI/ML Engine for ProjectMind",
        "version": "1.0.0",
        "endpoints": {
            "predictions": "/api/v1/predictions/*",
            "skills": "/api/v1/skills/*",
            "simulations": "/api/v1/simulations/*",
            "sentiment": "/api/v1/sentiment/*",
            "health": "/api/v1/health/*",
            "insights": "/api/v1/insights/*"
        },
        "docs": "/docs",
        "health": "/health"
    }

# Include routers
app.include_router(predictions.router, prefix="/api/v1", tags=["Predictions"])
app.include_router(skills.router, prefix="/api/v1", tags=["Skills"])
app.include_router(simulations.router, prefix="/api/v1", tags=["Simulations"])
app.include_router(sentiment.router, prefix="/api/v1", tags=["Sentiment"])
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(insights.router, prefix="/api/v1", tags=["Insights"])
app.include_router(conversation_routes.router, prefix="/api/v1", tags=["Conversation Intelligence"])


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.LOG_LEVEL == "DEBUG" else "An error occurred"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.SERVICE_PORT,
        reload=True,
        log_level=settings.LOG_LEVEL.lower()
    )
