import { create } from 'zustand';
import type { Dataset, TrainingJob, ModelResults } from '../types';

interface AppState {
  currentDataset: Dataset | null;
  currentJob: TrainingJob | null;
  currentResults: ModelResults | null;
  isUploading: boolean;
  isTraining: boolean;
  
  setDataset: (dataset: Dataset) => void;
  clearDataset: () => void;
  setJob: (job: TrainingJob) => void;
  updateJobProgress: (progress: number, step: string) => void;
  setResults: (results: ModelResults) => void;
  clearAll: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  currentDataset: null,
  currentJob: null,
  currentResults: null,
  isUploading: false,
  isTraining: false,
  
  setDataset: (dataset) => set({ currentDataset: dataset }),
  clearDataset: () => set({ currentDataset: null }),
  setJob: (job) => set({ currentJob: job, isTraining: true, currentResults: null }),
  updateJobProgress: (progress, step) => 
    set((state) => ({
      currentJob: state.currentJob 
        ? { ...state.currentJob, progress, current_step: step }
        : null,
    })),
  setResults: (results) => set({ currentResults: results, isTraining: false }),
  clearAll: () => set({
    currentDataset: null,
    currentJob: null,
    currentResults: null,
    isUploading: false,
    isTraining: false,
  }),
}));
