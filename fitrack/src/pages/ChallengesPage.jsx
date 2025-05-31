import React, { useState, useEffect } from 'react';
    import ChallengeCard from '@/components/ChallengeCard.jsx';
    import ActivityLogModal from '@/components/ActivityLogModal.jsx';
    import { useLocalStorage } from '@/hooks/useLocalStorage.jsx';
    import { motion, AnimatePresence } from 'framer-motion';
    import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs.jsx";
    import { PlusCircle } from 'lucide-react';
    import { Button } from '@/components/ui/button.jsx';
    import { Link } from 'react-router-dom';

    const initialChallenges = [
      { id: '1', name: 'Morning Mile Run', type: 'Running', description: 'Run 1 mile every morning for 30 days.', goal: 30, unit: 'miles', participants: 120 },
      { id: '2', name: '10k Steps Daily', type: 'Walking', description: 'Achieve 10,000 steps every day for a month.', goal: 300000, unit: 'steps', participants: 250 },
      { id: '3', name: 'Cycle 100km Weekly', type: 'Cycling', description: 'Cycle a total of 100km each week for 4 weeks.', goal: 400, unit: 'km', participants: 75 },
    ];

    const ChallengesPage = () => {
      const [challenges, setChallenges] = useLocalStorage('challenges', initialChallenges);
      const [userProgress, setUserProgress] = useLocalStorage('userProgress', {});
      const [isModalOpen, setIsModalOpen] = useState(false);
      const [selectedChallenge, setSelectedChallenge] = useState(null);

      const handleJoinChallenge = (challengeId) => {
        setUserProgress(prev => ({
          ...prev,
          [challengeId]: { ...(prev[challengeId] || { joined: false, current: 0 }), joined: true }
        }));
      };

      const handleLogActivity = (challengeId, value) => {
        setUserProgress(prev => {
          const currentVal = prev[challengeId]?.current || 0;
          return {
            ...prev,
            [challengeId]: { ...prev[challengeId], current: currentVal + value }
          };
        });
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
                  {challenges.length === 0 ? (
                    <p className="text-muted-foreground col-span-full text-center py-10">No challenges available yet. Admins can create new ones!</p>
                  ) : (
                    challenges.map(challenge => (
                      <ChallengeCard
                        key={challenge.id}
                        challenge={challenge}
                        onJoin={handleJoinChallenge}
                        onLogActivity={openLogModal}
                        isJoined={!!userProgress[challenge.id]?.joined}
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
                    <p className="text-muted-foreground col-span-full text-center py-10">You haven't joined any challenges yet.</p>
                  ) : (
                    joinedChallenges.map(challenge => (
                      <ChallengeCard
                        key={challenge.id}
                        challenge={challenge}
                        onJoin={handleJoinChallenge}
                        onLogActivity={openLogModal}
                        isJoined={!!userProgress[challenge.id]?.joined}
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
                  {availableChallenges.length === 0 ? (
                    <p className="text-muted-foreground col-span-full text-center py-10">No available challenges. Join or create a new one!</p>
                  ) : (
                    availableChallenges.map(challenge => (
                      <ChallengeCard
                        key={challenge.id}
                        challenge={challenge}
                        onJoin={handleJoinChallenge}
                        onLogActivity={openLogModal}
                        isJoined={!!userProgress[challenge.id]?.joined}
                        progress={calculateProgressPercent(challenge.id)}
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
