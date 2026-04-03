# AutoML Platform

Platform berbasis web yang memungkinkan pengguna untuk mengunggah dataset dan melatih model Machine Learning melalui dua pendekatan:

1. **1-Click AutoML**: Sistem secara otomatis melakukan EDA, preprocessing, pemilihan model terbaik, dan tuning menggunakan Auto-Sklearn.
2. **Custom/Manual Setup**: Pengguna memiliki kontrol penuh atas alur preprocessing, pemilihan algoritma, hingga metrik evaluasi.

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone repository and navigate to project
cd auto_ml

# Start all services (Docker required)
./start.sh          # Linux/Mac
.\start.ps1         # Windows PowerShell
```

That's it! Access the application at:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Option 2: Manual Setup

See [SETUP.md](SETUP.md) for detailed manual setup instructions without Docker.

## Tech Stack

### Frontend
- React 18 + TypeScript
- Vite (Build tool)
- Tailwind CSS (Styling)
- Zustand (State Management)
- React Query (Data Fetching)
- Axios (HTTP Client)

### Backend
- Python 3.10+
- FastAPI (REST API)
- SQLAlchemy (ORM)
- PostgreSQL (Database)
- Scikit-Learn (ML)
- Pandas & NumPy (Data Processing)

### Coming Soon
- Celery + Redis (Task Queue)
- Auto-Sklearn (AutoML)
- WebSocket (Real-time updates)

## Project Structure

```
auto_ml/
├── frontend/              # React + Vite + TypeScript
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Page components
│   │   ├── stores/       # Zustand state management
│   │   ├── services/     # API services
│   │   └── types/        # TypeScript types
│   └── ...
├── backend/               # FastAPI + ML
│   └── app/
│       ├── api/          # API routes
│       ├── core/         # Configuration & database
│       ├── models/       # SQLAlchemy models
│       ├── schemas/      # Pydantic schemas
│       └── services/     # Business logic
├── docker-compose.yml     # Docker services
└── SETUP.md              # Detailed setup guide
```

## Features (Phase 1 - MVP)

✅ **Implemented:**
- Dataset upload (CSV, Excel)
- Automatic column type detection
- Custom ML training with Random Forest
- Configurable preprocessing (imputation, encoding, scaling)
- Model evaluation metrics
- Basic dashboard UI

🚧 **Coming in Phase 2:**
- Asynchronous training with Celery
- Real-time progress via WebSocket
- Auto-Sklearn integration
- Enhanced monitoring dashboard

🚧 **Coming in Phase 3:**
- Exploratory Data Analysis (EDA)
- Model comparison visualizations
- Model export/download
- Inference API
- Production deployment

## Usage Example

### 1. Upload Dataset

Navigate to http://localhost:5173 and upload a CSV or Excel file containing your data.

Example datasets you can use:
- Medical diagnosis prediction (Yes/No)
- House price prediction (numeric)
- Customer churn prediction (categories)

### 2. Configure Training

Select your target column and choose:
- **Task Type**: Classification or Regression
- **Mode**: AutoML (automatic) or Custom (manual)

### 3. Train & Evaluate

Start training and view results including:
- Accuracy, Precision, Recall, F1-Score
- Feature Importance
- Confusion Matrix

## API Endpoints

### Projects

```http
POST /api/v1/projects/upload
Content-Type: multipart/form-data

Response: Dataset info with columns analysis
```

### Training Jobs

```http
POST /api/v1/jobs/train
Content-Type: application/json

{
  "dataset_id": 1,
  "target_column": "diagnosis",
  "task_type": "classification",
  "mode": "custom",
  "preprocessing": {
    "missing_values": "median",
    "categorical_encoding": "one_hot",
    "scaling": "standard"
  }
}

Response: { "job_id": 1, "status": "completed" }
```

```http
GET /api/v1/jobs/{job_id}/results

Response: Model metrics, feature importance, confusion matrix
```

## Development Status

This project is currently under development following a phased approach:

- ✅ **Phase 1**: Foundation & Custom ML MVP
  - Basic upload and training pipeline
  - Random Forest classifier/regressor
  - Preprocessing configuration
  - Evaluation metrics
  
- 🚧 **Phase 2**: Asynchronous Processing & AutoML
  - Celery task queue
  - WebSocket real-time updates
  - Auto-Sklearn integration
  - Enhanced UI

- 🚧 **Phase 3**: Advanced Features & Deployment
  - EDA visualizations
  - Model comparison
  - Export functionality
  - Production Docker setup

## Troubleshooting

**Backend won't start?**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend won't start?**
```bash
cd frontend
npm install
npm run dev
```

**Database errors?**
Make sure PostgreSQL is running and credentials in `.env` are correct.

For more help, see [SETUP.md](SETUP.md).

## Contributing

This is an educational project. Feel free to fork and enhance!

## License

MIT

---

**Built with ❤️ using FastAPI, React, and Scikit-Learn**
