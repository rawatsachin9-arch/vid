import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { XCircle } from 'lucide-react';

const PaymentFailurePage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const errorMessage = params.get('error') || 'Payment was not completed';

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 to-orange-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-lg shadow-xl p-8 text-center">
        <XCircle className="w-16 h-16 mx-auto mb-4 text-red-600" />
        <h2 className="text-2xl font-bold mb-2 text-red-600">Payment Failed</h2>
        <p className="text-gray-600 mb-6">
          {errorMessage}
        </p>
        <p className="text-sm text-gray-500 mb-6">
          No charges were made to your account.
        </p>
        <div className="flex gap-3">
          <button
            onClick={() => navigate('/')}
            className="flex-1 px-4 py-2 border border-gray-300 rounded text-gray-700 hover:bg-gray-50"
          >
            Go Home
          </button>
          <button
            onClick={() => navigate('/#pricing')}
            className="flex-1 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Try Again
          </button>
        </div>
      </div>
    </div>
  );
};

export default PaymentFailurePage;
