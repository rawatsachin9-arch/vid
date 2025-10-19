import React from 'react';
import { Facebook, Twitter, Linkedin, Youtube, Instagram } from 'lucide-react';
import { VideoMakerLogo, VideoMakerLogoText } from './Logo';

export const Footer = () => {
  const footerLinks = {
    Features: [
      'Script to Video',
      'Blog to Video',
      'Edit Video Using Text',
      'Video Highlights',
      'Auto Captions',
      'API Access',
    ],
    Resources: [
      'Help Center',
      'Blog',
      'Case Studies',
      'Video Tutorials',
      'Community',
      'Roadmap',
    ],
    Company: [
      'About Us',
      'Careers',
      'Press',
      'Partners',
      'Affiliate Program',
      'Contact',
    ],
    Legal: [
      'Privacy Policy',
      'Terms of Service',
      'Cookie Policy',
      'GDPR',
      'Security',
    ],
  };

  const socialLinks = [
    { icon: Facebook, href: '#', label: 'Facebook' },
    { icon: Twitter, href: '#', label: 'Twitter' },
    { icon: Linkedin, href: '#', label: 'LinkedIn' },
    { icon: Youtube, href: '#', label: 'YouTube' },
    { icon: Instagram, href: '#', label: 'Instagram' },
  ];

  return (
    <footer className="bg-secondary/30 border-t border-border pt-16 pb-8">
      <div className="container mx-auto px-4">
        {/* Main Footer Content */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-6 gap-8 mb-12">
          {/* Logo and Description */}
          <div className="lg:col-span-2">
            <div className="flex items-center gap-3 mb-4">
              <VideoMakerLogo />
              <VideoMakerLogoText className="text-xl" />
            </div>
            <p className="text-sm text-muted-foreground mb-4 max-w-sm">
              Create stunning videos in minutes using the power of AI. Trusted by 10M+ creators worldwide.
            </p>
            {/* Social Links */}
            <div className="flex gap-3">
              {socialLinks.map((social) => (
                <a
                  key={social.label}
                  href={social.href}
                  className="w-9 h-9 rounded-lg bg-muted hover:bg-primary hover:text-primary-foreground transition-all duration-300 flex items-center justify-center"
                  aria-label={social.label}
                >
                  <social.icon className="w-4 h-4" />
                </a>
              ))}
            </div>
          </div>

          {/* Footer Links */}
          {Object.entries(footerLinks).map(([category, links]) => (
            <div key={category}>
              <h4 className="font-semibold text-foreground mb-4">{category}</h4>
              <ul className="space-y-2">
                {links.map((link) => (
                  <li key={link}>
                    <a
                      href="#"
                      className="text-sm text-muted-foreground hover:text-primary transition-colors"
                    >
                      {link}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-border flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-muted-foreground text-center md:text-left">
            © 2024 VideoMaker. All rights reserved. SOC 2 & GDPR compliant.
          </p>
          <div className="flex flex-wrap items-center justify-center gap-6 text-sm text-muted-foreground">
            <a href="#" className="hover:text-primary transition-colors">
              Privacy Policy
            </a>
            <a href="#" className="hover:text-primary transition-colors">
              Terms of Service
            </a>
            <a href="#" className="hover:text-primary transition-colors">
              Cookies
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};