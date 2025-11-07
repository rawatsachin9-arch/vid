import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Play, Sparkles, Video, X, Zap, TrendingUp, Award } from 'lucide-react';

export const HeroSection = () => {
  const [showVideoModal, setShowVideoModal] = useState(false);
  const navigate = useNavigate();

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
      {/* Animated Background Gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-900 via-violet-900 to-blue-900"></div>
      
      {/* Animated Mesh Gradient Overlay */}
      <div className="absolute inset-0 opacity-30">
        <div className="absolute top-0 -left-4 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl animate-blob"></div>
        <div className="absolute top-0 -right-4 w-96 h-96 bg-pink-500 rounded-full mix-blend-multiply filter blur-3xl animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-20 w-96 h-96 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl animate-blob animation-delay-4000"></div>
      </div>

      {/* Grid Pattern Overlay */}
      <div className="absolute inset-0 bg-grid-white/[0.05] bg-grid"></div>
      
      {/* Floating Particles */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-2 h-2 bg-white/20 rounded-full animate-float"></div>
        <div className="absolute top-40 right-20 w-3 h-3 bg-purple-400/30 rounded-full animate-float animation-delay-1000"></div>
        <div className="absolute bottom-40 left-1/4 w-2 h-2 bg-pink-400/30 rounded-full animate-float animation-delay-2000"></div>
        <div className="absolute bottom-20 right-1/3 w-3 h-3 bg-blue-400/30 rounded-full animate-float animation-delay-3000"></div>
      </div>

      <div className="container mx-auto px-4 py-12 md:py-20 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div className="space-y-8 animate-fadeInUp">
            {/* Premium Badge */}
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-white">
              <Sparkles className="w-4 h-4 text-yellow-400" />
              <span className="text-sm font-medium">Powered by Advanced AI</span>
              <Zap className="w-4 h-4 text-yellow-400" />
            </div>

            {/* Main Heading */}
            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold leading-tight text-white">
              Create Stunning
              <br />
              <span className="bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent animate-gradient">
                AI Videos
              </span>
              <br />
              <span className="text-4xl sm:text-5xl lg:text-6xl">in Seconds</span>
            </h1>

            {/* Subheading */}
            <p className="text-xl text-gray-300 max-w-xl leading-relaxed">
              Transform your text into professional videos with AI-powered scene generation, images, and narration. No video editing skills required.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 pt-4">
              <Button 
                size="xl" 
                onClick={() => navigate('/register')}
                className="group bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white shadow-2xl shadow-purple-500/50 hover:shadow-purple-500/70 transition-all"
              >
                <Play className="w-5 h-5 mr-2 group-hover:scale-110 transition-transform" />
                Start Creating Free
              </Button>
              <Button 
                size="xl"
                variant="outline"
                onClick={() => setShowVideoModal(true)}
                className="bg-white/10 backdrop-blur-md border-white/20 text-white hover:bg-white/20"
              >
                <Video className="w-5 h-5 mr-2" />
                Watch Demo
              </Button>
            </div>

            {/* Trust Indicators */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4 pt-2">
              <p className="text-sm text-gray-400">
                ✨ No credit card required • Start with 5 free videos
              </p>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-6 pt-6">
              <div className="text-center sm:text-left">
                <div className="text-3xl font-bold text-white mb-1">10K+</div>
                <div className="text-sm text-gray-400">Videos Created</div>
              </div>
              <div className="text-center sm:text-left">
                <div className="text-3xl font-bold text-white mb-1">4.9★</div>
                <div className="text-sm text-gray-400">User Rating</div>
              </div>
              <div className="text-center sm:text-left">
                <div className="text-3xl font-bold text-white mb-1">5K+</div>
                <div className="text-sm text-gray-400">Happy Users</div>
              </div>
            </div>
          </div>

          {/* Right Content - Hero Visual */}
          <div className="relative animate-fadeInUp" style={{ animationDelay: '0.2s' }}>
            {/* Main Card */}
            <div className="relative">
              {/* Glow Effect */}
              <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-pink-600 rounded-3xl blur-2xl opacity-30"></div>
              
              {/* Content Card */}
              <div className="relative bg-white/10 backdrop-blur-xl rounded-3xl p-8 border border-white/20 shadow-2xl">
                {/* Video Preview Mockup */}
                <div className="relative aspect-video bg-gradient-to-br from-gray-900 to-gray-800 rounded-xl overflow-hidden mb-6">
                  {/* Play Button Overlay */}
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="w-20 h-20 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center group-hover:scale-110 transition-transform cursor-pointer">
                      <Play className="w-10 h-10 text-white fill-white ml-1" />
                    </div>
                  </div>
                  
                  {/* Video Thumbnail */}
                  <img
                    src="https://images.unsplash.com/photo-1626785774625-ddcddc3445e9?w=800&q=80"
                    alt="AI Video Creation"
                    className="w-full h-full object-cover opacity-60"
                  />
                </div>

                {/* Features Grid */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-white/5 backdrop-blur-sm rounded-xl p-4 border border-white/10">
                    <Zap className="w-8 h-8 text-yellow-400 mb-2" />
                    <div className="text-sm font-semibold text-white">Lightning Fast</div>
                    <div className="text-xs text-gray-400">Generate in seconds</div>
                  </div>
                  <div className="bg-white/5 backdrop-blur-sm rounded-xl p-4 border border-white/10">
                    <Award className="w-8 h-8 text-purple-400 mb-2" />
                    <div className="text-sm font-semibold text-white">HD Quality</div>
                    <div className="text-xs text-gray-400">Professional output</div>
                  </div>
                </div>
              </div>

              {/* Floating Stats Cards */}
              <div className="absolute -top-6 -right-6 bg-white/10 backdrop-blur-xl rounded-2xl p-4 border border-white/20 shadow-xl animate-float">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-green-400 to-emerald-600 flex items-center justify-center">
                    <TrendingUp className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-white">98%</div>
                    <div className="text-xs text-gray-400">Success Rate</div>
                  </div>
                </div>
              </div>

              <div className="absolute -bottom-6 -left-6 bg-white/10 backdrop-blur-xl rounded-2xl p-4 border border-white/20 shadow-xl animate-float animation-delay-2000">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-400 to-indigo-600 flex items-center justify-center">
                    <Sparkles className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-white">AI</div>
                    <div className="text-xs text-gray-400">Powered</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Company Logos */}
        <div className="mt-20 pt-12 border-t border-border">
          <p className="text-center text-sm text-muted-foreground mb-8">
            Trusted by leading companies worldwide
          </p>
          <div className="flex flex-wrap justify-center items-center gap-8 md:gap-12 opacity-60">
            {['Coursera', 'Pearson', 'Kajabi', 'D2L', 'Microsoft', 'Google'].map((company) => (
              <div key={company} className="text-lg font-semibold text-muted-foreground">
                {company}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Video Modal */}
      {showVideoModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-fadeInUp">
          <div className="relative w-full max-w-5xl">
            {/* Close Button */}
            <button
              onClick={() => setShowVideoModal(false)}
              className="absolute -top-12 right-0 w-10 h-10 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-white transition-colors"
            >
              <X className="w-6 h-6" />
            </button>

            {/* Video Container */}
            <div className="relative aspect-video bg-black rounded-xl overflow-hidden shadow-2xl">
              <iframe
                className="w-full h-full"
                src="https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1"
                title="VideoMaker Tutorial"
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              ></iframe>
            </div>

            {/* Video Info */}
            <div className="mt-6 text-center">
              <h3 className="text-xl font-bold text-white mb-2">
                Complete VideoMaker Tutorial
              </h3>
              <p className="text-white/80">
                Learn how to create stunning AI videos from start to finish
              </p>
            </div>
          </div>
        </div>
      )}
    </section>
  );
};