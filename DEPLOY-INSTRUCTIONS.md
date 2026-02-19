# 🚀 Production Deployment Instructions

## ✅ Local Testing Complete

- Bug fixed: NLP symptom extraction now working
- Criteria Met now shows correct count (was 0, now shows actual detected symptoms)
- Changes committed and pushed to GitHub

---

## 📋 Deploy to Render (Production)

### Option 1: Auto-Deploy from GitHub (Recommended)

If you have auto-deploy enabled on Render:

1. **Go to your Render Dashboard**: https://dashboard.render.com
2. Your services should automatically detect the new commit
3. Wait for services to rebuild and deploy (5-10 minutes)
4. Services to watch:
   - `ai-psych-nlp` (must rebuild for the bug fix)
   - `ai-psych-backend` (will use updated NLP service)
   - `ai-psych-rag` (no changes needed)
   - `ai-psych-frontend` (no changes needed)

### Option 2: Manual Deploy

If auto-deploy is not enabled:

1. **Login to Render**: https://dashboard.render.com
2. **For each service**, click "Manual Deploy" → "Deploy latest commit"
3. **Deploy in this order**:
   - ✅ Deploy `ai-psych-nlp` first
   - ✅ Deploy `ai-psych-backend` second
   - ✅ Deploy `ai-psych-frontend` last

### Option 3: Use Render CLI

```powershell
# Install Render CLI (if not installed)
npm install -g @render/cli

# Login
render login

# Deploy all services
render deploy
```

---

## 🔍 Verify Production Deployment

### 1. Check Service Health

Visit your production URLs and check health endpoints:

- NLP Service: `https://ai-psych-nlp.onrender.com/health`
- RAG Service: `https://ai-psych-rag.onrender.com/health`
- Backend: `https://ai-psych-backend.onrender.com/api/v1/health`
- Frontend: `https://ai-psych-frontend.onrender.com`

### 2. Test Symptom Detection

1. Open your production frontend URL
2. Enter a test case with depression symptoms
3. Click "Analyze"
4. **Verify**: "Criteria Met" should show actual count (e.g., "5/5" or "6/5"), NOT "0/5"

### 3. Sample Test Text

Use this text to verify the fix:

```
I have been feeling depressed and sad for over a month. I lost interest in
activities I used to enjoy. I can't sleep well at night, and I've lost
significant weight. I feel worthless and guilty all the time. I can't
concentrate on my work anymore and have been thinking about death frequently.
```

**Expected Result**: Should show "6/5 Criteria Met" or similar

---

## ⚠️ Important: Set OpenAI API Key

If this is your first deployment or you haven't set it yet:

1. Go to Render Dashboard → `ai-psych-rag` service
2. Click "Environment" tab
3. Add/Update: `OPENAI_API_KEY` = `your-api-key-here`
4. Click "Save Changes"
5. Service will automatically redeploy

---

## 📊 Monitor Deployment

### Check Logs

In Render Dashboard, click each service → "Logs" tab to monitor:

- ✅ NLP service: Should show "Loaded X token patterns"
- ✅ Backend: Should show "NLP Service: http://nlp-service:8000"
- ✅ No errors during startup

### Common Issues

**If "Criteria Met" still shows 0:**

1. Check NLP service logs for errors
2. Verify backend is connecting to NLP service (check backend logs)
3. Ensure NLP service finished downloading spaCy model

**If deployment fails:**

1. Check service logs in Render dashboard
2. Verify all environment variables are set
3. Check if you're on free tier (services sleep after 15 min of inactivity)

---

## 🎉 Success Criteria

Your deployment is successful when:

- ✅ All 4 services show "Live" status on Render
- ✅ Frontend loads without errors
- ✅ Test assessment shows criteria count > 0
- ✅ AI Clinical Assessment section displays properly
- ✅ No errors in service logs

---

## 📝 Next Steps After Deployment

1. **Test thoroughly** with various symptom descriptions
2. **Share your production URL** with stakeholders
3. **Monitor usage** in Render dashboard
4. **Keep API keys secure** - never commit them to Git

---

## 💰 Cost Estimate (Render Free Tier)

- All services can run on free tier initially
- Free tier services sleep after 15 min inactivity (first request after wake = slow)
- Upgrade to Starter ($7/month per service) for:
  - No sleeping
  - Persistent storage for RAG service
  - Better performance

**Total cost**: $0/month (free) or $28/month (all services on Starter)
