import React, { useState, useEffect } from 'react';
    import CreateChallengeForm from '@/components/CreateChallengeForm.jsx';
    import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card.jsx';
    import { Button } from '@/components/ui/button.jsx';
    import { Trash2, Edit3, Eye } from 'lucide-react';
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
     import { getApiUrl } from '@/config/api.js';

    const AdminPage = () => {
      const [challenges, setChallenges] = useState([]);
      const [isLoading, setIsLoading] = useState(true);
      const { toast } = useToast();

      // Fetch challenges from backend
      const fetchChallenges = async () => {
        try {
          const token = localStorage.getItem('fittrack_token');
          if (!token) {
            setIsLoading(false);
            return;
          }

          const response = await fetch(getApiUrl('mongoChallenges'), {
            headers: {
              'Authorization': `Bearer ${token}`,
            },
          });

          const data = await response.json();
          if (data.success) {
            setChallenges(data.data || []);
          } else {
            console.error('Failed to fetch challenges:', data.message);
          }
        } catch (error) {
          console.error('Error fetching challenges:', error);
        } finally {
          setIsLoading(false);
        }
      };

      useEffect(() => {
        fetchChallenges();
      }, []);

      const handleCreateChallenge = (newChallenge) => {
        setChallenges(prevChallenges => [newChallenge, ...prevChallenges]);
      };

      const handleDeleteChallenge = async (challengeId) => {
        try {
          const token = localStorage.getItem('fittrack_token');
          if (!token) {
            toast({
              title: "Authentication Required",
              description: "Please log in to delete challenges.",
              variant: "destructive",
            });
            return;
          }

          const response = await fetch(getApiUrl('mongoDeleteChallenge')(challengeId), {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${token}`,
            },
          });

          const data = await response.json();
          if (data.success) {
            setChallenges(prevChallenges => prevChallenges.filter(c => c.id !== challengeId));
            toast({
              title: "Challenge Deleted",
              description: "The challenge has been successfully deleted.",
            });
          } else {
            toast({
              title: "Error Deleting Challenge",
              description: data.message || "Failed to delete challenge.",
              variant: "destructive",
            });
          }
        } catch (error) {
          console.error('Error deleting challenge:', error);
          toast({
            title: "Network Error",
            description: "Failed to connect to server. Please try again.",
            variant: "destructive",
          });
        }
      };

      // Placeholder for edit functionality
      const handleEditChallenge = (challengeId) => {
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
          <h1 className="text-4xl font-extrabold mb-8 text-foreground tracking-tight">Admin Dashboard</h1>
          <div className="accent-line mb-8" />
          <div className="grid md:grid-cols-2 gap-8">
            <section>
              <CreateChallengeForm onCreateChallenge={handleCreateChallenge} />
            </section>
            <section>
              <Card className="glass-card premium-shadow border border-border">
                <CardHeader>
                  <CardTitle className="font-bold">Manage Challenges</CardTitle>
                  <div className="accent-line mb-2" />
                  <CardDescription>View, edit, or delete existing challenges.</CardDescription>
                </CardHeader>
                <CardContent>
                  {isLoading ? (
                    <p className="text-muted-foreground text-center py-4">Loading challenges...</p>
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
                          className="flex items-center justify-between p-4 border rounded-lg bg-secondary/20 hover:bg-secondary/40 transition-colors premium-shadow"
                        >
                          <span className="font-semibold text-foreground">{challenge.name}</span>
                          <div className="flex items-center gap-2">
                            <AlertDialog>
                              <AlertDialogTrigger asChild>
                                <Button variant="destructive" size="sm" className="premium-btn">Delete</Button>
                              </AlertDialogTrigger>
                              <AlertDialogContent>
                                <AlertDialogHeader>
                                  <AlertDialogTitle>Delete Challenge</AlertDialogTitle>
                                  <AlertDialogDescription>
                                    Are you sure you want to delete this challenge? This action cannot be undone.
                                  </AlertDialogDescription>
                                </AlertDialogHeader>
                                <AlertDialogFooter>
                                  <AlertDialogCancel>Cancel</AlertDialogCancel>
                                  <AlertDialogAction onClick={() => handleDeleteChallenge(challenge.id)} className="premium-btn">Delete</AlertDialogAction>
                                </AlertDialogFooter>
                              </AlertDialogContent>
                            </AlertDialog>
                            <Button variant="outline" size="sm" className="premium-btn" onClick={() => handleEditChallenge(challenge.id)}>Edit</Button>
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
