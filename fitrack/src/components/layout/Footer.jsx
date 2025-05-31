import React from 'react';
    import { motion } from 'framer-motion';
    import { Instagram } from 'lucide-react';

    const Footer = () => {
      const currentYear = new Date().getFullYear();
      return (
        <motion.footer
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5, duration: 0.5 }}
          className="bg-card/80 glass-card border-t border-border py-10 text-center text-muted-foreground mt-16"
          style={{
            boxShadow:
              '0 -2px 24px 0 rgba(255,255,255,0.04), 0 -2px 0 0 hsl(var(--accent-line))',
          }}
        >
          <div className="container mx-auto px-4">
            <div className="accent-line mb-6" />
            <p className="text-base font-semibold text-foreground mb-1 tracking-wide">
              &copy; {currentYear} Fitrack. All rights reserved.
            </p>
            <p className="text-xs mt-1 mb-2 text-muted-foreground">
              Join challenges, track progress, and conquer your fitness goals!
            </p>
            <a
              href="https://www.instagram.com/manishmellow"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center text-xs mt-2 text-primary hover:text-primary/80 transition-colors premium-btn"
            >
              <Instagram className="h-3.5 w-3.5 mr-1" />
              Developed by Manishmellow
            </a>
          </div>
        </motion.footer>
      );
    };

    export default Footer;
