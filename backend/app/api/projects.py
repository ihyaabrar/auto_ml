from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import os
import random
from datetime import datetime

from ..core.database import get_db
from ..models.database_models import Dataset
from ..schemas.schemas import DatasetResponse, ColumnInfo

router = APIRouter()


def analyze_columns(df: pd.DataFrame) -> List[ColumnInfo]:
    """Analyze dataframe columns and return metadata"""
    columns_info = []
    
    for col in df.columns:
        col_type = "numeric"
        unique_values = df[col].nunique()
        missing_values = df[col].isnull().sum()
        
        # Determine column type
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            col_type = "datetime"
        elif pd.api.types.is_categorical_dtype(df[col]) or (
            pd.api.types.is_object_dtype(df[col]) and unique_values < len(df) * 0.5
        ):
            col_type = "categorical"
        elif pd.api.types.is_numeric_dtype(df[col]):
            col_type = "numeric"
        
        columns_info.append(
            ColumnInfo(
                name=col,
                type=col_type,
                unique_values=int(unique_values),
                missing_values=int(missing_values),
            )
        )
    
    return columns_info


@router.post("/upload", response_model=DatasetResponse)
async def upload_dataset(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload a dataset file (CSV or Excel)
    """
    try:
        # Validate file extension
        allowed_extensions = [".csv", ".xlsx", ".xls"]
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Generate unique numeric ID for dataset
        import random
        dataset_id = random.randint(10000, 99999)
        
        # Create directory for this dataset
        dataset_dir = os.path.join("uploads", str(dataset_id))
        os.makedirs(dataset_dir, exist_ok=True)
        
        # Save file
        file_path = os.path.join(dataset_dir, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Read and analyze dataset
        if file_ext == ".csv":
            df = pd.read_csv(file_path, encoding='utf-8')
        else:
            df = pd.read_excel(file_path)
        
        # Get dataset info
        num_rows, num_cols = df.shape
        columns_info = analyze_columns(df)
        
        # Create database record (using project_id=1 as default for MVP)
        # In production, this would come from authenticated user
        db_dataset = Dataset(
            id=dataset_id,
            project_id=1,  # Default project for MVP
            file_name=file.filename,
            file_path=file_path,
            num_rows=num_rows,
            num_cols=num_cols,
            column_info=[col.dict() for col in columns_info],
            created_at=datetime.utcnow(),
        )
        
        db.add(db_dataset)
        db.commit()
        db.refresh(db_dataset)
        
        return DatasetResponse(
            id=db_dataset.id,
            file_name=db_dataset.file_name,
            num_rows=db_dataset.num_rows,
            num_cols=db_dataset.num_cols,
            columns=columns_info,
            created_at=db_dataset.created_at,
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{dataset_id}", response_model=DatasetResponse)
async def get_dataset_info(dataset_id: int, db: Session = Depends(get_db)):
    """
    Get dataset information
    """
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    return DatasetResponse(
        id=dataset.id,
        file_name=dataset.file_name,
        num_rows=dataset.num_rows,
        num_cols=dataset.num_cols,
        columns=[ColumnInfo(**col) if isinstance(col, dict) else col for col in dataset.column_info],
        created_at=dataset.created_at,
    )
