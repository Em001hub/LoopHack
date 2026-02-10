# 🚀 Quick Start Guide - Person T ML Pipeline

## ⚡ **3-Step Quick Start** (No Database Required)

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

## 🎯 **How Many Terminals Do You Need?**

### **For Testing ML Components: 1 Terminal** ✅
Just run the 3 commands above sequentially in one terminal.

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

## 📊 **What You Get**

After running the 3 steps, you'll have:

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

## ✅ **Success Indicators**

You'll know it's working when you see:
- ✅ "🎉 DATA PREPARATION COMPLETE!"
- ✅ "🎉 TRAINING COMPLETE!"
- ✅ "🎉 ALL TESTS PASSED!"

---

**That's it! You're ready to go! 🚀**
