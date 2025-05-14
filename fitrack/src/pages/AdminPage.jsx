
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
          <h1 className="text-4xl font-bold mb-8 text-foreground">Admin Dashboard</h1>
          
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
  