# Cloud Deployment Guide

This guide walks you through deploying your AI Psychologist application to cloud platforms so you can share it with teammates, clients, or your boss.

## 🎯 Quick Comparison

| Platform    | Best For                  | Free Tier             | Deploy Time | Difficulty      |
| ----------- | ------------------------- | --------------------- | ----------- | --------------- |
| **Railway** | Multi-service Docker apps | $5/month credit       | 5 min       | ⭐ Easy         |
| **Render**  | Individual microservices  | Limited (scales to 0) | 10 min      | ⭐⭐ Medium     |
| **Fly.io**  | Global edge deployment    | Limited               | 15 min      | ⭐⭐⭐ Advanced |

---

## 🚂 Option 1: Railway (Recommended - Easiest)

**Why Railway?**

- ✅ Native docker-compose support
- ✅ One-click deployment
- ✅ Automatic HTTPS & URLs
- ✅ Great for multi-service apps
- ⚠️ $5/month free credit (typically lasts 2-3 weeks for this app)

### Steps:

1. **Sign up for Railway**
   - Go to https://railway.app
   - Sign up with GitHub (recommended)

2. **Install Railway CLI** (optional but faster)

   ```powershell
   npm install -g @railway/cli
   railway login
   ```

3. **Deploy from dashboard** (easier for first time)
   - Click "New Project" → "Deploy from GitHub repo"
   - Connect your GitHub account
   - Push your code to GitHub:
     ```powershell
     git add .
     git commit -m "Prepare for Railway deployment"
     git push origin main
     ```
   - Select your repository
   - Railway auto-detects docker-compose.yml and deploys all services!

4. **Set environment variables**
   - In Railway dashboard, click on `rag-service`
   - Go to "Variables" tab
   - Add: `OPENAI_API_KEY` = your-openai-api-key
   - Click on `backend` service
   - Change `CORS_ORIGIN` to your frontend URL (Railway provides this)
   - Update `frontend` service
   - Change `VITE_API_BASE_URL` to your backend URL

5. **Access your app**
   - Railway generates URLs like: `https://your-app.up.railway.app`
   - Click on frontend service to get your public URL
   - Share this URL with your team! 🎉

### Cost Estimate (Railway):

- Free tier: $5/month credit
- Your app (4 services) ~= $10-15/month after free credit
- Starter plan: $5/month developer credit + usage

---

## 🟣 Option 2: Render (Free Tier Available)

**Why Render?**

- ✅ Generous free tier (services spin down after inactivity)
- ✅ Great documentation
- ✅ Individual service control
- ⚠️ No docker-compose support (deploy each service separately)
- ⚠️ Free tier: slow cold starts (30-60 seconds)

### Steps:

1. **Sign up for Render**
   - Go to https://render.com
   - Sign up with GitHub

2. **Push code to GitHub**

   ```powershell
   git add .
   git commit -m "Add Render configuration"
   git push origin main
   ```

3. **Deploy using Blueprint** (automated)
   - In Render dashboard, click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will detect `render.yaml` and create all 4 services automatically!

4. **Set secrets**
   - After deployment, go to `ai-psych-rag` service
   - Click "Environment" tab
   - Add `OPENAI_API_KEY` as a secret
   - Save changes (triggers redeploy)

5. **Initialize RAG data** (one-time setup - IMPORTANT!)
   - The RAG service needs DSM-5 documents in ChromaDB
   - SSH into rag-service:
     - In Render dashboard, click on `ai-psych-rag`
     - Click "Shell" tab
     - Run: `python scripts/ingest_pdf.py` (if you have this script)
   - OR: Upload pre-populated ChromaDB data

6. **Update CORS and API URLs**
   - Render auto-links services in blueprint, but verify:
   - Frontend should point to backend URL
   - Backend should allow frontend domain in CORS

7. **Access your app**
   - Frontend URL: `https://ai-psych-frontend.onrender.com`
   - Share this with your team!

### Important Notes for Render Free Tier:

- Services spin down after 15 minutes of inactivity
- First request after spindown takes 30-60 seconds to "wake up"
- Not recommended for production, but great for demos!

### Cost Estimate (Render):

- Free tier: $0/month (with cold starts)
- Paid tier: $7/month per service = $28/month for 4 services

---

## 🪂 Option 3: Fly.io (Advanced)

**Why Fly.io?**

- ✅ True free tier (persistent, no cold starts)
- ✅ Global edge deployment
- ✅ Excellent for Docker
- ⚠️ Requires more configuration

### Steps:

1. **Install flyctl CLI**

   ```powershell
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   ```

2. **Sign up**

   ```powershell
   fly auth signup
   fly auth login
   ```

