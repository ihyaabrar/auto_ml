from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_squared_error, r2_score
)
import joblib
import os
from datetime import datetime

from ..core.database import get_db
from ..core.config import get_settings
from ..models.database_models import Dataset, TrainingJob, Model
from ..schemas.schemas import (
    TrainingConfig, JobStatus, ModelResults, ModelMetrics, FeatureImportance
)

router = APIRouter()
settings = get_settings()


def load_and_prepare_data(dataset_id: int, db: Session):
    """Load dataset from file"""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Read dataset
    file_ext = os.path.splitext(dataset.file_name)[1].lower()
    if file_ext == ".csv":
        df = pd.read_csv(dataset.file_path, encoding='utf-8')
    else:
        df = pd.read_excel(dataset.file_path)
    
    return df, dataset


def preprocess_data(
    df: pd.DataFrame,
    target_column: str,
    config: TrainingConfig
):
    """Preprocess data according to configuration"""
    
    # Separate features and target
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    # Identify numeric and categorical columns
    numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
    
    preprocessing_steps = {}
    
    # Handle missing values
    if config.preprocessing and config.preprocessing.missing_values != "drop":
        impute_strategy = config.preprocessing.missing_values
        
        # Impute numeric columns
        if numeric_cols:
            if impute_strategy in ["mean", "median"]:
                strategy = impute_strategy
            else:
                strategy = "most_frequent"  # for mode
            
            imputer = SimpleImputer(strategy=strategy)
            X[numeric_cols] = imputer.fit_transform(X[numeric_cols])
            preprocessing_steps['numeric_imputer'] = imputer
        
        # Impute categorical columns
        if categorical_cols:
            cat_imputer = SimpleImputer(strategy='most_frequent')
            X[categorical_cols] = cat_imputer.fit_transform(X[categorical_cols])
            preprocessing_steps['categorical_imputer'] = cat_imputer
    
    # Encode categorical variables
    if categorical_cols and config.preprocessing and config.preprocessing.categorical_encoding == "one_hot":
        X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)
        preprocessing_steps['encoded_columns'] = categorical_cols
    elif categorical_cols:
        # Label encoding
        label_encoders = {}
        for col in categorical_cols:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            label_encoders[col] = le
        preprocessing_steps['label_encoders'] = label_encoders
    
    # Scale features
    if config.preprocessing and config.preprocessing.scaling != "none":
        if config.preprocessing.scaling == "standard":
            scaler = StandardScaler()
        elif config.preprocessing.scaling == "minmax":
            scaler = MinMaxScaler()
        elif config.preprocessing.scaling == "robust":
            scaler = RobustScaler()
        else:
            scaler = None
        
        if scaler:
            X_scaled = scaler.fit_transform(X)
            X = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
            preprocessing_steps['scaler'] = scaler
    
    # Encode target if categorical
    target_encoder = None
    if y.dtype == 'object':
        target_encoder = LabelEncoder()
        y_encoded = target_encoder.fit_transform(y)
    else:
        y_encoded = y.values
    
    return X, y_encoded, preprocessing_steps, target_encoder


@router.post("/train")
async def start_training(config: dict):
    """
    Start model training - DISABLED FOR DEMO
    Training requires PostgreSQL database.
    This is a placeholder to prevent frontend errors.
    """
    return {
        "job_id": 1,
        "status": "demo_mode",
        "message": "Training disabled - requires PostgreSQL database. Upload functionality working!"
    }


@router.get("/{job_id}/results")
async def get_job_results(job_id: int):
    """
    Get training job results - DEMO MODE
    """
    return {
        "job_id": job_id,
        "status": "completed",
        "message": "Results not available in demo mode"
    }


@router.get("/{job_id}/status", response_model=JobStatus)
async def get_job_status(job_id: int, db: Session = Depends(get_db)):
    """
    Get current job status
    """
    job = db.query(TrainingJob).filter(TrainingJob.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobStatus(
        job_id=job.id,
        status=job.status,
        progress=job.progress,
        current_step=job.current_step,
    )
