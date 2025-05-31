import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button.jsx';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Zap, Trophy, Users } from 'lucide-react';

// Minimal SVG background pattern
const BgPattern = () => (
  <svg
    className="absolute inset-0 w-full h-full pointer-events-none select-none opacity-10 z-0"
    width="100%" height="100%" viewBox="0 0 1440 720" fill="none"
    xmlns="http://www.w3.org/2000/svg"
    style={{ minHeight: '100vh' }}
  >
    <defs>
      <pattern id="dots" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
        <circle cx="2" cy="2" r="2" fill="#fff" fillOpacity="0.08" />
      </pattern>
    </defs>
    <rect width="100%" height="100%" fill="url(#dots)" />
  </svg>
);

const BgAccent = () => (
  <svg
    className="absolute left-1/2 top-0 -translate-x-1/2 -translate-y-1/3 z-0 pointer-events-none select-none"
    width="900" height="400" viewBox="0 0 900 400" fill="none"
    style={{ filter: 'blur(80px)', opacity: 0.18 }}
    aria-hidden="true"
  >
    <ellipse cx="450" cy="200" rx="400" ry="160" fill="white" />
  </svg>
);

const FeatureCard = ({ icon: Icon, title, description, link, linkText }) => (
  <motion.div
    className="bg-card glass-card p-6 rounded-xl premium-shadow border border-border relative z-10"
    whileHover={{ y: -5, boxShadow: "0px 10px 20px hsla(var(--ring) / 0.2)" }}
    transition={{ type: "spring", stiffness: 300 }}
  >
    <Icon className="h-12 w-12 text-primary mb-4" />
    <h3 className="text-xl font-semibold mb-2 text-foreground">{title}</h3>
    <p className="text-muted-foreground mb-4 text-sm">{description}</p>
    <Link to={link}>
      <Button variant="outline" className="w-full hover:bg-primary hover:text-primary-foreground transition-colors premium-btn">
        {linkText}
      </Button>
    </Link>
  </motion.div>
);

// Add a dark blurred accent behind the CTA card
const CtaAccent = () => (
  <svg
    className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-0 pointer-events-none select-none"
    width="600" height="220" viewBox="0 0 600 220" fill="none"
    style={{ filter: 'blur(60px)', opacity: 0.13 }}
    aria-hidden="true"
  >
    <ellipse cx="300" cy="110" rx="260" ry="90" fill="#000" />
  </svg>
);

const HomePage = () => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Check if user is logged in
    const userData = localStorage.getItem('fitrack_user');
    if (userData) {
      setUser(JSON.parse(userData));
    }
  }, []);

  return (
    <div className="relative min-h-screen flex flex-col justify-between overflow-x-hidden">
      <BgPattern />
      <BgAccent />
      <motion.div
        className="container mx-auto py-10 px-4 relative z-10"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.5 }}
      >
        <section className="text-center mb-16 flex flex-col items-center justify-center min-h-[260px] relative">
          <motion.h1
            className="text-6xl md:text-7xl font-extrabold mb-4 bg-gradient-to-r from-foreground via-muted-foreground to-foreground bg-clip-text text-transparent tracking-tight drop-shadow-xl"
            initial={{ y: -50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2, type: 'spring', stiffness: 100 }}
          >
            {user ? `Welcome, ${user.name?.split(' ')[0] || 'User'}!` : 'Conquer Your Fitness Goals'}
          </motion.h1>
          <div className="accent-line mb-6" />
          <motion.p
            className="text-2xl text-muted-foreground mb-12 max-w-2xl mx-auto font-medium"
            initial={{ y: -30, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.4, type: 'spring', stiffness: 100 }}
          >
            {user
              ? `Track your fitness goals, join challenges, and compete on the leaderboard, ${user.name?.split(' ')[0] || 'User'}!`
              : 'Join exciting fitness challenges, track your progress, compete with others, and achieve new personal bests with Fitrack.'}
          </motion.p>
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.6, type: 'spring', stiffness: 100 }}
            className="flex justify-center"
          >
            <Link to="/challenges">
              <Button size="lg" className="premium-btn bg-background text-foreground border border-accent px-10 py-7 text-xl font-semibold uppercase tracking-wider shadow-lg hover:bg-foreground hover:text-background transition-colors">
                Explore Challenges
              </Button>
            </Link>
          </motion.div>
        </section>

        <section className="grid md:grid-cols-3 gap-8 mb-8">
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

        {/* Remove top margin from CTA section for tighter spacing */}
        <section className="relative bg-card/80 glass-card p-12 rounded-2xl premium-shadow border border-border text-center flex flex-col items-center mt-8 overflow-hidden">
          <CtaAccent />
          <motion.h2
            className="text-3xl font-bold mb-4 text-foreground tracking-tight relative z-10"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2, duration: 0.5 }}
          >
            Ready to Start Your Fitness Journey?
          </motion.h2>
          <div className="accent-line mb-6 relative z-10" />
          <motion.p
            className="text-muted-foreground mb-10 max-w-xl mx-auto font-medium relative z-10"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ delay: 0.4, duration: 0.5 }}
          >
            Sign up (simulated for now) or explore existing challenges. It's time to move, compete, and achieve!
          </motion.p>
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ delay: 0.6, duration: 0.5 }}
            className="relative z-10"
          >
            <Link to="/challenges">
              <Button size="lg" variant="secondary" className="premium-btn text-lg px-10 py-7 font-semibold uppercase tracking-wider border border-accent flex items-center gap-3">
                View All Challenges
                <span className="inline-block animate-bounce-slow">
                  <svg width="22" height="22" fill="none" viewBox="0 0 24 24"><path d="M12 5v14m0 0l-6-6m6 6l6-6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
                </span>
              </Button>
            </Link>
          </motion.div>
        </section>
        {!user && (
          <div className="text-center mt-8">
            <div className="accent-line mb-4" />
          </div>
        )}
        {user && (
          <div className="text-center mt-8">
            <h1 className="text-5xl font-bold mb-6 text-foreground">
              Welcome, {user.name?.split(' ')[0] || 'User'}
            </h1>
            <div className="accent-line mb-4" />
            <p className="text-lg text-muted-foreground mb-8">
              Track your fitness goals, join challenges, and compete on the leaderboard.
            </p>
          </div>
        )}
      </motion.div>
    </div>
  );
};

export default HomePage;

/* Add this to your CSS for the chevron animation:
@keyframes bounce-slow {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(8px); }
}
.animate-bounce-slow {
  animation: bounce-slow 1.8s infinite;
}
*/
