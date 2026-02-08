from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.endpoints import jira, github, slack, calendar
from src.config.database import engine, Base
import time

# Initialize Database
Base.metadata.create_all(bind=engine)

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

# Register Routers
app.include_router(jira.router, prefix="/api/v1/jira", tags=["jira"])
app.include_router(github.router, prefix="/api/v1/github", tags=["github"])
app.include_router(slack.router, prefix="/api/v1/slack", tags=["slack"])
app.include_router(calendar.router, prefix="/api/v1/calendar", tags=["calendar"])

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
