import { useState } from 'react';
import FileUpload from '../components/FileUpload';
import { useAppStore } from '../stores/appStore';
import type { Dataset, TrainingConfig } from '../types';

const HomePage = () => {
  const { currentDataset, currentJob, isTraining } = useAppStore();
  const [step, setStep] = useState<'upload' | 'configure' | 'training' | 'results'>('upload');
  const [targetColumn, setTargetColumn] = useState('');
  const [taskType, setTaskType] = useState<'classification' | 'regression'>('classification');
  const [mode, setMode] = useState<'auto' | 'custom'>('custom');

  const handleUploadComplete = (dataset: Dataset) => {
    console.log('Dataset uploaded:', dataset);
    if (dataset.columns.length > 0) {
      // Auto-select first numeric or categorical column as target
      const suggestedTarget = dataset.columns.find(
        col => col.type === 'numeric' || col.type === 'categorical'
      );
      if (suggestedTarget) {
        setTargetColumn(suggestedTarget.name);
      }
    }
    setStep('configure');
  };

  const handleStartTraining = async () => {
    if (!currentDataset || !targetColumn) return;

    const config: TrainingConfig = {
      dataset_id: currentDataset.id,
      target_column: targetColumn,
      task_type: taskType,
      mode: mode,
      preprocessing: mode === 'custom' ? {
        missing_values: 'median',
        categorical_encoding: 'one_hot',
        scaling: 'standard'
      } : undefined,
      models: mode === 'custom' ? ['random_forest'] : undefined,
      hyperparameter_tuning: mode === 'custom',
      evaluation_metric: taskType === 'classification' ? 'f1_score' : 'rmse'
    };

    console.log('Starting training with config:', config);
    setStep('training');
    
    // TODO: Call API to start training
    // For now, just simulate
    setTimeout(() => {
      setStep('results');
    }, 5000);
  };

  const handleReset = () => {
    setStep('upload');
    setTargetColumn('');
    setTaskType('classification');
    setMode('custom');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-indigo-900 mb-4">
            🤖 AutoML Platform
          </h1>
          <p className="text-xl text-indigo-700">
            Build Machine Learning models with ease
          </p>
        </header>

        {/* Progress Steps */}
        <div className="max-w-4xl mx-auto mb-8">
          <div className="flex items-center justify-between">
            {['Upload Data', 'Configure', 'Training', 'Results'].map((label, idx) => (
              <div key={label} className="flex items-center">
                <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                  step >= (['upload', 'configure', 'training', 'results'][idx] as any)
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-300 text-gray-600'
                }`}>
                  {idx + 1}
                </div>
                <span className={`ml-2 text-sm font-medium ${
                  step >= (['upload', 'configure', 'training', 'results'][idx] as any)
                    ? 'text-indigo-900'
                    : 'text-gray-500'
                }`}>
                  {label}
                </span>
                {idx < 3 && (
                  <div className={`w-16 h-1 mx-2 ${
                    step > (['upload', 'configure', 'training', 'results'][idx] as any)
                      ? 'bg-indigo-600'
                      : 'bg-gray-300'
                  }`} />
                )}
              </div>
            ))}
          </div>
        </div>

        <main className="max-w-4xl mx-auto">
          <div className="bg-white rounded-lg shadow-xl p-8">
            {/* Step 1: Upload */}
            {step === 'upload' && (
              <div className="space-y-6">
                <h2 className="text-2xl font-semibold text-gray-800 mb-4">
                  Step 1: Upload Your Dataset
                </h2>
                <p className="text-gray-600 mb-6">
                  Upload a CSV or Excel file containing your data. The system will automatically analyze columns and detect data types.
                </p>
                <FileUpload onUploadComplete={handleUploadComplete} />
              </div>
            )}

            {/* Step 2: Configure */}
            {step === 'configure' && currentDataset && (
              <div className="space-y-6">
                <h2 className="text-2xl font-semibold text-gray-800 mb-4">
                  Step 2: Configure Training
                </h2>
                
                {/* Dataset Info */}
                <div className="bg-indigo-50 p-4 rounded-lg mb-6">
                  <h3 className="font-semibold text-indigo-900 mb-2">Dataset: {currentDataset.file_name}</h3>
                  <p className="text-sm text-indigo-700">
                    {currentDataset.num_rows.toLocaleString()} rows × {currentDataset.num_cols} columns
                  </p>
                </div>

                {/* Target Selection */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Target Column (What do you want to predict?)
                  </label>
                  <select
                    value={targetColumn}
                    onChange={(e) => setTargetColumn(e.target.value)}
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  >
                    <option value="">Select target column...</option>
                    {currentDataset.columns.map((col) => (
                      <option key={col.name} value={col.name}>
                        {col.name} ({col.type})
                      </option>
                    ))}
                  </select>
                </div>

                {/* Task Type */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Task Type
                  </label>
                  <div className="grid grid-cols-2 gap-4">
                    <button
                      onClick={() => setTaskType('classification')}
                      className={`p-4 border-2 rounded-lg text-center ${
                        taskType === 'classification'
                          ? 'border-indigo-600 bg-indigo-50'
                          : 'border-gray-300'
                      }`}
                    >
                      <div className="font-semibold text-gray-900">Classification</div>
                      <div className="text-sm text-gray-600 mt-1">Predict categories</div>
                    </button>
                    <button
                      onClick={() => setTaskType('regression')}
                      className={`p-4 border-2 rounded-lg text-center ${
                        taskType === 'regression'
                          ? 'border-indigo-600 bg-indigo-50'
                          : 'border-gray-300'
                      }`}
                    >
                      <div className="font-semibold text-gray-900">Regression</div>
                      <div className="text-sm text-gray-600 mt-1">Predict numbers</div>
                    </button>
                  </div>
                </div>

                {/* Mode Selection */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Training Mode
                  </label>
                  <div className="grid grid-cols-2 gap-4">
                    <button
                      onClick={() => setMode('auto')}
                      className={`p-4 border-2 rounded-lg text-center ${
                        mode === 'auto'
                          ? 'border-indigo-600 bg-indigo-50'
                          : 'border-gray-300'
                      }`}
                    >
                      <div className="font-semibold text-gray-900">🚀 AutoML</div>
                      <div className="text-sm text-gray-600 mt-1">Automatic model selection & tuning</div>
                    </button>
                    <button
                      onClick={() => setMode('custom')}
                      className={`p-4 border-2 rounded-lg text-center ${
                        mode === 'custom'
                          ? 'border-indigo-600 bg-indigo-50'
                          : 'border-gray-300'
                      }`}
                    >
                      <div className="font-semibold text-gray-900">⚙️ Custom</div>
                      <div className="text-sm text-gray-600 mt-1">Manual configuration</div>
                    </button>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex gap-4 pt-6">
                  <button
                    onClick={() => setStep('upload')}
                    className="px-6 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
                  >
                    Back
                  </button>
                  <button
                    onClick={handleStartTraining}
                    disabled={!targetColumn}
                    className="px-6 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed ml-auto"
                  >
                    Start Training →
                  </button>
                </div>
              </div>
            )}

            {/* Step 3: Training */}
            {step === 'training' && (
              <div className="space-y-6 text-center">
                <h2 className="text-2xl font-semibold text-gray-800 mb-4">
                  Training in Progress...
                </h2>
                <div className="py-12">
                  <svg className="animate-spin mx-auto h-16 w-16 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <p className="mt-6 text-lg text-gray-700">
                    {isTraining ? currentJob?.current_step || 'Training model...' : 'Preparing training...'}
                  </p>
                  <p className="mt-2 text-sm text-gray-500">
                    This may take a few minutes depending on your dataset size
                  </p>
                </div>
              </div>
            )}

            {/* Step 4: Results */}
            {step === 'results' && (
              <div className="space-y-6">
                <h2 className="text-2xl font-semibold text-gray-800 mb-4">
                  🎉 Training Complete!
                </h2>
                <div className="bg-green-50 border border-green-200 rounded-lg p-6 mb-6">
                  <h3 className="text-lg font-semibold text-green-900 mb-2">
                    Model Successfully Trained
                  </h3>
                  <p className="text-green-700">
                    Your model has been trained and is ready for use. Results and metrics will be displayed here once the backend integration is complete.
                  </p>
                </div>
                
                <div className="flex gap-4">
                  <button
                    onClick={handleReset}
                    className="px-6 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
                  >
                    Train Another Model
                  </button>
                  <button
                    className="px-6 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
                  >
                    Download Model
                  </button>
                </div>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
};

export default HomePage;
