import React from 'react';

export const VideoMakerLogo = ({ className = "", size = "default" }) => {
  const sizes = {
    small: { container: "w-8 h-8", icon: "w-5 h-5" },
    default: { container: "w-10 h-10", icon: "w-6 h-6" },
    large: { container: "w-16 h-16", icon: "w-10 h-10" }
  };

  const currentSize = sizes[size] || sizes.default;

  return (
    <div className={`${currentSize.container} ${className}`}>
      <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-full h-full">
        {/* Background gradient circle */}
        <defs>
          <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#14b8a6" />
            <stop offset="50%" stopColor="#0ea5e9" />
            <stop offset="100%" stopColor="#3b82f6" />
          </linearGradient>
          <linearGradient id="playGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#ffffff" />
            <stop offset="100%" stopColor="#f0f9ff" />
          </linearGradient>
        </defs>
        
        {/* Outer circle with gradient */}
        <circle cx="50" cy="50" r="45" fill="url(#logoGradient)" />
        
        {/* Inner decoration - film strips */}
        <rect x="20" y="35" width="2" height="30" fill="white" opacity="0.3" rx="1"/>
        <rect x="25" y="35" width="2" height="30" fill="white" opacity="0.3" rx="1"/>
        <rect x="73" y="35" width="2" height="30" fill="white" opacity="0.3" rx="1"/>
        <rect x="78" y="35" width="2" height="30" fill="white" opacity="0.3" rx="1"/>
        
        {/* Play button triangle - centered */}
        <path 
          d="M 42 32 L 42 68 L 68 50 Z" 
          fill="url(#playGradient)"
          stroke="white"
          strokeWidth="1.5"
          strokeLinejoin="round"
        />
        
        {/* Sparkle effect - AI indicator */}
        <circle cx="65" cy="30" r="3" fill="#fbbf24" />
        <path d="M 65 26 L 65 34 M 61 30 L 69 30" stroke="#fbbf24" strokeWidth="1.5" strokeLinecap="round"/>
      </svg>
    </div>
  );
};

export const VideoMakerLogoText = ({ className = "" }) => {
  return (
    <span className={`font-bold font-heading ${className}`}>
      <span style={{
        background: 'linear-gradient(135deg, #14b8a6 0%, #0ea5e9 50%, #3b82f6 100%)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        backgroundClip: 'text'
      }}>
        VideoMaker
      </span>
    </span>
  );
};
