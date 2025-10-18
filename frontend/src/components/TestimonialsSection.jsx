import React from 'react';
import { Card, CardContent } from './ui/card';
import { Star } from 'lucide-react';

export const TestimonialsSection = () => {
  const testimonials = [
    {
      name: 'Sarah Johnson',
      role: 'Content Creator',
      company: 'Digital Marketing Agency',
      rating: 5,
      text: 'Pictory has completely transformed my content creation workflow. What used to take hours now takes minutes. The AI is incredibly accurate!',
      avatar: 'SJ',
    },
    {
      name: 'Michael Chen',
      role: 'YouTube Creator',
      company: 'Tech Reviews Channel',
      rating: 5,
      text: 'The video production time has now been slashed. I can create more content in less time, and the quality is outstanding. Best tool I\'ve used!',
      avatar: 'MC',
    },
    {
      name: 'Emily Rodriguez',
      role: 'Marketing Manager',
      company: 'SaaS Startup',
      rating: 5,
      text: 'As a first-time content creator, I find this incredibly easy to use. The AI voices are so realistic, and the automatic captions are perfect.',
      avatar: 'ER',
    },
    {
      name: 'David Thompson',
      role: 'Educator',
      company: 'Online Learning Platform',
      rating: 5,
      text: 'Even someone with no experience can generate proper videos. My students love the engaging content, and I can create lessons in minutes.',
      avatar: 'DT',
    },
    {
      name: 'Lisa Wang',
      role: 'Social Media Manager',
      company: 'E-commerce Brand',
      rating: 5,
      text: 'From a 15-second ad to a 5-minute presentation, it\'s a great product! The automation saves us countless hours every week.',
      avatar: 'LW',
    },
    {
      name: 'James Mitchell',
      role: 'Podcast Host',
      company: 'Business Podcast',
      rating: 5,
      text: 'Turning my podcast episodes into short video clips for social media has never been easier. The highlight extraction is pure magic!',
      avatar: 'JM',
    },
  ];

  return (
    <section id="testimonials" className="py-20 md:py-32 bg-background">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-16 animate-fadeInUp">
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold font-heading mb-4">
            Loved by
            <span className="gradient-text"> 10M+ Creators</span>
          </h2>
          <p className="text-lg text-muted-foreground">
            See what our users are saying about their experience
          </p>
        </div>

        {/* Testimonials Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {testimonials.map((testimonial, index) => (
            <Card
              key={index}
              className="hover-lift transition-all duration-300 animate-fadeInUp"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <CardContent className="p-6 flex flex-col h-full">
                {/* Rating */}
                <div className="flex gap-1 mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                  ))}
                </div>

                {/* Testimonial Text */}
                <p className="text-foreground mb-6 flex-1 leading-relaxed">
                  "{testimonial.text}"
                </p>

                {/* Author Info */}
                <div className="flex items-center gap-3 pt-4 border-t border-border">
                  <div className="w-12 h-12 rounded-full bg-gradient-to-br from-primary to-primary-glow flex items-center justify-center flex-shrink-0">
                    <span className="text-sm font-semibold text-primary-foreground">
                      {testimonial.avatar}
                    </span>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-semibold text-foreground truncate">
                      {testimonial.name}
                    </p>
                    <p className="text-sm text-muted-foreground truncate">
                      {testimonial.role}
                    </p>
                    <p className="text-xs text-muted-foreground truncate">
                      {testimonial.company}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Trust Indicators */}
        <div className="mt-16 glass rounded-2xl p-8 md:p-12">
          <div className="grid sm:grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <p className="text-4xl font-bold gradient-text mb-2">4.8/5</p>
              <p className="text-sm text-muted-foreground">Average Rating</p>
            </div>
            <div>
              <p className="text-4xl font-bold gradient-text mb-2">10M+</p>
              <p className="text-sm text-muted-foreground">Videos Created</p>
            </div>
            <div>
              <p className="text-4xl font-bold gradient-text mb-2">150+</p>
              <p className="text-sm text-muted-foreground">Countries</p>
            </div>
            <div>
              <p className="text-4xl font-bold gradient-text mb-2">99.9%</p>
              <p className="text-sm text-muted-foreground">Uptime</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};