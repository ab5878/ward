import React, { useState } from 'react';
import { Button } from './ui/button';
import {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from './ui/dialog';
import { Textarea } from './ui/textarea';
import { toast } from 'sonner';

const STATE_FLOW = {
  REPORTED: 'CLARIFIED',
  CLARIFIED: 'DECISION_REQUIRED',
  DECISION_REQUIRED: 'DECIDED',
  DECIDED: 'IN_PROGRESS',
  IN_PROGRESS: 'RESOLVED',
  RESOLVED: null,
};

export const StateTransitionBar = ({ currentState, canAdvance, onAdvance }) => {
  const [reason, setReason] = useState('');
  const [open, setOpen] = useState(false);
  
  const nextState = STATE_FLOW[currentState];

  if (!canAdvance) {
    return (
      <div
        className="text-sm text-muted-foreground p-3 bg-muted/30 rounded-md border border-border"
        data-testid="transition-guard"
      >
        Only the decision owner can advance the state.
      </div>
    );
  }

  if (!nextState) {
    return (
      <div
        className="text-sm text-muted-foreground p-3 bg-success/10 rounded-md border border-success/20"
        data-testid="transition-resolved"
      >
        This disruption is resolved. No further state transitions available.
      </div>
    );
  }

  const handleConfirm = async () => {
    try {
      await onAdvance(nextState, reason || undefined);
      toast.success(`State advanced to ${nextState.replace('_', ' ')}`);
      setOpen(false);
      setReason('');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to advance state');
    }
  };

  return (
    <div className="space-y-2" data-testid="transition-actions">
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogTrigger asChild>
          <Button
            data-testid={`advance-to-${nextState}-button`}
            className="w-full font-medium"
            size="lg"
          >
            Advance to {nextState.replace('_', ' ')}
          </Button>
        </DialogTrigger>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Confirm State Transition</DialogTitle>
            <DialogDescription>
              Move from <strong>{currentState.replace('_', ' ')}</strong> to{' '}
              <strong>{nextState.replace('_', ' ')}</strong>?
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-3">
            <div>
              <label className="text-sm font-medium mb-1 block">
                Reason (optional)
              </label>
              <Textarea
                value={reason}
                onChange={(e) => setReason(e.target.value)}
                rows={3}
                placeholder="Why are you advancing this disruption?"
                data-testid="transition-reason-input"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button
              data-testid="confirm-transition-button"
              onClick={handleConfirm}
            >
              Confirm
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};
