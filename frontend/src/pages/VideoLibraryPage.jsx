import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Navbar } from '../components/Navbar';
import { Footer } from '../components/Footer';

// Use empty string for relative URLs (same domain)
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';

const VideoLibraryPage = () => {
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      const token = localStorage.getItem('token');
      
      const headers = {};
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
      
      const response = await fetch(`${BACKEND_URL}/api/video/projects`, {
        headers: headers,
        credentials: 'include' // Important for session cookie auth
      });

      if (!response.ok) {
        throw new Error('Failed to fetch projects');
      }

      const data = await response.json();
      setProjects(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (projectId) => {
    if (!window.confirm('Are you sure you want to delete this project?')) return;

    try {
      const token = localStorage.getItem('token');
      
      const headers = {};
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
      
      const response = await fetch(`${BACKEND_URL}/api/video/projects/${projectId}`, {
        method: 'DELETE',
        headers: headers,
        credentials: 'include' // Important for session cookie auth
      });

      if (!response.ok) {
        throw new Error('Failed to delete project');
      }

      // Refresh the list
      fetchProjects();
    } catch (err) {
      alert(err.message);
    }
  };

  const getStatusBadge = (status) => {
    const badges = {
      'pending': 'bg-yellow-500/20 text-yellow-300',
      'processing': 'bg-blue-500/20 text-blue-300',
      'generating_script': 'bg-blue-500/20 text-blue-300',
      'generating_images': 'bg-purple-500/20 text-purple-300',
      'completed': 'bg-green-500/20 text-green-300',
      'failed': 'bg-red-500/20 text-red-300'
    };
    return badges[status] || 'bg-gray-500/20 text-gray-300';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-purple-900 via-blue-900 to-black flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-white mx-auto mb-4"></div>
          <p className="text-white text-xl">Loading your projects...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-900 via-blue-900 to-black">
      <Navbar />
      
      <div className="container mx-auto px-4 py-20">
        {/* Header */}
        <div className="flex justify-between items-center mb-12">
          <div>
            <h1 className="text-5xl font-bold text-white mb-4">Video Library</h1>
            <p className="text-xl text-gray-300">Manage and view all your AI-generated video projects</p>
          </div>
          <button
            onClick={() => navigate('/create-video')}
            className="px-8 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 transition-all transform hover:scale-105 flex items-center"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Create New Video
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-500/20 border border-red-500 rounded-lg p-4 mb-8">
            <p className="text-red-200">{error}</p>
          </div>
        )}

        {/* Projects Grid */}
        {projects.length === 0 ? (
          <div className="text-center py-20">
            <svg className="w-24 h-24 text-gray-600 mx-auto mb-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
            <h2 className="text-3xl font-bold text-white mb-4">No videos yet</h2>
            <p className="text-gray-400 mb-8">Create your first AI-powered video to get started</p>
            <button
              onClick={() => navigate('/create-video')}
              className="px-8 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700"
            >
              Create Your First Video
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {projects.map((project) => (
              <div
                key={project.id}
                className="bg-white/10 backdrop-blur-lg rounded-xl overflow-hidden border border-white/20 hover:border-purple-500 transition-all cursor-pointer group"
                onClick={() => navigate(`/video-project/${project.id}`)}
              >
                {/* Thumbnail */}
                <div className="aspect-video bg-gray-800 relative overflow-hidden">
                  {project.thumbnail_url ? (
                    <img
                      src={project.thumbnail_url}
                      alt={project.title}
                      className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center">
                      <svg className="w-16 h-16 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                      </svg>
                    </div>
                  )}
                  
                  {/* Status Badge */}
                  <div className={`absolute top-2 right-2 px-3 py-1 rounded-full text-xs font-semibold ${getStatusBadge(project.status)}`}>
                    {project.status}
                  </div>
                </div>

                {/* Project Info */}
                <div className="p-5">
                  <h3 className="text-white font-bold text-lg mb-2 truncate">{project.title}</h3>
                  
                  <div className="flex items-center justify-between text-sm text-gray-400 mb-4">
                    <span>{project.scenes.length} scenes</span>
                    <span>{project.duration}s</span>
                  </div>

                  <div className="flex items-center justify-between">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        navigate(`/video-project/${project.id}`);
                      }}
                      className="text-purple-400 hover:text-purple-300 text-sm font-semibold"
                    >
                      View Details
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDelete(project.id);
                      }}
                      className="text-red-400 hover:text-red-300"
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <Footer />
    </div>
  );
};

export default VideoLibraryPage;
