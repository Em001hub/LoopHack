# 🚀 LoopHack - Complete Startup Guide

## 📋 Prerequisites

Before starting, ensure you have:
- ✅ Python 3.9+ installed
- ✅ Node.js 16+ and npm installed
- ✅ Git installed

---

## 🎯 Quick Start (3 Steps)

### Step 1: Start Intelligence Service (Backend)

```powershell
# Navigate to intelligence service
cd c:\Projects\LoopHack\services\intelligence-service

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Start the service
python -m uvicorn src.main:app --reload --port 8002
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8002
INFO:     Application startup complete.
```

**Verify:** Open http://localhost:8002/docs in browser

---

### Step 2: Start Frontend

```powershell
# Open NEW terminal
cd c:\Projects\LoopHack\frontend

# Start development server
npm run dev
```

**Expected Output:**
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

**Verify:** Open http://localhost:5173 in browser

---

### Step 3: Access the Applications

#### Main Dashboard
```
http://localhost:5173/
```

#### Intelligence Dashboard
```
http://localhost:5173/intelligence
```

#### Conversation Intelligence (NEW!)
```
http://localhost:5173/conversation
```

---

## 🧪 Testing

### Backend Tests

```powershell
cd c:\Projects\LoopHack\services\intelligence-service
.\.venv\Scripts\Activate.ps1
python -m pytest tests/ -v
```

**Expected:** All tests pass ✅

### Test NLP Components

```powershell
cd c:\Projects\LoopHack\services\intelligence-service
.\.venv\Scripts\Activate.ps1
python test_nlp_components.py
```

**Expected:** Decisions, questions, and entities extracted successfully ✅

### Frontend Build Test

```powershell
cd c:\Projects\LoopHack\frontend
npm run build
```

**Expected:** Build completes successfully ✅

---

## 📊 Features Overview

### 1. Intelligence Dashboard (`/intelligence`)
- **Timeline Predictions** - ML-powered project completion estimates
- **Team Sentiment Analysis** - Real-time morale tracking
- **Project Insights** - AI-generated recommendations
- **Monte Carlo Simulation** - Risk analysis and probability distributions
- **Risk Factors** - Automated risk detection

### 2. Conversation Intelligence (`/conversation`) 🆕
- **Decision Extraction** - Automatically extract decisions from conversations
- **Question Tracking** - Monitor unanswered questions with urgency levels
- **Entity Recognition** - Identify people, tasks, and technologies
- **Relationship Mapping** - Visualize connections between entities

---

## 🔧 API Endpoints

### Intelligence Service (Port 8002)

#### Core Endpoints
```
GET  /health                          - Health check
GET  /docs                            - API documentation
POST /api/v1/predict-timeline         - Timeline prediction
GET  /api/v1/team-sentiment/{id}      - Team sentiment
GET  /api/v1/project-insights/{id}    - Project insights
POST /api/v1/run-simulation           - Monte Carlo simulation
```

#### Conversation Intelligence (NEW!)
```
POST /api/v1/conversation/analyze-decisions    - Extract decisions
POST /api/v1/conversation/analyze-questions    - Detect questions
POST /api/v1/conversation/extract-entities     - Extract entities
POST /api/v1/conversation/analyze-full         - Complete analysis
```

---

## 🛠️ Troubleshooting

### Issue: Backend won't start

**Solution:**
```powershell
cd c:\Projects\LoopHack\services\intelligence-service
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn src.main:app --reload --port 8002
```

### Issue: Frontend won't start

**Solution:**
```powershell
cd c:\Projects\LoopHack\frontend
npm install
npm run dev
```

### Issue: Port already in use

**Solution:**
```powershell
# Find process using port 8002
netstat -ano | findstr :8002

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or use different port
python -m uvicorn src.main:app --reload --port 8003
```

### Issue: CORS errors

**Solution:** Backend already configured for CORS. Ensure backend is running before frontend.

---

## 📁 Project Structure

