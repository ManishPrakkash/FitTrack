import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation, Navigate } from 'react-router-dom';
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

const RequireAuth = ({ children }) => {
  const isAuthenticated = !!localStorage.getItem('fitrack_user');
  const location = useLocation();
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  return children;
};

const AppContent = () => {
  const location = useLocation();
  const [, forceUpdate] = React.useState({});

  // Force update when user logs in
  React.useEffect(() => {
    const handleUserLogin = () => {
      forceUpdate({});
    };

    window.addEventListener('userLogin', handleUserLogin);

    return () => {
      window.removeEventListener('userLogin', handleUserLogin);
    };
  }, []);

  return (
    <div className="flex flex-col min-h-screen bg-background text-foreground">
      <Header key={localStorage.getItem('fitrack_user') ? 'logged-in' : 'logged-out'} />
      <main className="flex-grow">
        <AnimatePresence mode="wait">
          <Routes location={location} key={location.pathname}>
            <Route path="/login" element={<PageLayout><LoginPage /></PageLayout>} />
            <Route path="/signup" element={<PageLayout><SignupPage /></PageLayout>} />
            <Route
              path="*"
              element={
                <RequireAuth>
                  <Routes location={location} key={location.pathname}>
                    <Route path="/" element={<PageLayout><HomePage /></PageLayout>} />
                    <Route path="/challenges" element={<PageLayout><ChallengesPage /></PageLayout>} />
                    <Route path="/leaderboard" element={<PageLayout><LeaderboardPage /></PageLayout>} />
                    <Route path="/admin" element={<PageLayout><AdminPage /></PageLayout>} />
                    <Route path="*" element={<PageLayout><NotFoundPage /></PageLayout>} />
                  </Routes>
                </RequireAuth>
              }
            />
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
    <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <AppContent />
    </Router>
  );
}

export default App;
