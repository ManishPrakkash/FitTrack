import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import Header from '@/components/layout/Header.jsx';
import Footer from '@/components/layout/Footer.jsx';
import HomePage from '@/pages/HomePage.jsx';
import ChallengesPage from '@/pages/ChallengesPage.jsx';
import LeaderboardPage from '@/pages/LeaderboardPage.jsx';
import AdminPage from '@/pages/AdminPage.jsx';
import NotFoundPage from '@/pages/NotFoundPage.jsx';
import LoginPage from '@/pages/login.jsx';
import SignupPage from '@/pages/signup.jsx';
import { Toaster } from '@/components/ui/toaster.jsx';
import { AnimatePresence, motion } from 'framer-motion';

const PageLayout = ({ children }) => {
  const location = useLocation();
  return (
    <motion.div
      key={location.pathname}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
    >
      {children}
    </motion.div>
  );
};

const AppContent = () => {
  const location = useLocation();
  return (
    <div className="flex flex-col min-h-screen bg-background text-foreground">
      <Header />
      <main className="flex-grow">
        <AnimatePresence mode="wait">
          <Routes location={location} key={location.pathname}>
            <Route path="/" element={<PageLayout><HomePage /></PageLayout>} />
            <Route path="/challenges" element={<PageLayout><ChallengesPage /></PageLayout>} />
            <Route path="/leaderboard" element={<PageLayout><LeaderboardPage /></PageLayout>} />
            <Route path="/admin" element={<PageLayout><AdminPage /></PageLayout>} />
            <Route path="/login" element={<PageLayout><LoginPage /></PageLayout>} />
            <Route path="/signup" element={<PageLayout><SignupPage /></PageLayout>} />
            <Route path="*" element={<PageLayout><NotFoundPage /></PageLayout>} />
          </Routes>
        </AnimatePresence>
      </main>
      <Footer />
      <Toaster />
    </div>
  );
};

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;
