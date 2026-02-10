
import sys
import os
import traceback

# Ensure the project root is in path
sys.path.append(os.getcwd())

try:
    print("Testing imports...")
    from src.config.settings import settings
    from src.main import app
    print("Imports successful!")
    
    import uvicorn
    print(f"Starting uvicorn on port {settings.SERVICE_PORT}...")
    uvicorn.run(app, host="127.0.0.1", port=4002, log_level="debug")
except Exception as e:
    print(f"FAILED TO START SERVER: {e}")
    traceback.print_exc()
