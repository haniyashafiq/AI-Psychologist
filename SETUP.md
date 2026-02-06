# Setup Guide - AI Psychologist Depression Diagnosis System

Complete step-by-step guide to get the system running on your machine.

## Prerequisites

### Required Software

- **Node.js 18+**: [Download](https://nodejs.org/)
- **Python 3.10+**: [Download](https://www.python.org/downloads/)
- **Git**: [Download](https://git-scm.com/)
- **npm** (comes with Node.js)
- **pip** (comes with Python)

### System Requirements

- **RAM**: 4GB minimum (8GB recommended for smooth operation)
- **Disk Space**: ~2GB for dependencies and models
- **OS**: Windows 10+, macOS 10.15+, or Linux

---

## Installation Steps

### Step 1: Verify Prerequisites

Open a terminal/command prompt and verify installations:

```bash
node --version    # Should show v18.x or higher
python --version  # Should show 3.10.x or higher
npm --version     # Should show 9.x or higher
pip --version     # Should show 23.x or higher
```

### Step 2: Clone/Navigate to Project

```bash
cd d:\Projects\AI-Psychologist
```

### Step 3: Set Up Python NLP Service

```bash
# Navigate to NLP service directory
cd nlp-service

# Create virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Or on macOS/Linux:
# python3 -m venv venv
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy language model (685MB - will take a few minutes)
python -m spacy download en_core_web_md

# Verify installation
python -c "import spacy; nlp = spacy.load('en_core_web_md'); print('✓ spaCy model loaded successfully')"
```

**Expected Output**: `✓ spaCy model loaded successfully`

### Step 4: Set Up Backend API

```bash
# Open a NEW terminal window
cd d:\Projects\AI-Psychologist\backend

# Install dependencies
npm install

# Verify installation
npm list express
```

**Expected Output**: Should show `express@4.18.2` or similar

### Step 5: Set Up Frontend

```bash
# Open a NEW terminal window
cd d:\Projects\AI-Psychologist\frontend

# Install dependencies
npm install

# Verify installation
npm list react
```

**Expected Output**: Should show `react@18.2.0` or similar

---

## Running the Application

You'll need **3 terminal windows** running simultaneously.

### Terminal 1: Start NLP Service (Port 8000)

```bash
cd d:\Projects\AI-Psychologist\nlp-service
venv\Scripts\activate  # On macOS/Linux: source venv/bin/activate
python -m app.main
```

**Expected Output**:

```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test it**: Open browser to http://localhost:8000 - should see JSON response

### Terminal 2: Start Backend API (Port 3000)

```bash
cd d:\Projects\AI-Psychologist\backend
npm run dev
```

**Expected Output**:

```
🚀 Backend server running on port 3000
📍 Environment: development
🔗 NLP Service: http://localhost:8000
```

**Test it**: Open browser to http://localhost:3000/api/v1/health - should see health status

### Terminal 3: Start Frontend (Port 5173)

```bash
cd d:\Projects\AI-Psychologist\frontend
npm run dev
```

**Expected Output**:

```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

**Test it**: Browser should automatically open to http://localhost:5173

---

## Verification Checklist

### ✅ NLP Service Health Check

```bash
curl http://localhost:8000/health
```

**Expected Response**:

```json
{
  "status": "healthy",
  "service": "nlp-service",
  "version": "1.0.0",
  "spacy_model": "en_core_web_md",
  "spacy_model_loaded": true
}
```

### ✅ Backend Health Check

```bash
curl http://localhost:3000/api/v1/health
```

**Expected Response**:

```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "dependencies": {
      "nlpService": { "status": "healthy" }
    }
  }
}
```

### ✅ Full System Test

1. Open http://localhost:5173 in your browser
2. Click "Use Example" button to load sample text
3. Click "Analyze Symptoms"
4. Should see diagnostic report in < 2 seconds

**Expected Result**:

- Diagnosis shows MDD criteria met
- Severity: Moderate
- 7-8 symptoms detected
- Recommendations displayed

---

## Troubleshooting

### Problem: "Module not found" errors in Python

**Solution**:

```bash
cd nlp-service
venv\Scripts\activate
pip install -r requirements.txt --force-reinstall
```

### Problem: "spaCy model not found"

**Solution**:

```bash
python -m spacy download en_core_web_md
# If that fails, try:
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_md-3.7.1/en_core_web_md-3.7.1-py3-none-any.whl
```

### Problem: "Port already in use"

**Solution**:

```bash
# Windows - Kill process on port 8000:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

### Problem: "NLP service unavailable" in backend

**Checklist**:

1. Is NLP service running? Check Terminal 1
2. Can you access http://localhost:8000/health?
3. Check backend .env file - is `NLP_SERVICE_URL=http://localhost:8000`?

### Problem: Frontend shows connection error

**Checklist**:

1. Is backend running? Check Terminal 2
2. Can you access http://localhost:3000/api/v1/health?
3. Check frontend .env file - is `VITE_API_BASE_URL=http://localhost:3000`?
4. Check browser console for CORS errors

### Problem: Slow response times (> 5 seconds)

**Possible Causes**:

- First request after startup (cold start) - normal
- Large text input (> 2000 words) - consider splitting
- Low system RAM - close other applications
- Check NLP service logs for errors

---

## Alternative: Docker Setup (Optional)

If you have Docker installed, you can run everything with one command:

```bash
cd d:\Projects\AI-Psychologist
docker-compose up
```

**Note**: First build will take 10-15 minutes to download dependencies and models.

---

## Next Steps

Once everything is running:

1. **Try the Example**: Use the "Use Example" button to test the system
2. **Read Documentation**: Check `shared/docs/DSM5-MDD-Criteria.md` for details
3. **Run Test Cases**: Try examples from `shared/docs/Test-Cases.md`
4. **Customize**: Modify symptom patterns in `nlp-service/app/models/symptom_patterns.py`

---

## Quick Reference

| Service     | URL                   | Port | Purpose            |
| ----------- | --------------------- | ---- | ------------------ |
| Frontend    | http://localhost:5173 | 5173 | User interface     |
| Backend API | http://localhost:3000 | 3000 | REST API           |
| NLP Service | http://localhost:8000 | 8000 | Symptom extraction |

### Useful Commands

```bash
# Stop all services: Ctrl+C in each terminal

# View backend logs: Already visible in Terminal 2
# View NLP logs: Already visible in Terminal 1

# Clear backend cache:
cd backend && rm -rf node_modules && npm install

# Clear Python cache:
cd nlp-service && find . -type d -name __pycache__ -exec rm -r {} +

# Rebuild frontend:
cd frontend && npm run build
```

---

## Getting Help

If you encounter issues:

1. Check all three terminals for error messages
2. Verify all prerequisites are installed correctly
3. Ensure no firewall is blocking ports 3000, 5173, or 8000
4. Try restarting all services
5. Check the troubleshooting section above

---

**🎉 Congratulations!** If all three services are running and the health checks pass, your system is ready to use.

Start by opening http://localhost:5173 in your browser and trying the example symptom description!
