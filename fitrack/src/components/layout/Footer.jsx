
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
          className="bg-card border-t border-border py-8 text-center text-muted-foreground"
        >
          <div className="container mx-auto px-4">
            <p className="text-sm">
              &copy; {currentYear} Fitrack. All rights reserved.
            </p>
            <p className="text-xs mt-1">
              Join challenges, track progress, and conquer your fitness goals!
            </p>
            <a
              href="https://www.instagram.com/manishmellow"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center text-xs mt-2 text-primary hover:text-primary/80 transition-colors"
            >
              <Instagram className="h-3.5 w-3.5 mr-1" />
              Developed by Manishmellow
            </a>
          </div>
        </motion.footer>
      );
    };

    export default Footer;
