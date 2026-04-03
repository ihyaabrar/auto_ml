# AutoML Platform - Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v18 or higher)
- **Python** (v3.10 or higher)
- **Docker** and **Docker Compose** (optional, for containerized deployment)
- **PostgreSQL** (v15 or higher) - for local development without Docker
- **Redis** (v7 or higher) - for local development without Docker

## Quick Start with Docker (Recommended)

### 1. Clone and Setup

```bash
cd auto_ml

# Copy environment template
cp .env.example .env
```

Edit `.env` file and update with your configuration if needed.

### 2. Start All Services

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database
- Redis message broker
- Backend API (port 8000)
- Frontend dev server (port 5173)
- Celery worker

### 3. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 4. Stop Services

```bash
docker-compose down
```

---

## Manual Setup (Without Docker)

### Backend Setup

#### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Setup Database

Start PostgreSQL and create database:

```sql
CREATE DATABASE automl_db;
```

Or use an existing database.

#### 4. Configure Environment

Create `.env` file in `backend/` directory:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/automl_db
DEBUG=True
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:5173
REDIS_URL=redis://localhost:6379/0
```

#### 5. Start Redis

```bash
# Windows (download from GitHub releases)
redis-server

# Linux
sudo systemctl start redis

# Mac
brew services start redis
```

#### 6. Run Backend Server

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will now be running at http://localhost:8000

---

### Frontend Setup

#### 1. Install Dependencies

```bash
cd frontend
npm install
```

#### 2. Configure Environment

Create `.env` file in `frontend/` directory:

```env
VITE_API_URL=http://localhost:8000
```

#### 3. Start Development Server

```bash
npm run dev
```

The frontend will now be running at http://localhost:5173

---

## Usage Guide

### 1. Upload Dataset

1. Go to http://localhost:5173
2. Click on "Upload a file" or drag & drop your CSV/Excel file
3. Wait for the system to analyze your dataset

### 2. Configure Training

1. Select your target column (what you want to predict)
2. Choose task type:
   - **Classification**: For categorical predictions (Yes/No, categories)
   - **Regression**: For numerical predictions (prices, scores)
3. Choose training mode:
   - **AutoML**: Automatic model selection and tuning
   - **Custom**: Manual configuration of preprocessing and models

### 3. Train Model

1. Click "Start Training"
2. Monitor the training progress
3. View results including:
   - Model metrics (accuracy, precision, recall, F1-score)
   - Feature importance
   - Confusion matrix (for classification)

---

## API Endpoints

### Projects

- `POST /api/v1/projects/upload` - Upload dataset
- `GET /api/v1/datasets/{dataset_id}` - Get dataset info

### Jobs

- `POST /api/v1/jobs/train` - Start training
- `GET /api/v1/jobs/{job_id}/results` - Get training results
- `GET /api/v1/jobs/{job_id}/status` - Get job status

### Health Check

- `GET /health` - Check API health

---

## Troubleshooting

### Backend Issues

**Database Connection Error:**
```
Make sure PostgreSQL is running and credentials in .env are correct
```

**Redis Connection Error:**
```
Ensure Redis server is running on port 6379
```

### Frontend Issues

**Cannot Connect to API:**
```
1. Check if backend is running at http://localhost:8000
2. Verify VITE_API_URL in frontend/.env
3. Check CORS settings in backend
```

### Common Issues

**Port Already in Use:**
```bash
# Kill process on port 8000 (Linux/Mac)
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

## Development

### Run Tests (Backend)

```bash
cd backend
pytest
```

### Run Tests (Frontend)

```bash
cd frontend
npm test
```

---

## Next Steps

Currently implemented (Phase 1):
- ✅ Dataset upload and analysis
- ✅ Custom ML training pipeline (Random Forest)
- ✅ Model evaluation metrics
- ✅ Basic frontend UI

Coming in Phase 2:
- ⏳ Asynchronous training with Celery
- ⏳ Real-time WebSocket progress updates
- ⏳ Auto-Sklearn integration for AutoML mode
- ⏳ Enhanced monitoring dashboard

Coming in Phase 3:
- ⏳ Exploratory Data Analysis (EDA) visualizations
- ⏳ Model comparison and visualization
- ⏳ Model export/download
- ⏳ Inference API endpoint
- ⏳ Docker production deployment

---

## Support

For issues or questions:
1. Check the API docs at http://localhost:8000/docs
2. Review backend logs in terminal
3. Check browser console for frontend errors

---

## License

MIT
