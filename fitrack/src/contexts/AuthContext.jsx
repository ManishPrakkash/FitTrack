import React, { createContext, useContext, useState, useEffect } from 'react';
import { getApiUrl } from '@/config/api';

// Create the authentication context
const AuthContext = createContext();

// Custom hook to use the auth context
export const useAuth = () => {
  return useContext(AuthContext);
};

// Provider component that wraps the app and makes auth object available to any child component
export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  // Load user from localStorage on initial render
  useEffect(() => {
    const storedUser = localStorage.getItem('fittrack_user');
    const storedToken = localStorage.getItem('fittrack_token');
    
    if (storedUser && storedToken) {
      setCurrentUser(JSON.parse(storedUser));
      setToken(storedToken);
      
      // Validate token with backend
      validateToken(storedToken);
    } else {
      setLoading(false);
    }
  }, []);

  // Validate token with backend
  const validateToken = async (token) => {
    try {
      const response = await fetch(getApiUrl('validate-token'), {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      const data = await response.json();
      
      if (!data.success) {
        // Token is invalid, log out
        logout();
      }
      
      setLoading(false);
    } catch (error) {
      console.error('Token validation error:', error);
      setLoading(false);
    }
  };

  // Login function
  const login = async (email, password) => {
    try {
      const response = await fetch(getApiUrl('login'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      
      const data = await response.json();
      
      if (data.success) {
        setCurrentUser(data.user);
        setToken(data.token);
        
        // Store in localStorage
        localStorage.setItem('fittrack_user', JSON.stringify(data.user));
        localStorage.setItem('fittrack_token', data.token);
        
        // Dispatch event for components that need to know about login
        window.dispatchEvent(new Event('userLogin'));
        
        return { success: true };
      } else {
        return { 
          success: false, 
          message: data.message || 'Login failed'
        };
      }
    } catch (error) {
      console.error('Login error:', error);
      return { 
        success: false, 
        message: `Connection error: ${error.message || 'Unable to connect to the server'}`
      };
    }
  };

  // Register function
  const register = async (name, email, password) => {
    try {
      const response = await fetch(getApiUrl('register'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password }),
      });
      
      const data = await response.json();
      
      return { 
        success: data.success, 
        message: data.message,
        error: data.error
      };
    } catch (error) {
      console.error('Registration error:', error);
      return { 
        success: false, 
        message: `Connection error: ${error.message || 'Unable to connect to the server'}`
      };
    }
  };

  // Logout function
  const logout = () => {
    setCurrentUser(null);
    setToken(null);
    localStorage.removeItem('fittrack_user');
    localStorage.removeItem('fittrack_token');
    window.dispatchEvent(new Event('userLogout'));
  };

  // Create value object with auth state and functions
  const value = {
    currentUser,
    token,
    login,
    register,
    logout,
    isAuthenticated: !!currentUser,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};
