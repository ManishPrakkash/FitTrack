
    import React from 'react';
    import { motion } from 'framer-motion';

    const Footer = () => {
      const currentYear = new Date().getFullYear();
      return (
        <motion.footer 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5, duration: 0.5 }}
          className="bg-card border-t border-border py-8 text-center text-muted-foreground"
        >
          <div className="container mx-auto px-4">
            <p className="text-sm">
              &copy; {currentYear} FitTrack. All rights reserved.
            </p>
            <p className="text-xs mt-1">
              Join challenges, track progress, and conquer your fitness goals!
            </p>
          </div>
        </motion.footer>
      );
    };

    export default Footer;
  