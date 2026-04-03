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


@router.post("/train", response_model=dict)
async def start_training(
    config: TrainingConfig,
    db: Session = Depends(get_db)
):
    """
    Start model training (synchronous for MVP - will be async in Phase 2)
    """
    try:
        # Load data
        df, dataset = load_and_prepare_data(config.dataset_id, db)
        
        # Validate target column
        if config.target_column not in df.columns:
            raise HTTPException(
                status_code=400,
                detail=f"Target column '{config.target_column}' not found in dataset"
            )
        
        # Create training job record
        job = TrainingJob(
            dataset_id=config.dataset_id,
            status="running",
            mode=config.mode,
            config=config.dict(),
            progress=0,
            current_step="Loading dataset...",
            start_time=datetime.utcnow(),
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        
        # Preprocess data
        job.current_step = "Preprocessing data..."
        db.commit()
        
        X, y, preprocessing_steps, target_encoder = preprocess_data(
            df, config.target_column, config
        )
        
        # Split data
        job.current_step = "Splitting data into train/test sets..."
        db.commit()
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y if config.task_type == "classification" else None
        )
        
        # Train model
        job.current_step = "Training Random Forest model..."
        db.commit()
        
        if config.task_type == "classification":
            model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
        else:
            model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
        
        model.fit(X_train, y_train)
        job.progress = 70
        db.commit()
        
        # Evaluate model
        job.current_step = "Evaluating model..."
        db.commit()
        
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        if config.task_type == "classification":
            metrics = {
                "accuracy": float(accuracy_score(y_test, y_pred)),
                "precision": float(precision_score(y_test, y_pred, average='weighted', zero_division=0)),
                "recall": float(recall_score(y_test, y_pred, average='weighted', zero_division=0)),
                "f1_score": float(f1_score(y_test, y_pred, average='weighted', zero_division=0)),
            }
            
            # Confusion matrix
            from sklearn.metrics import confusion_matrix
            cm = confusion_matrix(y_test, y_pred).tolist()
        else:
            metrics = {
                "mse": float(mean_squared_error(y_test, y_pred)),
                "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
                "r2": float(r2_score(y_test, y_pred)),
            }
            cm = []
        
        # Feature importance
        feature_importance = [
            {"feature": feat, "importance": float(imp)}
            for feat, imp in zip(X.columns, model.feature_importances_)
        ]
        feature_importance.sort(key=lambda x: x["importance"], reverse=True)
        
        # Save model
        job.current_step = "Saving model..."
        db.commit()
        
        model_filename = f"model_{job.id}.pkl"
        model_path = os.path.join(settings.MODELS_DIR, model_filename)
        
        # Save complete pipeline
        pipeline = {
            'model': model,
            'preprocessing': preprocessing_steps,
            'target_encoder': target_encoder,
            'feature_names': X.columns.tolist(),
            'config': config.dict(),
        }
        
        joblib.dump(pipeline, model_path)
        
        # Create model record
        db_model = Model(
            job_id=job.id,
            algorithm_name="RandomForest",
            metrics=metrics,
            feature_importance=feature_importance[:10],  # Top 10 features
            confusion_matrix=cm,
            model_path=model_path,
        )
        db.add(db_model)
        
        # Update job status
        job.status = "completed"
        job.progress = 100
        job.current_step = "Training completed successfully!"
        job.end_time = datetime.utcnow()
        db.commit()
        
        return {
            "job_id": job.id,
            "status": "completed",
            "message": "Model trained successfully"
        }
        
    except Exception as e:
        # Update job status on error
        if 'job' in locals():
            job.status = "failed"
            job.error_message = str(e)
            job.end_time = datetime.utcnow()
            db.commit()
        
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{job_id}/results", response_model=ModelResults)
async def get_job_results(job_id: int, db: Session = Depends(get_db)):
    """
    Get training job results
    """
    job = db.query(TrainingJob).filter(TrainingJob.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.status != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Job is not completed. Current status: {job.status}"
        )
    
    # Get model
    model = db.query(Model).filter(Model.job_id == job_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    return ModelResults(
        job_id=job.id,
        status=job.status,
        metrics=ModelMetrics(**model.metrics),
        feature_importance=[FeatureImportance(**fi) for fi in model.feature_importance],
        confusion_matrix=model.confusion_matrix,
        model_url=f"/api/v1/models/{model.id}/download",
    )


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
