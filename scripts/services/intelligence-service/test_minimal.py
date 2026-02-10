from fastapi import FastAPI
from contextlib import asynccontextmanager
import sys

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("MIMINAL APP STARTING...")
    yield
    print("MINIMAL APP SHUTTING DOWN...")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "ok", "message": "Minimal app running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=4002)
