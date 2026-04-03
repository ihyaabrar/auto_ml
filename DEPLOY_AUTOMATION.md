# 🚀 Automated Deployment - AutoML Platform

## ⚡ Quick Start (2 Steps!)

### Step 1: Login Railway (Manual)

**PILIH SALAH SATU:**

#### Option A: Via Browser (Recommended)
```
1. Buka: https://railway.app
2. Click "Login with GitHub"
3. Authorize access
```

#### Option B: Via CLI (If working)
```bash
railway login
```

---

### Step 2: Run Deployment Script

#### Windows PowerShell:
```powershell
cd c:\Users\WAYCOM\Downloads\auto_ml
.\deploy-railway.ps1
```

#### Git Bash / WSL:
```bash
cd /c/Users/WAYCOM/Downloads/auto_ml
bash deploy-railway.sh
```

---

## 📋 What the Script Does

The automated script will:

1. ✅ Check Railway login status
2. ✅ Create Railway project
3. ✅ Provision PostgreSQL database
4. ✅ Deploy backend service
5. ✅ Set environment variables
6. ✅ Get deployment URL
7. ✅ Configure frontend
8. ✅ Deploy to Vercel (optional)

**Total time:** ~5-10 minutes

---

## 🎯 Manual Alternative (If Script Fails)

If the automated script doesn't work, here's the manual process:

### 1. Login Railway
```
https://railway.app → Login with GitHub
```

### 2. Create Project
```
Dashboard → New Project → Deploy from GitHub repo
Select: ihyaabrar/auto_ml
Name: auto-ml-platform
```

### 3. Add Database
```
New → Database → PostgreSQL
Wait for provisioning
Copy DATABASE_URL from Variables tab
```

### 4. Deploy Backend
```
New → GitHub Repo (select same repo)
Settings tab:
  - Root Directory: backend
  - Build Command: pip install -r requirements.txt
  - Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT

Variables tab:
  - DATABASE_URL: <paste from step 3>
  - UPLOAD_DIR: ./uploads
  - MODELS_DIR: ./models
  - PYTHON_VERSION: 3.11
```

### 5. Get URL
After deployment completes:
```
https://auto-ml-backend-production.up.railway.app
```

### 6. Deploy Frontend
```bash
cd frontend
vercel login
vercel
```

Set environment variable in Vercel dashboard:
```
VITE_API_URL = https://auto-ml-backend-production.up.railway.app
```

---

## 🧪 Testing

After deployment, test the API:

```bash
curl -X POST \
  https://auto-ml-backend-production.up.railway.app/api/v1/projects/upload \
  -F "file=@sample_dataset.csv"
```

Expected response:
```json
{
  "id": 12345,
  "file_name": "sample_dataset.csv",
  "num_rows": 50,
  "num_cols": 8,
  "columns": [...]
}
```

---

## 🔧 Troubleshooting

### Script fails at "railway init"
```bash
# Make sure you're logged in
railway login

# Or manually create project in Railway dashboard first
```

### Database not provisioned
```bash
# Wait longer and re-run script
# Or manually add PostgreSQL from Railway dashboard
```

### Backend deployment fails
```bash
# Check logs in Railway dashboard
# Verify requirements.txt exists in backend/ folder
```

### Vercel deployment skipped
```bash
# Manual deploy:
cd frontend
vercel login
vercel --prod
```

---

## 💰 Cost Breakdown

| Service | Free Tier | Usage | Cost |
|---------|-----------|-------|------|
| **Railway** | $5 credit | Backend + DB | $0 |
| **Vercel** | Unlimited | Frontend | $0 |
| **Total** | | | **$0/month** |

---

## 📊 Post-Deployment Checklist

- [ ] Backend URL accessible
- [ ] Upload API works
- [ ] Frontend deployed to Vercel
- [ ] Frontend connects to backend
- [ ] Database is running
- [ ] Environment variables set correctly

---

## 🎉 Success Indicators

You'll know it's successful when:

✅ Railway dashboard shows:
- Backend service: Running
- PostgreSQL: Active
- Green checkmarks everywhere

✅ Can access:
- `https://your-backend.up.railway.app/api/v1/projects/upload`
- `https://your-app.vercel.app`

✅ Test upload returns JSON response with dataset info

---

## 📞 Need Help?

If you encounter issues:

1. Check Railway dashboard logs
2. Check Vercel deployment logs
3. Verify environment variables
4. Review error messages

Common fixes:
- Re-run the script
- Manually follow steps in documentation
- Check Railway/Vercel status pages

---

## 🔄 Redeploy

To redeploy after changes:

```bash
# Backend
cd backend
git push origin main
# Railway auto-deploys from GitHub

# Frontend
cd frontend
vercel --prod
```

---

**Happy Deploying! 🚀**
