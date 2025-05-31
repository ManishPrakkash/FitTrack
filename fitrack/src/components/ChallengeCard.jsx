import React from 'react';
    import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card.jsx';
    import { Button } from '@/components/ui/button.jsx';
    import { Progress } from '@/components/ui/progress.jsx';
    import { Zap, Users, Calendar } from 'lucide-react';
    import { motion } from 'framer-motion';

    const ChallengeCard = ({ challenge, onJoin, onLogActivity, isJoined, progress }) => {
      return (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <Card className="overflow-hidden glass-card premium-shadow border border-border hover:shadow-2xl transition-shadow duration-300">
            <CardHeader className="bg-secondary/30 p-4 border-b border-accent/30">
              <CardTitle className="text-xl flex items-center font-bold tracking-tight">
                <Zap className="mr-2 h-5 w-5 text-primary" />
                {challenge.name}
              </CardTitle>
              <CardDescription className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{challenge.type}</CardDescription>
            </CardHeader>
            <CardContent className="p-4 space-y-3">
              <p className="text-sm text-muted-foreground font-medium">{challenge.description}</p>
              <div className="flex items-center text-xs text-muted-foreground">
                <Calendar className="mr-1 h-3 w-3" />
                <span>Goal: {challenge.goal} {challenge.unit}</span>
              </div>
              <div className="flex items-center text-xs text-muted-foreground">
                <Users className="mr-1 h-3 w-3" />
                <span>Participants: {challenge.participants}</span>
              </div>
              {isJoined && (
                <div className="pt-2">
                  <div className="flex justify-between text-xs mb-1 font-semibold">
                    <span>Your Progress</span>
                    <span>{progress}%</span>
                  </div>
                  <Progress value={progress} className="h-2 bg-muted premium-shadow" />
                </div>
              )}
            </CardContent>
            <CardFooter className="p-4 bg-secondary/10 border-t border-accent/30">
              {isJoined ? (
                <Button onClick={() => onLogActivity(challenge.id)} variant="outline" className="w-full premium-btn font-semibold">
                  Log Activity
                </Button>
              ) : (
                <Button onClick={() => onJoin(challenge.id)} className="w-full premium-btn bg-primary text-primary-foreground hover:bg-primary/90 font-semibold">
                  Join Challenge
                </Button>
              )}
            </CardFooter>
          </Card>
        </motion.div>
      );
    };

    export default ChallengeCard;
