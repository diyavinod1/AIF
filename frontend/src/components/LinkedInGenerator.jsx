import React, { useState } from 'react';
import { useResume } from '../context/ResumeContext';
import { ArrowLeft, Copy, Check, Linkedin, User, Star, Award } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const LinkedInGenerator = () => {
  const { analysisData } = useResume();
  const navigate = useNavigate();
  const [copiedSection, setCopiedSection] = useState(null);

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

  const { linkedin_suggestions, parsed_data } = analysisData;

  const handleCopyToClipboard = async (text, section) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedSection(section);
      setTimeout(() => setCopiedSection(null), 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  const Card = ({ title, icon: Icon, children, section, content }) => (
    <div className="bg-white rounded-xl shadow-sm border p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Icon className="h-5 w-5 text-primary-600" />
          <h3 className="font-semibold text-gray-900">{title}</h3>
        </div>
        {content && (
          <button
            onClick={() => handleCopyToClipboard(content, section)}
            className="inline-flex items-center gap-1 px-3 py-1 text-sm text-gray-600 hover:text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
          >
            {copiedSection === section ? (
              <>
                <Check className="h-4 w-4" />
                Copied!
              </>
            ) : (
              <>
                <Copy className="h-4 w-4" />
                Copy
              </>
            )}
          </button>
        )}
      </div>
      {children}
    </div>
  );

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
          <div className="flex items-center gap-3">
            <Linkedin className="h-8 w-8 text-blue-600" />
            <div>
              <h2 className="text-3xl font-bold text-gray-900">LinkedIn Optimization</h2>
              <p className="text-gray-600 mt-1">
                Boost your profile visibility with AI-generated content
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left Column */}
        <div className="space-y-6">
          {/* Headline Suggestions */}
          <Card 
            title="Headline Suggestions" 
            icon={User}
            section="headline"
            content={linkedin_suggestions.headline?.[0]}
          >
            <div className="space-y-3">
              {linkedin_suggestions.headline?.map((headline, index) => (
                <div
                  key={index}
                  className="p-3 border border-gray-200 rounded-lg hover:border-primary-300 transition-colors cursor-pointer"
                  onClick={() => handleCopyToClipboard(headline, `headline-${index}`)}
                >
                  <p className="text-gray-900 font-medium">{headline}</p>
                  <div className="flex items-center gap-1 mt-2">
                    <Star className="h-3 w-3 text-yellow-500" />
                    <span className="text-xs text-gray-500">
                      {index === 0 ? 'Recommended' : `Alternative ${index}`}
                    </span>
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-4 p-3 bg-blue-50 rounded-lg">
              <p className="text-sm text-blue-800">
                <strong>Pro Tip:</strong> Your headline is the first thing recruiters see. 
                Include your target role and key skills.
              </p>
            </div>
          </Card>

          {/* Skills Recommendations */}
          <Card title="Skills Recommendations" icon={Award}>
            <div className="flex flex-wrap gap-2">
              {linkedin_suggestions.skills?.map((skill, index) => (
                <span
                  key={index}
                  className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium"
                >
                  {skill}
                </span>
              ))}
            </div>
            <div className="mt-4 p-3 bg-green-50 rounded-lg">
              <p className="text-sm text-green-800">
                <strong>Note:</strong> LinkedIn allows up to 50 skills. Focus on the most relevant 
                and in-demand skills for your target roles.
              </p>
            </div>
          </Card>
        </div>

        {/* Right Column */}
        <div className="space-y-6">
          {/* About Section */}
          <Card 
            title="About Section" 
            icon={User}
            section="about"
            content={linkedin_suggestions.about_section}
          >
            <div className="bg-gray-50 rounded-lg p-4">
              <pre className="text-sm text-gray-700 whitespace-pre-wrap font-sans">
                {linkedin_suggestions.about_section}
              </pre>
            </div>
            <div className="mt-4 p-3 bg-purple-50 rounded-lg">
              <p className="text-sm text-purple-800">
                <strong>Best Practices:</strong> Keep it professional but personal, include keywords, 
                highlight achievements, and end with a call to action.
              </p>
            </div>
          </Card>

          {/* Keywords for SEO */}
          <Card title="Profile Keywords" icon={Star}>
            <div className="flex flex-wrap gap-2">
              {linkedin_suggestions.keywords?.map((keyword, index) => (
                <span
                  key={index}
                  className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm"
                >
                  {keyword}
                </span>
              ))}
            </div>
            <div className="mt-4 p-3 bg-yellow-50 rounded-lg">
              <p className="text-sm text-yellow-800">
                <strong>SEO Tip:</strong> Sprinkle these keywords naturally throughout your 
                profile to improve search visibility.
              </p>
            </div>
          </Card>
        </div>
      </div>

      {/* LinkedIn Best Practices */}
      <div className="mt-8 bg-white rounded-xl shadow-sm border p-6">
        <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <Linkedin className="h-5 w-5 text-blue-600" />
          LinkedIn Profile Best Practices
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-3">
            <div className="flex items-start gap-2">
              <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                <span className="text-green-600 text-sm font-bold">1</span>
              </div>
              <div>
                <h4 className="font-medium text-gray-900">Professional Photo</h4>
                <p className="text-sm text-gray-600">Use a clear, professional headshot with good lighting</p>
              </div>
            </div>
            <div className="flex items-start gap-2">
              <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                <span className="text-green-600 text-sm font-bold">2</span>
              </div>
              <div>
                <h4 className="font-medium text-gray-900">Custom URL</h4>
                <p className="text-sm text-gray-600">Create a custom LinkedIn URL with your name</p>
              </div>
            </div>
            <div className="flex items-start gap-2">
              <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                <span className="text-green-600 text-sm font-bold">3</span>
              </div>
              <div>
                <h4 className="font-medium text-gray-900">Featured Section</h4>
                <p className="text-sm text-gray-600">Showcase your best work, projects, or publications</p>
              </div>
            </div>
          </div>
          <div className="space-y-3">
            <div className="flex items-start gap-2">
              <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                <span className="text-green-600 text-sm font-bold">4</span>
              </div>
              <div>
                <h4 className="font-medium text-gray-900">Engage Regularly</h4>
                <p className="text-sm text-gray-600">Share insights and engage with your network</p>
              </div>
            </div>
            <div className="flex items-start gap-2">
              <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                <span className="text-green-600 text-sm font-bold">5</span>
              </div>
              <div>
                <h4 className="font-medium text-gray-900">Recommendations</h4>
                <p className="text-sm text-gray-600">Request recommendations from colleagues and managers</p>
              </div>
            </div>
            <div className="flex items-start gap-2">
              <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                <span className="text-green-600 text-sm font-bold">6</span>
              </div>
              <div>
                <h4 className="font-medium text-gray-900">Regular Updates</h4>
                <p className="text-sm text-gray-600">Keep your profile updated with new skills and experiences</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
        <button
          onClick={() => window.open('https://linkedin.com', '_blank')}
          className="inline-flex items-center justify-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Linkedin className="mr-2 h-5 w-5" />
          Go to LinkedIn
        </button>
        <button
          onClick={() => navigate('/optimize')}
          className="inline-flex items-center justify-center px-6 py-3 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors"
        >
          Back to Optimization
        </button>
      </div>
    </div>
  );
};

export default LinkedInGenerator;