# 🚀 AutoML Platform - Machine Learning Made Simple

<div align="center">

![AutoML Platform](https://img.shields.io/badge/AutoML-Platform-blue)
![License](https://img.shields.io/badge/License-Private-red)
![Python](https://img.shields.io/badge/Python-3.11-green)
![React](https://img.shields.io/badge/React-18-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![Deployment](https://img.shields.io/badge/Deploy-Railway%20+%20Vercel-brightgreen)

**Build, Train, and Deploy ML Models with Just a Few Clicks!**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Deployment](#-deployment)

</div>

---

## 📋 What is AutoML Platform?

AutoML Platform adalah platform **all-in-one** untuk membangun dan men-deploy model machine learning tanpa perlu coding yang kompleks. Platform ini menggabungkan kemudahan penggunaan dengan kekuatan framework ML terbaik.

### ✨ Key Capabilities:

- **🎯 1-Click AutoML** - Upload data, dapatkan model optimal secara otomatis
- **🔧 Custom ML Setup** - Kontrol penuh atas preprocessing, model selection, dan hyperparameters
- **📊 Smart EDA** - Exploratory Data Analysis otomatis untuk memahami data Anda
- **⚡ Real-time Training** - Monitor progress training secara real-time
- **📈 Comprehensive Evaluation** - Analisis performa model dengan metrik lengkap

---

## 🛠️ Tech Stack

### Frontend
```
⚛️  React 18 + TypeScript
🎨 Tailwind CSS v4 (Modern UI)
🔍 Vite (Lightning-fast build)
📊 Recharts (Data visualization)
🌐 React Query 5 (Data fetching)
🦮 Zustand (State management)
```

### Backend
```
🚀 FastAPI (High-performance API)
🐍 Python 3.11
💾 SQLAlchemy (ORM)
🧪 Scikit-Learn (Machine Learning)
📊 Pandas & NumPy (Data manipulation)
🔄 Celery (Task queue - Phase 2)
```

### Infrastructure
```
🗄️  PostgreSQL (Database)
📦 Redis (Cache & Queue)
🚂 Railway.app (Backend hosting)
▲ Vercel (Frontend hosting)
🐳 Docker (Containerization)
```

---

## 🚀 Quick Start

### Prerequisites

Pastikan sudah terinstall:
- Python 3.11+
- Node.js 18+
- Git

### 1. Clone Repository

```bash
git clone https://github.com/ihyaabrar/auto_ml.git
cd auto_ml
```

### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run server (Demo mode - no database required)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Open browser: http://localhost:5176
```

### 4. Test Upload

Upload sample dataset:
```bash
curl -X POST http://localhost:8000/api/v1/projects/upload \
  -F "file=@sample_dataset.csv"
```

---

## 📖 Documentation

| Guide | Description |
|-------|-------------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture & design |
| [SETUP.md](SETUP.md) | Detailed setup instructions |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | API endpoints & commands |
| [DEPLOY_AUTOMATION.md](DEPLOY_AUTOMATION.md) | Automated deployment guide |
| [RAILWAY_SETUP.md](RAILWAY_SETUP.md) | Manual Railway deployment |

---

## 🌐 Deployment

### One-Click Deploy (Recommended)

#### Step 1: Login Railway
```
Visit: https://railway.app
Login dengan GitHub account
```

#### Step 2: Run Deployment Script
```powershell
cd auto_ml
.\deploy-railway.ps1
```

**That's it!** Script akan otomatis:
- ✅ Create Railway project
- ✅ Provision PostgreSQL database
- ✅ Deploy backend API
- ✅ Configure environment variables
- ✅ Deploy frontend ke Vercel

### Manual Deployment

Lihat panduan lengkap di [DEPLOY_AUTOMATION.md](DEPLOY_AUTOMATION.md)

### Cost Breakdown

| Service | Free Tier | Usage | Cost |
|---------|-----------|-------|------|
| **Railway** | $5 credit | Backend + DB | $0 |
| **Vercel** | Unlimited | Frontend | $0 |
| **Total** | | | **$0/month** ✨ |

---

## 📁 Project Structure

```
auto_ml/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   │   ├── projects.py    # File upload & dataset management
│   │   │   └── jobs.py        # Model training & evaluation
│   │   ├── core/           # Configuration & database
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic
│   ├── requirements.txt
│   └── uploads/            # Dataset storage
│
├── frontend/               # React + TypeScript frontend
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── pages/         # Application pages
│   │   ├── services/      # API integration
│   │   ├── stores/        # State management
│   │   └── types/         # TypeScript types
│   ├── package.json
│   └── vite.config.ts
│
├── deploy-railway.ps1     # Automated deployment script
├── deploy-railway.sh
├── docker-compose.yml     # Docker orchestration
└── sample_dataset.csv     # Sample medical dataset
```

---

## 🎯 Features

### Phase 1 (MVP) - ✅ Complete

- [x] File upload (CSV/Excel support)
- [x] Automatic column analysis
- [x] Dataset preview & metadata
- [x] Target column selection
- [x] Task type detection (Classification/Regression)
- [x] Custom ML configuration
- [x] Preprocessing pipeline
- [x] Random Forest training
- [x] Model evaluation metrics
- [x] Results visualization

### Phase 2 (Coming Soon)

- [ ] AutoML with Auto-Sklearn
- [ ] PyCaret integration
- [ ] Multiple model comparison
- [ ] Hyperparameter optimization
- [ ] Celery task queue
- [ ] Real-time training progress
- [ ] Model persistence
- [ ] Batch predictions
- [ ] REST API endpoints
- [ ] User authentication

### Phase 3 (Future)

- [ ] S3 file storage
- [ ] Advanced EDA reports
- [ ] Feature engineering suggestions
- [ ] Model interpretability (SHAP/LIME)
- [ ] Ensemble methods
- [ ] Deep learning support
- [ ] API rate limiting
- [ ] Admin dashboard

---

## 🧪 Testing

### Upload Test Dataset

```bash
# Using sample dataset
curl -X POST http://localhost:8000/api/v1/projects/upload \
  -F "file=@sample_dataset.csv"

# Response:
{
  "id": 12345,
  "file_name": "sample_dataset.csv",
  "num_rows": 50,
  "num_cols": 8,
  "columns": [
    {"name": "age", "type": "numeric"},
    {"name": "bmi", "type": "numeric"},
    ...
  ]
}
```

### Training Test

```bash
curl -X POST http://localhost:8000/api/v1/jobs/train \
  -H "Content-Type: application/json" \
  -d '{
    "dataset_id": 12345,
    "target_column": "stroke",
    "task_type": "classification",
    "mode": "custom",
    "models": ["random_forest"]
  }'
```

---

## 🤝 Contributing

This is a **private project**. All rights reserved.

Untuk pertanyaan atau kolaborasi, silakan hubungi owner repository.

---

## 📄 License

**Private License** - See [LICENSE](LICENSE) file for details.

All code and documentation are proprietary and confidential.
Unauthorized copying, distribution, or use is strictly prohibited.

---

## 👨‍💻 Author

**Created by:** ihyaabrar  
**Repository:** [github.com/ihyaabrar/auto_ml](https://github.com/ihyaabrar/auto_ml)

---

## 🙏 Acknowledgments

Built with amazing tools and frameworks:
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Scikit-Learn](https://scikit-learn.org/)
- [Railway](https://railway.app/)
- [Vercel](https://vercel.com/)

---

<div align="center">

**Made with ❤️ for simplifying Machine Learning**

⭐ Star this repo if you find it useful!

</div>
