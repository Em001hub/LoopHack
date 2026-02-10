# Intelligence Service - Verification Commands

## 🚀 Starting the Service

```bash
# Navigate to the service directory
cd c:\Project\LoopHack\services\intelligence-service

# Start the server
uvicorn src.main:app --host 127.0.0.1 --port 4002 --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:4002 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
2026-02-09 XX:XX:XX | INFO     | src.main:<module>:13 - Initializing Intelligence Service...
2026-02-09 XX:XX:XX | INFO     | src.main:lifespan:29 - 🚀 Starting Intelligence Service lifespan...
2026-02-09 XX:XX:XX | INFO     | src.main:lifespan:34 - Loading Timeline Predictor...
2026-02-09 XX:XX:XX | INFO     | src.main:lifespan:52 - ✅ Service startup sequence complete
INFO:     Application startup complete.
```

## ✅ Verification Commands (Run in a NEW terminal)

### 1. Check Service Health
```bash
curl http://localhost:4002/
```
**Expected Output:**
```json
{
  "message": "Welcome to intelligence-service",
  "docs": "/docs",
  "endpoints": [
    "/api/v1/predict-timeline",
    "/api/v1/extract-skills",
    "/api/v1/analyze-sentiment",
    "/health-check"
  ]
}
```

### 2. Test Timeline Prediction
```bash
curl -X POST http://localhost:4002/api/v1/predict-timeline -H "Content-Type: application/json" -d "{\"project_id\": \"test-123\"}"
```
**Expected Output:**
```json
{
  "predicted_completion_date": "2024-XX-XX",
  "predicted_weeks_remaining": X.X,
  "confidence_intervals": {...},
  "risk_factors": [...]
}
```

### 3. Test Skill Extraction
```bash
curl -X POST http://localhost:4002/api/v1/extract-skills -H "Content-Type: application/json" -d "{\"text\": \"Looking for a Python developer with FastAPI and Docker experience\"}"
```
**Expected Output:**
```json
{
  "skills": ["Python", "FastAPI", "Machine Learning", "Docker", "PostgreSQL"],
  "confidence_scores": {...},
  "categories": {...}
}
```

### 4. Test Sentiment Analysis
```bash
curl -X POST http://localhost:4002/api/v1/analyze-sentiment -H "Content-Type: application/json" -d "{\"text\": \"Great progress on the project today!\"}"
```
**Expected Output:**
```json
{
  "sentiment": "positive",
  "score": 0.75,
  "confidence": 0.88,
  "emotions": {...}
}
```

### 5. Run Demo Script (Tests All Endpoints)
```bash
python scripts/demo_endpoints.py
```
**Expected Output:**
```
╔═══════════════════════════════════════╗
║  Intelligence Service API Demo        ║
╚═══════════════════════════════════════╝

Testing Timeline Prediction...
✅ SUCCESS

Testing Skill Extraction...
✅ SUCCESS

Testing Sentiment Analysis...
✅ SUCCESS

[... more endpoint tests ...]

╔═══════════════════════════════════════╗
║  All Tests Completed Successfully!    ║
╚═══════════════════════════════════════╝
```

## 🎯 Key Indicators of Successful Changes

1. **✅ No Pydantic Errors**: Service starts without `TypeError: ForwardRef._evaluate()` errors
2. **✅ Python 3.12 Compatible**: All imports successful with warning logs for optional ML dependencies
3. **✅ Graceful Fallbacks**: ML models load or fallback to heuristics without crashing
4. **✅ All Routes Active**: `/api/v1/*` endpoints respond correctly
5. **✅ Auto-reload Works**: File changes trigger automatic server restart

## 📊 Access API Documentation

Open in browser: http://localhost:4002/docs

This shows the interactive Swagger UI with all available endpoints.
