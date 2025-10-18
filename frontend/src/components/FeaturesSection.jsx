import React from 'react';
import { Card, CardContent } from './ui/card';
import { FileText, Globe, Video, Captions, Presentation, Sparkles, Zap, Users } from 'lucide-react';
import { Button } from './ui/button';

export const FeaturesSection = () => {
  const features = [
    {
      icon: FileText,
      title: 'Text to Video',
      description: 'Generate professional-quality videos from your text, complete with realistic AI voices, automatically matched visuals, and music.',
      color: 'from-purple-500 to-purple-600',
    },
    {
      icon: Globe,
      title: 'URL to Video',
      description: 'Effortlessly generate videos from any URL. Turn your web content into engaging videos that captivate your audience.',
      color: 'from-blue-500 to-blue-600',
    },
    {
      icon: Video,
      title: 'Video Highlights',
      description: 'Transform long-form videos into engaging branded clips. Perfect for Zoom, Teams, Webinar and Podcast recordings.',
      color: 'from-pink-500 to-pink-600',
    },
    {
      icon: Captions,
      title: 'AI Captions',
      description: '85% of social media videos are watched on mute. Automatically add captions for up to 12% longer view time.',
      color: 'from-green-500 to-green-600',
    },
    {
      icon: Presentation,
      title: 'PPT to Video',
      description: 'Convert PowerPoint presentations into professional videos. Simply upload, summarize, and customize instantly.',
      color: 'from-orange-500 to-orange-600',
    },
    {
      icon: Sparkles,
      title: 'Idea to Video',
      description: 'Describe your idea, pick a video type and get a professional video in minutes. No more staring at a blank page.',
      color: 'from-indigo-500 to-indigo-600',
    },
  ];

  const benefits = [
    { icon: Zap, title: 'Lightning Fast', description: 'Create videos in minutes, not hours' },
    { icon: Sparkles, title: 'AI-Powered', description: 'Cutting-edge AI technology' },
    { icon: Users, title: 'Collaborative', description: 'Work together with your team' },
  ];

  return (
    <section id="features" className="py-20 md:py-32 bg-gradient-to-b from-background to-secondary/20">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-16 animate-fadeInUp">
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold font-heading mb-4">
            What Video Will You
            <span className="gradient-text"> Create Today?</span>
          </h2>
          <p className="text-lg text-muted-foreground">
            Powerful AI features to transform any content into professional videos
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-16">
          {features.map((feature, index) => (
            <Card
              key={index}
              className="group hover-lift cursor-pointer border-2 hover:border-primary/50 transition-all duration-300 animate-fadeInUp"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <CardContent className="p-6 flex flex-col h-full">
                <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${feature.color} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300`}>
                  <feature.icon className="w-7 h-7 text-white" />
                </div>
                <h3 className="text-xl font-semibold font-heading mb-2">
                  {feature.title}
                </h3>
                <p className="text-muted-foreground mb-4 flex-1">
                  {feature.description}
                </p>
                <Button variant="ghost" size="sm" className="w-fit group-hover:text-primary mt-auto">
                  Learn more →
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Benefits Bar */}
        <div className="glass rounded-2xl p-8 md:p-12">
          <div className="grid md:grid-cols-3 gap-8">
            {benefits.map((benefit, index) => (
              <div key={index} className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                  <benefit.icon className="w-6 h-6 text-primary" />
                </div>
                <div>
                  <h4 className="font-semibold mb-1">{benefit.title}</h4>
                  <p className="text-sm text-muted-foreground">{benefit.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};