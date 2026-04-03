from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# Dataset Schemas
class ColumnInfo(BaseModel):
    name: str
    type: str  # numeric, categorical, datetime
    unique_values: Optional[int] = None
    missing_values: Optional[int] = None


class DatasetResponse(BaseModel):
    id: int
    file_name: str
    num_rows: int
    num_cols: int
    columns: List[ColumnInfo] = []
    created_at: datetime
    
    class Config:
        from_attributes = True


# Training Configuration Schemas
class PreprocessingConfig(BaseModel):
    missing_values: str = "median"  # mean, median, mode, drop
    categorical_encoding: str = "one_hot"  # one_hot, label
    scaling: str = "standard"  # standard, minmax, robust, none


class TrainingConfig(BaseModel):
    dataset_id: int
    target_column: str
    task_type: str  # classification or regression
    mode: str = "custom"  # auto or custom
    preprocessing: Optional[PreprocessingConfig] = None
    models: Optional[List[str]] = None
    hyperparameter_tuning: Optional[bool] = True
    evaluation_metric: Optional[str] = None


# Job Status Schemas
class JobStatus(BaseModel):
    job_id: int
    status: str
    progress: Optional[int] = None
    current_step: Optional[str] = None


# Model Results Schema
class FeatureImportance(BaseModel):
    feature: str
    importance: float


class ModelMetrics(BaseModel):
    accuracy: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1_score: Optional[float] = None
    mse: Optional[float] = None
    rmse: Optional[float] = None
    r2: Optional[float] = None


class ModelResults(BaseModel):
    job_id: int
    status: str
    metrics: ModelMetrics
    feature_importance: Optional[List[FeatureImportance]] = None
    confusion_matrix: Optional[List[List[int]]] = None
    model_url: Optional[str] = None


# WebSocket Message Schema
class WebSocketMessage(BaseModel):
    status: str
    step: Optional[str] = None
    progress: Optional[int] = None
    timestamp: Optional[datetime] = None
    error: Optional[str] = None
