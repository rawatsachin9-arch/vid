import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Navbar } from '../components/Navbar';
import { Footer } from '../components/Footer';

// Use empty string for relative URLs (same domain)
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';

const VideoProjectPage = () => {
  const { projectId } = useParams();
  const navigate = useNavigate();
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchProject();
    const interval = setInterval(() => {
      if (project && (project.status === 'pending' || project.status === 'processing' || project.status === 'generating_script' || project.status === 'generating_images')) {
        fetchProject();
      }
    }, 3000); // Poll every 3 seconds

    return () => clearInterval(interval);
  }, [projectId, project]);

  const fetchProject = async () => {
    try {
      const token = localStorage.getItem('token');
      
      const headers = {};
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
      
      const response = await fetch(`${BACKEND_URL}/api/video/projects/${projectId}`, {
        headers: headers,
        credentials: 'include' // Important for session cookie auth
      });

      if (!response.ok) {
        throw new Error('Failed to fetch project');
      }

      const data = await response.json();
      setProject(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getStatusMessage = (status) => {
    const messages = {
      'pending': 'Preparing your video...',
      'processing': 'Processing your content...',
      'generating_script': 'AI is creating your video script...',
      'generating_images': 'Generating stunning visuals...',
      'completed': 'Your video is ready!',
      'failed': 'Something went wrong'
    };
    return messages[status] || status;
  };

  const getStatusColor = (status) => {
    if (status === 'completed') return 'text-green-400';
    if (status === 'failed') return 'text-red-400';
    return 'text-blue-400';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-purple-900 via-blue-900 to-black flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-white mx-auto mb-4"></div>
          <p className="text-white text-xl">Loading project...</p>
        </div>
      </div>
    );
  }

  if (error || !project) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-purple-900 via-blue-900 to-black">
        <Navbar />
        <div className="container mx-auto px-4 py-20">
          <div className="max-w-2xl mx-auto text-center">
            <h1 className="text-4xl font-bold text-white mb-4">Project Not Found</h1>
            <p className="text-gray-300 mb-8">{error}</p>
            <button
              onClick={() => navigate('/video-library')}
              className="px-8 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
            >
              Back to Library
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-900 via-blue-900 to-black">
      <Navbar />
      
      <div className="container mx-auto px-4 py-12 sm:py-20">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="mb-6 sm:mb-8">
            <button
              onClick={() => navigate('/video-library')}
              className="text-gray-300 hover:text-white mb-4 flex items-center text-sm sm:text-base"
            >
              <svg className="w-4 h-4 sm:w-5 sm:h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              Back to Library
            </button>
            <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-white mb-2">{project.title}</h1>
            <p className={`text-base sm:text-lg md:text-xl ${getStatusColor(project.status)}`}>
              {getStatusMessage(project.status)}
            </p>
          </div>

          {/* Progress Indicator */}
          {project.status !== 'completed' && project.status !== 'failed' && (
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-4 sm:p-6 border border-white/20 mb-6 sm:mb-8">
              <div className="flex items-center justify-center space-x-3 sm:space-x-4">
                <div className="animate-spin rounded-full h-6 w-6 sm:h-8 sm:w-8 border-b-2 border-white"></div>
                <p className="text-white text-sm sm:text-base md:text-lg">AI is working on your video...</p>
              </div>
            </div>
          )}

          {/* Error Message */}
          {project.status === 'failed' && (
            <div className="bg-red-500/20 border border-red-500 rounded-2xl p-4 sm:p-6 mb-6 sm:mb-8">
              <h3 className="text-red-200 font-semibold text-base sm:text-lg mb-2">Generation Failed</h3>
              <p className="text-red-200 text-sm sm:text-base">{project.error_message || 'An unexpected error occurred'}</p>
            </div>
          )}

          {/* Scenes Grid */}
          {project.scenes && project.scenes.length > 0 && (
            <div>
              <h2 className="text-xl sm:text-2xl font-bold text-white mb-4 sm:mb-6">Video Scenes</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
                {project.scenes.map((scene, index) => (
                  <div
                    key={index}
                    className="bg-white/10 backdrop-blur-lg rounded-xl overflow-hidden border border-white/20 hover:border-purple-500 transition-all"
                  >
                    {/* Scene Image */}
                    <div className="aspect-video bg-gray-800 relative">
                      {scene.image_url ? (
                        <img
                          src={scene.image_url}
                          alt={`Scene ${scene.scene_number}`}
                          className="w-full h-full object-cover"
                        />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center">
                          <div className="text-center">
                            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white mx-auto mb-2"></div>
                            <p className="text-gray-400 text-sm">Generating image...</p>
                          </div>
                        </div>
                      )}
                      <div className="absolute top-2 left-2 bg-black/50 backdrop-blur-sm px-3 py-1 rounded-full">
                        <span className="text-white font-semibold">Scene {scene.scene_number}</span>
                      </div>
                    </div>

                    {/* Scene Details */}
                    <div className="p-4">
                      <p className="text-gray-300 text-sm mb-2">{scene.description}</p>
                      <div className="bg-white/5 rounded p-3 mb-2">
                        <p className="text-white text-sm italic">"{scene.narration}"</p>
                      </div>
                      <div className="flex items-center justify-between text-xs text-gray-400">
                        <span>Duration: {scene.duration}s</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Video Stats */}
              {project.status === 'completed' && (
                <div className="mt-8 bg-gradient-to-r from-purple-600/20 to-blue-600/20 backdrop-blur-lg rounded-xl p-6 border border-white/20">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
                    <div>
                      <p className="text-gray-400 text-sm mb-1">Total Scenes</p>
                      <p className="text-white text-2xl font-bold">{project.scenes.length}</p>
                    </div>
                    <div>
                      <p className="text-gray-400 text-sm mb-1">Total Duration</p>
                      <p className="text-white text-2xl font-bold">{project.duration}s</p>
                    </div>
                    <div>
                      <p className="text-gray-400 text-sm mb-1">Status</p>
                      <p className="text-green-400 text-2xl font-bold">Completed</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      <Footer />
    </div>
  );
};

export default VideoProjectPage;
