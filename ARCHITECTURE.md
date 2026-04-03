# System Architecture

## High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         USER BROWSER                        │
│                     http://localhost:5173                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP/REST API
                         │ WebSocket (Phase 2)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + Vite)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   File       │  │    Config    │  │   Results    │      │
│  │   Upload     │  │    Wizard    │  │   Display    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────────────────────────────────────────┐       │
│  │        Zustand State + React Query               │       │
│  └──────────────────────────────────────────────────┘       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Axios HTTP Client
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                 BACKEND (FastAPI + Python)                  │
│                     http://localhost:8000                   │
│  ┌──────────────────────────────────────────────────┐       │
│  │              API Routes (Routers)                │       │
│  │  • /api/v1/projects  - Dataset management        │       │
│  │  • /api/v1/jobs      - Training & evaluation     │       │
│  └──────────────────────────────────────────────────┘       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Pydantic    │  │  SQLAlchemy  │  │   Scikit-    │      │
│  │  Schemas     │  │  ORM Models  │  │   Learn ML   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────────────────────────────────────────┐       │
│  │         Business Logic & Preprocessing           │       │
│  └──────────────────────────────────────────────────┘       │
└─────────┬──────────────────────┬────────────────────────────┘
          │                      │
          │                      │
          ▼                      ▼
┌──────────────────┐   ┌──────────────────┐
│   PostgreSQL     │   │   File System    │
│   Database       │   │   Storage        │
│                  │   │                  │
│ • users          │   │ • uploads/       │
│ • projects       │   │   {dataset_id}/  │
│ • datasets       │   │ • models/        │
│ • jobs_training  │   │   model_{id}.pkl │
│ • models         │   │                  │
└──────────────────┘   └──────────────────┘
```

---

## Data Flow Diagrams

### 1. Dataset Upload Flow

```
User → Browser
  │
  ├─→ Select CSV/Excel file
  │
  ├─→ POST /api/v1/projects/upload (multipart/form-data)
  │
  ▼
FastAPI Backend
  │
  ├─→ Validate file type (CSV/XLSX)
  │
  ├─→ Save to uploads/{dataset_id}/filename
  │
  ├─→ Read with Pandas (read_csv/read_excel)
  │
  ├─→ Analyze columns:
  │     • Detect data types
  │     • Count missing values
  │     • Calculate statistics
  │
  ├─→ Store metadata in Dataset table
  │
  └─→ Return JSON response
        {
          "id": 1,
          "file_name": "data.csv",
          "num_rows": 1000,
          "columns": [...]
        }
```

### 2. Model Training Flow (Synchronous - Phase 1)

```
User → Browser
  │
  ├─→ Configure training:
  │     • Target column
  │     • Task type (Classification/Regression)
  │     • Mode (Auto/Custom)
  │
  ├─→ POST /api/v1/jobs/train
  │     {
  │       "dataset_id": 1,
  │       "target_column": "stroke",
  │       "task_type": "classification",
  │       "mode": "custom"
  │     }
  │
  ▼
FastAPI Backend
  │
  ├─→ Create TrainingJob record (status: running)
  │
  ├─→ Load dataset from database
  │
  ├─→ Preprocessing Pipeline:
  │     1. Separate features (X) and target (y)
  │     2. Identify numeric/categorical columns
  │     3. Impute missing values
  │     4. Encode categorical variables
  │     5. Scale features
  │
  ├─→ Train/Test Split (80/20)
  │
  ├─→ Train Random Forest:
  │     • Classification or Regression
  │     • n_estimators=100
  │     • max_depth=10
  │
  ├─→ Evaluate Model:
  │     • Accuracy, Precision, Recall, F1
  │     • Confusion Matrix
  │     • Feature Importance
  │
  ├─→ Save model pipeline to models/model_{id}.pkl
  │
  ├─→ Create Model record with metrics
  │
  ├─→ Update TrainingJob (status: completed)
  │
  └─→ Return job_id
```

### 3. Results Retrieval Flow

```
User → Browser
  │
  ├─→ GET /api/v1/jobs/{job_id}/results
  │
  ▼
FastAPI Backend
  │
  ├─→ Query TrainingJob by ID
  │
  ├─→ Check status == "completed"
  │
  ├─→ Get associated Model record
  │
  └─→ Return results:
        {
          "metrics": {...},
          "feature_importance": [...],
          "confusion_matrix": [[...]]
        }
```

---

## Component Architecture

### Frontend Components

```
App.tsx
  │
  ├─→ QueryClientProvider (React Query)
  │
  └─→ Router
        │
        └─→ HomePage (Main Dashboard)
              │
              ├─→ FileUpload Component
              │     • Drag & drop zone
              │     • File validation
              │     • Upload progress
              │
              ├─→ Configuration Form
              │     • Target selector
              │     • Task type buttons
              │     • Mode selector
              │
              ├─→ Progress Steps
              │     • Visual wizard
              │     • Step indicators
              │
              └─→ Results Display
                    • Metrics cards
                    • Charts (Phase 3)
