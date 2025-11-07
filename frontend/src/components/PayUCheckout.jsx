import React, { useState } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const PayUCheckout = ({ plan, billing, onSuccess, onCancel }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [userInfo, setUserInfo] = useState({
    name: '',
    email: '',
    phone: ''
  });

  const handleInputChange = (e) => {
    setUserInfo({
      ...userInfo,
      [e.target.name]: e.target.value
    });
  };

  const handlePayment = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Validate inputs
      if (!userInfo.name || !userInfo.email || !userInfo.phone) {
        setError('Please fill in all fields');
        setLoading(false);
        return;
      }

      // Create payment request
      const response = await axios.post(`${BACKEND_URL}/api/payu/create-payment`, {
        plan,
        billing,
        name: userInfo.name,
        email: userInfo.email,
        phone: userInfo.phone,
        success_url: `${window.location.origin}/payment-success`,
        failure_url: `${window.location.origin}/payment-failure`
      });

      if (response.data.success) {
        // Create form and submit to PayU
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = response.data.payment_url;

        // Add all payment data as hidden fields
        Object.keys(response.data.payment_data).forEach(key => {
          const input = document.createElement('input');
          input.type = 'hidden';
          input.name = key;
          input.value = response.data.payment_data[key];
          form.appendChild(input);
        });

        document.body.appendChild(form);
        form.submit();
      }
    } catch (err) {
      console.error('Payment error:', err);
      setError(err.response?.data?.detail || 'Payment initiation failed');
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
        <h2 className="text-2xl font-bold mb-4">Complete Your Purchase</h2>
        
        <div className="mb-4 p-4 bg-gray-100 rounded">
          <p className="text-sm text-gray-600">Plan: <span className="font-semibold text-gray-900">{plan}</span></p>
          <p className="text-sm text-gray-600">Billing: <span className="font-semibold text-gray-900">{billing}</span></p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}

        <form onSubmit={handlePayment}>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Full Name *
            </label>
            <input
              type="text"
              name="name"
              value={userInfo.name}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="John Doe"
              required
            />
          </div>

          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Email *
            </label>
            <input
              type="email"
              name="email"
              value={userInfo.email}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="john@example.com"
              required
            />
          </div>

          <div className="mb-6">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Phone Number *
            </label>
            <input
              type="tel"
              name="phone"
              value={userInfo.phone}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="9876543210"
              pattern="[0-9]{10}"
              required
            />
          </div>

          <div className="flex gap-3">
            <button
              type="button"
              onClick={onCancel}
              disabled={loading}
              className="flex-1 px-4 py-2 border border-gray-300 rounded text-gray-700 hover:bg-gray-50 disabled:opacity-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex-1 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Processing...' : 'Proceed to Payment'}
            </button>
          </div>
        </form>

        <p className="text-xs text-gray-500 mt-4 text-center">
          You will be redirected to PayU for secure payment
        </p>
      </div>
    </div>
  );
};

export default PayUCheckout;
