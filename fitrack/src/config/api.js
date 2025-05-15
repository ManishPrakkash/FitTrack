// API configuration for Fitrack application

// Determine the base URL based on the environment
const getBaseUrl = () => {
  // For local development
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return 'http://localhost:8000';
  }
  
  // For production - replace this with your deployed backend URL
  // This should be the URL where your Django backend is hosted
  return 'https://your-backend-url.com'; // Replace with your actual backend URL
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
