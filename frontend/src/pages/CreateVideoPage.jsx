import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Navbar } from '../components/Navbar';
import { Footer } from '../components/Footer';
import SubscriptionBanner from '../components/SubscriptionBanner';

// Use empty string for relative URLs (same domain)
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';

const CreateVideoPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    input_text: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Get token from localStorage (JWT auth)
      const token = localStorage.getItem('token');
      
      const headers = {
        'Content-Type': 'application/json'
      };
      
      // Add token if available (for JWT auth)
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
      
      const response = await fetch(`${BACKEND_URL}/api/video/generate`, {
        method: 'POST',
        headers: headers,
        credentials: 'include', // Important for session cookie auth
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        throw new Error('Failed to create video project');
      }

      const data = await response.json();
      
      // Navigate to the project page
      navigate(`/video-project/${data.id}`);
    } catch (err) {
      setError(err.message || 'Failed to create video. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-900 via-blue-900 to-black">
      <Navbar />
      
      <div className="container mx-auto px-4 py-20">
        <div className="max-w-3xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-white mb-4">
              Create Your AI Video
            </h1>
            <p className="text-xl text-gray-300">
              Transform your text into engaging videos with AI-powered scene generation
            </p>
          </div>

          {/* Form */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Title Input */}
              <div>
                <label className="block text-white text-sm font-semibold mb-2">
                  Video Title
                </label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="Enter your video title"
                  required
                />
              </div>

              {/* Input Text */}
              <div>
                <label className="block text-white text-sm font-semibold mb-2">
                  Your Content
                </label>
                <textarea
                  value={formData.input_text}
                  onChange={(e) => setFormData({ ...formData, input_text: e.target.value })}
                  className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 min-h-[200px]"
                  placeholder="Enter your script, article, or any text content you want to convert into a video..."
                  required
                />
                <p className="text-gray-400 text-sm mt-2">
                  Tip: The AI will break down your content into engaging visual scenes
                </p>
              </div>

              {/* Error Message */}
              {error && (
                <div className="bg-red-500/20 border border-red-500 rounded-lg p-4">
                  <p className="text-red-200">{error}</p>
                </div>
              )}

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white py-4 rounded-lg font-semibold text-lg hover:from-purple-700 hover:to-blue-700 transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
              >
                {loading ? (
                  <span className="flex items-center justify-center">
                    <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                    Creating Your Video...
                  </span>
                ) : (
                  'Generate AI Video'
                )}
              </button>
            </form>
          </div>

          {/* Features */}
          <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="w-12 h-12 bg-purple-600 rounded-full flex items-center justify-center mx-auto mb-3">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-white font-semibold mb-1">Lightning Fast</h3>
              <p className="text-gray-400 text-sm">AI generates scenes in seconds</p>
            </div>

            <div className="text-center">
              <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-3">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z" />
                </svg>
              </div>
              <h3 className="text-white font-semibold mb-1">Smart Scenes</h3>
              <p className="text-gray-400 text-sm">Auto-generated visual storytelling</p>
            </div>

            <div className="text-center">
              <div className="w-12 h-12 bg-indigo-600 rounded-full flex items-center justify-center mx-auto mb-3">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="text-white font-semibold mb-1">AI Images</h3>
              <p className="text-gray-400 text-sm">Custom visuals for each scene</p>
            </div>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
};

export default CreateVideoPage;
