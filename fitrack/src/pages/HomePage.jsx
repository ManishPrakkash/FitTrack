import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button.jsx';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Zap, Trophy, Users } from 'lucide-react';

const FeatureCard = ({ icon: Icon, title, description, link, linkText }) => (
  <motion.div
    className="bg-card p-6 rounded-lg shadow-lg border border-border"
    whileHover={{ y: -5, boxShadow: "0px 10px 20px hsla(var(--ring) / 0.2)"}}
    transition={{ type: "spring", stiffness: 300 }}
  >
    <Icon className="h-12 w-12 text-primary mb-4" />
    <h3 className="text-xl font-semibold mb-2 text-foreground">{title}</h3>
    <p className="text-muted-foreground mb-4 text-sm">{description}</p>
    <Link to={link}>
      <Button variant="outline" className="w-full hover:bg-primary hover:text-primary-foreground transition-colors">
        {linkText}
      </Button>
    </Link>
  </motion.div>
);

const HomePage = () => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Check if user is logged in
    const userData = localStorage.getItem('fittrack_user');
    if (userData) {
      setUser(JSON.parse(userData));
    }
  }, []);

  return (
    <motion.div
      className="container mx-auto py-12 px-4"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.5 }}
    >
      <section className="text-center mb-16">
        <motion.h1
          className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-primary via-muted-foreground to-primary bg-clip-text text-transparent"
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2, type: "spring", stiffness: 100 }}
        >
          Conquer Your Fitness Goals
        </motion.h1>
        <motion.p
          className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto"
          initial={{ y: -30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.4, type: "spring", stiffness: 100 }}
        >
          Join exciting fitness challenges, track your progress, compete with others, and achieve new personal bests with FitTrack.
        </motion.p>
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.6, type: "spring", stiffness: 100 }}
        >
          <Link to="/challenges">
            <Button size="lg" className="bg-primary text-primary-foreground hover:bg-primary/90 text-lg px-8 py-6">
              Explore Challenges
            </Button>
          </Link>
        </motion.div>
      </section>

      <section className="grid md:grid-cols-3 gap-8 mb-16">
        <FeatureCard
          icon={Zap}
          title="Join Challenges"
          description="Discover a variety of fitness challenges tailored to different activities and fitness levels."
          link="/challenges"
          linkText="Find a Challenge"
        />
        <FeatureCard
          icon={Trophy}
          title="Track Progress"
          description="Log your activities seamlessly and visualize your journey towards achieving challenge goals."
          link="/challenges"
          linkText="View My Progress"
        />
        <FeatureCard
          icon={Users}
          title="Compete & Share"
          description="See how you stack up against others on leaderboards and share your accomplishments."
          link="/leaderboard"
          linkText="Check Leaderboards"
        />
      </section>

      <section className="bg-card p-8 rounded-lg shadow-lg border border-border text-center">
        <motion.h2
          className="text-3xl font-semibold mb-4 text-foreground"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.2, duration: 0.5}}
        >
          Ready to Start Your Fitness Journey?
        </motion.h2>
        <motion.p
          className="text-muted-foreground mb-6 max-w-xl mx-auto"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.4, duration: 0.5}}
        >
          Sign up (simulated for now) or explore existing challenges. It's time to move, compete, and achieve!
        </motion.p>
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.6, duration: 0.5}}
        >
          <Link to="/challenges">
            <Button size="lg" variant="secondary" className="text-lg px-8 py-6">
              View All Challenges
            </Button>
          </Link>
        </motion.div>
      </section>
      {!user && (
        <div className="text-center mt-8">
          <h1 className="text-5xl font-bold mb-6 text-foreground">Welcome to FitTrack</h1>
          <p className="text-lg text-muted-foreground mb-8">
            Track your fitness goals, join challenges, and compete on the leaderboard.
          </p>
          <div className="space-x-4">
            <Link to="/login" className="bg-primary text-primary-foreground px-6 py-3 rounded hover:bg-primary/90">
              Login
            </Link>
            <Link to="/signup" className="bg-secondary text-secondary-foreground px-6 py-3 rounded hover:bg-secondary/90">
              Sign Up
            </Link>
          </div>
        </div>
      )}

      {user && (
        <div className="text-center mt-8">
          <h1 className="text-5xl font-bold mb-6 text-foreground">Welcome back, {user.name}!</h1>
          <p className="text-lg text-muted-foreground mb-8">
            Continue your fitness journey, join new challenges, or check your progress.
          </p>
        </div>
      )}
    </motion.div>
  );
};

export default HomePage;
