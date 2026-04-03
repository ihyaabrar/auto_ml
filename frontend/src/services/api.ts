import axios from 'axios';
import type { Dataset, TrainingConfig, ModelResults } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const datasetService = {
  uploadDataset: async (file: File): Promise<Dataset> => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/api/v1/projects/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  },

  getDatasetInfo: async (datasetId: string): Promise<Dataset> => {
    const response = await api.get(`/api/v1/datasets/${datasetId}`);
    return response.data;
  },
};

export const trainingService = {
  startTraining: async (config: TrainingConfig): Promise<{ job_id: string }> => {
    const response = await api.post('/api/v1/jobs/train', config);
    return response.data;
  },

  getJobResults: async (jobId: string): Promise<ModelResults> => {
    const response = await api.get(`/api/v1/jobs/${jobId}/results`);
    return response.data;
  },

  getJobStatus: async (jobId: string): Promise<{ status: string; progress?: number }> => {
    const response = await api.get(`/api/v1/jobs/${jobId}/status`);
    return response.data;
  },
};

export const websocketService = {
  connect: (jobId: string, onMessage: (data: any) => void) => {
    const wsUrl = API_BASE_URL.replace('http', 'ws').replace('https', 'wss');
    const socket = new WebSocket(`${wsUrl}/ws/jobs/${jobId}`);
    
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessage(data);
    };
    
    return socket;
  },
};
