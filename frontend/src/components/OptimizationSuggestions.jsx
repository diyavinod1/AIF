import React, { useState } from 'react';
import { useResume } from '../context/ResumeContext';
import { ArrowLeft, Download, Lightbulb, Zap, Target } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const OptimizationSuggestions = () => {
  const { analysisData } = useResume();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('skills');
  const [region, setRegion] = useState('US');

  if (!analysisData) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">No analysis data available. Please upload a resume first.</p>
        <button
          onClick={() => navigate('/')}
          className="mt-4 inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Upload
        </button>
      </div>
    );
  }

  const { optimization_suggestions, parsed_data } = analysisData;

  const handleOptimizeResume = async () => {
    try {
      const formData = new URLSearchParams();
      formData.append('filename', 'resume.pdf'); // This should be the actual uploaded filename
      formData.append('job_description', '');
      formData.append('region', region);

      const response = await fetch('http://localhost:8000/api/optimize-resume', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        // Handle download or preview of optimized resume
        alert('Resume optimized successfully!');
      }
    } catch (error) {
      console.error('Error optimizing resume:', error);
    }
  };

  const tabs = [
    { id: 'skills', name: 'Skills', icon: Target },
    { id: 'experience', name: 'Experience', icon: Zap },
    { id: 'summary', name: 'Summary', icon: Lightbulb },
    { id: 'keywords', name: 'Keywords', icon: Lightbulb },
  ];

  const renderTabContent = () => {
    switch (activeTab) {
      case 'skills':
        return (
          <div className="space-y-6">
            <div>
              <h4 className="font-semibold text-gray-900 mb-3">Current Skills</h4>
              <div className="flex flex-wrap gap-2 mb-6">
                {parsed_data.skills.map((skill, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            {optimization_suggestions.skills && optimization_suggestions.skills.length > 0 && (
              <div>
                <h4 className="font-semibold text-gray-900 mb-3">Recommended Skills to Add</h4>
                <div className="flex flex-wrap gap-2">
                  {optimization_suggestions.skills.map((skill, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm font-medium"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
                <p className="text-sm text-gray-600 mt-3">
                  These skills were identified from the job description and are commonly sought after in your field.
                </p>
              </div>
            )}
          </div>
        );

      case 'experience':
        return (
          <div className="space-y-6">
            <h4 className="font-semibold text-gray-900">Bullet Point Improvements</h4>
            
            {optimization_suggestions.experience && optimization_suggestions.experience.length > 0 ? (
              optimization_suggestions.experience.map((job, jobIndex) => (
                <div key={jobIndex} className="border rounded-lg p-4">
                  <h5 className="font-medium text-gray-900 mb-3">{job.title}</h5>
                  <div className="space-y-3">
                    {job.suggestions.map((suggestion, suggestionIndex) => (
                      <div key={suggestionIndex} className="bg-gray-50 rounded-lg p-3">
                        <div className="text-sm text-gray-600 mb-2">
                          <span className="font-medium">Original:</span> {suggestion.original}
                        </div>
                        <div className="text-sm font-medium text-gray-900 mb-2">
                          <span className="font-medium">Improved:</span> {suggestion.improved}
                        </div>
                        <div className="text-xs text-blue-600">
                          💡 {suggestion.suggestion}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center py-8 text-gray-500">
                <Lightbulb className="mx-auto h-12 w-12 text-gray-400 mb-3" />
                <p>No major improvements needed for your experience section. Great job!</p>
              </div>
            )}
          </div>
        );

      case 'summary':
        return (
          <div className="space-y-6">
            <div>
              <h4 className="font-semibold text-gray-900 mb-3">Current Summary</h4>
              <div className="bg-gray-50 rounded-lg p-4 mb-4">
                <p className="text-gray-700">{parsed_data.summary || 'No summary found in resume.'}</p>
              </div>
            </div>

            {optimization_suggestions.summary && optimization_suggestions.summary.length > 0 && (
              <div>
                <h4 className="font-semibold text-gray-900 mb-3">Improvement Suggestions</h4>
                <div className="space-y-3">
                  {optimization_suggestions.summary.map((suggestion, index) => (
                    <div key={index} className="flex items-start gap-3 p-3 bg-yellow-50 rounded-lg">
                      <Lightbulb className="h-5 w-5 text-yellow-600 mt-0.5 flex-shrink-0" />
                      <p className="text-sm text-yellow-800">{suggestion}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="bg-blue-50 rounded-lg p-4">
              <h5 className="font-semibold text-blue-900 mb-2">Pro Tips for Summary</h5>
              <ul className="text-sm text-blue-800 space-y-1">
                <li>• Start with a strong action verb</li>
                <li>• Include 2-3 key achievements</li>
                <li>• Mention your years of experience</li>
                <li>• Include relevant industry keywords</li>
                <li>• Keep it concise (3-5 lines)</li>
              </ul>
            </div>
          </div>
        );

      case 'keywords':
        return (
          <div className="space-y-6">
            {optimization_suggestions.keywords && optimization_suggestions.keywords.length > 0 ? (
              <>
                <div>
                  <h4 className="font-semibold text-gray-900 mb-3">Recommended Keywords</h4>
                  <div className="flex flex-wrap gap-2 mb-4">
                    {optimization_suggestions.keywords.map((keyword, index) => (
                      <span
                        key={index}
                        className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-medium"
                      >
                        {keyword}
                      </span>
                    ))}
                  </div>
                  <p className="text-sm text-gray-600">
                    These keywords are commonly searched by recruiters and ATS systems in your industry.
                  </p>
                </div>

                <div className="bg-green-50 rounded-lg p-4">
                  <h5 className="font-semibold text-green-900 mb-2">How to Use These Keywords</h5>
                  <ul className="text-sm text-green-800 space-y-1">
                    <li>• Sprinkle naturally throughout your resume</li>
                    <li>• Include in skills, experience, and summary sections</li>
                    <li>• Don't overuse - maintain readability</li>
                    <li>• Focus on the most relevant 5-7 keywords</li>
                  </ul>
                </div>
              </>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <Target className="mx-auto h-12 w-12 text-gray-400 mb-3" />
                <p>No specific keyword suggestions available. Consider adding a job description for targeted keyword recommendations.</p>
              </div>
            )}
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <button
            onClick={() => navigate('/analysis')}
            className="inline-flex items-center text-gray-600 hover:text-gray-900 mb-2"
          >
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Analysis
          </button>
          <h2 className="text-3xl font-bold text-gray-900">Optimization Suggestions</h2>
          <p className="text-gray-600 mt-1">
            AI-powered recommendations to improve your resume's impact
          </p>
        </div>

        <div className="flex items-center gap-4">
          <select
            value={region}
            onChange={(e) => setRegion(e.target.value)}
            className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="US">US Format</option>
            <option value="UK">UK Format</option>
            <option value="India">India Format</option>
          </select>

          <button
            onClick={handleOptimizeResume}
            className="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            <Download className="mr-2 h-4 w-4" />
            Download Optimized
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-2 px-1 border-b-2 font-medium text-sm whitespace-nowrap flex items-center gap-2 ${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <Icon className="h-4 w-4" />
                {tab.name}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="bg-white rounded-xl shadow-sm border p-6">
        {renderTabContent()}
      </div>

      {/* Quick Actions */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-lg border p-4 text-center">
          <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-2">
            <Zap className="h-5 w-5 text-blue-600" />
          </div>
          <h4 className="font-semibold text-gray-900 text-sm">Action Verbs</h4>
          <p className="text-xs text-gray-600 mt-1">Use strong action-oriented language</p>
        </div>

        <div className="bg-white rounded-lg border p-4 text-center">
          <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-2">
            <Target className="h-5 w-5 text-green-600" />
          </div>
          <h4 className="font-semibold text-gray-900 text-sm">Quantify Results</h4>
          <p className="text-xs text-gray-600 mt-1">Add numbers and metrics</p>
        </div>

        <div className="bg-white rounded-lg border p-4 text-center">
          <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-2">
            <Lightbulb className="h-5 w-5 text-purple-600" />
          </div>
          <h4 className="font-semibold text-gray-900 text-sm">ATS Friendly</h4>
          <p className="text-xs text-gray-600 mt-1">Optimize for applicant tracking systems</p>
        </div>
      </div>
    </div>
  );
};

export default OptimizationSuggestions;