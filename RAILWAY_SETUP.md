# 🚀 Railway Setup Manual - AutoML Platform

## Step 1: Login Railway

1. **Buka:** https://railway.app
2. **Click:** "Start a New Project" atau "Login"
3. **Pilih:** "Login with GitHub"
4. **Authorize:** Izinkan akses ke repository `ihyaabrar/auto_ml`

---

## Step 2: Buat Project Baru

1. **Dashboard Railway** → Click **"New Project"**
2. **Pilih:** "Deploy from GitHub repo"
3. **Select repo:** `ihyaabrar/auto_ml`
4. **Project name:** `auto-ml-platform`
5. **Click:** "Create Project"

---

## Step 3: Deploy PostgreSQL Database

1. Di project dashboard → **"New"** → **"Database"** → **"Add PostgreSQL"**
2. Tunggu provisioning selesai (~30 detik)
3. **Copy DATABASE_URL:**
   - Click service `postgres`
   - Tab **"Variables"**
   - Copy value dari `DATABASE_URL`
   - Format: `postgresql://postgres:password@...`

**Simpan URL ini!** Akan dipakai di step berikutnya.

---

## Step 4: Deploy Backend Service

### A. Add Service dari GitHub

1. Back ke project dashboard
2. **"New"** → **"GitHub Repo"**
3. Pilih lagi: `ihyaabrar/auto_ml`
4. **Service name:** `backend`

### B. Configure Settings

Click service `backend` → Tab **"Settings"**:

```
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### C. Set Environment Variables

Tab **"Variables"** → **"Add Variable"**:

| Variable Name | Value |
|---------------|-------|
| `DATABASE_URL` | Paste dari Step 3 |
| `UPLOAD_DIR` | `./uploads` |
| `MODELS_DIR` | `./models` |
| `PYTHON_VERSION` | `3.11` |

---

## Step 5: Deploy!

1. Tab **"Deployments"**
2. Click **"Deploy"** (atau auto-deploy kalau enabled)
3. Tunggu build selesai (~2-3 menit)

**Status:**
- ⏳ Building...
- ✅ Deployed!

### Get Public URL

Setelah deploy sukses, dapat URL:
```
https://auto-ml-backend-production.up.railway.app
```

**Test API:**
```
https://auto-ml-backend-production.up.railway.app/api/v1/projects/upload
```

---

## Step 6: Test Upload

Buka browser dan test:

```bash
curl -X POST \
  https://auto-ml-backend-production.up.railway.app/api/v1/projects/upload \
  -F "file=@sample_dataset.csv"
```

**Expected Response:**
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

## Step 7: Deploy Frontend ke Vercel

### Install & Login Vercel

```bash
cd frontend
vercel login
```

### Deploy

```bash
cd frontend
vercel
```

**Follow prompt:**

```
? Set up and deploy "~/Downloads/auto_ml/frontend"? [Y/n] y
? Which scope do you want to deploy to? [Your Name]
? Link to existing project? [y/N] n
? Want to override the settings? [y/N] n
? Framework Preset: Vite
? Build Command: npm run build
? Output Directory: dist
? Install Command: npm install
```

### Set Environment Variable

Di Vercel Dashboard project:

1. **Settings** → **Environment Variables**
2. **Add Variable:**
   ```
   Key: VITE_API_URL
   Value: https://auto-ml-backend-production.up.railway.app
   ```
3. **Redeploy** untuk apply changes

---

## Step 8: Update Frontend Code

Edit file: `frontend/src/services/api.ts`

```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
```

Commit & push:

```bash
git add .
git commit -m "Update API URL for production"
git push origin main
```

Vercel akan auto-redeploy!

---

## 🎉 DONE!

### URLs Anda:

| Component | URL | Status |
|-----------|-----|--------|
| **Frontend** | `https://auto-ml.vercel.app` | ✅ LIVE |
| **Backend** | `https://auto-ml-backend.railway.app` | ✅ LIVE |
| **Database** | PostgreSQL (Railway managed) | ✅ RUNNING |

### Test Full Flow:

1. Buka: `https://auto-ml.vercel.app`
2. Upload: `sample_dataset.csv`
3. Configure target column
4. Start training (akan muncul demo message)

---

## 💰 Cost: $0/month

- Railway: Free $5 credit (cukup untuk 500+ jam/bulan)
- Vercel: Free tier unlimited
- Total: **GRATIS!**

---

## 🔧 Troubleshooting

### Error: "DATABASE_URL not found"
- Pastikan environment variable sudah diset di Railway
- Redeploy backend setelah set variables

### Error: "Build failed"
- Check logs di Railway → Tab "Deployments"
- Pastikan `requirements.txt` ada di folder `backend/`

### Frontend tidak connect ke backend
- Pastikan `VITE_API_URL` di Vercel sudah benar
- Check CORS di backend (sudah enabled)

### Port conflict
- Railway otomatis assign port via `$PORT` environment variable
- Backend code sudah handle ini

---

## 📊 Monitoring

### Railway Dashboard
- Real-time logs
- Resource usage (CPU/RAM)
- Database size

### Vercel Dashboard
- Deployment history
- Analytics (optional)
- Function logs

---

## ✅ Checklist

- [ ] Login Railway dengan GitHub
- [ ] Create project dari repo
- [ ] Deploy PostgreSQL database
- [ ] Deploy backend service
- [ ] Set environment variables
- [ ] Test upload API
- [ ] Deploy frontend ke Vercel
- [ ] Set VITE_API_URL di Vercel
- [ ] Test full flow di browser

---

**Happy Deploying! 🚀**
