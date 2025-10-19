import React from 'react';
import { Navbar } from '../components/Navbar';
import { Footer } from '../components/Footer';
import { Card, CardContent } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Briefcase, MapPin, Clock } from 'lucide-react';

const CareersPage = () => {
  const jobs = [
    {
      title: 'Senior Full Stack Engineer',
      department: 'Engineering',
      location: 'San Francisco, CA (Remote)',
      type: 'Full-time'
    },
    {
      title: 'Product Designer',
      department: 'Design',
      location: 'Remote',
      type: 'Full-time'
    },
    {
      title: 'Customer Success Manager',
      department: 'Customer Success',
      location: 'New York, NY',
      type: 'Full-time'
    }
  ];

  return (
    <div className="min-h-screen">
      <Navbar />
      
      {/* Hero with Image */}
      <div className="pt-20 relative overflow-hidden">
        <div className="absolute inset-0 z-0">
          <img
            src="https://images.unsplash.com/photo-1758611972613-3afe657c3249?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHwxfHxoYXBweSUyMHdvcmtwbGFjZSUyMG9mZmljZSUyMGN1bHR1cmV8ZW58MHx8fHwxNzYwODY0ODMzfDA&ixlib=rb-4.1.0&q=85"
            alt="Happy workplace"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-background/95 via-background/80 to-background/90"></div>
        </div>
        
        <div className="relative z-10 container mx-auto px-4 py-24">
          <div className="text-center max-w-3xl mx-auto">
            <h1 className="text-4xl md:text-5xl font-bold font-heading mb-4">
              Join Our <span className="gradient-text">Team</span>
            </h1>
            <p className="text-lg text-muted-foreground">
              Help us revolutionize video creation with AI
            </p>
          </div>
        </div>
      </div>

      <div className="pb-16 bg-gradient-to-b from-background to-secondary/20">
        <div className="container mx-auto px-4 -mt-8">
          {/* Culture Images */}
          <div className="max-w-4xl mx-auto mb-12">
            <div className="grid md:grid-cols-2 gap-6">
              <div className="relative h-64 rounded-xl overflow-hidden hover-lift">
                <img
                  src="https://images.unsplash.com/photo-1758518731462-b2eb77e63020?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHwyfHxoYXBweSUyMHdvcmtwbGFjZSUyMG9mZmljZSUyMGN1bHR1cmV8ZW58MHx8fHwxNzYwODY0ODMzfDA&ixlib=rb-4.1.0&q=85"
                  alt="Team collaboration"
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="relative h-64 rounded-xl overflow-hidden hover-lift">
                <img
                  src="https://images.unsplash.com/photo-1758518730523-c9f6336ebdae?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHwzfHxoYXBweSUyMHdvcmtwbGFjZSUyMG9mZmljZSUyMGN1bHR1cmV8ZW58MHx8fHwxNzYwODY0ODMzfDA&ixlib=rb-4.1.0&q=85"
                  alt="Office culture"
                  className="w-full h-full object-cover"
                />
              </div>
            </div>
          </div>

          <div className="max-w-4xl mx-auto space-y-6">
            <h2 className="text-2xl font-bold mb-6">Open Positions</h2>
            {jobs.map((job, i) => (
              <Card key={i} className="hover-lift">
                <CardContent className="p-8">
                  <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                    <div>
                      <h3 className="text-xl font-bold mb-2">{job.title}</h3>
                      <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                        <div className="flex items-center gap-1">
                          <Briefcase className="w-4 h-4" />
                          {job.department}
                        </div>
                        <div className="flex items-center gap-1">
                          <MapPin className="w-4 h-4" />
                          {job.location}
                        </div>
                        <div className="flex items-center gap-1">
                          <Clock className="w-4 h-4" />
                          {job.type}
                        </div>
                      </div>
                    </div>
                    <Button variant="primary">Apply Now</Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default CareersPage;