/**
 * Test script to verify frontend-backend connection for authentication
 *
 * This script tests the connection between the frontend and backend
 * for user authentication (login and signup).
 */

// Import fetch
import fetch from 'node-fetch';

// Base URL for the API
// const BASE_URL = 'https://fitrack-backend.vercel.app';
const BASE_URL = 'http://localhost:8000'; // Uncomment for local testing

// Test user data
const testUser = {
  name: 'Test User',
  email: `testuser_${Date.now()}@example.com`,
  password: 'testpassword123'
};

// Test registration
async function testRegistration() {
  console.log('Testing registration...');
  console.log(`Using test user: ${testUser.email}`);

  try {
    const response = await fetch(`${BASE_URL}/api/mongodb/register/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(testUser)
    });

    const data = await response.json();
    console.log(`Status code: ${response.status}`);
    console.log('Response:', data);

    if (response.status === 201) {
      console.log('Registration successful!');
      return true;
    } else {
      console.log('Registration failed.');
      return false;
    }
  } catch (error) {
    console.error('Error during registration:', error);
    return false;
  }
}

// Test login
async function testLogin() {
  console.log('\nTesting login...');

  try {
    const response = await fetch(`${BASE_URL}/api/mongodb/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: testUser.email,
        password: testUser.password
      })
    });

    const data = await response.json();
    console.log(`Status code: ${response.status}`);
    console.log('Response:', data);

    if (response.status === 200) {
      console.log('Login successful!');
      return data.token;
    } else {
      console.log('Login failed.');
      return null;
    }
  } catch (error) {
    console.error('Error during login:', error);
    return null;
  }
}

// Test token validation
async function testTokenValidation(token) {
  console.log('\nTesting token validation...');

  try {
    const response = await fetch(`${BASE_URL}/api/mongodb/validate-token/`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    const data = await response.json();
    console.log(`Status code: ${response.status}`);
    console.log('Response:', data);

    if (response.status === 200) {
      console.log('Token validation successful!');
      return true;
    } else {
      console.log('Token validation failed.');
      return false;
    }
  } catch (error) {
    console.error('Error during token validation:', error);
    return false;
  }
}

// Run the tests
async function runTests() {
  console.log('Starting frontend-backend connection tests...');

  // Test registration
  const registrationSuccess = await testRegistration();

  if (!registrationSuccess) {
    console.log('Registration test failed. Stopping tests.');
    return;
  }

  // Test login
  const token = await testLogin();

  if (!token) {
    console.log('Login test failed. Stopping tests.');
    return;
  }

  // Test token validation
  const validationSuccess = await testTokenValidation(token);

  if (!validationSuccess) {
    console.log('Token validation test failed.');
    return;
  }

  console.log('\nAll tests passed successfully!');
}

// Run the tests
runTests();
