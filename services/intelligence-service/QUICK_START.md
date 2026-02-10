# 🚀 Quick Start Guide - Intelligence Service

## ⚡ **Option 1: ML Pipeline Quick Start** (No Database Required)

Perfect for testing the ML components standalone.

### **Step 1: Prepare Data** (30 seconds)
```bash
cd c:\Projects\LoopHack\services\intelligence-service
python src/ml/training/data_preparation_standalone.py
```
**Output:** Creates 105 training samples (5 real + 100 synthetic)

---

### **Step 2: Train Model** (1-2 minutes)
```bash
python src/ml/training/train_timeline_standalone.py
```
**Output:** Trains Random Forest model, saves to `src/data/models/timeline_model.pkl`

---

### **Step 3: Test Everything** (5 seconds)
```bash
python test_ml_components.py
```
**Output:** Runs 7 tests, confirms everything works ✅

---

## 🚀 **Option 2: Full Service Quick Start**

Run the complete Intelligence Service with API endpoints.

### Step 1: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 2: Start the Service

Open a terminal in the `intelligence-service` folder and run:

```powershell
python -m uvicorn src.main:app --reload --port 4002
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:4002
INFO:     Application startup complete.
```

### Step 3: Test the API

Open your browser and go to:
- **API Documentation**: http://localhost:4002/docs
- **Health Check**: http://localhost:4002/health

### Step 4: Try the Demo Page (Optional)

1. Open `demo.html` in your browser (double-click the file)
2. The demo page will automatically connect to the service
3. Try the different tabs:
   - **Timeline Prediction**: Predict project completion dates
   - **Sentiment Analysis**: Analyze text sentiment
   - **Service Health**: Check service status

---

## 🎯 **How Many Terminals Do You Need?**

### **For Testing ML Components: 1 Terminal** ✅
Just run the 3 commands from Option 1 sequentially in one terminal.

### **For Full Application: 2-3 Terminals**

#### **Minimum (Backend Only): 2 Terminals**
1. **Terminal 1:** API Gateway (Port 8000)
   ```bash
   cd c:\Projects\LoopHack\services\api-gateway
   npm run dev
   ```

2. **Terminal 2:** Intelligence Service (Port 4002)
   ```bash
   cd c:\Projects\LoopHack\services\intelligence-service
   python -m uvicorn src.main:app --host 0.0.0.0 --port 4002 --reload
   ```

#### **Full Stack (With Frontend): 3 Terminals**
Add this third terminal:

3. **Terminal 3:** Frontend (Port 3000)
   ```bash
   cd c:\Projects\LoopHack\frontend
   npm run dev
   ```

---

## 📊 **Testing the API**

### Using the Swagger UI (http://localhost:4002/docs)

1. Click on any endpoint (e.g., `/api/v1/predict-timeline`)
2. Click "Try it out"
3. Modify the request body:
```json
{
  "project_id": "my_project_123",
  "target_date": "2024-12-31T00:00:00Z"
}
```
4. Click "Execute"
5. See the prediction results!

### Using curl

```bash
# Predict timeline
curl -X POST "http://localhost:4002/api/v1/predict-timeline" \
  -H "Content-Type: application/json" \
  -d '{"project_id": "test_123"}'

# Analyze sentiment
curl -X POST "http://localhost:4002/api/v1/analyze-sentiment" \
  -H "Content-Type: application/json" \
  -d '{"text": "The team is doing great!"}'

# Check health
curl "http://localhost:4002/health"
```

---

## 🎯 **What to Expect**

### Timeline Prediction Response
```json
{
  "project_id": "test_123",
  "predicted_completion_date": "2026-04-01T00:00:00",
  "predicted_weeks_remaining": 7.2,
  "confidence_intervals": {
    "p10": "2026-03-15T00:00:00",
    "p50": "2026-04-01T00:00:00",
    "p90": "2026-04-20T00:00:00"
  },
  "probability_on_time": null,
  "risk_factors": [
    "2 blocked tasks",
    "5 high-complexity tasks"
  ],
  "model_confidence": 0.6,
  "note": "Heuristic prediction (model not trained)"
}
```

### Sentiment Analysis Response
```json
{
  "sentiment": "positive",
  "score": 0.75,
  "confidence": 0.88,
  "emotions": {
    "joy": 0.6,
    "trust": 0.4,
    "anticipation": 0.3,
    "fear": 0.1
  }
}
```

---

## 📊 **What You Get**

After running Option 1 (ML Pipeline), you'll have:

✅ **Trained ML Model** - Ready to predict project timelines  
✅ **Training Data** - 105 samples split into train/val/test  
✅ **Visualizations** - Charts showing model performance  
✅ **Test Results** - Confirmation that everything works  

---

## 🎓 **Example Prediction**

```python
# Input: 100 story points, 5 team members, 20 points/week velocity
# Output: 7.3 weeks predicted timeline
```

---

## 🔧 **Troubleshooting**

### Service won't start?
```powershell
# Make sure dependencies are installed
pip install -r requirements.txt

# Check if port 4002 is available
netstat -ano | findstr :4002
```

### Demo page can't connect?
1. Make sure the service is running on port 4002
2. Check the browser console for errors (F12)
3. Verify the API_BASE URL in demo.html matches your service URL

### Import errors?
```powershell
# Run the simple test
python test_simple.py

# This will tell you which dependencies are missing
```

---

## ✅ **Success Indicators**

You'll know it's working when you see:
- ✅ "🎉 DATA PREPARATION COMPLETE!"
- ✅ "🎉 TRAINING COMPLETE!"
- ✅ "🎉 ALL TESTS PASSED!"
- ✅ "INFO: Application startup complete."

---

## 📚 **Next Steps**

1. **Explore the API**: http://localhost:4002/docs
2. **Read the README**: Complete documentation in README.md
3. **Run tests**: `python -m pytest tests/ -v`
4. **Train the ML model**: Follow Option 1 above
5. **Integrate with other services**: Use the API endpoints

---

## 🎉 **You're All Set!**

The Intelligence Service is now running and ready to provide AI-powered insights for your projects!

**Need help?** Check the README.md or IMPLEMENTATION_SUMMARY.md for detailed documentation.
