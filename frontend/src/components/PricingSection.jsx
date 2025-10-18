import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Check } from 'lucide-react';

export const PricingSection = () => {
  const [isAnnual, setIsAnnual] = useState(false);

  const plans = [
    {
      name: 'Starter',
      description: 'Perfect for individuals getting started',
      priceMonthly: 19,
      priceAnnual: 15,
      features: [
        '10 videos per month',
        'Text to video generation',
        'AI voiceovers (5 languages)',
        'HD 1080p exports',
        'Stock library access',
        'Basic branding',
      ],
      cta: 'Start Free Trial',
      popular: false,
    },
    {
      name: 'Professional',
      description: 'For content creators and marketers',
      priceMonthly: 49,
      priceAnnual: 39,
      features: [
        'Unlimited videos',
        'All AI features included',
        'AI voiceovers (29+ languages)',
        '4K exports',
        'Priority stock library',
        'Advanced branding kit',
        'Remove watermark',
        'Team collaboration (3 users)',
      ],
      cta: 'Get Started',
      popular: true,
    },
    {
      name: 'Enterprise',
      description: 'For teams and organizations',
      priceMonthly: 99,
      priceAnnual: 79,
      features: [
        'Everything in Professional',
        'Unlimited team members',
        'API access',
        'Custom AI training',
        'Dedicated account manager',
        'Priority support',
        'Custom integrations',
        'SSO & advanced security',
      ],
      cta: 'Contact Sales',
      popular: false,
    },
  ];

  return (
    <section id="pricing" className="py-20 md:py-32 bg-gradient-to-b from-secondary/20 to-background">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-12 animate-fadeInUp">
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold font-heading mb-4">
            Choose Your
            <span className="gradient-text"> Perfect Plan</span>
          </h2>
          <p className="text-lg text-muted-foreground mb-8">
            Start creating videos for free, upgrade when you need more
          </p>

          {/* Billing Toggle */}
          <div className="inline-flex items-center gap-3 glass rounded-full p-1.5">
            <button
              onClick={() => setIsAnnual(false)}
              className={`px-6 py-2 rounded-full text-sm font-medium transition-all duration-300 ${
                !isAnnual
                  ? 'bg-primary text-primary-foreground shadow-md'
                  : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              Monthly
            </button>
            <button
              onClick={() => setIsAnnual(true)}
              className={`px-6 py-2 rounded-full text-sm font-medium transition-all duration-300 ${
                isAnnual
                  ? 'bg-primary text-primary-foreground shadow-md'
                  : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              Annual
              <Badge variant="success" className="ml-2 text-xs">Save 20%</Badge>
            </button>
          </div>
        </div>

        {/* Pricing Cards */}
        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {plans.map((plan, index) => (
            <Card
              key={index}
              className={`relative hover-lift transition-all duration-300 ${
                plan.popular
                  ? 'border-primary shadow-elegant scale-105 md:scale-110'
                  : 'border-border'
              } animate-fadeInUp`}
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <Badge variant="premium" className="px-4 py-1">
                    Most Popular
                  </Badge>
                </div>
              )}

              <CardHeader className="text-center pb-8 pt-8">
                <CardTitle className="text-2xl mb-2">{plan.name}</CardTitle>
                <CardDescription className="text-sm">{plan.description}</CardDescription>
                <div className="mt-6">
                  <div className="flex items-baseline justify-center gap-2">
                    <span className="text-5xl font-bold gradient-text">
                      ${isAnnual ? plan.priceAnnual : plan.priceMonthly}
                    </span>
                    <span className="text-muted-foreground">/month</span>
                  </div>
                  {isAnnual && (
                    <p className="text-sm text-muted-foreground mt-2">
                      Billed annually (${plan.priceAnnual * 12}/year)
                    </p>
                  )}
                </div>
              </CardHeader>

              <CardContent className="space-y-6">
                <Button
                  variant={plan.popular ? 'premium' : 'default'}
                  size="lg"
                  className="w-full"
                >
                  {plan.cta}
                </Button>

                <div className="space-y-3">
                  {plan.features.map((feature, i) => (
                    <div key={i} className="flex items-start gap-3">
                      <div className="w-5 h-5 rounded-full bg-success/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                        <Check className="w-3.5 h-3.5 text-success" />
                      </div>
                      <span className="text-sm text-foreground">{feature}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Bottom CTA */}
        <div className="text-center mt-16">
          <p className="text-muted-foreground mb-4">
            All plans include 14-day free trial • No credit card required
          </p>
          <Button variant="ghost" size="default">
            Compare all features →
          </Button>
        </div>
      </div>
    </section>
  );
};