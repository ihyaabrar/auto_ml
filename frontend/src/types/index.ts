export interface Dataset {
  id: string;
  file_name: string;
  num_rows: number;
  num_cols: number;
  columns: ColumnInfo[];
  created_at?: string;
}

export interface ColumnInfo {
  name: string;
  type: 'numeric' | 'categorical' | 'datetime';
  unique_values?: number;
  missing_values?: number;
}

export interface TrainingConfig {
  dataset_id: string;
  target_column: string;
  task_type: 'classification' | 'regression';
  mode: 'auto' | 'custom';
  preprocessing?: {
    missing_values: 'mean' | 'median' | 'mode' | 'drop';
    categorical_encoding: 'one_hot' | 'label';
    scaling: 'standard' | 'minmax' | 'robust' | 'none';
  };
  models?: string[];
  hyperparameter_tuning?: boolean;
  evaluation_metric?: string;
}

export interface TrainingJob {
  id: string;
  dataset_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  mode: 'auto' | 'custom';
  progress?: number;
  current_step?: string;
  created_at?: string;
}

export interface ModelResults {
  job_id: string;
  status: string;
  metrics: {
    accuracy?: number;
    precision?: number;
    recall?: number;
    f1_score?: number;
    mse?: number;
    rmse?: number;
    r2?: number;
  };
  feature_importance?: FeatureImportance[];
  confusion_matrix?: number[][];
  model_url?: string;
}

export interface FeatureImportance {
  feature: string;
  importance: number;
}

export interface WebSocketMessage {
  status: 'pending' | 'running' | 'completed' | 'failed';
  step?: string;
  progress?: number;
  timestamp?: string;
  error?: string;
}
