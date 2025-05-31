import React, { useState, useEffect } from 'react';
    import { Link } from 'react-router-dom';
    import { useLocalStorage } from '@/hooks/useLocalStorage.jsx';
    import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow, TableCaption } from "@/components/ui/table.jsx";
    import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar.jsx";
    import { Card } from "@/components/ui/card.jsx";
    import { Trophy, TrendingUp, Share2 } from 'lucide-react';
    import { Button } from '@/components/ui/button.jsx';
    import { motion } from 'framer-motion';
    import { useToast } from "@/components/ui/use-toast.jsx";
    import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select.jsx";
    import { Progress } from '@/components/ui/progress.jsx';

    const mockUsers = [
      { id: 'user1', name: 'Alex P.', avatarText: 'AP' },
      { id: 'user2', name: 'Jamie L.', avatarText: 'JL' },
      { id: 'user3', name: 'Casey B.', avatarText: 'CB' },
      { id: 'user4', name: 'Morgan K.', avatarText: 'MK' },
      { id: 'user5', name: 'Taylor S.', avatarText: 'TS' },
    ];

    const LeaderboardPage = () => {
      const [challenges] = useLocalStorage('challenges', []);
      const [userProgressData] = useLocalStorage('userProgress', {});
      const [selectedChallengeId, setSelectedChallengeId] = useState('');
      const [leaderboardData, setLeaderboardData] = useState([]);
      const { toast } = useToast();

      useEffect(() => {
        if (challenges.length > 0 && !selectedChallengeId) {
          setSelectedChallengeId(challenges[0].id);
        }
      }, [challenges, selectedChallengeId]);

      useEffect(() => {
        if (!selectedChallengeId || !challenges.length) {
          setLeaderboardData([]);
          return;
        }

        const currentChallenge = challenges.find(c => c.id === selectedChallengeId);
        if (!currentChallenge) {
          setLeaderboardData([]);
          return;
        }
        
        const data = mockUsers.map(user => {
          const userChallengeProgress = userProgressData[selectedChallengeId];
          let progress = 0;
          if (user.id === 'currentUserPlaceholder' && userChallengeProgress) { 
             progress = (userChallengeProgress.current / currentChallenge.goal) * 100;
          } else {
            const randomFactor = Math.random();
            if (randomFactor < 0.2) progress = 0; 
            else if (randomFactor < 0.8) progress = Math.random() * currentChallenge.goal * 0.8; 
            else progress = currentChallenge.goal * (0.8 + Math.random() * 0.25) ; 
          }

          return {
            ...user,
            score: parseFloat(progress.toFixed(1)),
            unit: currentChallenge.unit,
          };
        }).sort((a, b) => b.score - a.score);

        setLeaderboardData(data);

      }, [selectedChallengeId, userProgressData, challenges]);
      
      const handleShare = () => {
        const challengeName = challenges.find(c => c.id === selectedChallengeId)?.name || "Fitness Challenge";
        const text = `Checking out the leaderboard for ${challengeName} on FitTrack! Come join the fun!`;
        if (navigator.share) {
          navigator.share({
            title: 'FitTrack Leaderboard',
            text: text,
            url: window.location.href,
          }).catch(console.error);
        } else {
          navigator.clipboard.writeText(`${text} ${window.location.href}`);
          toast({
            title: "Link Copied!",
            description: "Leaderboard link copied to clipboard. Share it with your friends!",
          });
        }
      };
      
      return (
        <motion.div 
          className="container mx-auto py-8 px-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="flex flex-col sm:flex-row justify-between items-center mb-8 gap-4">
            <h1 className="text-4xl font-extrabold text-foreground flex items-center tracking-tight">
              <Trophy className="mr-3 h-10 w-10 text-primary" />
              Leaderboard
            </h1>
            <div className="accent-line sm:mb-0 mb-4" />
            {challenges.length > 0 && (
              <div className="w-full sm:w-auto min-w-[200px]">
                <Select onValueChange={setSelectedChallengeId} value={selectedChallengeId}>
                  <SelectTrigger className="bg-background border border-accent/30 text-foreground font-semibold">
                    <SelectValue placeholder="Select a challenge" />
                  </SelectTrigger>
                  <SelectContent>
                    {challenges.map(challenge => (
                      <SelectItem key={challenge.id} value={challenge.id} className="font-semibold">
                        {challenge.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            )}
          </div>
          {leaderboardData.length > 0 ? (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }}>
              <Card className="overflow-hidden border border-border glass-card premium-shadow">
                <Table>
                  <TableCaption>
                    <span className="font-semibold">Leaderboard for: {challenges.find(c => c.id === selectedChallengeId)?.name || 'Selected Challenge'}.</span>
                    <Button variant="link" size="sm" onClick={handleShare} className="ml-2 text-primary premium-btn">
                      <Share2 className="mr-1 h-4 w-4" /> Share
                    </Button>
                  </TableCaption>
                  <TableHeader>
                    <TableRow>
                      <TableHead className="w-[80px] font-bold">Rank</TableHead>
                      <TableHead className="font-bold">Participant</TableHead>
                      <TableHead className="text-right font-bold">Score</TableHead>
                      <TableHead className="text-right w-[100px] font-bold">Progress</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {leaderboardData.map((user, index) => (
                      <TableRow key={user.id} className={index < 3 ? 'bg-secondary/30' : ''}>
                        <TableCell className="font-medium text-lg">
                          {index === 0 && <Trophy className="inline-block h-5 w-5 text-yellow-400" />}
                          {index === 1 && <Trophy className="inline-block h-5 w-5 text-gray-400" />}
                          {index === 2 && <Trophy className="inline-block h-5 w-5 text-yellow-600" />}
                          {index >= 3 && ''}
                          <span className="ml-2">{index + 1}</span>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center">
                            <Avatar className="h-9 w-9 mr-3 premium-shadow">
                              <AvatarImage src={`https://avatar.vercel.sh/${user.name}.png?size=40`} alt={user.name} />
                              <AvatarFallback>{user.avatarText}</AvatarFallback>
                            </Avatar>
                            <span className="font-medium">{user.name}</span>
                          </div>
                        </TableCell>
                        <TableCell className="text-right font-semibold">{user.score} {user.unit}</TableCell>
                        <TableCell className="text-right">
                          <div className="w-full flex items-center gap-2">
                            <Progress value={user.score} className="h-2 bg-muted premium-shadow" />
                            <span className="text-xs font-semibold">{Math.round(user.score)}%</span>
                            {index === 0 && <TrendingUp className="inline-block h-5 w-5 text-green-500" />}
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </Card>
            </motion.div>
          ) : (
            <div className="text-center py-10 text-muted-foreground">
              <p>{challenges.length === 0 ? "No challenges available to display a leaderboard." : "Select a challenge to view its leaderboard or no participants yet."}</p>
              {challenges.length === 0 && 
                <Link to="/admin">
                  <Button variant="link" className="mt-2 premium-btn">Create a challenge</Button>
                </Link>
              }
            </div>
          )}
        </motion.div>
      );
    };

    export default LeaderboardPage;
