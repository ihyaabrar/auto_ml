# 🚨 CRITICAL: Force Railway to Use Dockerfile

## ⚠️ Problem

Railway terus menggunakan **Railpack** meskipun sudah ada:
- ✅ `Dockerfile`
- ✅ `railway.toml`  
- ✅ `.railway` (JSON)

**Error:**
```
sh: 1: pip: not found
exit code: 127
```

---

## 🔧 Solution: Manual Reset Required

### Step 1: Open Railway Dashboard
```
https://railway.app/dashboard
```

### Step 2: Delete Current Deployment

1. Select your project (`auto-ml-platform`)
2. Click service `backend`
3. Tab **"Settings"**
4. Scroll down → Click **"Delete Service"**
5. Confirm deletion

### Step 3: Create New Service from Dockerfile

1. Back to project dashboard
2. **"New"** → **"GitHub Repo"**
3. Select: `ihyaabrar/auto_ml`
4. **Root Directory:** `backend`
5. Railway akan auto-detect Dockerfile!

### Step 4: Configure Settings

Tab **"Settings"**:

```yaml
# Biarkan kosong - Railway akan detect Dockerfile otomatis!
Build Command: (leave empty)
Deploy Command: (leave empty)
```

### Step 5: Set Environment Variables

Tab **"Variables"**:

| Variable | Value |
|----------|-------|
| `DATABASE_URL` | `postgresql://postgres:PcIPBCirhhyGQHjerMOjzGUgcedqeZxa@junction.proxy.rlwy.net:23565/railway` |
| `UPLOAD_DIR` | `./uploads` |
| `MODELS_DIR` | `./models` |

### Step 6: Deploy!

1. Tab **"Deployments"**
2. Click **"Deploy"**
3. Sekarang akan gunakan Dockerfile! ✅

---

## 🎯 Expected Build Logs (Success)

```
✅ FROM python:3.11-slim
✅ RUN apt-get update
✅ RUN pip install -r requirements.txt
✅ Collecting fastapi==0.109.0
✅ Collecting uvicorn[standard]==0.27.0
✅ ... (all packages installed)
✅ Successfully built image
✅ Container started
✅ Health check passed
```

---

## 📊 Why This Happens

Railway kadang cache configuration lama. Meskipun kita push config baru, Railway masih pakai setting lama.

**Solution:** Delete dan recreate service memaksa Railway read fresh config dari GitHub!

---

## 🔄 Alternative: Use Railway CLI

If manual delete doesn't work:

```bash
# Link to project
cd backend
railway link

# Force rebuild
railway up --force-rebuild
```

---

## ✅ Success Checklist

After redeploy, verify:

- [ ] Build logs show Docker commands (bukan Railpack)
- [ ] `pip install -r requirements.txt` berhasil
- [ ] Status: Deployed ✅
- [ ] Health check: Passed ✅
- [ ] Backend URL accessible

---

## 🎉 After Success

1. Get URL dari Settings → Domains
2. Test upload API:
   ```bash
   curl -X POST <your-url>/api/v1/projects/upload \
     -F "file=@sample_dataset.csv"
   ```
3. Deploy frontend ke Vercel

---

**Do this NOW via Railway Dashboard!** 

Manual delete & recreate adalah cara paling reliable untuk force penggunaan Dockerfile. 🚀
