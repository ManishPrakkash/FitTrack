import React from 'react';
    import { Link } from 'react-router-dom';
    import { Button } from '@/components/ui/button.jsx';
    import { Frown } from 'lucide-react';
    import { motion } from 'framer-motion';

    const NotFoundPage = () => {
      return (
        <motion.div 
          className="flex flex-col items-center justify-center min-h-[calc(100vh-10rem)] text-center px-4"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
        >
          <Frown className="w-32 h-32 text-primary mb-8" />
          <h1 className="text-6xl font-extrabold text-foreground mb-2 tracking-tight">404</h1>
          <div className="accent-line mb-4" />
          <p className="text-2xl text-muted-foreground mb-8 font-medium">
            Oops! The page you're looking for doesn't exist.
          </p>
          <Link to="/">
            <Button size="lg" className="premium-btn bg-background text-foreground border border-accent px-8 py-4 text-lg font-semibold uppercase tracking-wider shadow-md hover:bg-foreground hover:text-background transition-colors">
              Go Back Home
            </Button>
          </Link>
        </motion.div>
      );
    };

    export default NotFoundPage;
