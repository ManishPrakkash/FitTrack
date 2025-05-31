import React from 'react';
    import CreateChallengeForm from '@/components/CreateChallengeForm.jsx';
    import { useLocalStorage } from '@/hooks/useLocalStorage.jsx';
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
    } from "@/components/ui/alert-dialog.jsx"; // Assuming alert-dialog is created
     import { useToast } from "@/components/ui/use-toast.jsx";

    const AdminPage = () => {
      const [challenges, setChallenges] = useLocalStorage('challenges', []);
      const { toast } = useToast();

      const handleCreateChallenge = (newChallenge) => {
        setChallenges(prevChallenges => [newChallenge, ...prevChallenges]);
      };

      const handleDeleteChallenge = (challengeId) => {
        setChallenges(prevChallenges => prevChallenges.filter(c => c.id !== challengeId));
         toast({
          title: "Challenge Deleted",
          description: "The challenge has been successfully deleted.",
        });
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
                  {challenges.length === 0 ? (
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
