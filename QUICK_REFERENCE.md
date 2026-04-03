# Quick Reference Guide

## 🚀 Getting Started (30 seconds)

```bash
# Clone and start
cd auto_ml
./start.sh          # or .\start.ps1 on Windows

# Access
# Frontend: http://localhost:5173
# Backend:  http://localhost:8000
# Docs:     http://localhost:8000/docs
```

## 📁 Project Structure at a Glance

```
auto_ml/
├── frontend/src/           # React app
│   ├── components/        # UI components
│   ├── pages/             # Page components
│   ├── stores/            # State (Zustand)
│   ├── services/          # API calls
│   └── types/             # TypeScript types
├── backend/app/            # FastAPI app
│   ├── api/               # Routes
│   ├── core/              # Config & DB
│   ├── models/            # ORM models
│   └── schemas/           # Pydantic schemas
└── sample_dataset.csv      # Test data
```

## 🔧 Common Tasks

### Start Development

**With Docker:**
```bash
docker-compose up -d
docker-compose down    # Stop
```

**Without Docker:**
```bash
# Terminal 1 - Backend
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm install
npm run dev
```

### Database Commands

**Reset Database:**
```bash
docker-compose exec postgres psql -U postgres -c "DROP DATABASE IF EXISTS automl_db;"
docker-compose exec postgres psql -U postgres -c "CREATE DATABASE automl_db;"
```

**View Tables:**
```bash
docker-compose exec postgres psql -U postgres -d automl_db
\dt                 # List tables
SELECT * FROM datasets;  # View data
```

### Install New Dependencies

**Backend:**
```bash
cd backend
pip install package-name
echo "package-name==version" >> requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install package-name --save
```

## 🌐 API Endpoints

### Upload Dataset
```bash
curl -X POST http://localhost:8000/api/v1/projects/upload \
  -F "file=@sample_dataset.csv"
```

### Start Training
```bash
curl -X POST http://localhost:8000/api/v1/jobs/train \
  -H "Content-Type: application/json" \
  -d '{
    "dataset_id": 1,
    "target_column": "stroke",
    "task_type": "classification",
    "mode": "custom"
  }'
```

### Get Results
```bash
curl http://localhost:8000/api/v1/jobs/1/results
```

## 🐛 Debugging

### Check Backend Logs
```bash
docker-compose logs backend
docker-compose logs -f backend  # Follow logs
```

### Check Frontend
- Open browser DevTools (F12)
- Check Console tab
- Check Network tab for API calls

### Test Backend Directly
```bash
cd backend
python
>>> from app.core.database import get_db
>>> from app.models.database_models import Dataset
# Test database queries
```

## 📊 Sample Dataset

Use `sample_dataset.csv` for testing:
- **Features**: age, bmi, hypertension, heart_disease, smoking_status, glucose_level, blood_pressure
- **Target**: stroke (0 = No, 1 = Yes)
- **Task Type**: Classification
- **Rows**: 50
- **Columns**: 8

## 💡 Tips & Tricks

### Hot Reload
Both frontend and backend support hot reload:
- Frontend changes: Instant update (Vite HMR)
- Backend changes: Auto-reload (Uvicorn --reload)

### Environment Variables
Copy templates before starting:
```bash
cp .env.example .env          # Root
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

### Clear Uploads
```bash
rm -rf backend/uploads/*
rm -rf backend/models/*
```

### Performance Tips
- Use smaller datasets (< 10MB) for development
- Enable DEBUG=False in production
- Use PostgreSQL indexes for large datasets

## 🎨 Frontend Development

### Component Template
```tsx
import { useState } from 'react';

interface Props {
  title: string;
}

const MyComponent = ({ title }: Props) => {
  const [state, setState] = useState('');
  
  return (
    <div className="p-4">
      <h2>{title}</h2>
    </div>
  );
};

export default MyComponent;
```

### State Management
```tsx
import { useAppStore } from './stores/appStore';

const MyComponent = () => {
  const { currentDataset, setDataset } = useAppStore();
  
  // Use state...
};
```

### API Calls
```tsx
import { datasetService } from './services/api';

const upload = async (file: File) => {
  const dataset = await datasetService.uploadDataset(file);
};
```

## 🐍 Backend Development

### Create New Endpoint
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db

router = APIRouter()

@router.get("/my-endpoint")
async def my_endpoint(db: Session = Depends(get_db)):
    return {"message": "Hello"}
```

### Database Query
```python
from ..models.database_models import Dataset

datasets = db.query(Dataset).filter(Dataset.id == 1).all()
```

### Add New Model
```python
# In app/models/database_models.py
class MyModel(Base):
    __tablename__ = "my_table"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
```

## 🧪 Testing

### Test Upload
1. Go to http://localhost:5173
2. Upload `sample_dataset.csv`
3. Select "stroke" as target
4. Choose "Classification"
5. Click "Start Training"

### Test API Directly
Visit http://localhost:8000/docs for interactive Swagger UI

## 📦 Deployment Checklist

- [ ] Set DEBUG=False
- [ ] Change SECRET_KEY
- [ ] Update CORS_ORIGINS
- [ ] Use production database
- [ ] Configure Redis for Celery
- [ ] Build frontend for production
- [ ] Set up reverse proxy (Nginx)
- [ ] Enable HTTPS
- [ ] Configure logging
- [ ] Set up monitoring

## 🔗 Useful Links

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Docs**: https://react.dev/
- **Tailwind CSS**: https://tailwindcss.com/
- **Scikit-Learn**: https://scikit-learn.org/
- **SQLAlchemy**: https://www.sqlalchemy.org/

## 🆘 Common Issues

**"Port already in use"**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9    # Linux/Mac
netstat -ano | findstr :8000     # Windows
```

**"Module not found"**
```bash
# Reinstall dependencies
cd frontend && npm install
cd backend && pip install -r requirements.txt
```

**"Database connection error"**
```bash
# Restart PostgreSQL
docker-compose restart postgres
```

**"CORS error"**
- Check CORS_ORIGINS in backend/.env
- Ensure frontend URL matches exactly

---

**Need more help?** See [SETUP.md](SETUP.md) for detailed setup instructions.
