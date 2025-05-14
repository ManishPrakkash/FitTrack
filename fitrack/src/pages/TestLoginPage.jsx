import { useState } from 'react';
import { Button } from '@/components/ui/button.jsx';
import { Input } from '@/components/ui/input.jsx';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx';

const TestLoginPage = () => {
  const [email, setEmail] = useState('test@example.com');
  const [password, setPassword] = useState('password123');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    setLoading(true);
    setResult('Attempting to login...');
    
    try {
      const res = await fetch('http://localhost:8000/api/login/', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ email, password }),
      });
      
      setResult(`Response status: ${res.status}`);
      
      const data = await res.json();
      setResult(prev => `${prev}\nResponse data: ${JSON.stringify(data, null, 2)}`);
      
      if (data.success) {
        localStorage.setItem('fitrack_user', JSON.stringify(data.user));
        setResult(prev => `${prev}\nUser data stored in localStorage!`);
      }
    } catch (err) {
      setResult(`Error: ${err.message}`);
      console.error('Login error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto py-12 px-4 flex flex-col items-center">
      <Card className="w-full max-w-md mb-8">
        <CardHeader>
          <CardTitle>Test Login</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="block mb-2">Email</label>
            <Input 
              value={email} 
              onChange={(e) => setEmail(e.target.value)} 
              placeholder="Email"
            />
          </div>
          <div>
            <label className="block mb-2">Password</label>
            <Input 
              type="password" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)} 
              placeholder="Password"
            />
          </div>
          <Button 
            onClick={handleLogin} 
            disabled={loading}
            className="w-full"
          >
            {loading ? 'Loading...' : 'Test Login'}
          </Button>
        </CardContent>
      </Card>
      
      {result && (
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle>Result</CardTitle>
          </CardHeader>
          <CardContent>
            <pre className="whitespace-pre-wrap bg-secondary/20 p-4 rounded-md">
              {result}
            </pre>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default TestLoginPage;
