"""
Intelligence Service - Main FastAPI Application
Handles all ML/AI endpoints for ProjectMind
"""

import sys
import os
from loguru import logger
from datetime import datetime # Added datetime import

# Configure logging
logger.remove()
logger.add(sys.stderr, level="INFO")
logger.info("Initializing Intelligence Service...")

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from contextlib import asynccontextmanager
    
    from src.config.settings import settings
    
    # Global storage for models
    ml_models = {}

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """Startup and shutdown events"""
        logger.info("🚀 Starting Intelligence Service lifespan...")
        
        # Try to import and load ML models (optional/deferred)
        try:
            from src.ml.models.timeline_predictor import TimelinePredictor
            logger.info("Loading Timeline Predictor...")
            ml_models['timeline_predictor'] = TimelinePredictor()
            
            # Try to load pre-trained models
            model_file = f"{settings.ML_MODEL_PATH}/timeline_model.pkl"
            if os.path.exists(model_file):
                try:
                    ml_models['timeline_predictor'].load(model_file)
                    logger.success("✅ Loaded pre-trained timeline model")
                except Exception as e:
                    logger.warning(f"⚠️ Error loading model file: {e}")
            else:
                logger.info("ℹ️ No pre-trained model found, using heuristics")
            
        except Exception as e:
            logger.warning(f"⚠️ Timeline models not available or incompatible: {e}")
        
        # Load other services/ML if needed
        logger.success("✅ Service startup sequence complete")
        
        yield
        
        # Cleanup on shutdown
        logger.info("🛑 Shutting down Intelligence Service...")
        ml_models.clear()

    app = FastAPI(
        title=settings.SERVICE_NAME,
        description="AI/ML Intelligence Service for project management",
        version="1.0.0",
        lifespan=lifespan
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    logger.info("Including API routers...")
    from src.api.v1.endpoints import predictions, skills, simulations, sentiment, health, insights
    
    app.include_router(predictions.router, prefix="/api/v1", tags=["predictions"])
    app.include_router(skills.router, prefix="/api/v1", tags=["skills"])
    app.include_router(simulations.router, prefix="/api/v1", tags=["simulations"])
    app.include_router(sentiment.router, prefix="/api/v1", tags=["sentiment"])
    app.include_router(health.router, prefix="/api/v1", tags=["health"])
    app.include_router(insights.router, prefix="/api/v1", tags=["insights"])

    @app.get("/health")
    async def health():
        """Main health endpoint"""
        return {
            "status": "healthy",
            "service": settings.SERVICE_NAME,
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "models_loaded": list(ml_models.keys())
        }
    
    @app.get("/health-check")
    async def health_check_simple():
        return {
            "status": "up",
            "service": settings.SERVICE_NAME,
            "timestamp": os.environ.get("COMPUTERNAME", "unknown")
        }

    @app.get("/")
    async def root():
        return {
            "message": f"Welcome to {settings.SERVICE_NAME}",
            "docs": "/docs",
            "endpoints": [
                "/api/v1/predict-timeline",
                "/api/v1/extract-skills",
                "/api/v1/analyze-sentiment",
                "/health"
            ]
        }

except Exception as e:
    logger.critical(f"FATAL ERROR DURING INITIALIZATION: {e}")
    import traceback
    logger.critical(traceback.format_exc())
    # Minimal fallback app
    from fastapi import FastAPI
    app = FastAPI()
    @app.get("/")
    async def error_root():
        return {"error": "Initialization failure", "detail": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4002)
