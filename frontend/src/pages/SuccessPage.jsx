import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { CheckCircle, Loader2 } from 'lucide-react';

const SuccessPage = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const sessionId = searchParams.get('session_id');

  useEffect(() => {
    // Simulate verification
    setTimeout(() => {
      setLoading(false);
    }, 2000);
  }, [sessionId]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-background to-secondary/20">
        <Card className="w-full max-w-md">
          <CardContent className="p-8 text-center">
            <Loader2 className="w-12 h-12 text-primary mx-auto mb-4 animate-spin" />
            <p className="text-lg font-semibold">Verifying your payment...</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-background to-secondary/20 p-4">
      <Card className="w-full max-w-md animate-fadeInUp">
        <CardHeader className="text-center pb-4">
          <div className="w-16 h-16 rounded-full bg-success/10 flex items-center justify-center mx-auto mb-4">
            <CheckCircle className="w-10 h-10 text-success" />
          </div>
          <CardTitle className="text-2xl">Payment Successful!</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6 text-center">
          <p className="text-muted-foreground">
            Thank you for subscribing to VideoAI. Your payment has been processed successfully.
          </p>
          
          <div className="glass rounded-lg p-4 space-y-2">
            <p className="text-sm font-semibold">What's Next?</p>
            <ul className="text-sm text-muted-foreground space-y-1">
              <li>✓ Check your email for subscription details</li>
              <li>✓ Access to all premium features</li>
              <li>✓ Start creating amazing videos</li>
            </ul>
          </div>

          {sessionId && (
            <div className="text-xs text-muted-foreground">
              Session ID: {sessionId}
            </div>
          )}

          <div className="flex flex-col gap-3 pt-4">
            <Button
              variant="premium"
              size="lg"
              onClick={() => navigate('/')}
              className="w-full"
            >
              Start Creating Videos
            </Button>
            <Button
              variant="ghost"
              size="default"
              onClick={() => navigate('/')}
            >
              Return to Home
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default SuccessPage;