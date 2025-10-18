import React from 'react';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Play, Sparkles, Video } from 'lucide-react';

export const HeroSection = () => {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-to-b from-background via-secondary/20 to-background pt-20">
      {/* Decorative elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-72 h-72 bg-primary/10 rounded-full blur-3xl animate-float"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-accent/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '1s' }}></div>
      </div>

      <div className="container mx-auto px-4 py-12 md:py-20 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div className="space-y-8 animate-fadeInUp">
            <Badge variant="premium" className="text-sm px-4 py-1">
              <Sparkles className="w-4 h-4 mr-2" />
              AI-Powered Video Generation
            </Badge>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold font-heading leading-tight">
              The Best AI Video
              <br />
              Generator for{' '}
              <span className="gradient-text">EVERYONE!</span>
            </h1>

            <p className="text-lg text-muted-foreground max-w-xl">
              Create engaging videos in minutes using the power of AI. No video editing experience required.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4">
              <Button variant="premium" size="xl" className="group">
                Get started for FREE
                <Play className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
              </Button>
              <Button variant="hero" size="xl">
                <Video className="w-5 h-5 mr-2" />
                Watch Demo
              </Button>
            </div>

            <p className="text-sm text-muted-foreground">
              No credit card required • Free forever plan available
            </p>

            {/* Trust Badges */}
            <div className="flex flex-wrap items-center gap-6 pt-4">
              <div className="flex items-center gap-2">
                <div className="flex">
                  {[...Array(5)].map((_, i) => (
                    <svg
                      key={i}
                      className="w-5 h-5 text-yellow-400 fill-current"
                      viewBox="0 0 20 20"
                    >
                      <path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z" />
                    </svg>
                  ))}
                </div>
                <span className="text-sm font-semibold">4.8/5.0</span>
              </div>
              <div className="text-sm text-muted-foreground">
                Trusted by <span className="font-semibold text-foreground">10M+</span> creators
              </div>
            </div>
          </div>

          {/* Right Content - Hero Image */}
          <div className="relative animate-fadeInUp" style={{ animationDelay: '0.2s' }}>
            <div className="relative rounded-2xl overflow-hidden shadow-2xl hover-lift">
              <img
                src="https://images.unsplash.com/photo-1559860199-52dc7841bf5c?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDF8MHwxfHNlYXJjaHwxfHxBSSUyMHZpZGVvJTIwY3JlYXRpb258ZW58MHx8fHwxNzYwODA5NDE4fDA&ixlib=rb-4.1.0&q=85"
                alt="AI Video Creation"
                className="w-full h-auto object-cover"
              />
              {/* Overlay gradient */}
              <div className="absolute inset-0 bg-gradient-to-tr from-primary/20 to-transparent"></div>
              
              {/* Floating card */}
              <div className="absolute bottom-6 left-6 right-6 glass rounded-xl p-4 animate-scaleIn" style={{ animationDelay: '0.8s' }}>
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-lg bg-primary flex items-center justify-center">
                    <Video className="w-6 h-6 text-primary-foreground" />
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-semibold">Video Generated</p>
                    <p className="text-xs text-muted-foreground">In just 2 minutes</p>
                  </div>
                  <div className="w-10 h-10 rounded-full bg-success flex items-center justify-center">
                    <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>

            {/* Decorative elements */}
            <div className="absolute -top-4 -right-4 w-24 h-24 bg-accent/20 rounded-full blur-2xl"></div>
            <div className="absolute -bottom-4 -left-4 w-32 h-32 bg-primary/20 rounded-full blur-2xl"></div>
          </div>
        </div>

        {/* Company Logos */}
        <div className="mt-20 pt-12 border-t border-border">
          <p className="text-center text-sm text-muted-foreground mb-8">
            Trusted by leading companies worldwide
          </p>
          <div className="flex flex-wrap justify-center items-center gap-8 md:gap-12 opacity-60">
            {['Coursera', 'Pearson', 'Kajabi', 'D2L', 'Microsoft', 'Google'].map((company) => (
              <div key={company} className="text-lg font-semibold text-muted-foreground">
                {company}
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};