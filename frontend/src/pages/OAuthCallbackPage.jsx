import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Loader2 } from 'lucide-react';

const OAuthCallbackPage = () => {
  const [error, setError] = useState('');
  const { loginWithGoogle } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const processOAuthCallback = async () => {
      try {
        // Get session_id from URL fragment
        const hash = window.location.hash;
        
        if (!hash || !hash.includes('session_id=')) {
          setError('No session ID found in callback');
          setTimeout(() => navigate('/login'), 2000);
          return;
        }

        // Extract session_id
        const sessionId = hash.split('session_id=')[1]?.split('&')[0];
        
        if (!sessionId) {
          setError('Invalid session ID');
          setTimeout(() => navigate('/login'), 2000);
          return;
        }

        // Login with Google using session_id
        const result = await loginWithGoogle(sessionId);
        
        if (result.success) {
          // Clean up URL
          window.location.hash = '';
          
          // Navigate to dashboard
          navigate('/dashboard', { replace: true });
        } else {
          setError(result.error || 'Google login failed');
          setTimeout(() => navigate('/login'), 2000);
        }
      } catch (err) {
        console.error('OAuth callback error:', err);
        setError('Authentication failed. Please try again.');
        setTimeout(() => navigate('/login'), 2000);
      }
    };

    processOAuthCallback();
  }, [loginWithGoogle, navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-background via-secondary/20 to-background">
      <div className="text-center">
        {error ? (
          <div className="space-y-4">
            <div className="text-destructive text-lg font-medium">{error}</div>
            <p className="text-sm text-muted-foreground">Redirecting to login...</p>
          </div>
        ) : (
          <div className="space-y-4">
            <Loader2 className="w-12 h-12 animate-spin mx-auto text-primary" />
            <p className="text-lg font-medium">Signing in with Google...</p>
            <p className="text-sm text-muted-foreground">Please wait while we complete your authentication</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default OAuthCallbackPage;
