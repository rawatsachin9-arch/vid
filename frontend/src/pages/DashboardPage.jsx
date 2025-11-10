import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import DashboardLayout from '../components/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Sparkles, Video, Wand2, Loader2, FileText, Mic } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const DashboardPage = () => {
  const { user, token } = useAuth();
  const [prompt, setPrompt] = useState('');
  const [videoLength, setVideoLength] = useState('short');
  const [includeVoiceover, setIncludeVoiceover] = useState(true);
  const [voice, setVoice] = useState('alloy');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);
  const navigate = useNavigate();

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('Please enter a video idea or script');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post(
        `${BACKEND_URL}/api/videos/generate-video`,
        {
          prompt,
          video_length: videoLength,
          include_voiceover: includeVoiceover,
          voice
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate video');
    } finally {
      setLoading(false);
    }
  };

  const voices = [
    { value: 'alloy', label: 'Alloy (Neutral)' },
    { value: 'echo', label: 'Echo (Male)' },
    { value: 'fable', label: 'Fable (British)' },
    { value: 'onyx', label: 'Onyx (Deep)' },
    { value: 'nova', label: 'Nova (Female)' },
    { value: 'shimmer', label: 'Shimmer (Soft)' },
  ];

  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto space-y-6 sm:space-y-8 px-4">
        {/* Welcome Section */}
        <div className="text-center space-y-2">
          <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold font-heading">
            Welcome back, <span className="gradient-text">{user?.name}!</span>
          </h1>
          <p className="text-sm sm:text-base text-muted-foreground">
            Create professional videos in minutes with AI
          </p>
          
          {/* Quick Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center mt-6">
            <Button
              onClick={() => navigate('/create-video')}
              variant="premium"
              size="lg"
              className="flex items-center gap-2 w-full sm:w-auto"
            >
              <Video className="w-5 h-5" />
              Create AI Video
            </Button>
            <Button
              onClick={() => navigate('/video-library')}
              variant="outline"
              size="lg"
              className="flex items-center gap-2 w-full sm:w-auto"
            >
              <FileText className="w-5 h-5" />
              My Videos
            </Button>
          </div>
        </div>

        {/* Video Generator Card */}
        <Card className="animate-fadeInUp">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-primary" />
              <CardTitle>AI Video Generator</CardTitle>
            </div>
            <CardDescription>
              Describe your video idea and let AI create it for you
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Prompt Input */}
            <div className="space-y-2">
              <label className="text-sm font-medium flex items-center gap-2">
                <FileText className="w-4 h-4" />
                Video Idea or Script
              </label>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Example: Create a video about the benefits of morning exercise, including tips for beginners and how it improves mental health..."
                className="w-full px-4 py-3 border border-input rounded-lg focus:outline-none focus:ring-2 focus:ring-ring min-h-32 resize-y"
                disabled={loading}
              />
            </div>

            {/* Video Length */}
            <div className="space-y-2">
              <label className="text-sm font-medium">Video Length</label>
              <div className="flex flex-col sm:flex-row gap-2">
                {[
                  { value: 'short', label: 'Short (30s)', desc: '100-150 words' },
                  { value: 'medium', label: 'Medium (1m)', desc: '200-300 words' },
                  { value: 'long', label: 'Long (2m)', desc: '400-500 words' },
                ].map((option) => (
                  <button
                    key={option.value}
                    onClick={() => setVideoLength(option.value)}
                    disabled={loading}
                    className={`flex-1 p-3 rounded-lg border-2 transition-all text-left ${
                      videoLength === option.value
                        ? 'border-primary bg-primary/10'
                        : 'border-border hover:border-primary/50'
                    }`}
                  >
                    <p className="font-medium text-sm">{option.label}</p>
                    <p className="text-xs text-muted-foreground">{option.desc}</p>
                  </button>
                ))}
              </div>
            </div>

            {/* Voiceover Options */}
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  id="voiceover"
                  checked={includeVoiceover}
                  onChange={(e) => setIncludeVoiceover(e.target.checked)}
                  disabled={loading}
                  className="w-4 h-4 rounded border-border"
                />
                <label htmlFor="voiceover" className="text-sm font-medium flex items-center gap-2">
                  <Mic className="w-4 h-4" />
                  Include AI Voiceover
                </label>
              </div>

              {includeVoiceover && (
                <div className="ml-6 space-y-2">
                  <label className="text-sm">Voice Style</label>
                  <select
                    value={voice}
                    onChange={(e) => setVoice(e.target.value)}
                    disabled={loading}
                    className="w-full px-4 py-2 border border-input rounded-lg focus:outline-none focus:ring-2 focus:ring-ring"
                  >
                    {voices.map((v) => (
                      <option key={v.value} value={v.value}>
                        {v.label}
                      </option>
                    ))}
                  </select>
                </div>
              )}
            </div>

            {/* Error Display */}
            {error && (
              <div className="p-3 rounded-lg bg-destructive/10 border border-destructive/20 text-destructive text-sm">
                {error}
              </div>
            )}

            {/* Generate Button */}
            <Button
              variant="premium"
              size="lg"
              className="w-full"
              onClick={handleGenerate}
              disabled={loading}
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                  Generating Video...
                </>
              ) : (
                <>
                  <Wand2 className="w-5 h-5 mr-2" />
                  Generate Video with AI
                </>
              )}
            </Button>
          </CardContent>
        </Card>

        {/* Result Display */}
        {result && (
          <Card className="animate-fadeInUp border-primary/50">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Video className="w-5 h-5 text-success" />
                  <CardTitle>Video Generated Successfully!</CardTitle>
                </div>
                <Badge variant="success">Complete</Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="glass rounded-lg p-4">
                <h3 className="font-semibold mb-2">Generated Script:</h3>
                <p className="text-sm text-muted-foreground whitespace-pre-wrap">
                  {result.script}
                </p>
              </div>

              <div className="space-y-2">
                <h3 className="font-semibold">Video Scenes ({result.scenes?.length || 0}):</h3>
                <div className="grid gap-3">
                  {result.scenes?.map((scene, index) => (
                    <div key={index} className="glass rounded-lg p-4 flex gap-4">
                      <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                        <span className="font-bold text-primary">{index + 1}</span>
                      </div>
                      <div className="flex-1">
                        <p className="text-sm">{scene.text}</p>
                        {scene.footage && (
                          <img
                            src={scene.footage.thumbnail}
                            alt={`Scene ${index + 1}`}
                            className="mt-2 rounded-lg w-full h-32 object-cover"
                          />
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="flex gap-3">
                <Button
                  variant="default"
                  onClick={() => navigate('/dashboard/library')}
                  className="flex-1"
                >
                  View in Library
                </Button>
                <Button
                  variant="outline"
                  onClick={() => {
                    setPrompt('');
                    setResult(null);
                  }}
                  className="flex-1"
                >
                  Create Another
                </Button>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </DashboardLayout>
  );
};

export default DashboardPage;