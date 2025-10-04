import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useResume } from '../context/ResumeContext';
import { ArrowRight, Download, Star, AlertCircle, CheckCircle } from 'lucide-react';

const AnalysisResults = () => {
  const { analysisData } = useResume();
  const navigate = useNavigate();

  if (!analysisData) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">No analysis data available. Please upload a resume first.</p>
      </div>
    );
  }

  const { ats_score, parsed_data, optimization_suggestions } = analysisData;

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBgColor = (score) => {
    if (score >= 80) return 'bg-green-100';
    if (score >= 60) return 'bg-yellow-100';
    return 'bg-red-100';
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900">Resume Analysis Results</h2>
        <p className="text-gray-600 mt-2">
          Here's how your resume performs and where you can improve
        </p>
      </div>

      {/* ATS Score Card */}
      <div className="bg-white rounded-xl shadow-sm border p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-semibold text-gray-900">ATS Score</h3>
          <div className={`px-4 py-2 rounded-full ${getScoreBgColor(ats_score.total_score)} ${getScoreColor(ats_score.total_score)} font-semibold`}>
            {ats_score.total_score}/100
          </div>
        </div>

        {/* Score Breakdown */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {Object.entries(ats_score.breakdown).map(([category, data]) => (
            <div key={category} className="border rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium text-gray-700">{category}</span>
                <span className="text-sm font-semibold">
                  {data.score}/{data.max_score}
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${(data.score / data.max_score) * 100}%` }}
                ></div>
              </div>
              <div className="mt-2 space-y-1">
                {data.details.map((detail, index) => (
                  <div key={index} className="flex items-start gap-2 text-xs text-gray-600">
                    <CheckCircle className="h-3 w-3 text-green-500 mt-0.5 flex-shrink-0" />
                    <span>{detail}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Parsed Information */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Skills */}
        <div className="bg-white rounded-xl shadow-sm border p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Skills Found</h3>
          <div className="flex flex-wrap gap-2">
            {parsed_data.skills.map((skill, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-primary-100 text-primary-800 rounded-full text-sm font-medium"
              >
                {skill}
              </span>
            ))}
          </div>
        </div>

        {/* Experience Summary */}
        <div className="bg-white rounded-xl shadow-sm border p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Experience Summary</h3>
          <div className="space-y-3">
            {parsed_data.experience.slice(0, 3).map((job, index) => (
              <div key={index} className="border-l-4 border-primary-500 pl-4">
                <h4 className="font-semibold text-gray-900">{job.title}</h4>
                {job.dates && (
                  <p className="text-sm text-gray-600">{job.dates.join(' - ')}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Quick Suggestions */}
      {optimization_suggestions && (
        <div className="bg-white rounded-xl shadow-sm border p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Quick Improvements</h3>
          <div className="space-y-4">
            {optimization_suggestions.skills && optimization_suggestions.skills.length > 0 && (
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Skills to Add</h4>
                <div className="flex flex-wrap gap-2">
                  {optimization_suggestions.skills.map((skill, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {optimization_suggestions.bullet_points && optimization_suggestions.bullet_points.length > 0 && (
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Bullet Point Improvements</h4>
                <div className="space-y-2">
                  {optimization_suggestions.bullet_points.slice(0, 3).map((improvement, index) => (
                    <div key={index} className="bg-gray-50 p-3 rounded-lg">
                      <div className="text-sm text-gray-600 line-through mb-1">
                        {improvement.original}
                      </div>
                      <div className="text-sm font-medium text-gray-900">
                        {improvement.improved}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-4 justify-center pt-6">
        <button
          onClick={() => navigate('/optimize')}
          className="inline-flex items-center justify-center px-6 py-3 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 transition-colors"
        >
          View Detailed Optimization
          <ArrowRight className="ml-2 h-5 w-5" />
        </button>

        <button
          onClick={() => navigate('/linkedin')}
          className="inline-flex items-center justify-center px-6 py-3 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors"
        >
          LinkedIn Suggestions
          <Star className="ml-2 h-5 w-5" />
        </button>
      </div>
    </div>
  );
};

export default AnalysisResults;
