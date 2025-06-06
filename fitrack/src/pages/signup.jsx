import React, { useState } from 'react';
import { Button } from '@/components/ui/button.jsx';
import { Input } from '@/components/ui/input.jsx';
import { Label } from '@/components/ui/label.jsx';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card.jsx';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { AlertCircle } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext.jsx';

const SignupPage = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [nameError, setNameError] = useState('');
  const [emailError, setEmailError] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const { register } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Reset previous errors
    setError('');
    setNameError('');
    setEmailError('');
    setPasswordError('');

    // Validate inputs
    let isValid = true;

    if (!name) {
      setNameError('Name is required');
      isValid = false;
    }

    if (!email) {
      setEmailError('Email is required');
      isValid = false;
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      setEmailError('Please enter a valid email address');
      isValid = false;
    }

    if (!password) {
      setPasswordError('Password is required');
      isValid = false;
    } else if (password.length < 6) {
      setPasswordError('Password must be at least 6 characters');
      isValid = false;
    }

    if (!isValid) return;

    setIsLoading(true);

    try {
      console.log('Registering user with:', { name, email, password: '***' });
      const result = await register(name, email, password);
      console.log('Registration result:', result);

      if (result.success) {
        // Redirect to login page after successful registration
        navigate('/login', {
          state: {
            message: 'Registration successful! Please log in with your new account.'
          }
        });
      } else {
        // Handle different error types
        console.error('Registration failed:', result);
        if (result.error?.message?.includes('Email already exists')) {
          setEmailError('This email is already registered');
        } else {
          setError(result.error?.message || result.message || 'Signup failed. Please try again.');
        }
      }
    } catch (err) {
      console.error('Signup error:', err);
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
      <Card className="w-full max-w-md glass-card premium-shadow border border-border">
        <CardHeader>
          <CardTitle className="text-3xl font-bold tracking-tight mb-1">Sign Up</CardTitle>
          <div className="accent-line mb-2" />
          <CardDescription className="text-base text-muted-foreground">Create your Fitrack account</CardDescription>
        </CardHeader>
        <CardContent>
          {error && (
            <div className="bg-destructive/10 text-destructive text-sm p-3 rounded-md flex items-center mb-4">
              <AlertCircle className="h-4 w-4 mr-2" />
              {error}
            </div>
          )}
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="name">Name</Label>
              <Input
                id="name"
                type="text"
                value={name}
                onChange={(e) => {
                  setName(e.target.value);
                  if (nameError) setNameError('');
                }}
                placeholder="Enter your name"
                autoComplete="name"
                className={`bg-background border border-accent/30 text-foreground placeholder-muted-foreground focus:ring-primary focus:border-primary rounded-md`}
              />
              {nameError && (
                <div className="text-destructive text-sm flex items-center mt-1">
                  <AlertCircle className="h-3 w-3 mr-1" />
                  {nameError}
                </div>
              )}
            </div>
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
                className={`bg-background border border-accent/30 text-foreground placeholder-muted-foreground focus:ring-primary focus:border-primary rounded-md`}
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
                autoComplete="new-password"
                className={`bg-background border border-accent/30 text-foreground placeholder-muted-foreground focus:ring-primary focus:border-primary rounded-md`}
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
              className="w-full premium-btn bg-primary text-primary-foreground hover:bg-primary/90 text-base font-semibold tracking-wide rounded-md"
              disabled={isLoading}
            >
              {isLoading ? 'Creating Account...' : 'Sign Up'}
            </Button>
          </form>
          <p className="text-sm text-muted-foreground mt-4 text-center">
            Already have an account?{' '}
            <Link to="/login" className="text-primary hover:underline font-semibold">
              Login
            </Link>
          </p>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default SignupPage;