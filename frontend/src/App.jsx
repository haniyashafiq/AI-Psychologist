/**
 * Main App component
 */
import { useState } from 'react';
import { TextInputForm } from './components/assessment/TextInputForm';
import { Spinner } from './components/common/Spinner';
import { DiagnosisReport } from './components/results/DiagnosisReport';
import { useAssessment } from './hooks/useAssessment';
import './index.css';

function App() {
  const { isLoading, results, error, analyze, reset } = useAssessment();
  const [showResults, setShowResults] = useState(false);

  const handleAnalyze = async (text) => {
    try {
      await analyze(text);
      setShowResults(true);
    } catch (err) {
      console.error('Analysis failed:', err);
    }
  };

  const handleReset = () => {
    reset();
    setShowResults(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">🧠 AI Psychologist</h1>
          <p className="text-lg text-gray-600">DSM-5 Based Depression Diagnosis Assistant</p>
          <p className="text-sm text-gray-500 mt-2">
            For use by qualified mental health professionals only
          </p>
        </header>

        {/* Main Content */}
        <main className="bg-white rounded-xl shadow-xl p-8">
          {!showResults ? (
            <>
              <div className="mb-6">
                <h2 className="text-2xl font-semibold text-gray-800 mb-2">Patient Assessment</h2>
                <p className="text-gray-600">
                  Enter patient symptom descriptions in natural language. The system will analyze
                  the text and provide a diagnostic assessment based on DSM-5 criteria for Major
                  Depressive Disorder.
                </p>
              </div>

              <TextInputForm onSubmit={handleAnalyze} isLoading={isLoading} />

              {error && (
                <div className="mt-6 bg-red-50 border-2 border-red-400 rounded-lg p-4">
                  <div className="flex items-start space-x-2">
                    <span className="text-2xl">❌</span>
                    <div>
                      <p className="font-semibold text-red-900">Error</p>
                      <p className="text-red-800 text-sm">{error}</p>
                    </div>
                  </div>
                </div>
              )}
            </>
          ) : (
            <>
              {isLoading ? (
                <div className="py-12">
                  <Spinner size="lg" />
                  <p className="text-center text-gray-600 mt-4">
                    Analyzing symptoms and generating diagnostic report...
                  </p>
                </div>
              ) : (
                <DiagnosisReport results={results} onReset={handleReset} />
              )}
            </>
          )}
        </main>

        {/* Footer */}
        <footer className="text-center mt-8 text-sm text-gray-600">
          <p>Version 1.0.0 • Built with React, Express, and Python FastAPI</p>
          <p className="mt-1">
            Rule-based NLP system using DSM-5 Major Depressive Disorder criteria
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;
