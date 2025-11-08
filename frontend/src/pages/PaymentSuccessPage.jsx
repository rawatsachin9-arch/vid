import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import { CheckCircle, Loader } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const PaymentSuccessPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [verifying, setVerifying] = useState(true);
  const [verified, setVerified] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    verifyPayment();
  }, []);

  const verifyPayment = async () => {
    try {
      // Get payment data from URL params
      const params = new URLSearchParams(location.search);
      const paymentData = {
        status: params.get('status'),
        txnid: params.get('txnid'),
        amount: params.get('amount'),
        productinfo: params.get('productinfo'),
        firstname: params.get('firstname'),
        email: params.get('email'),
        hash: params.get('hash')
      };

      // Verify with backend
      const response = await axios.post(`${BACKEND_URL}/api/payu/verify-payment`, paymentData);

      if (response.data.verified && response.data.status === 'success') {
        setVerified(true);
        // Update user subscription in your database here
        setTimeout(() => {
          navigate('/dashboard');
        }, 3000);
      } else {
        setError('Payment verification failed');
      }
    } catch (err) {
      console.error('Verification error:', err);
      setError(err.response?.data?.detail || 'Payment verification failed');
    } finally {
      setVerifying(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-lg shadow-xl p-8 text-center">
        {verifying ? (
          <>
            <Loader className="w-16 h-16 mx-auto mb-4 text-blue-600 animate-spin" />
            <h2 className="text-2xl font-bold mb-2">Verifying Payment...</h2>
            <p className="text-gray-600">Please wait while we confirm your payment</p>
          </>
        ) : verified ? (
          <>
            <CheckCircle className="w-16 h-16 mx-auto mb-4 text-green-600" />
            <h2 className="text-2xl font-bold mb-2 text-green-600">Payment Successful!</h2>
            <p className="text-gray-600 mb-4">
              Thank you for your purchase. Your subscription is now active.
            </p>
            <p className="text-sm text-gray-500">
              Redirecting to dashboard...
            </p>
          </>
        ) : (
          <>
            <div className="w-16 h-16 mx-auto mb-4 bg-red-100 rounded-full flex items-center justify-center">
              <span className="text-3xl">❌</span>
            </div>
            <h2 className="text-2xl font-bold mb-2 text-red-600">Verification Failed</h2>
            <p className="text-gray-600 mb-4">{error || 'Unable to verify payment'}</p>
            <button
              onClick={() => navigate('/')}
              className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Go to Home
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default PaymentSuccessPage;
