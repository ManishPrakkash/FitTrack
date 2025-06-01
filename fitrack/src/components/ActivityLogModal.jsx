import React, { useState } from 'react';
    import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter, DialogClose } from '@/components/ui/dialog.jsx';
    import { Button } from '@/components/ui/button.jsx';
    import { Input } from '@/components/ui/input.jsx';
    import { Label } from '@/components/ui/label.jsx';
    import { useToast } from '@/components/ui/use-toast.jsx';
    import { getApiUrl } from '@/config/api.js';

    const ActivityLogModal = ({ challenge, isOpen, setIsOpen, onLog }) => {
      const [activityValue, setActivityValue] = useState('');
      const [notes, setNotes] = useState('');
      const [isLoading, setIsLoading] = useState(false);
      const { toast } = useToast();

      const handleSubmit = async (e) => {
        e.preventDefault();
        if (!activityValue || isNaN(parseFloat(activityValue)) || parseFloat(activityValue) <= 0) {
          toast({
            title: "Invalid Input",
            description: `Please enter a valid positive number for ${challenge?.unit || 'activity'}.`,
            variant: "destructive",
          });
          return;
        }

        setIsLoading(true);

        try {
          const token = localStorage.getItem('fittrack_token');
          if (!token) {
            toast({
              title: "Authentication Required",
              description: "Please log in to log activities.",
              variant: "destructive",
            });
            setIsLoading(false);
            return;
          }

          const response = await fetch(getApiUrl('mongoLogToChallenge')(challenge.id), {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify({
              value: parseFloat(activityValue),
              notes: notes,
            }),
          });

          const data = await response.json();

          if (data.success) {
            toast({
              title: "Activity Logged!",
              description: `Successfully logged ${activityValue} ${challenge?.unit || ''} for ${challenge?.name}.`,
            });

            // Call the parent callback if provided
            if (onLog) {
              onLog(challenge.id, parseFloat(activityValue));
            }

            setActivityValue('');
            setNotes('');
            setIsOpen(false);
          } else {
            toast({
              title: "Error Logging Activity",
              description: data.message || "Failed to log activity.",
              variant: "destructive",
            });
          }
        } catch (error) {
          console.error('Error logging activity:', error);
          toast({
            title: "Network Error",
            description: "Failed to connect to server. Please try again.",
            variant: "destructive",
          });
        } finally {
          setIsLoading(false);
        }
      };

      if (!challenge) return null;

      return (
        <Dialog open={isOpen} onOpenChange={setIsOpen}>
          <DialogContent className="sm:max-w-[425px] glass-card premium-shadow border border-border">
            <DialogHeader>
              <DialogTitle className="font-bold tracking-tight">Log Activity for {challenge.name}</DialogTitle>
              <div className="accent-line mb-2" />
              <DialogDescription className="font-medium">
                Enter your achieved {challenge.unit}. Current goal: {challenge.goal} {challenge.unit}.
              </DialogDescription>
            </DialogHeader>
            <form onSubmit={handleSubmit}>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="activityValue" className="text-right font-semibold">
                    {challenge.unit}
                  </Label>
                  <Input
                    id="activityValue"
                    type="number"
                    value={activityValue}
                    onChange={(e) => setActivityValue(e.target.value)}
                    className="col-span-3 bg-background border border-accent/30 text-foreground placeholder-muted-foreground focus:ring-primary focus:border-primary rounded-md"
                    placeholder={`e.g., ${challenge.unit === 'km' ? '5' : (challenge.unit === 'steps' ? '10000' : '30')}`}
                    required
                    min="0.1"
                    step="any"
                    disabled={isLoading}
                  />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="notes" className="text-right font-semibold">
                    Notes
                  </Label>
                  <Input
                    id="notes"
                    type="text"
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    className="col-span-3 bg-background border border-accent/30 text-foreground placeholder-muted-foreground focus:ring-primary focus:border-primary rounded-md"
                    placeholder="Optional notes about your activity"
                    disabled={isLoading}
                  />
                </div>
              </div>
              <DialogFooter>
                <DialogClose asChild>
                  <Button type="button" variant="outline" className="premium-btn font-semibold" disabled={isLoading}>
                    Cancel
                  </Button>
                </DialogClose>
                <Button
                  type="submit"
                  className="premium-btn bg-primary text-primary-foreground hover:bg-primary/90 font-semibold"
                  disabled={isLoading}
                >
                  {isLoading ? 'Logging...' : 'Log Activity'}
                </Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      );
    };

    export default ActivityLogModal;


