# 🚀 Manual Railway Deployment Guide

## ✅ Step-by-Step (Paling Mudah!)

Karena Anda sudah punya deployments sebelumnya, kita akan gunakan project yang ada.

---

### **Step 1: Buka Railway Dashboard**

Anda punya 2 deployments aktif:
- **beneficial-wisdom / production**
- **ample-trust / production**

**Buka:** https://railway.app/dashboard

---

### **Step 2: Pilih atau Buat Project Baru**

#### Option A: Gunakan Project Yang Ada
Jika salah satu dari 2 deployments Anda adalah auto_ml:

1. Click project `beneficial-wisdom` atau `ample-trust`
2. Lanjut ke Step 4

#### Option B: Buat Project Baru (Recommended)

1. **Dashboard** → **"New Project"**
2. **"Deploy from GitHub repo"**
3. **Select repository:** `ihyaabrar/auto_ml`
4. **Project name:** `auto-ml-platform`
5. **Click "Create Project"**

---

### **Step 3: Add PostgreSQL Database**

1. Di project dashboard → **"New"** → **"Database"** → **"PostgreSQL"**
2. Tunggu provisioning (~30 detik)
3. **Copy DATABASE_URL:**
   - Click service `postgres`
   - Tab **"Variables"**
   - Copy value `DATABASE_URL`
   - Format: `postgresql://postgres:...@...`

**Simpan URL ini!**

---

### **Step 4: Deploy Backend Service**

#### A. Create Service

1. Back ke project dashboard
2. **"New"** → **"GitHub Repo"** (pilih lagi `ihyaabrar/auto_ml`)
3. **Service name:** `backend`

#### B. Configure Settings

Click service `backend` → Tab **"Settings"**:

```yaml
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

#### C. Set Environment Variables

Tab **"Variables"** → **"Add Variable"**:

| Variable Name | Value |
|---------------|-------|
| `DATABASE_URL` | Paste dari Step 3 |
| `UPLOAD_DIR` | `./uploads` |
| `MODELS_DIR` | `./models` |
| `PYTHON_VERSION` | `3.11` |

---

### **Step 5: Deploy!**

1. Tab **"Deployments"**
2. Click **"Deploy"**
3. Tunggu build selesai (~2-3 menit)

**Status akan berubah:**
- ⏳ Building...
- ✅ Deployed!

---

### **Step 6: Get Public URL**

Setelah deploy sukses:

1. Tab **"Settings"**
2. Scroll ke **"Domains"**
3. Click **"Generate Domain"**
4. Dapat URL seperti:
   ```
   https://auto-ml-backend-production.up.railway.app
   ```

**Test API:**
```
https://auto-ml-backend-production.up.railway.app/api/v1/projects/upload
```

---

### **Step 7: Deploy Frontend ke Vercel**

#### A. Login Vercel

```bash
cd frontend
vercel login
```

#### B. Deploy

```bash
cd frontend
vercel
```

**Follow prompt:**
```
? Set up and deploy "~/Downloads/auto_ml/frontend"? Yes
? Which scope do you want to deploy to? [Your Name]
? Link to existing project? No
? Want to override the settings? No
? Framework Preset: Vite
? Build Command: npm run build
? Output Directory: dist
? Install Command: npm install
```

#### C. Set Environment Variable

Di Vercel Dashboard project:

1. **Settings** → **Environment Variables**
2. **Add Variable:**
   ```
   Key: VITE_API_URL
   Value: https://<your-railway-backend-url>.up.railway.app
   ```
3. **Redeploy** untuk apply changes

---

## 🧪 Testing

### Test Upload API

```bash
curl -X POST \
  https://<your-railway-backend-url>.up.railway.app/api/v1/projects/upload \
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

### Test Frontend

Buka browser:
```
https://<your-vercel-frontend-url>.vercel.app
```

Upload sample dataset dan test!

---

## 💰 Cost: $0/month

- Railway: Free $5 credit (~500 jam/bulan)
- Vercel: Free tier unlimited
- **Total: GRATIS!** ✅

---

## 🔧 Troubleshooting

### Error: "Build failed"

**Check logs di Railway:**
1. Tab "Deployments"
2. Click deployment
3. View logs

**Common issues:**
- Missing `requirements.txt`
- Python version mismatch
- Build command salah

### Error: "DATABASE_URL not found"

Pastikan environment variable sudah diset:
1. Tab "Variables"
2. Check `DATABASE_URL` ada
3. Redeploy setelah set

### Frontend tidak connect ke backend

1. Check `VITE_API_URL` di Vercel
2. Pastikan URL backend benar
3. Check CORS di backend (sudah enabled)

---

## 📊 Monitoring

### Railway Dashboard

- Real-time logs
- Resource usage (CPU/RAM)
- Database size
- Network traffic

### Vercel Dashboard

- Deployment history
- Analytics
- Function logs
- Bandwidth usage

---

## ✅ Checklist

- [ ] Login Railway (done: ihyakpati1144@gmail.com)
- [ ] Create/Select project
- [ ] Add PostgreSQL database
- [ ] Copy DATABASE_URL
- [ ] Deploy backend service
- [ ] Set environment variables
- [ ] Get Railway URL
- [ ] Deploy frontend ke Vercel
- [ ] Set VITE_API_URL di Vercel
- [ ] Test upload API
- [ ] Test frontend di browser

---

## 🎉 Success!

Anda dapat:

| Component | URL | Status |
|-----------|-----|--------|
| **Backend API** | `https://...up.railway.app` | ✅ LIVE |
| **Frontend** | `https://...vercel.app` | ✅ LIVE |
| **Database** | PostgreSQL managed | ✅ RUNNING |

**Total Cost: $0/month** 🎊

---

**Happy Deploying! 🚀**
