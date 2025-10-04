import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ResumeUpload from './components/ResumeUpload';
import AnalysisResults from './components/AnalysisResults';
import OptimizationSuggestions from './components/OptimizationSuggestions';
import LinkedInGenerator from './components/LinkedInGenerator';
import { ResumeProvider } from './context/ResumeContext';

function App() {
  return (
    <ResumeProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <header className="bg-white shadow-sm">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
              <h1 className="text-2xl font-bold text-gray-900">
                AI Resume Optimizer
              </h1>
            </div>
          </header>

          <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <Routes>
              <Route path="/" element={<ResumeUpload />} />
              <Route path="/analysis" element={<AnalysisResults />} />
              <Route path="/optimize" element={<OptimizationSuggestions />} />
              <Route path="/linkedin" element={<LinkedInGenerator />} />
            </Routes>
          </main>
        </div>
      </Router>
    </ResumeProvider>
  );
}

export default App;
