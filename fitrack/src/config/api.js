// API configuration for Fitrack application

// Determine the base URL based on the environment
const getBaseUrl = () => {
  // For local development
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return 'http://localhost:8000';
  }

  // TEMPORARY SOLUTION: Use your local machine's IP address and port
  // This allows your phone to connect to your laptop's backend when on the same network
  return 'http://10.0.0.219:8000';

  // PRODUCTION SOLUTION (uncomment when you deploy your backend):
  // return 'https://your-deployed-backend-url.com';
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
