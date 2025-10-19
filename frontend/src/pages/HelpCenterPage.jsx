import React from 'react';
import { Navbar } from '../components/Navbar';
import { Footer } from '../components/Footer';
import { Card, CardContent } from '../components/ui/card';
import { Search, MessageCircle, BookOpen, FileText } from 'lucide-react';

const HelpCenterPage = () => {
  const categories = [
    { icon: Search, title: 'Getting Started', articles: 12 },
    { icon: MessageCircle, title: 'Account & Billing', articles: 8 },
    { icon: BookOpen, title: 'Video Creation', articles: 15 },
    { icon: FileText, title: 'Troubleshooting', articles: 10 }
  ];

  return (
    <div className="min-h-screen">
      <Navbar />
      
      {/* Hero with Image */}
      <div className="pt-20 relative overflow-hidden">
        <div className="absolute inset-0 z-0">
          <img
            src="https://images.unsplash.com/photo-1646756089735-487709743361?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODF8MHwxfHNlYXJjaHwxfHx0ZWNoJTIwc3VwcG9ydCUyMGxlYXJuaW5nfGVufDB8fHx8MTc2MDg2NDgzN3ww&ixlib=rb-4.1.0&q=85"
            alt="Tech support"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-b from-background/90 via-background/85 to-background"></div>
        </div>
        
        <div className="relative z-10 container mx-auto px-4 py-24">
          <div className="text-center max-w-3xl mx-auto">
            <h1 className="text-4xl md:text-5xl font-bold font-heading mb-4">
              Help <span className="gradient-text">Center</span>
            </h1>
            <p className="text-lg text-muted-foreground mb-8">
              Find answers to your questions
            </p>
            <div className="relative max-w-xl mx-auto">
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-muted-foreground" />
              <input
                type="text"
                placeholder="Search for help..."
                className="w-full pl-12 pr-4 py-3 border border-input rounded-lg focus:outline-none focus:ring-2 focus:ring-ring bg-card"
              />
            </div>
          </div>
        </div>
      </div>

      <div className="pb-16 bg-gradient-to-b from-background to-secondary/20">
        <div className="container mx-auto px-4 -mt-8">
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
            {categories.map((cat, i) => (
              <Card key={i} className="hover-lift cursor-pointer">
                <CardContent className="p-6 text-center">
                  <cat.icon className="w-12 h-12 text-primary mx-auto mb-4" />
                  <h3 className="font-bold mb-2">{cat.title}</h3>
                  <p className="text-sm text-muted-foreground">{cat.articles} articles</p>
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

export default HelpCenterPage;