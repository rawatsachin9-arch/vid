import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Mail, Loader2, CheckCircle } from 'lucide-react';
import { VideoMakerLogo, VideoMakerLogoText } from '../components/Logo';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';

const ForgotPasswordPage = () => {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [resetToken, setResetToken] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await axios.post(`${BACKEND_URL}/api/auth/forgot-password`, {
        email
      });
      
      setSuccess(true);
      // Store token temporarily (in production, this would be sent via email)
      if (response.data.reset_token) {
        setResetToken(response.data.reset_token);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to send reset link');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-background via-secondary/20 to-background p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="flex items-center justify-center gap-3 mb-6 sm:mb-8">
          <VideoMakerLogo size="large" />
          <VideoMakerLogoText className="text-2xl sm:text-3xl" />
        </div>

        <Card className="animate-fadeInUp">
          <CardHeader className="text-center">
            <CardTitle className="text-xl sm:text-2xl">Reset Password</CardTitle>
            <CardDescription className="text-sm sm:text-base">
              {success ? 'Check your email for reset instructions' : 'Enter your email to receive a password reset link'}
            </CardDescription>
          </CardHeader>
          <CardContent>
            {success ? (
              <div className="space-y-4">
                <div className="flex flex-col items-center justify-center py-6 sm:py-8">
                  <CheckCircle className="w-12 h-12 sm:w-16 sm:h-16 text-success mb-4" />
                  <h3 className="text-base sm:text-lg font-semibold text-center mb-2">Reset Link Sent!</h3>
                  <p className="text-xs sm:text-sm text-muted-foreground text-center">
                    If an account exists with <strong>{email}</strong>, you will receive a password reset link shortly.
                  </p>
                  
                  {/* Show token for development (remove in production) */}
                  {resetToken && (
                    <div className="mt-4 p-3 sm:p-4 bg-muted rounded-lg w-full">
                      <p className="text-xs sm:text-sm font-semibold mb-2">Reset Token (Dev Only):</p>
                      <p className="text-xs break-all text-muted-foreground">{resetToken}</p>
                      <Link 
                        to={`/reset-password?token=${resetToken}`}
                        className="text-xs sm:text-sm text-primary hover:underline mt-2 block"
                      >
                        Click here to reset password
                      </Link>
                    </div>
                  )}
                </div>

                <div className="flex flex-col gap-3">
                  <Link to="/login" className="w-full">
                    <Button variant="premium" size="lg" className="w-full text-sm sm:text-base">
                      Back to Login
                    </Button>
                  </Link>
                </div>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-4">
                {error && (
                  <div className="p-3 rounded-lg bg-destructive/10 border border-destructive/20 text-destructive text-xs sm:text-sm">
                    {error}
                  </div>
                )}

                <div className="space-y-2">
                  <label className="text-xs sm:text-sm font-medium">Email</label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                    <input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className="w-full pl-10 pr-4 py-2 border border-input rounded-lg focus:outline-none focus:ring-2 focus:ring-ring text-sm sm:text-base"
                      placeholder="you@example.com"
                      required
                    />
                  </div>
                </div>

                <Button 
                  type="submit" 
                  variant="premium" 
                  size="lg" 
                  className="w-full text-sm sm:text-base"
                  disabled={loading}
                >
                  {loading ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      Sending...
                    </>
                  ) : (
                    'Send Reset Link'
                  )}
                </Button>

                <div className="text-center text-xs sm:text-sm">
                  <span className="text-muted-foreground">Remember your password? </span>
                  <Link to="/login" className="text-primary hover:underline font-medium">
                    Sign in
                  </Link>
                </div>
              </form>
            )}

            <div className="mt-4 text-center">
              <Link to="/" className="text-xs sm:text-sm text-muted-foreground hover:text-primary">
                ← Back to home
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ForgotPasswordPage;
