from fastapi import FastAPI
from src.config.settings import settings
from src.api.v1 import api_router

app = FastAPI(title="Integration Service")

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok"}
