from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")


class Project(Base):
    """Project model"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="projects")
    datasets = relationship("Dataset", back_populates="project", cascade="all, delete-orphan")


class Dataset(Base):
    """Dataset model"""
    __tablename__ = "datasets"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    num_rows = Column(Integer, nullable=False)
    num_cols = Column(Integer, nullable=False)
    column_info = Column(JSON, default=[])  # Store column metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="datasets")
    jobs = relationship("TrainingJob", back_populates="dataset", cascade="all, delete-orphan")


class TrainingJob(Base):
    """Training job model"""
    __tablename__ = "jobs_training"
    
    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    status = Column(String, default="pending")  # pending, running, completed, failed
    mode = Column(String, default="custom")  # auto or custom
    config = Column(JSON, default={})  # Store training configuration
    progress = Column(Integer, default=0)
    current_step = Column(String, default="")
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    dataset = relationship("Dataset", back_populates="jobs")
    models = relationship("Model", back_populates="job", cascade="all, delete-orphan")


class Model(Base):
    """Trained model metadata"""
    __tablename__ = "models"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs_training.id"), nullable=False)
    algorithm_name = Column(String, nullable=False)
    metrics = Column(JSON, default={})  # Store evaluation metrics
    feature_importance = Column(JSON, default=[])
    confusion_matrix = Column(JSON, default=[])
    model_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    job = relationship("TrainingJob", back_populates="models")
