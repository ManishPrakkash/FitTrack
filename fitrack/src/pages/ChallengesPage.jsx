
    import React, { useState, useEffect } from 'react';
    import ChallengeCard from '@/components/ChallengeCard.jsx';
    import ActivityLogModal from '@/components/ActivityLogModal.jsx';
    import { motion, AnimatePresence } from 'framer-motion';
    import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs.jsx";
    import { PlusCircle, RefreshCw } from 'lucide-react';
    import { Button } from '@/components/ui/button.jsx';
    import { Link } from 'react-router-dom';
    import { useToast } from '@/components/ui/use-toast.jsx';

    const ChallengesPage = () => {
      const [challenges, setChallenges] = useState([]);
      const [userProgress, setUserProgress] = useState({});
      const [isModalOpen, setIsModalOpen] = useState(false);
      const [selectedChallenge, setSelectedChallenge] = useState(null);
      const [isLoading, setIsLoading] = useState(true);
      const [user, setUser] = useState(null);
      const { toast } = useToast();

      useEffect(() => {
        // Get user data from localStorage
        const userData = localStorage.getItem('fittrack_user');
        if (userData) {
          setUser(JSON.parse(userData));
        }

        // Fetch challenges and user progress
        fetchChallenges();
      }, []);

      const fetchChallenges = async () => {
        setIsLoading(true);
        try {
          // Fetch all challenges
          const response = await fetch('http://localhost:8000/api/challenges/');
          const data = await response.json();

          if (data.success) {
            setChallenges(data.challenges);

            // If user is logged in, fetch their progress
            if (user) {
              fetchUserProgress(user.id);
            }
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
      };

      const fetchUserProgress = async (userId) => {
        try {
          const response = await fetch(`http://localhost:8000/api/progress/${userId}/`);
          const data = await response.json();

          if (data.success) {
            // Convert array of progress objects to a map for easier access
            const progressMap = {};
            data.progress.forEach(item => {
              progressMap[item.challenge_id] = {
                joined: true,
                current: item.current_value
              };
            });
            setUserProgress(progressMap);
          }
        } catch (error) {
          console.error("Error fetching user progress:", error);
        }
      };

      const handleJoinChallenge = async (challengeId) => {
        if (!user) {
          toast({
            title: "Authentication Required",
            description: "You must be logged in to join challenges.",
            variant: "destructive"
          });
          return;
        }

        try {
          // Create progress entry with 0 value
          const progressData = {
            user_id: user.id,
            challenge_id: challengeId,
            current_value: 0
          };

          const response = await fetch('http://localhost:8000/api/progress/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(progressData)
          });

          const data = await response.json();

          if (data.success) {
            // Update local state
            setUserProgress(prev => ({
              ...prev,
              [challengeId]: { joined: true, current: 0 }
            }));

            toast({
              title: "Challenge Joined",
              description: "You've successfully joined this challenge!"
            });
          } else {
            toast({
              title: "Error",
              description: data.error?.message || "Failed to join challenge.",
              variant: "destructive"
            });
          }
        } catch (error) {
          console.error("Error joining challenge:", error);
          toast({
            title: "Connection Error",
            description: "Could not connect to the server.",
            variant: "destructive"
          });
        }
      };

      const handleLogActivity = async (challengeId, value) => {
        if (!user) {
          toast({
            title: "Authentication Required",
            description: "You must be logged in to log activity.",
            variant: "destructive"
          });
          return;
        }

        try {
          // Get current progress
          const currentVal = userProgress[challengeId]?.current || 0;
          const newValue = currentVal + value;

          // Update progress in the backend
          const progressData = {
            user_id: user.id,
            challenge_id: challengeId,
            current_value: newValue
          };

          const response = await fetch('http://localhost:8000/api/progress/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(progressData)
          });

          const data = await response.json();

          if (data.success) {
            // Update local state
            setUserProgress(prev => ({
              ...prev,
              [challengeId]: { ...prev[challengeId], current: newValue }
            }));

            toast({
              title: "Activity Logged",
              description: `You've logged ${value} ${challenges.find(c => c.id === challengeId)?.unit}!`
            });
          } else {
            toast({
              title: "Error",
              description: data.error?.message || "Failed to log activity.",
              variant: "destructive"
            });
          }
        } catch (error) {
          console.error("Error logging activity:", error);
          toast({
            title: "Connection Error",
            description: "Could not connect to the server.",
            variant: "destructive"
          });
        }
      };

      const openLogModal = (challengeId) => {
        setSelectedChallenge(challenges.find(c => c.id === challengeId));
        setIsModalOpen(true);
      };

      const calculateProgressPercent = (challengeId) => {
        const challenge = challenges.find(c => c.id === challengeId);
        if (!challenge || !userProgress[challengeId] || !userProgress[challengeId].joined) return 0;
        const progress = (userProgress[challengeId].current / challenge.goal) * 100;
        return Math.min(Math.round(progress), 100);
      };

      const joinedChallenges = challenges.filter(c => userProgress[c.id]?.joined);
      const availableChallenges = challenges.filter(c => !userProgress[c.id]?.joined);

      return (
        <motion.div
          className="container mx-auto py-8 px-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-4xl font-bold text-foreground">Fitness Challenges</h1>
            <div className="flex space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={fetchChallenges}
                className="flex items-center"
              >
                <RefreshCw className="h-4 w-4 mr-2" />
                Refresh
              </Button>
              <Link to="/admin">
                <Button variant="outline">
                  <PlusCircle className="mr-2 h-4 w-4" /> Create Challenge
                </Button>
              </Link>
            </div>
          </div>

          <Tabs defaultValue="all" className="w-full">
            <TabsList className="grid w-full grid-cols-2 md:grid-cols-3 mb-6">
              <TabsTrigger value="all">All Challenges</TabsTrigger>
              <TabsTrigger value="joined">My Challenges</TabsTrigger>
              <TabsTrigger value="available">Available</TabsTrigger>
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
                    <div className="flex justify-center py-8 col-span-full">
                      <RefreshCw className="h-8 w-8 animate-spin text-primary" />
                    </div>
                  ) : challenges.length === 0 ? (
                     <p className="text-muted-foreground col-span-full text-center py-10">No challenges available yet. Admins can create new ones!</p>
                  ) : (
                    challenges.map(challenge => (
                      <ChallengeCard
                        key={challenge.id}
                        challenge={challenge}
                        onJoin={handleJoinChallenge}
                        onLogActivity={openLogModal}
                        isJoined={userProgress[challenge.id]?.joined || false}
                        progress={calculateProgressPercent(challenge.id)}
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
                    <p className="text-muted-foreground col-span-full text-center py-10">You haven't joined any challenges yet. Explore available challenges!</p>
                  ) : (
                    joinedChallenges.map(challenge => (
                      <ChallengeCard
                        key={challenge.id}
                        challenge={challenge}
                        onJoin={handleJoinChallenge}
                        onLogActivity={openLogModal}
                        isJoined={true}
                        progress={calculateProgressPercent(challenge.id)}
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
                   {availableChallenges.length === 0 && challenges.length > 0 ? (
                    <p className="text-muted-foreground col-span-full text-center py-10">You've joined all available challenges! Great job!</p>
                  ) : availableChallenges.length === 0 && challenges.length === 0 ? (
                     <p className="text-muted-foreground col-span-full text-center py-10">No challenges available to join at the moment.</p>
                  ) : (
                    availableChallenges.map(challenge => (
                      <ChallengeCard
                        key={challenge.id}
                        challenge={challenge}
                        onJoin={handleJoinChallenge}
                        onLogActivity={openLogModal}
                        isJoined={false}
                        progress={calculateProgressPercent(challenge.id)}
                      />
                    ))
                  )}
                </motion.div>
              </TabsContent>
            </AnimatePresence>
          </Tabs>

          {selectedChallenge && (
            <ActivityLogModal
              challenge={selectedChallenge}
              isOpen={isModalOpen}
              setIsOpen={setIsModalOpen}
              onLog={handleLogActivity}
            />
          )}
        </motion.div>
      );
    };

    export default ChallengesPage;
