import React, { useState } from 'react';
import { loadStripe } from '@stripe/stripe-js';
import { Button } from './ui/button';
import { Loader2 } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const stripePublishableKey = process.env.REACT_APP_STRIPE_PUBLISHABLE_KEY;

// Initialize Stripe only if publishable key is available
const stripePromise = stripePublishableKey ? loadStripe(stripePublishableKey) : null;

export const StripeCheckout = ({ plan, billing, buttonText = 'Subscribe', variant = 'default' }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleCheckout = async () => {
    setLoading(true);
    setError(null);

    // Check if Stripe is configured
    if (!stripePromise) {
      setError('Stripe is not configured. Please add your Stripe publishable key to the .env file.');
      setLoading(false);
      return;
    }

    try {
      const stripe = await stripePromise;

      // Create checkout session
      const response = await axios.post(
        `${BACKEND_URL}/api/stripe/create-checkout-session`,
        {
          plan: plan.toLowerCase(),
          billing: billing,
          success_url: `${window.location.origin}/success?session_id={CHECKOUT_SESSION_ID}`,
          cancel_url: window.location.origin,
        }
      );

      if (response.data.success && response.data.sessionId) {
        // Redirect to Stripe Checkout
        const result = await stripe.redirectToCheckout({
          sessionId: response.data.sessionId,
        });

        if (result.error) {
          setError(result.error.message);
        }
      } else {
        setError('Failed to create checkout session');
      }
    } catch (err) {
      console.error('Checkout error:', err);
      setError(err.response?.data?.detail || 'An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-2">
      <Button
        variant={variant}
        size="lg"
        className="w-full"
        onClick={handleCheckout}
        disabled={loading}
      >
        {loading ? (
          <>
            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
            Processing...
          </>
        ) : (
          buttonText
        )}
      </Button>
      {error && (
        <p className="text-sm text-destructive text-center">{error}</p>
      )}
    </div>
  );
};