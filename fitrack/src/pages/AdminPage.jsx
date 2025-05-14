
    import React, { useState, useEffect } from 'react';
    import CreateChallengeForm from '@/components/CreateChallengeForm.jsx';
    import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card.jsx';
    import { Button } from '@/components/ui/button.jsx';
    import { Trash2, Edit3, RefreshCw } from 'lucide-react';
    import { motion } from 'framer-motion';
    import {
      AlertDialog,
      AlertDialogAction,
      AlertDialogCancel,
      AlertDialogContent,
      AlertDialogDescription,
      AlertDialogFooter,
      AlertDialogHeader,
      AlertDialogTitle,
      AlertDialogTrigger,
    } from "@/components/ui/alert-dialog.jsx";
    import { useToast } from "@/components/ui/use-toast.jsx";

    const AdminPage = () => {
      const [challenges, setChallenges] = useState([]);
      const [isLoading, setIsLoading] = useState(true);
      const { toast } = useToast();
      const [user, setUser] = useState(null);

      useEffect(() => {
        // Get user data from localStorage
        const userData = localStorage.getItem('fitrack_user');
        if (userData) {
          try {
            const parsedUser = JSON.parse(userData);
            console.log('User data found in AdminPage:', parsedUser);
            setUser(parsedUser);
          } catch (err) {
            console.error('Error parsing user data:', err);
          }
        } else {
          console.log('No user data found in localStorage');
        }

        // Fetch challenges from the backend
        fetchChallenges();
      }, []);

      const fetchChallenges = async () => {
        setIsLoading(true);

        // Use mock data for now
        setTimeout(() => {
          const mockChallenges = [
            {
              id: '1',
              name: 'Morning Mile Run',
              type: 'Running',
              description: 'Run 1 mile every morning for 30 days.',
              goal: 30,
              unit: 'miles',
              created_by: '123456'
            },
            {
              id: '2',
              name: '10k Steps Daily',
              type: 'Walking',
              description: 'Achieve 10,000 steps every day for a month.',
              goal: 300000,
              unit: 'steps',
              created_by: '123456'
            },
            {
              id: '3',
              name: 'Cycle 100km Weekly',
              type: 'Cycling',
              description: 'Cycle a total of 100km each week for 4 weeks.',
              goal: 400,
              unit: 'km',
              created_by: '123456'
            }
          ];

          setChallenges(mockChallenges);
          setIsLoading(false);
        }, 500);

        // The code below is the original implementation
        // Uncomment when the backend is properly set up
        /*
        try {
          const response = await fetch('http://localhost:8000/api/challenges/');
          const data = await response.json();

          if (data.success) {
            setChallenges(data.challenges);
          } else {
            toast({
              title: "Error",
              description: "Failed to load challenges.",
              variant: "destructive"
            });
          }
        } catch (error) {
          console.error("Error fetching challenges:", error);
          toast({
            title: "Connection Error",
            description: "Could not connect to the server.",
            variant: "destructive"
          });
        } finally {
          setIsLoading(false);
        }
        */
      };

      const handleCreateChallenge = async (newChallenge) => {
        if (!user) {
          toast({
            title: "Authentication Required",
            description: "You must be logged in to create challenges.",
            variant: "destructive"
          });
          return;
        }

        // Create a mock challenge with user ID
        const mockChallenge = {
          ...newChallenge,
          id: Date.now().toString(), // Generate a unique ID
          created_by: user.id,
          created_at: new Date().toISOString()
        };

        // Add the new challenge to the state
        setChallenges(prevChallenges => [mockChallenge, ...prevChallenges]);

        toast({
          title: "Challenge Created!",
          description: `Successfully created challenge: ${newChallenge.name}.`
        });

        // The code below is the original implementation
        // Uncomment when the backend is properly set up
        /*
        try {
          // Add the user ID to the challenge
          const challengeWithUser = {
            ...newChallenge,
            created_by: user.id
          };

          const response = await fetch('http://localhost:8000/api/challenges/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(challengeWithUser)
          });

          const data = await response.json();

          if (data.success) {
            // Add the new challenge to the state
            setChallenges(prevChallenges => [data.challenge, ...prevChallenges]);
            toast({
              title: "Challenge Created!",
              description: `Successfully created challenge: ${newChallenge.name}.`
            });
          } else {
            toast({
              title: "Error",
              description: data.error?.message || "Failed to create challenge.",
              variant: "destructive"
            });
          }
        } catch (error) {
          console.error("Error creating challenge:", error);
          toast({
            title: "Connection Error",
            description: "Could not connect to the server.",
            variant: "destructive"
          });
        }
        */
      };

      const handleDeleteChallenge = async (challengeId) => {
        // Simply remove the challenge from the state
        setChallenges(prevChallenges => prevChallenges.filter(c => c.id !== challengeId));

        toast({
          title: "Challenge Deleted",
          description: "The challenge has been successfully deleted."
        });

        // The code below is the original implementation
        // Uncomment when the backend is properly set up
        /*
        try {
          const response = await fetch(`http://localhost:8000/api/challenges/${challengeId}/`, {
            method: 'DELETE'
          });

          const data = await response.json();

          if (data.success) {
            // Remove the challenge from the state
            setChallenges(prevChallenges => prevChallenges.filter(c => c.id !== challengeId));
            toast({
              title: "Challenge Deleted",
              description: "The challenge has been successfully deleted."
            });
          } else {
            toast({
              title: "Error",
              description: data.error?.message || "Failed to delete challenge.",
              variant: "destructive"
            });
          }
        } catch (error) {
          console.error("Error deleting challenge:", error);
          toast({
            title: "Connection Error",
            description: "Could not connect to the server.",
            variant: "destructive"
          });
        }
        */
      };

      // Placeholder for edit functionality
      const handleEditChallenge = (/* challengeId */) => {
        toast({
          title: "Edit Not Implemented",
          description: "Challenge editing functionality is planned for a future update.",
          variant: "default"
        });
      };


      return (
        <motion.div
          className="container mx-auto py-8 px-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h1 className="text-4xl font-bold mb-8 text-foreground">Admin Dashboard</h1>

          <div className="flex justify-end mb-4">
            <Button
              variant="outline"
              size="sm"
              onClick={fetchChallenges}
              className="flex items-center"
            >
              <RefreshCw className="h-4 w-4 mr-2" />
              Refresh Challenges
            </Button>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            <section>
              <CreateChallengeForm onCreateChallenge={handleCreateChallenge} />
            </section>

            <section>
              <Card>
                <CardHeader>
                  <CardTitle>Manage Challenges</CardTitle>
                  <CardDescription>View, edit, or delete existing challenges.</CardDescription>
                </CardHeader>
                <CardContent>
                  {isLoading ? (
                    <div className="flex justify-center py-8">
                      <RefreshCw className="h-8 w-8 animate-spin text-primary" />
                    </div>
                  ) : challenges.length === 0 ? (
                    <p className="text-muted-foreground text-center py-4">No challenges created yet.</p>
                  ) : (
                    <ul className="space-y-4">
                      {challenges.map(challenge => (
                        <motion.li
                          key={challenge.id}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ duration: 0.3 }}
                          className="flex items-center justify-between p-4 border rounded-lg bg-secondary/20 hover:bg-secondary/40 transition-colors"
                        >
                          <div>
                            <h3 className="font-semibold text-foreground">{challenge.name}</h3>
                            <p className="text-sm text-muted-foreground">{challenge.type} - {challenge.goal} {challenge.unit}</p>
                          </div>
                          <div className="flex space-x-2">
                             <Button variant="ghost" size="icon" onClick={() => handleEditChallenge(challenge.id)} title="Edit Challenge (Not Implemented)">
                              <Edit3 className="h-4 w-4" />
                            </Button>
                            <AlertDialog>
                              <AlertDialogTrigger asChild>
                                <Button variant="ghost" size="icon" className="text-destructive hover:text-destructive hover:bg-destructive/10" title="Delete Challenge">
                                  <Trash2 className="h-4 w-4" />
                                </Button>
                              </AlertDialogTrigger>
                              <AlertDialogContent>
                                <AlertDialogHeader>
                                  <AlertDialogTitle>Are you sure?</AlertDialogTitle>
                                  <AlertDialogDescription>
                                    This action cannot be undone. This will permanently delete the challenge
                                    "{challenge.name}".
                                  </AlertDialogDescription>
                                </AlertDialogHeader>
                                <AlertDialogFooter>
                                  <AlertDialogCancel>Cancel</AlertDialogCancel>
                                  <AlertDialogAction onClick={() => handleDeleteChallenge(challenge.id)} className="bg-destructive text-destructive-foreground hover:bg-destructive/90">
                                    Delete
                                  </AlertDialogAction>
                                </AlertDialogFooter>
                              </AlertDialogContent>
                            </AlertDialog>
                          </div>
                        </motion.li>
                      ))}
                    </ul>
                  )}
                </CardContent>
              </Card>
            </section>
          </div>
        </motion.div>
      );
    };

    export default AdminPage;
