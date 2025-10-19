import React, { useState } from 'react';
import { X, Sparkles, Gift, Zap } from 'lucide-react';

export const TopBanner = ({ 
  message = "🎉 Limited Time Offer: Get 50% OFF on all plans! Use code: LAUNCH50",
  type = "promo", // promo, announcement, info
  dismissible = true,
  ctaText = "Claim Offer",
  ctaLink = "#pricing"
}) => {
  const [isVisible, setIsVisible] = useState(true);

  if (!isVisible) return null;

  const bgColors = {
    promo: 'bg-gradient-to-r from-pink-500 via-purple-500 to-blue-500',
    announcement: 'bg-gradient-to-r from-blue-500 via-teal-500 to-green-500',
    info: 'bg-gradient-to-r from-orange-500 via-red-500 to-pink-500'
  };

  const icons = {
    promo: Gift,
    announcement: Sparkles,
    info: Zap
  };

  const Icon = icons[type];

  return (
    <div className={`${bgColors[type]} text-white py-2 px-4 relative z-50 animate-fadeInUp`}>
      <div className="container mx-auto flex items-center justify-between gap-4">
        {/* Left side - Icon + Message */}
        <div className="flex items-center gap-3 flex-1">
          <Icon className="w-5 h-5 flex-shrink-0 animate-pulse" />
          <p className="text-sm md:text-base font-medium">
            {message}
          </p>
        </div>

        {/* Center - CTA Button (desktop only) */}
        {ctaText && (
          <a
            href={ctaLink}
            className="hidden md:inline-flex items-center px-4 py-1.5 bg-white/20 hover:bg-white/30 backdrop-blur-sm rounded-full text-sm font-semibold transition-all duration-300 hover:scale-105"
          >
            {ctaText} →
          </a>
        )}

        {/* Right side - Close button */}
        {dismissible && (
          <button
            onClick={() => setIsVisible(false)}
            className="p-1 hover:bg-white/20 rounded-full transition-colors flex-shrink-0"
            aria-label="Close banner"
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </div>

      {/* Mobile CTA */}
      {ctaText && (
        <div className="md:hidden mt-2 text-center">
          <a
            href={ctaLink}
            className="inline-flex items-center px-4 py-1.5 bg-white/20 hover:bg-white/30 backdrop-blur-sm rounded-full text-sm font-semibold transition-all duration-300"
          >
            {ctaText} →
          </a>
        </div>
      )}
    </div>
  );
};

export default TopBanner;
