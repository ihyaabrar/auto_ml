import { useState, useCallback } from 'react';
import { useAppStore } from '../stores/appStore';
import { datasetService } from '../services/api';
import type { Dataset } from '../types';

interface Props {
  onUploadComplete: (dataset: Dataset) => void;
}

const FileUpload = ({ onUploadComplete }: Props) => {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { setDataset } = useAppStore();

  const handleDrop = useCallback(async (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    
    const file = e.dataTransfer.files[0];
    if (file) {
      await uploadFile(file);
    }
  }, []);

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      await uploadFile(file);
    }
  };

  const uploadFile = async (file: File) => {
    setIsUploading(true);
    setError(null);
    
    try {
      const dataset = await datasetService.uploadDataset(file);
      setDataset(dataset);
      onUploadComplete(dataset);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to upload file');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="w-full">
      <div
        onDrop={handleDrop}
        onDragOver={(e) => e.preventDefault()}
        className="border-2 border-dashed border-indigo-300 rounded-lg p-12 text-center hover:border-indigo-500 transition-colors bg-indigo-50"
      >
        <div className="space-y-4">
          <svg
            className="mx-auto h-12 w-12 text-indigo-400"
            stroke="currentColor"
            fill="none"
            viewBox="0 0 48 48"
            aria-hidden="true"
          >
            <path
              d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
              strokeWidth={2}
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          
          <div className="text-sm text-gray-600">
            <label
              htmlFor="file-upload"
              className="relative cursor-pointer bg-white rounded-md font-medium text-indigo-600 hover:text-indigo-500"
            >
              <span>Upload a file</span>
              <input
                id="file-upload"
                name="file-upload"
                type="file"
                accept=".csv,.xlsx,.xls"
                onChange={handleFileSelect}
                className="sr-only"
                disabled={isUploading}
              />
            </label>
            <p className="pt-1">or drag and drop</p>
            <p className="text-xs text-gray-500">
              CSV, Excel files up to 100MB
            </p>
          </div>
          
          {isUploading && (
            <div className="text-indigo-600">
              <svg className="animate-spin mx-auto h-8 w-8" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <p className="mt-2 text-sm">Uploading and analyzing dataset...</p>
            </div>
          )}
          
          {error && (
            <div className="text-red-600 bg-red-50 p-4 rounded-md">
              <p className="text-sm font-medium">Error: {error}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default FileUpload;
