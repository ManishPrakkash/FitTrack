
import React, { useState } from 'react';
import { Button } from '@/components/ui/button.jsx';
import { Input } from '@/components/ui/input.jsx';
import { Label } from '@/components/ui/label.jsx';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card.jsx';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { AlertCircle } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext.jsx';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [emailError, setEmailError] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();

  // Check for success message from registration
  React.useEffect(() => {
    if (location.state?.message) {
      setSuccess(location.state.message);
      // Clear the message from location state
      navigate(location.pathname, { replace: true, state: {} });
    }
  }, [location, navigate]);

  // Get the redirect path from location state or default to home
  const from = location.state?.from?.pathname || '/';

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Reset previous errors
    setError('');
    setEmailError('');
    setPasswordError('');

    // Validate inputs
    if (!email) {
      setEmailError('Email is required');
      return;
    }

    if (!password) {
      setPasswordError('Password is required');
      return;
    }

    setIsLoading(true);

    try {
      const result = await login(email, password);

      if (result.success) {
        // Redirect to the page they were trying to access or home
        navigate(from, { replace: true });
      } else {
        // Handle different error types
        if (result.message === 'User not found') {
          setEmailError('No account found with this email');
        } else if (result.message === 'Invalid credentials') {
          setPasswordError('Incorrect password');
        } else {
          setError(result.message || 'Login failed. Please try again.');
        }
      }
    } catch (err) {
      console.error('Login error:', err);
      setError(`Connection error: ${err.message || 'Unable to connect to the server'}. Please check your network connection and try again.`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <motion.div
      className="container mx-auto py-12 px-4 flex justify-center items-center min-h-screen"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Login</CardTitle>
          <CardDescription>Access your Fitrack account</CardDescription>
        </CardHeader>
        <CardContent>
          {error && (
            <div className="bg-destructive/10 text-destructive text-sm p-3 rounded-md flex items-center mb-4">
              <AlertCircle className="h-4 w-4 mr-2" />
              {error}
            </div>
          )}

          {success && (
            <div className="bg-green-100 text-green-800 text-sm p-3 rounded-md flex items-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              {success}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(e) => {
                  setEmail(e.target.value);
                  if (emailError) setEmailError('');
                }}
                placeholder="Enter your email"
                autoComplete="email"
                className={`bg-secondary/10 border ${
                  emailError ? 'border-destructive' : 'border-secondary/50'
                } text-foreground placeholder-muted-foreground focus:ring-primary focus:border-primary`}
              />
              {emailError && (
                <div className="text-destructive text-sm flex items-center mt-1">
                  <AlertCircle className="h-3 w-3 mr-1" />
                  {emailError}
                </div>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value);
                  if (passwordError) setPasswordError('');
                }}
                placeholder="Enter your password"
                autoComplete="current-password"
                className={`bg-secondary/10 border ${
                  passwordError ? 'border-destructive' : 'border-secondary/50'
                } text-foreground placeholder-muted-foreground focus:ring-primary focus:border-primary`}
              />
              {passwordError && (
                <div className="text-destructive text-sm flex items-center mt-1">
                  <AlertCircle className="h-3 w-3 mr-1" />
                  {passwordError}
                </div>
              )}
            </div>

            <Button
              type="submit"
              className="w-full bg-primary text-primary-foreground hover:bg-primary/90"
              disabled={isLoading}
            >
              {isLoading ? 'Logging in...' : 'Login'}
            </Button>
          </form>
          <p className="text-sm text-muted-foreground mt-4 text-center">
            Don't have an account?{' '}
            <Link to="/signup" className="text-primary hover:underline">
              Sign Up
            </Link>
          </p>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default LoginPage;