import React from 'react';
import { Navbar } from '../components/Navbar';
import { Footer } from '../components/Footer';
import { Card, CardContent } from '../components/ui/card';
import { Users, Target, Award, Heart } from 'lucide-react';

const AboutPage = () => {
  return (
    <div className="min-h-screen">
      <Navbar />
      
      {/* Hero Section with Image */}
      <div className="pt-20 relative overflow-hidden">
        <div className="absolute inset-0 z-0">
          <img
            src="https://images.unsplash.com/photo-1670851050245-d861fd433d06?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDN8MHwxfHNlYXJjaHwxfHxwcm9mZXNzaW9uYWwlMjB0ZWFtJTIwY29sbGFib3JhdGlvbiUyMG9mZmljZXxlbnwwfHx8fDE3NjA4NjQ4MjF8MA&ixlib=rb-4.1.0&q=85"
            alt="Team collaboration"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-background/95 via-background/80 to-background/95"></div>
        </div>
        
        <div className="relative z-10 container mx-auto px-4 py-24">
          <div className="text-center max-w-3xl mx-auto">
            <h1 className="text-4xl md:text-5xl font-bold font-heading mb-4">
              About <span className="gradient-text">VideoMaker</span>
            </h1>
            <p className="text-lg text-muted-foreground">
              We're on a mission to democratize video creation with the power of AI
            </p>
          </div>
        </div>
      </div>

      <div className="pb-16 bg-gradient-to-b from-background to-secondary/20">
        <div className="container mx-auto px-4">
          {/* Story Section */}
          <div className="max-w-4xl mx-auto space-y-12 -mt-8">
            <Card>
              <CardContent className="p-8">
                <h2 className="text-2xl font-bold mb-4">Our Story</h2>
                <p className="text-muted-foreground mb-4">
                  VideoMaker was founded with a simple belief: everyone should have the power to create professional videos, regardless of their technical expertise or budget.
                </p>
                <p className="text-muted-foreground mb-4">
                  We saw content creators, marketers, and businesses struggling with expensive video production, complicated editing software, and time-consuming workflows. We knew there had to be a better way.
                </p>
                <p className="text-muted-foreground">
                  Today, VideoMaker helps over 10 million creators worldwide turn their ideas into stunning videos in minutes, not hours or days.
                </p>
              </CardContent>
            </Card>

            {/* Team Images */}
            <div className="grid md:grid-cols-3 gap-6">
              <div className="relative h-64 rounded-xl overflow-hidden hover-lift">
                <img
                  src="https://images.unsplash.com/photo-1758518729685-f88df7890776?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDN8MHwxfHNlYXJjaHwyfHxwcm9mZXNzaW9uYWwlMjB0ZWFtJTIwY29sbGFib3JhdGlvbiUyMG9mZmljZXxlbnwwfHx8fDE3NjA4NjQ4MjF8MA&ixlib=rb-4.1.0&q=85"
                  alt="Team collaboration"
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="relative h-64 rounded-xl overflow-hidden hover-lift">
                <img
                  src="https://images.unsplash.com/photo-1758518730178-6e237bc8b87d?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDN8MHwxfHNlYXJjaHwzfHxwcm9mZXNzaW9uYWwlMjB0ZWFtJTIwY29sbGFib3JhdGlvbiUyMG9mZmljZXxlbnwwfHx8fDE3NjA4NjQ4MjF8MA&ixlib=rb-4.1.0&q=85"
                  alt="Team meeting"
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="relative h-64 rounded-xl overflow-hidden hover-lift">
                <img
                  src="https://images.unsplash.com/photo-1758691737568-a1572060ce5a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDN8MHwxfHNlYXJjaHw0fHxwcm9mZXNzaW9uYWwlMjB0ZWFtJTIwY29sbGFib3JhdGlvbiUyMG9mZmljZXxlbnwwfHx8fDE3NjA4NjQ4MjF8MA&ixlib=rb-4.1.0&q=85"
                  alt="Office culture"
                  className="w-full h-full object-cover"
                />
              </div>
            </div>

            {/* Values */}
            <div className="grid md:grid-cols-2 gap-6">
              <Card className="hover-lift">
                <CardContent className="p-6">
                  <Target className="w-12 h-12 text-primary mb-4" />
                  <h3 className="text-xl font-bold mb-2">Our Mission</h3>
                  <p className="text-muted-foreground">
                    Empower everyone to create professional videos with AI, making video creation accessible, affordable, and effortless.
                  </p>
                </CardContent>
              </Card>
              <Card className="hover-lift">
                <CardContent className="p-6">
                  <Heart className="w-12 h-12 text-primary mb-4" />
                  <h3 className="text-xl font-bold mb-2">Our Values</h3>
                  <p className="text-muted-foreground">
                    Innovation, simplicity, and customer success drive everything we do. We put creators first.
                  </p>
                </CardContent>
              </Card>
              <Card className="hover-lift">
                <CardContent className="p-6">
                  <Users className="w-12 h-12 text-primary mb-4" />
                  <h3 className="text-xl font-bold mb-2">Our Team</h3>
                  <p className="text-muted-foreground">
                    A diverse team of AI experts, designers, and creators passionate about transforming video production.
                  </p>
                </CardContent>
              </Card>
              <Card className="hover-lift">
                <CardContent className="p-6">
                  <Award className="w-12 h-12 text-primary mb-4" />
                  <h3 className="text-xl font-bold mb-2">Our Impact</h3>
                  <p className="text-muted-foreground">
                    10M+ videos created, 150+ countries served, 4.8/5 rating from happy creators worldwide.
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default AboutPage;