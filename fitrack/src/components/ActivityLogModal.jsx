import React, { useState } from 'react';
    import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter, DialogClose } from '@/components/ui/dialog.jsx';
    import { Button } from '@/components/ui/button.jsx';
    import { Input } from '@/components/ui/input.jsx';
    import { Label } from '@/components/ui/label.jsx';
    import { useToast } from '@/components/ui/use-toast.jsx';

    const ActivityLogModal = ({ challenge, isOpen, setIsOpen, onLog }) => {
      const [activityValue, setActivityValue] = useState('');
      const { toast } = useToast();

      const handleSubmit = (e) => {
        e.preventDefault();
        if (!activityValue || isNaN(parseFloat(activityValue)) || parseFloat(activityValue) <= 0) {
          toast({
            title: "Invalid Input",
            description: `Please enter a valid positive number for ${challenge?.unit || 'activity'}.`,
            variant: "destructive",
          });
          return;
        }
        onLog(challenge.id, parseFloat(activityValue));
        toast({
          title: "Activity Logged!",
          description: `Successfully logged ${activityValue} ${challenge?.unit || ''} for ${challenge?.name}.`,
        });
        setActivityValue('');
        setIsOpen(false);
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
                  />
                </div>
              </div>
              <DialogFooter>
                <DialogClose asChild>
                  <Button type="button" variant="outline" className="premium-btn font-semibold">Cancel</Button>
                </DialogClose>
                <Button type="submit" className="premium-btn bg-primary text-primary-foreground hover:bg-primary/90 font-semibold">Log Activity</Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      );
    };

    export default ActivityLogModal;


