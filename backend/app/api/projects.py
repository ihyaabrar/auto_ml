from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import pandas as pd
import os
import random
from datetime import datetime

router = APIRouter()

# Temporary in-memory storage for demo (no database required)
datasets_storage = {}


def analyze_columns(df: pd.DataFrame) -> List[dict]:
    """Analyze dataframe columns and return metadata"""
    columns_info = []
    
    for col in df.columns:
        col_type = "numeric"
        unique_values = int(df[col].nunique())
        missing_values = int(df[col].isnull().sum())
        
        # Determine column type
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            col_type = "datetime"
        elif pd.api.types.is_categorical_dtype(df[col]) or (
            pd.api.types.is_object_dtype(df[col]) and unique_values < len(df) * 0.5
        ):
            col_type = "categorical"
        elif pd.api.types.is_numeric_dtype(df[col]):
            col_type = "numeric"
        
        columns_info.append({
            "name": col,
            "type": col_type,
            "unique_values": unique_values,
            "missing_values": missing_values,
        })
    
    return columns_info


@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    """
    Upload a dataset file (CSV or Excel) - DEMO MODE (no database)
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
        
        # Store in memory (no database)
        datasets_storage[dataset_id] = {
            "id": dataset_id,
            "file_name": file.filename,
            "file_path": file_path,
            "num_rows": num_rows,
            "num_cols": num_cols,
            "columns": columns_info,
            "created_at": datetime.utcnow().isoformat(),
        }
        
        return {
            "id": dataset_id,
            "file_name": file.filename,
            "num_rows": num_rows,
            "num_cols": num_cols,
            "columns": columns_info,
            "created_at": datasets_storage[dataset_id]["created_at"],
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{dataset_id}")
async def get_dataset_info(dataset_id: int):
    """
    Get dataset information - DEMO MODE
    """
    dataset = datasets_storage.get(dataset_id)
    
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    return dataset
