import React, { useState } from 'react';
import { Button } from '@/components/ui/button.jsx';
import { Input } from '@/components/ui/input.jsx';
import { Label } from '@/components/ui/label.jsx';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card.jsx';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { AlertCircle } from 'lucide-react';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [emailError, setEmailError] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const navigate = useNavigate();

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

    try {
      const res = await fetch('http://localhost:8000/api/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();

      if (data.success) {
        localStorage.setItem('fitrack_user', JSON.stringify(data.user));
        // Dispatch a custom event to notify other components about the login
        window.dispatchEvent(new Event('userLogin'));
        navigate('/');
      } else {
        // Handle different error types
        if (data.message === 'User not found') {
          setEmailError('No account found with this email');
        } else if (data.message === 'Invalid credentials') {
          setPasswordError('Incorrect password');
        } else {
          setError(data.message || 'Login failed. Please try again.');
        }
      }
    } catch (err) {
      setError('Connection error. Please try again later.');
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

            <Button type="submit" className="w-full bg-primary text-primary-foreground hover:bg-primary/90">
              Login
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