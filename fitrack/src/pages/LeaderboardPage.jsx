
    import React, { useState, useEffect } from 'react';
    import { Link } from 'react-router-dom';
    import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow, TableCaption } from "@/components/ui/table.jsx";
    import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar.jsx";
    import { Card } from "@/components/ui/card.jsx";
    import { Trophy, TrendingUp, Share2, RefreshCw } from 'lucide-react';
    import { Button } from '@/components/ui/button.jsx';
    import { motion } from 'framer-motion';
    import { useToast } from "@/components/ui/use-toast.jsx";
    import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select.jsx";

    const LeaderboardPage = () => {
      const [challenges, setChallenges] = useState([]);
      const [selectedChallengeId, setSelectedChallengeId] = useState('');
      const [leaderboardData, setLeaderboardData] = useState([]);
      const [isLoading, setIsLoading] = useState(true);
      const [isLeaderboardLoading, setIsLeaderboardLoading] = useState(false);
      const { toast } = useToast();

      useEffect(() => {
        // Fetch challenges when component mounts
        fetchChallenges();
      }, []);

      useEffect(() => {
        // Set the first challenge as selected when challenges are loaded
        if (challenges.length > 0 && !selectedChallengeId) {
          setSelectedChallengeId(challenges[0].id);
        }
      }, [challenges, selectedChallengeId]);

      useEffect(() => {
        // Fetch leaderboard data when a challenge is selected
        if (selectedChallengeId) {
          fetchLeaderboard(selectedChallengeId);
        }
      }, [selectedChallengeId]);

      const fetchChallenges = async () => {
        setIsLoading(true);
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
      };

      const fetchLeaderboard = async (challengeId) => {
        setIsLeaderboardLoading(true);
        try {
          const response = await fetch(`http://localhost:8000/api/leaderboard/${challengeId}/`);
          const data = await response.json();

          if (data.success) {
            setLeaderboardData(data.leaderboard);
          } else {
            toast({
              title: "Error",
              description: "Failed to load leaderboard data.",
              variant: "destructive"
            });
            setLeaderboardData([]);
          }
        } catch (error) {
          console.error("Error fetching leaderboard:", error);
          toast({
            title: "Connection Error",
            description: "Could not connect to the server.",
            variant: "destructive"
          });
          setLeaderboardData([]);
        } finally {
          setIsLeaderboardLoading(false);
        }
      };

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
            <h1 className="text-4xl font-bold text-foreground flex items-center">
              <Trophy className="mr-3 h-10 w-10 text-primary" />
              Leaderboard
            </h1>
            <div className="flex space-x-2 items-center">
              <Button
                variant="outline"
                size="sm"
                onClick={fetchChallenges}
                className="flex items-center"
              >
                <RefreshCw className="h-4 w-4 mr-2" />
                Refresh
              </Button>
              {challenges.length > 0 && (
                <div className="w-full sm:w-auto min-w-[200px]">
                  <Select onValueChange={setSelectedChallengeId} value={selectedChallengeId}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select a challenge" />
                    </SelectTrigger>
                    <SelectContent>
                      {challenges.map(challenge => (
                        <SelectItem key={challenge.id} value={challenge.id}>
                          {challenge.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              )}
            </div>
          </div>

          {isLoading ? (
            <div className="flex justify-center py-20">
              <RefreshCw className="h-12 w-12 animate-spin text-primary" />
            </div>
          ) : leaderboardData.length > 0 ? (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }}>
              <Card className="overflow-hidden border border-border">
                <Table>
                  <TableCaption>
                    Leaderboard for: {challenges.find(c => c.id === selectedChallengeId)?.name || 'Selected Challenge'}.
                    <Button variant="link" size="sm" onClick={handleShare} className="ml-2 text-primary">
                      <Share2 className="mr-1 h-4 w-4" /> Share
                    </Button>
                  </TableCaption>
                  <TableHeader>
                    <TableRow>
                      <TableHead className="w-[80px]">Rank</TableHead>
                      <TableHead>Participant</TableHead>
                      <TableHead className="text-right">Score</TableHead>
                      <TableHead className="text-right w-[100px]">Progress</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {isLeaderboardLoading ? (
                      <TableRow>
                        <TableCell colSpan={4} className="text-center py-8">
                          <RefreshCw className="h-8 w-8 animate-spin text-primary mx-auto" />
                        </TableCell>
                      </TableRow>
                    ) : (
                      leaderboardData.map((user, index) => (
                        <TableRow key={user.user_id} className={index < 3 ? 'bg-secondary/30' : ''}>
                          <TableCell className="font-medium text-lg">
                            {index === 0 && <Trophy className="inline-block h-5 w-5 text-yellow-400" />}
                            {index === 1 && <Trophy className="inline-block h-5 w-5 text-gray-400" />}
                            {index === 2 && <Trophy className="inline-block h-5 w-5 text-yellow-600" />}
                            {index >= 3 && ''}
                            <span className="ml-2">{index + 1}</span>
                          </TableCell>
                          <TableCell>
                            <div className="flex items-center">
                              <Avatar className="h-9 w-9 mr-3">
                                <AvatarImage src={`https://avatar.vercel.sh/${user.name}.png?size=40`} alt={user.name} />
                                <AvatarFallback>{user.avatar_text}</AvatarFallback>
                              </Avatar>
                              <span className="font-medium">{user.name}</span>
                            </div>
                          </TableCell>
                          <TableCell className="text-right font-semibold">{user.score} {user.unit}</TableCell>
                          <TableCell className="text-right">
                            <TrendingUp className="inline-block h-5 w-5 text-green-500" />
                          </TableCell>
                        </TableRow>
                      ))
                    )}
                  </TableBody>
                </Table>
              </Card>
            </motion.div>
          ) : (
            <div className="text-center py-10 text-muted-foreground">
              <p>{challenges.length === 0 ? "No challenges available to display a leaderboard." : "Select a challenge to view its leaderboard or no participants yet."}</p>
               {challenges.length === 0 &&
                <Link to="/admin">
                  <Button variant="link" className="mt-2">Create a challenge</Button>
                </Link>
              }
            </div>
          )}
        </motion.div>
      );
    };

    export default LeaderboardPage;
