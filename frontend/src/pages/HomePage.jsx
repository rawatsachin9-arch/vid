import React from 'react';
import { Navbar } from '../components/Navbar';
import { TopBanner } from '../components/TopBanner';
import { HeroSection } from '../components/HeroSection';
import { FeaturesSection } from '../components/FeaturesSection';
import { HowItWorksSection } from '../components/HowItWorksSection';
import { PricingSection } from '../components/PricingSection';
import { TestimonialsSection } from '../components/TestimonialsSection';
import { CTASection } from '../components/CTASection';
import { Footer } from '../components/Footer';

const HomePage = () => {
  return (
    <div className="min-h-screen">
      <TopBanner 
        message="🚀 Launch Special: Create unlimited AI videos FREE for 7 days! No credit card required."
        type="promo"
        ctaText="Start Free Trial"
        ctaLink="#pricing"
      />
      <Navbar />
      <HeroSection />
      <FeaturesSection />
      <HowItWorksSection />
      <TestimonialsSection />
      <PricingSection />
      <CTASection />
      <Footer />
    </div>
  );
};

export default HomePage;