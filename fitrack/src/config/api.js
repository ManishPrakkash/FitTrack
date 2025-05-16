// API configuration for Fitrack application

// Determine the base URL based on the environment
const getBaseUrl = () => {
  // For local development
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return 'http://localhost:8000';
  }

  // For production deployment
  // This will use the deployed backend URL when the app is hosted on Vercel
  return process.env.REACT_APP_API_URL || 'https://fitrack-backend.vercel.app';
};

// API endpoints
const API = {
  baseUrl: getBaseUrl(),
  endpoints: {
    login: '/api/login/',
    register: '/api/register/',
    // Add other endpoints as needed
  }
};

// Helper function to get full URL for an endpoint
export const getApiUrl = (endpoint) => {
  return API.baseUrl + API.endpoints[endpoint];
};

export default API;