```

### Backend Layers

```
┌─────────────────────────────────────┐
│         Presentation Layer          │
│  FastAPI Routes (api/)              │
│  • projects.py                      │
│  • jobs.py                          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│         Business Logic Layer        │
│  Services (services/)               │
│  • Data preprocessing               │
│  • Model training                   │
│  • Evaluation                       │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│         Data Access Layer           │
│  Models & Database (models/, core/) │
│  • SQLAlchemy ORM                   │
│  • Pydantic Schemas                 │
│  • Database sessions                │
└─────────────────────────────────────┘
```

---

## Database Schema

```
┌──────────────────────┐
│       users          │
├──────────────────────┤
│ id (PK)             │
│ email               │
│ password_hash       │
│ created_at          │
└──────────┬───────────┘
           │
           │ 1:N
           ▼
┌──────────────────────┐
│      projects        │
├──────────────────────┤
│ id (PK)             │
│ user_id (FK)        │
│ project_name        │
│ created_at          │
└──────────┬───────────┘
           │
           │ 1:N
           ▼
┌──────────────────────┐
│      datasets        │
├──────────────────────┤
│ id (PK)             │
│ project_id (FK)     │
│ file_name           │
│ file_path           │
│ num_rows            │
│ num_cols            │
│ column_info (JSON)  │
│ created_at          │
└──────────┬───────────┘
           │
           │ 1:N
           ▼
┌──────────────────────┐
│    jobs_training     │
├──────────────────────┤
│ id (PK)             │
│ dataset_id (FK)     │
│ status              │
│ mode                │
│ config (JSON)       │
│ progress            │
│ current_step        │
│ start_time          │
│ end_time            │
│ error_message       │
│ created_at          │
└──────────┬───────────┘
           │
           │ 1:1
           ▼
┌──────────────────────┐
│       models         │
├──────────────────────┤
│ id (PK)             │
│ job_id (FK)         │
│ algorithm_name      │
│ metrics (JSON)      │
│ feature_importance  │
│ confusion_matrix    │
│ model_path          │
│ created_at          │
└──────────────────────┘
```

---

## Phase 2 Architecture (Async with Celery)

```
┌─────────────────────────────────────────────────────────────┐
│                         User Request                        │
│              POST /api/v1/jobs/train                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                          │
│  ┌────────────────────────────────────────────────┐         │
│  │ Create Job Record (pending)                    │         │
│  │ Send Task to Redis                             │         │
│  │ Return job_id immediately                      │         │
│  └────────────────────────────────────────────────┘         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Push to Redis Queue
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      Redis Broker                           │
│  Queue: celery                                              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Pop from Queue
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Celery Worker                             │
│  ┌────────────────────────────────────────────────┐         │
│  │ train_model_task(job_id, config)               │         │
│  │   • Load dataset                               │         │
│  │   • Preprocess                                 │         │
│  │   • Train                                      │         │
│  │   • Evaluate                                   │         │
│  │   • Save model                                 │         │
│  │   • Update job status                          │         │
│  └────────────────────────────────────────────────┘         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ WebSocket Message
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React)                         │
│  ┌────────────────────────────────────────────────┐         │
│  │ WebSocket Listener                             │         │
│  │   • status: "running"                          │         │
│  │   • step: "Training..."                        │         │
│  │   • progress: 60%                              │         │
│  └────────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

---

## Security Considerations

### Current (MVP)
- ✅ File type validation
- ✅ Input sanitization with Pydantic
- ✅ CORS configuration
- ✅ SQL injection prevention (SQLAlchemy ORM)

### Phase 3 Additions
- 🔲 JWT Authentication
- 🔲 Rate limiting
- 🔲 File size limits
- 🔲 Malware scanning
- 🔲 HTTPS enforcement
- 🔲 API key management

---

## Deployment Architecture (Production)

```
                    ┌─────────────┐
                    │   Nginx     │
                    │  Reverse    │
                    │   Proxy     │
                    └──────┬──────┘
                           │
            ┌──────────────┴──────────────┐
            │                             │
            ▼                             ▼
┌──────────────────────┐      ┌──────────────────────┐
│   Frontend (Nginx)   │      │   Backend (Gunicorn) │
│   :80                │      │   :8000              │
│   Static files       │      │   FastAPI app        │
└──────────────────────┘      └──────────┬───────────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
                    ▼                    ▼                    ▼
          ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
          │   PostgreSQL    │  │     Redis       │  │   MinIO/S3      │
          │   Database      │  │     Broker      │  │   Object Store  │
          └─────────────────┘  └─────────────────┘  └─────────────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │   Celery Workers    │
                              │   (Multiple)        │
                              └─────────────────────┘
```

---

**This architecture provides:**
- ✅ Scalability (horizontal scaling with containers)
- ✅ Maintainability (clear separation of concerns)
- ✅ Extensibility (easy to add new features)
- ✅ Reliability (async processing, error handling)
- ✅ Performance (caching, optimized queries)
