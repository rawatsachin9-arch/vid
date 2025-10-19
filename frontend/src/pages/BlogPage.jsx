import React from 'react';
import { Navbar } from '../components/Navbar';
import { Footer } from '../components/Footer';
import { Card, CardContent } from '../components/ui/card';
import { Calendar, User, Tag } from 'lucide-react';

const BlogPage = () => {
  const posts = [
    {
      title: '10 Tips for Creating Engaging Video Content',
      excerpt: 'Learn the secrets to keeping your audience hooked from start to finish with professional video creation techniques.',
      date: 'Jan 15, 2024',
      author: 'Sarah Johnson',
      category: 'Tips',
      image: 'https://images.unsplash.com/photo-1686061592315-af9342dc8d74?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzF8MHwxfHNlYXJjaHwxfHxjb250ZW50JTIwY3JlYXRpb24lMjB2aWRlbyUyMHByb2R1Y3Rpb258ZW58MHx8fHwxNzYwODY0ODQxfDA&ixlib=rb-4.1.0&q=85'
    },
    {
      title: 'How AI is Revolutionizing Video Production',
      excerpt: 'Discover how artificial intelligence is changing the video creation landscape and making professional content accessible to everyone.',
      date: 'Jan 12, 2024',
      author: 'Michael Chen',
      category: 'Technology',
      image: 'https://images.unsplash.com/photo-1686061594179-4ac2edf0e13c?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzF8MHwxfHNlYXJjaHwyfHxjb250ZW50JTIwY3JlYXRpb24lMjB2aWRlbyUyMHByb2R1Y3Rpb258ZW58MHx8fHwxNzYwODY0ODQxfDA&ixlib=rb-4.1.0&q=85'
    },
    {
      title: 'Video Marketing Statistics You Need to Know',
      excerpt: 'Latest data on video marketing performance, consumer behavior, and trends that will shape your content strategy.',
      date: 'Jan 10, 2024',
      author: 'Emily Rodriguez',
      category: 'Marketing',
      image: 'https://images.unsplash.com/photo-1758273239504-b026c5bb2190?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzF8MHwxfHNlYXJjaHwzfHxjb250ZW50JTIwY3JlYXRpb24lMjB2aWRlbyUyMHByb2R1Y3Rpb258ZW58MHx8fHwxNzYwODY0ODQxfDA&ixlib=rb-4.1.0&q=85'
    }
  ];

  return (
    <div className="min-h-screen">
      <Navbar />
      <div className="pt-24 pb-16 bg-gradient-to-b from-background to-secondary/20">
        <div className="container mx-auto px-4">
          <div className="text-center max-w-3xl mx-auto mb-12">
            <h1 className="text-4xl md:text-5xl font-bold font-heading mb-4">
              VideoMaker <span className="gradient-text">Blog</span>
            </h1>
            <p className="text-lg text-muted-foreground">
              Tips, tutorials, and insights for video creators
            </p>
          </div>

          <div className="max-w-4xl mx-auto space-y-6">
            {posts.map((post, i) => (
              <Card key={i} className="hover-lift cursor-pointer overflow-hidden">
                <div className="grid md:grid-cols-3 gap-6">
                  <div className="relative h-48 md:h-auto">
                    <img
                      src={post.image}
                      alt={post.title}
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <CardContent className="md:col-span-2 p-8">
                    <div className="flex flex-wrap gap-4 text-sm text-muted-foreground mb-3">
                      <div className="flex items-center gap-1">
                        <Calendar className="w-4 h-4" />
                        {post.date}
                      </div>
                      <div className="flex items-center gap-1">
                        <User className="w-4 h-4" />
                        {post.author}
                      </div>
                      <div className="flex items-center gap-1">
                        <Tag className="w-4 h-4" />
                        {post.category}
                      </div>
                    </div>
                    <h2 className="text-2xl font-bold mb-2">{post.title}</h2>
                    <p className="text-muted-foreground">{post.excerpt}</p>
                  </CardContent>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default BlogPage;