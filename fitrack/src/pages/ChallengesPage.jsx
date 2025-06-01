import React, { useState, useEffect } from 'react';
    import ChallengeCard from '@/components/ChallengeCard.jsx';
    import ActivityLogModal from '@/components/ActivityLogModal.jsx';
    import { motion, AnimatePresence } from 'framer-motion';
    import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs.jsx";
    import { PlusCircle } from 'lucide-react';
    import { Button } from '@/components/ui/button.jsx';
    import { Link } from 'react-router-dom';
    import { getApiUrl } from '@/config/api.js';
    import { useToast } from '@/components/ui/use-toast.jsx';

    const ChallengesPage = () => {
      const [challenges, setChallenges] = useState([]);
      const [isLoading, setIsLoading] = useState(true);
      const [isModalOpen, setIsModalOpen] = useState(false);
      const [selectedChallenge, setSelectedChallenge] = useState(null);
      const { toast } = useToast();

      // Fetch challenges from backend
      const fetchChallenges = async (type = 'all') => {
        try {
          const token = localStorage.getItem('fittrack_token');
          if (!token) {
            setIsLoading(false);
            return;
          }

          const url = type === 'all'
            ? getApiUrl('mongoChallenges')
            : `${getApiUrl('mongoChallenges')}?type=${type}`;

          const response = await fetch(url, {
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

      const handleJoinChallenge = async (challengeId) => {
        try {
          const token = localStorage.getItem('fittrack_token');
          if (!token) {
            toast({
              title: "Authentication Required",
              description: "Please log in to join challenges.",
              variant: "destructive",
            });
            return;
          }

          const response = await fetch(getApiUrl('mongoJoinChallenge')(challengeId), {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${token}`,
            },
          });

          const data = await response.json();
          if (data.success) {
            toast({
              title: "Challenge Joined!",
              description: "You have successfully joined the challenge.",
            });
            // Refresh challenges to update join status
            fetchChallenges();
          } else {
            toast({
              title: "Error Joining Challenge",
              description: data.message || "Failed to join challenge.",
              variant: "destructive",
            });
          }
        } catch (error) {
          console.error('Error joining challenge:', error);
          toast({
            title: "Network Error",
            description: "Failed to connect to server. Please try again.",
            variant: "destructive",
          });
        }
      };

      const handleLogActivity = (challengeId, value) => {
        // Refresh challenges to update progress after logging activity
        fetchChallenges();
      };

      const openLogModal = (challengeId) => {
        setSelectedChallenge(challenges.find(c => c.id === challengeId));
        setIsModalOpen(true);
      };

      // Filter challenges based on join status
      const joinedChallenges = challenges.filter(c => c.is_joined);
      const availableChallenges = challenges.filter(c => !c.is_joined);

      return (
        <motion.div 
          className="container mx-auto py-8 px-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-4xl font-extrabold text-foreground tracking-tight">Fitness Challenges</h1>
            <Link to="/admin">
              <Button variant="outline" className="premium-btn font-semibold">
                <PlusCircle className="mr-2 h-4 w-4" /> Create Challenge
              </Button>
            </Link>
          </div>
          <div className="accent-line mb-6" />
          <Tabs defaultValue="all" className="w-full">
            <TabsList className="grid w-full grid-cols-2 md:grid-cols-3 mb-6 bg-background border border-accent/30 rounded-lg">
              <TabsTrigger value="all" className="font-semibold">All Challenges</TabsTrigger>
              <TabsTrigger value="joined" className="font-semibold">My Challenges</TabsTrigger>
              <TabsTrigger value="available" className="font-semibold">Available</TabsTrigger>
            </TabsList>
            <AnimatePresence mode="wait">
              <TabsContent value="all">
                <motion.div
                  key="all"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.3 }}
                  className="grid md:grid-cols-2 lg:grid-cols-3 gap-6"
                >
                  {isLoading ? (
                    <p className="text-muted-foreground col-span-full text-center py-10">Loading challenges...</p>
                  ) : challenges.length === 0 ? (
                    <p className="text-muted-foreground col-span-full text-center py-10">No challenges available yet. Admins can create new ones!</p>
                  ) : (
                    challenges.map(challenge => (
                      <ChallengeCard
                        key={challenge.id}
                        challenge={challenge}
                        onJoin={handleJoinChallenge}
                        onLogActivity={openLogModal}
                        isJoined={challenge.is_joined || false}
                        progress={challenge.progress_percentage || 0}
                      />
                    ))
                  )}
                </motion.div>
              </TabsContent>
              <TabsContent value="joined">
                <motion.div
                  key="joined"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.3 }}
                  className="grid md:grid-cols-2 lg:grid-cols-3 gap-6"
                >
                  {joinedChallenges.length === 0 ? (
                    <p className="text-muted-foreground col-span-full text-center py-10">You haven't joined any challenges yet.</p>
                  ) : (
                    joinedChallenges.map(challenge => (
                      <ChallengeCard
                        key={challenge.id}
                        challenge={challenge}
                        onJoin={handleJoinChallenge}
                        onLogActivity={openLogModal}
                        isJoined={challenge.is_joined || false}
                        progress={challenge.progress_percentage || 0}
                      />
                    ))
                  )}
                </motion.div>
              </TabsContent>
              <TabsContent value="available">
                <motion.div
                  key="available"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.3 }}
                  className="grid md:grid-cols-2 lg:grid-cols-3 gap-6"
                >
                  {availableChallenges.length === 0 ? (
                    <p className="text-muted-foreground col-span-full text-center py-10">No available challenges. Join or create a new one!</p>
                  ) : (
                    availableChallenges.map(challenge => (
                      <ChallengeCard
                        key={challenge.id}
                        challenge={challenge}
                        onJoin={handleJoinChallenge}
                        onLogActivity={openLogModal}
                        isJoined={challenge.is_joined || false}
                        progress={challenge.progress_percentage || 0}
                      />
                    ))
                  )}
                </motion.div>
              </TabsContent>
            </AnimatePresence>
          </Tabs>
          <ActivityLogModal
            challenge={selectedChallenge}
            isOpen={isModalOpen}
            setIsOpen={setIsModalOpen}
            onLog={handleLogActivity}
          />
        </motion.div>
      );
    };

    export default ChallengesPage;
