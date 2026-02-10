# 🚀 Intelligence Service - Quick Start Guide

## ✅ Running the Service (NO API Keys Required!)

The Intelligence Service works **out of the box** with smart defaults and heuristics. You don't need any API keys to run it!

### Start the Server

```bash
cd c:\Project\LoopHack\services\intelligence-service
uvicorn src.main:app --host 127.0.0.1 --port 4002 --reload
```

**Expected Startup Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:4002
INFO:     Started server process [XXXX]
2026-02-09 XX:XX:XX | INFO     | src.main:lifespan:29 - 🚀 Starting Intelligence Service lifespan...
2026-02-09 XX:XX:XX | INFO     | src.main:lifespan:34 - Loading Timeline Predictor...
2026-02-09 XX:XX:XX | SUCCESS  | src.main:lifespan:52 - ✅ Service startup sequence complete
INFO:     Application startup complete.
```

✅ **Service is ready!** Keep this terminal open.

### Test It (Open a NEW Terminal)

```bash
# 1. Check service health
curl http://localhost:4002/

# 2. Test timeline prediction
curl -X POST http://localhost:4002/api/v1/predict-timeline -H "Content-Type: application/json" -d "{\"project_id\":\"test-123\"}"

# 3. Test skill extraction
curl -X POST http://localhost:4002/api/v1/extract-skills -H "Content-Type: application/json" -d "{\"text\":\"Python developer with FastAPI experience\"}"
```

## 🔑 Optional Configuration

### When Do I Need API Keys?

**You DON'T need any API keys for:**
- ✅ Timeline predictions (uses ML heuristics)
- ✅ Skill extraction (keyword-based)
- ✅ Sentiment analysis (built-in models)
- ✅ All basic endpoints

**You ONLY need API keys if:**
- 🔹 **OpenAI API Key** - If you want GPT-powered insights (optional upgrade)
- 🔹 **Anthropic API Key** - If you want Claude-powered insights (optional upgrade)
- 🔹 **Database** - If you want to persist data (optional, uses in-memory by default)
- 🔹 **Redis** - If you want distributed caching (optional, uses in-memory by default)

### How to Get Optional API Keys

**OpenAI (Optional):**
1. Visit: https://platform.openai.com/api-keys
2. Sign up or log in
3. Create new API key
4. Copy and save it

**Anthropic Claude (Optional):**
1. Visit: https://console.anthropic.com/
2. Sign up or log in
3. Go to API Keys section
4. Create new key

### Setting Up .env File (Optional)

Only create this if you want to use advanced features:

```bash
# Copy the example
cp .env.example .env

# Edit and uncomment the keys you want to use
# Leave commented if you don't need them
```

## 📊 Access the API Documentation

Open in browser: **http://localhost:4002/docs**

This shows all available endpoints with interactive testing!

## ⚠️ Common Issues

**"Unable to connect to remote server"**
- The service stopped running. Just restart it with `uvicorn src.main:app --host 127.0.0.1 --port 4002 --reload`

**Port 4002 already in use**
- Use a different port: `uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload`

**ML model warnings**
- These are normal! The service falls back to heuristics and works perfectly fine.
