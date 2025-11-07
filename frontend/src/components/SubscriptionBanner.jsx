import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { AlertCircle, Crown, Zap } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';

const SubscriptionBanner = () => {
  const [subscriptionInfo, setSubscriptionInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    if (isAuthenticated) {
      fetchSubscriptionInfo();
    }
  }, [isAuthenticated]);

  const fetchSubscriptionInfo = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await axios.get(`${BACKEND_URL}/api/video/subscription-info`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setSubscriptionInfo(response.data);
    } catch (error) {
      console.error('Failed to fetch subscription info:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated || loading || !subscriptionInfo) {
    return null;
  }

  const { 
    plan_name, 
    videos_remaining, 
    video_limit, 
    usage_percentage,
    max_duration_minutes 
  } = subscriptionInfo;

  const isLowOnVideos = videos_remaining <= 2;
  const isOutOfVideos = videos_remaining === 0;

  return (
    <div className={`rounded-lg p-4 mb-6 ${
      isOutOfVideos 
        ? 'bg-red-50 border-2 border-red-200' 
        : isLowOnVideos 
        ? 'bg-yellow-50 border-2 border-yellow-200'
        : 'bg-blue-50 border-2 border-blue-200'
    }`}>
      <div className="flex items-start justify-between">
        <div className="flex items-start gap-3 flex-1">
          {plan_name === 'Enterprise' ? (
            <Crown className="w-5 h-5 text-purple-600 mt-0.5" />
          ) : plan_name === 'Professional' ? (
            <Zap className="w-5 h-5 text-blue-600 mt-0.5" />
          ) : (
            <AlertCircle className={`w-5 h-5 mt-0.5 ${
              isOutOfVideos ? 'text-red-600' : isLowOnVideos ? 'text-yellow-600' : 'text-blue-600'
            }`} />
          )}
          
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
              <h3 className="font-semibold text-gray-900">{plan_name} Plan</h3>
              {isOutOfVideos && (
                <span className="text-xs bg-red-100 text-red-700 px-2 py-0.5 rounded-full font-medium">
                  Limit Reached
                </span>
              )}
            </div>
            
            <p className="text-sm text-gray-700 mb-2">
              {isOutOfVideos ? (
                <>You've used all {video_limit} videos this month. Upgrade to create more!</>
              ) : (
                <>{videos_remaining} of {video_limit} videos remaining this month</>
              )}
            </p>

            {/* Progress Bar */}
            <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
              <div 
                className={`h-2 rounded-full transition-all duration-300 ${
                  isOutOfVideos 
                    ? 'bg-red-500' 
                    : isLowOnVideos 
                    ? 'bg-yellow-500'
                    : 'bg-blue-500'
                }`}
                style={{ width: `${usage_percentage}%` }}
              ></div>
            </div>

            <p className="text-xs text-gray-600">
              Max video duration: {max_duration_minutes} {max_duration_minutes === 1 ? 'minute' : 'minutes'}
            </p>
          </div>
        </div>

        {(isOutOfVideos || isLowOnVideos) && (
          <a 
            href="/#pricing"
            className="ml-4 px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white text-sm font-medium rounded-lg hover:from-blue-700 hover:to-purple-700 transition whitespace-nowrap"
          >
            Upgrade Plan
          </a>
        )}
      </div>
    </div>
  );
};

export default SubscriptionBanner;
