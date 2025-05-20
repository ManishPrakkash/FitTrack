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
    // Authentication (Django)
    login: '/api/login/',
    register: '/api/register/',
    'validate-token': '/api/validate-token/',
    profile: '/api/profile/',

    // MongoDB Authentication (Direct)
    mongoLogin: '/api/mongodb/login/',
    mongoRegister: '/api/mongodb/register/',
    'mongo-validate-token': '/api/mongodb/validate-token/',

    // Challenges
    challenges: '/api/challenges/',
    joinedChallenges: '/api/challenges/joined/',
    availableChallenges: '/api/challenges/available/',
    joinChallenge: (id) => `/api/challenges/${id}/join/`,
    leaderboard: (id) => `/api/challenges/leaderboard/${id}/`,

    // Activities
    activities: '/api/activities/',
    logActivity: '/api/activities/log/',
    challengeActivities: '/api/activities/challenge/',
  }
};

// Helper function to get full URL for an endpoint
export const getApiUrl = (endpoint, ...args) => {
  const endpointValue = API.endpoints[endpoint];

  // If the endpoint is a function (like joinChallenge), call it with the provided args
  if (typeof endpointValue === 'function') {
    return API.baseUrl + endpointValue(...args);
  }

  return API.baseUrl + endpointValue;
};

export default API;