3. **Deploy each service** (Fly.io doesn't support docker-compose directly)

   **NLP Service:**

   ```powershell
   cd nlp-service
   fly launch --name ai-psych-nlp --region ord
   # Follow prompts (say no to database)
   fly deploy
   cd ..
   ```

   **RAG Service:**

   ```powershell
   cd rag-service
   fly launch --name ai-psych-rag --region ord
   fly volumes create rag_data --size 1 --region ord
   # Edit fly.toml to mount volume
   fly deploy
   cd ..
   ```

   **Backend:**

   ```powershell
   cd backend
   fly launch --name ai-psych-backend --region ord
   fly secrets set NLP_SERVICE_URL=https://ai-psych-nlp.fly.dev
   fly secrets set RAG_SERVICE_URL=https://ai-psych-rag.fly.dev
   fly deploy
   cd ..
   ```

   **Frontend:**

   ```powershell
   cd frontend
   fly launch --name ai-psych-frontend --region ord
   fly secrets set VITE_API_BASE_URL=https://ai-psych-backend.fly.dev
   fly deploy
   cd ..
   ```

4. **Set secrets**

   ```powershell
   fly secrets set OPENAI_API_KEY=your-key --app ai-psych-rag
   ```

5. **Access your app**
   - URL: `https://ai-psych-frontend.fly.dev`

### Cost Estimate (Fly.io):

- Free tier: 3 shared-cpu VMs + 3GB storage = FREE for this project!
- Paid: ~$5-10/month for better performance

---

## 📝 Pre-Deployment Checklist

Before deploying to any platform:

- [ ] Push code to GitHub
- [ ] Commit the new files:
  ```powershell
  git add .
  git commit -m "Add cloud deployment configuration"
  git push origin main
  ```
- [ ] Have your OpenAI API key ready
- [ ] (Optional) Test locally first: `docker-compose up`
- [ ] Ensure RAG service has DSM-5 data or setup script

---

## 🔐 Environment Variables Summary

Make sure to set these in your chosen platform:

### NLP Service

- `HOST=0.0.0.0`
- `PORT=8000`
- `LOG_LEVEL=info`

### RAG Service

- `HOST=0.0.0.0`
- `PORT=8001`
- `OPENAI_API_KEY=<your-key>` ⚠️ SECRET
- `CHROMA_PERSIST_DIR=/data/chroma_db`

### Backend

- `PORT=3000`
- `NODE_ENV=production`
- `NLP_SERVICE_URL=<nlp-service-url>`
- `RAG_SERVICE_URL=<rag-service-url>`
- `CORS_ORIGIN=<frontend-url>`

### Frontend

- `VITE_API_BASE_URL=<backend-url>`

---

## 🎨 Sharing with Your Team

Once deployed, you can:

1. **Share the URL**
   - "Hey team, check out the app: https://your-app.com"

2. **Monitor logs**
   - All platforms provide log viewers
   - Railway: Click service → Logs
   - Render: Click service → Logs
   - Fly.io: `fly logs --app <app-name>`

3. **Update/Redeploy**

   ```powershell
   git add .
   git commit -m "Update feature X"
   git push origin main
   # Auto-deploys on Railway/Render (if configured)
   ```

4. **Share API endpoints**
   - Backend API: `https://your-backend.com/api/v1/health`
   - Swagger docs: `https://your-rag.com/docs`

---

## 🐛 Common Issues & Solutions

### Issue: "Service won't start"

**Solution:** Check logs for errors. Usually missing environment variables.

### Issue: "CORS errors in frontend"

**Solution:** Update `CORS_ORIGIN` in backend to match frontend URL.

### Issue: "Frontend shows blank page"

**Solution:** Check `VITE_API_BASE_URL` points to correct backend URL.

### Issue: "RAG service returns errors"

**Solution:**

1. Verify `OPENAI_API_KEY` is set
2. Check ChromaDB data is present
3. May need to run data ingestion

### Issue: "Slow response times" (Render free tier)

**Solution:** Services are "waking up" from sleep. Upgrade to paid tier or use Railway/Fly.io.

---

## 💡 My Recommendation

**For quick demo/testing (send to boss):**

- Use **Railway** - fastest & easiest
- Cost: Free for first 2-3 weeks with $5 credit

**For longer-term free hosting:**

- Use **Fly.io** - truly free tier, better performance
- Cost: $0/month

**For production:**

- Consider **Render paid tier** or **AWS ECS**
- Better uptime, monitoring, and support

---

## 🚀 Quick Start: Railway Deployment (5 Minutes)

```powershell
# 1. Make sure code is committed
git add .
git commit -m "Add cloud deployment config"

# 2. Push to GitHub
git push origin main

# 3. Go to railway.app
# 4. "New Project" → "Deploy from GitHub repo"
# 5. Select your repo → Railway auto-deploys!
# 6. Set OPENAI_API_KEY in rag-service environment
# 7. Share frontend URL with team! 🎉
```

---

## 📚 Additional Resources

- Railway Docs: https://docs.railway.app
- Render Docs: https://render.com/docs
- Fly.io Docs: https://fly.io/docs
- Docker Best Practices: https://docs.docker.com/develop/dev-best-practices/

---

**Need help?** Most platforms have excellent support:

- Railway: Discord community
- Render: Email support
- Fly.io: Community forum

Good luck with your deployment! 🚀
