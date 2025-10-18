import React from 'react';
import { Card, CardContent } from './ui/card';
import { Upload, Wand2, Download, ArrowRight } from 'lucide-react';
import { Button } from './ui/button';

export const HowItWorksSection = () => {
  const steps = [
    {
      icon: Upload,
      title: 'Upload Your Content',
      description: 'Upload text, URL, PowerPoint, or describe your idea. Multiple input formats supported.',
      step: '01',
    },
    {
      icon: Wand2,
      title: 'AI Magic Happens',
      description: 'Our AI analyzes your content, selects perfect visuals, adds voiceovers, and applies branding.',
      step: '02',
    },
    {
      icon: Download,
      title: 'Download & Share',
      description: 'Preview, customize if needed, and download your professional video ready to share.',
      step: '03',
    },
  ];

  return (
    <section id="how-it-works" className="py-20 md:py-32 bg-background">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-16 animate-fadeInUp">
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold font-heading mb-4">
            Start Making Professional Videos
            <span className="gradient-text"> in Minutes</span>
          </h2>
          <p className="text-lg text-muted-foreground">
            Three simple steps to create stunning AI-powered videos
          </p>
        </div>

        {/* Steps */}
        <div className="grid md:grid-cols-3 gap-8 mb-12">
          {steps.map((step, index) => (
            <div key={index} className="relative animate-fadeInUp" style={{ animationDelay: `${index * 0.15}s` }}>
              <Card className="hover-lift h-full">
                <CardContent className="p-8 text-center">
                  {/* Step Number */}
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <div className="w-12 h-12 rounded-full bg-gradient-to-br from-primary to-primary-glow flex items-center justify-center shadow-lg">
                      <span className="text-lg font-bold text-primary-foreground">
                        {step.step}
                      </span>
                    </div>
                  </div>

                  {/* Icon */}
                  <div className="mt-8 mb-6 flex justify-center">
                    <div className="w-20 h-20 rounded-2xl bg-primary/10 flex items-center justify-center">
                      <step.icon className="w-10 h-10 text-primary" />
                    </div>
                  </div>

                  {/* Content */}
                  <h3 className="text-xl font-semibold font-heading mb-3">
                    {step.title}
                  </h3>
                  <p className="text-muted-foreground">
                    {step.description}
                  </p>
                </CardContent>
              </Card>

              {/* Arrow between cards (desktop only) */}
              {index < steps.length - 1 && (
                <div className="hidden md:block absolute top-1/2 -right-4 transform -translate-y-1/2 z-10">
                  <ArrowRight className="w-8 h-8 text-primary" />
                </div>
              )}
            </div>
          ))}
        </div>

        {/* CTA */}
        <div className="text-center mt-12">
          <Button variant="premium" size="xl">
            Get Started for Free
          </Button>
          <p className="text-sm text-muted-foreground mt-4">
            No credit card required • 3 free videos to start
          </p>
        </div>

        {/* Feature Highlights */}
        <div className="mt-20 grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {[
            { label: '18M+ Stock Assets', value: 'Getty Images, Storyblocks' },
            { label: '29+ Languages', value: 'AI Voiceovers' },
            { label: '10M+ Videos', value: 'Created worldwide' },
            { label: '4.8/5 Rating', value: 'Trusted by creators' },
          ].map((stat, index) => (
            <div key={index} className="glass rounded-xl p-6 text-center">
              <p className="text-2xl font-bold gradient-text mb-1">{stat.label}</p>
              <p className="text-sm text-muted-foreground">{stat.value}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};