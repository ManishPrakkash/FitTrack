
    import React from 'react';
    import { Link, NavLink } from 'react-router-dom';
    import { Dumbbell, Home, Trophy, ShieldCheck, Users } from 'lucide-react';
    import { Button } from '@/components/ui/button.jsx';
    import { motion } from 'framer-motion';

    const NavItem = ({ to, icon: Icon, children }) => (
      <NavLink
        to={to}
        className={({ isActive }) =>
          `flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors ${
            isActive
              ? 'bg-primary text-primary-foreground'
              : 'text-muted-foreground hover:bg-secondary hover:text-secondary-foreground'
          }`
        }
      >
        <Icon className="mr-2 h-5 w-5" />
        {children}
      </NavLink>
    );

    const Header = () => {
      return (
        <motion.header 
          initial={{ y: -100 }}
          animate={{ y: 0 }}
          transition={{ type: "spring", stiffness: 120, damping: 20 }}
          className="bg-card border-b border-border shadow-sm sticky top-0 z-40"
        >
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              <Link to="/" className="flex items-center text-2xl font-bold text-foreground">
                <Dumbbell className="h-8 w-8 mr-2 text-primary" />
                FitTrack
              </Link>
              <nav className="flex items-center space-x-2 sm:space-x-4">
                <NavItem to="/" icon={Home}>Home</NavItem>
                <NavItem to="/challenges" icon={Trophy}>Challenges</NavItem>
                <NavItem to="/leaderboard" icon={Users}>Leaderboard</NavItem>
                <NavItem to="/admin" icon={ShieldCheck}>Admin</NavItem>
              </nav>
            </div>
          </div>
        </motion.header>
      );
    };

    export default Header;
  