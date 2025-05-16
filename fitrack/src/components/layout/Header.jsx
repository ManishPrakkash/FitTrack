
    import React, { useState, useEffect, useRef } from 'react';
    import { Link, NavLink, useNavigate } from 'react-router-dom';
    import { Dumbbell, Home, Trophy, ShieldCheck, Users, LogOut } from 'lucide-react';
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

    const ProfileMenu = ({ user, onLogout }) => {
      const [isOpen, setIsOpen] = useState(false);
      const menuRef = useRef(null);

      // Get first letter of user's name for the avatar
      const userInitial = user?.name ? user.name.charAt(0).toUpperCase() : '?';

      // Close menu when clicking outside
      useEffect(() => {
        const handleClickOutside = (event) => {
          if (menuRef.current && !menuRef.current.contains(event.target)) {
            setIsOpen(false);
          }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => {
          document.removeEventListener('mousedown', handleClickOutside);
        };
      }, []);

      return (
        <div className="relative" ref={menuRef}>
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="flex items-center justify-center w-10 h-10 bg-primary text-primary-foreground rounded-full hover:bg-primary/90 font-semibold"
            title={user?.name || 'Profile'}
          >
            {userInitial}
          </button>

          {isOpen && (
            <div className="absolute right-0 mt-2 w-48 bg-card rounded-md shadow-lg py-1 z-50 border border-border">
              <div className="px-4 py-2 border-b border-border">
                <p className="text-sm font-medium text-foreground">{user?.name}</p>
                <p className="text-xs text-muted-foreground truncate">{user?.email}</p>
              </div>
              <button
                onClick={onLogout}
                className="flex w-full items-center px-4 py-2 text-sm text-muted-foreground hover:bg-secondary hover:text-secondary-foreground"
              >
                <LogOut className="mr-2 h-4 w-4" />
                Logout
              </button>
            </div>
          )}
        </div>
      );
    };

    const Header = () => {
      const navigate = useNavigate();
      const [user, setUser] = useState(null);

      useEffect(() => {
        // Check if user is logged in
        const userData = localStorage.getItem('fittrack_user');
        if (userData) {
          setUser(JSON.parse(userData));
        }

        // Listen for login events
        const handleUserLogin = () => {
          const userData = localStorage.getItem('fittrack_user');
          if (userData) {
            setUser(JSON.parse(userData));
          }
        };

        window.addEventListener('userLogin', handleUserLogin);

        // Cleanup event listener on component unmount
        return () => {
          window.removeEventListener('userLogin', handleUserLogin);
        };
      }, []);

      const handleLogout = () => {
        localStorage.removeItem('fittrack_user');
        setUser(null);
        // Dispatch event to notify other components
        window.dispatchEvent(new Event('userLogin'));
        navigate('/login');
      };

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
                Fitrack
              </Link>

              {user ? (
                <div className="flex items-center">
                  <nav className="flex items-center space-x-2 sm:space-x-4 mr-4">
                    <NavItem to="/" icon={Home}>Home</NavItem>
                    <NavItem to="/challenges" icon={Trophy}>Challenges</NavItem>
                    <NavItem to="/leaderboard" icon={Users}>Leaderboard</NavItem>
                    <NavItem to="/admin" icon={ShieldCheck}>Admin</NavItem>
                  </nav>
                  <ProfileMenu user={user} onLogout={handleLogout} />
                </div>
              ) : (
                <div className="flex items-center space-x-2">
                  <Link to="/login">
                    <Button variant="secondary" size="sm">Login</Button>
                  </Link>
                  <Link to="/signup">
                    <Button variant="primary" size="sm">Sign Up</Button>
                  </Link>
                </div>
              )}
            </div>
          </div>
        </motion.header>
      );
    };

    export default Header;
