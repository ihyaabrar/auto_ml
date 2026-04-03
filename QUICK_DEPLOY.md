# 🚀 Quick Deploy - AutoML Platform

## ⚡ 2-Minute Setup

### Step 1: Login Railway
```
Buka: https://railway.app
Login dengan GitHub
```

### Step 2: Run Script
```powershell
cd c:\Users\WAYCOM\Downloads\auto_ml
.\deploy-railway.ps1
```

**DONE!** Script akan otomatis:
- ✅ Create project
- ✅ Setup PostgreSQL database
- ✅ Deploy backend
- ✅ Configure frontend
- ✅ Deploy ke Vercel

---

## 📖 Detailed Guide

Lihat dokumentasi lengkap di: **[DEPLOY_AUTOMATION.md](DEPLOY_AUTOMATION.md)**

---

## 🎯 Manual Setup (If Script Fails)

Panduan manual step-by-step ada di: **[RAILWAY_SETUP.md](RAILWAY_SETUP.md)**

---

## 💻 Local Development

Kalau mau test lokal dulu sebelum deploy:

### Frontend
```bash
cd frontend
npm run dev
# http://localhost:5176
```

### Backend (tanpa database)
```bash
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload
# http://localhost:8000
```

---

## 🌐 Production URLs

After deployment:

| Component | URL |
|-----------|-----|
| **Backend API** | `https://auto-ml-backend.up.railway.app` |
| **Frontend** | `https://auto-ml.vercel.app` |
| **Database** | PostgreSQL (Railway managed) |

---

## 🧪 Test Upload

```bash
curl -X POST \
  https://auto-ml-backend.up.railway.app/api/v1/projects/upload \
  -F "file=@sample_dataset.csv"
```

---

## 🔧 Scripts

| Script | Purpose |
|--------|---------|
| `deploy-railway.ps1` | Automated deployment (PowerShell) |
| `deploy-railway.sh` | Automated deployment (Bash) |

---

## 💰 Free Tier

- Railway: $5 credit/month (~500 hours)
- Vercel: Unlimited free tier
- **Total: $0/month** ✅

---

**Let's deploy! 🎉**
