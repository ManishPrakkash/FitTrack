
    import React, { useState } from 'react';
    import { Button } from '@/components/ui/button.jsx';
    import { Input } from '@/components/ui/input.jsx';
    import { Label } from '@/components/ui/label.jsx';
    import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card.jsx';
    import { useToast } from '@/components/ui/use-toast.jsx';
    import { motion } from 'framer-motion';
    import { getApiUrl } from '@/config/api.js';

    const CreateChallengeForm = ({ onCreateChallenge }) => {
      const [name, setName] = useState('');
      const [type, setType] = useState('Walking');
      const [description, setDescription] = useState('');
      const [goal, setGoal] = useState('');
      const [unit, setUnit] = useState('km');
      const [isLoading, setIsLoading] = useState(false);
      const { toast } = useToast();

      const handleSubmit = async (e) => {
        e.preventDefault();
        if (!name || !description || !goal || isNaN(parseFloat(goal)) || parseFloat(goal) <= 0) {
           toast({
            title: "Invalid Input",
            description: "Please fill all fields correctly. Goal must be a positive number.",
            variant: "destructive",
          });
          return;
        }

        setIsLoading(true);

        try {
          // Get token from localStorage
          const token = localStorage.getItem('fittrack_token');
          if (!token) {
            toast({
              title: "Authentication Required",
              description: "Please log in to create challenges.",
              variant: "destructive",
            });
            setIsLoading(false);
            return;
          }

          // Create challenge via API
          const response = await fetch(getApiUrl('mongoCreateChallenge'), {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify({
              name,
              type,
              description,
              goal: parseFloat(goal),
              unit,
            }),
          });

          const data = await response.json();

          if (data.success) {
            onCreateChallenge(data.data);
            toast({
              title: "Challenge Created!",
              description: `Successfully created challenge: ${name}.`,
            });

            // Reset form
            setName('');
            setType('Walking');
            setDescription('');
            setGoal('');
            setUnit('km');
          } else {
            toast({
              title: "Error Creating Challenge",
              description: data.message || "Failed to create challenge.",
              variant: "destructive",
            });
          }
        } catch (error) {
          console.error('Error creating challenge:', error);
          toast({
            title: "Network Error",
            description: "Failed to connect to server. Please try again.",
            variant: "destructive",
          });
        } finally {
          setIsLoading(false);
        }
      };

      return (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
          <Card>
            <CardHeader>
              <CardTitle>Create New Fitness Challenge</CardTitle>
              <CardDescription>Define the details for a new challenge.</CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="space-y-2">
                  <Label htmlFor="challengeName">Challenge Name</Label>
                  <Input id="challengeName" value={name} onChange={(e) => setName(e.target.value)} placeholder="e.g., 30-Day Walking Challenge" required />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="challengeType">Challenge Type</Label>
                  <select 
                    id="challengeType" 
                    value={type} 
                    onChange={(e) => setType(e.target.value)} 
                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                  >
                    <option value="Walking">Walking</option>
                    <option value="Running">Running</option>
                    <option value="Cycling">Cycling</option>
                    <option value="Steps">Steps Count</option>
                    <option value="Workout">Workout Minutes</option>
                  </select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="challengeDescription">Description</Label>
                  <Input id="challengeDescription" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Briefly describe the challenge" required />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="challengeGoal">Goal</Label>
                    <Input id="challengeGoal" type="number" value={goal} onChange={(e) => setGoal(e.target.value)} placeholder="e.g., 100" required min="1"/>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="challengeUnit">Unit</Label>
                     <select 
                      id="challengeUnit" 
                      value={unit} 
                      onChange={(e) => setUnit(e.target.value)} 
                      className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                    >
                      <option value="km">km</option>
                      <option value="miles">miles</option>
                      <option value="steps">steps</option>
                      <option value="minutes">minutes</option>
                      <option value="hours">hours</option>
                    </select>
                  </div>
                </div>
                <Button
                  type="submit"
                  className="w-full bg-primary text-primary-foreground hover:bg-primary/90"
                  disabled={isLoading}
                >
                  {isLoading ? 'Creating...' : 'Create Challenge'}
                </Button>
              </form>
            </CardContent>
          </Card>
        </motion.div>
      );
    };

    export default CreateChallengeForm;
  