```
LoopHack/
├── frontend/                          # React frontend
│   ├── src/
│   │   ├── components/intelligence/  # Visualization components
│   │   ├── pages/                     # Page components
│   │   ├── services/                  # API clients
│   │   └── utils/                     # Utilities
│   ├── INTELLIGENCE_QUICKSTART.md     # Intelligence Dashboard guide
│   └── CONVERSATION_INTELLIGENCE_GUIDE.md  # Conversation guide
│
└── services/intelligence-service/     # Python backend
    ├── src/
    │   ├── api/                       # API routes
    │   ├── ml/models/                 # ML models
    │   ├── nlp/                       # NLP components (NEW!)
    │   ├── services/                  # Business logic
    │   └── simulation/                # Monte Carlo simulation
    ├── tests/                         # Test suite
    ├── README.md                      # Service documentation
    └── NLP_COMPONENTS_COMPLETE.md     # NLP documentation
```

---

## 🎨 Key Technologies

### Backend
- **FastAPI** - Modern Python web framework
- **scikit-learn** - Machine learning
- **NumPy/Pandas** - Data processing
- **Loguru** - Logging
- **spaCy** - NLP (optional)

### Frontend
- **React** - UI framework
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **Framer Motion** - Animations
- **Chart.js** - Data visualization
- **Axios** - HTTP client

---

## 📈 Sample Data

The application includes sample data for demonstration:

### Projects
- `proj_alpha` - Alpha Project
- `proj_beta` - Beta Project
- `proj_gamma` - Gamma Project

### Sample Conversation
8 messages demonstrating:
- 3 decisions (technical choices)
- 3 questions (2 unanswered)
- 9 entities (people, tasks, technologies)

---

## 🔐 Environment Variables

### Backend (`.env`)
```env
SERVICE_NAME=intelligence-service
SERVICE_PORT=8002
LOG_LEVEL=INFO
ML_MODEL_PATH=models
DATABASE_URL=postgresql://user:pass@localhost/loophack
```

### Frontend (`.env`)
```env
VITE_INTELLIGENCE_API_URL=http://localhost:8002/api/v1
```

---

## ✅ Success Checklist

- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Can access http://localhost:8002/docs
- [ ] Can access http://localhost:5173
- [ ] Intelligence Dashboard loads
- [ ] Conversation Intelligence loads
- [ ] API calls return data
- [ ] All tests pass

---

## 🎯 Next Steps

### 1. Customize Sample Data
Edit `ConversationIntelligence.jsx` to add your own messages

### 2. Integrate Real Data
Connect to:
- Slack API
- Microsoft Teams
- Jira
- GitHub

### 3. Deploy to Production
```powershell
# Build frontend
cd frontend
npm run build

# Serve with nginx or similar
```

---

## 📚 Documentation

- **Intelligence Dashboard:** `frontend/INTELLIGENCE_QUICKSTART.md`
- **Conversation Intelligence:** `frontend/CONVERSATION_INTELLIGENCE_GUIDE.md`
- **NLP Components:** `services/intelligence-service/NLP_COMPONENTS_COMPLETE.md`
- **API Documentation:** http://localhost:8002/docs (when running)

---

## 🆘 Support

### Common Commands

**Start Everything:**
```powershell
# Terminal 1: Backend
cd c:\Projects\LoopHack\services\intelligence-service
.\.venv\Scripts\Activate.ps1
python -m uvicorn src.main:app --reload --port 8002

# Terminal 2: Frontend
cd c:\Projects\LoopHack\frontend
npm run dev
```

**Stop Everything:**
- Press `Ctrl+C` in each terminal

**Run Tests:**
```powershell
# Backend tests
cd c:\Projects\LoopHack\services\intelligence-service
.\.venv\Scripts\Activate.ps1
python -m pytest tests/ -v

# NLP tests
python test_nlp_components.py

# Frontend build test
cd c:\Projects\LoopHack\frontend
npm run build
```

---

## 🎉 You're All Set!

Your LoopHack Intelligence Platform is ready to use with:
- ✅ ML-powered project predictions
- ✅ Real-time sentiment analysis
- ✅ AI conversation intelligence
- ✅ Beautiful visualizations
- ✅ Comprehensive testing

**Start exploring at:** http://localhost:5173

---

**Happy Coding!** 🚀✨
