from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI(
    title="ProjectMind Integration Service",
    description="Handles external API integrations for Jira, GitHub, Slack, etc.",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {
        "status": "UP",
        "service": "integration-service",
        "timestamp": time.time()
    }

@app.get("/api/v1")
async def root():
    return {"message": "ProjectMind Integration Service API v1"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
