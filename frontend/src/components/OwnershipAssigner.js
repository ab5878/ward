import React, { useState, useEffect } from 'react';
import {
  Select,
  SelectTrigger,
  SelectContent,
  SelectItem,
  SelectValue,
} from './ui/select';
import { Button } from './ui/button';
import { UserPlus } from 'lucide-react';
import { toast } from 'sonner';
import api from '../services/api';

export const OwnershipAssigner = ({ caseId, currentOwner, onAssigned }) => {
  const [users, setUsers] = useState([]);
  const [selectedEmail, setSelectedEmail] = useState(currentOwner || '');
  const [assigning, setAssigning] = useState(false);

  useEffect(() => {
    // For now, we'll use the current user's email as the only option
    // In a real system, you'd fetch all users from /api/users
    const fetchCurrentUser = async () => {
      try {
        const response = await api.get('/auth/me');
        setUsers([response.data]);
        if (!currentOwner) {
          setSelectedEmail(response.data.email);
        }
      } catch (error) {
        console.error('Failed to fetch user:', error);
      }
    };
    fetchCurrentUser();
  }, [currentOwner]);

  const handleAssign = async () => {
    if (!selectedEmail) {
      toast.error('Please select an owner');
      return;
    }

    setAssigning(true);
    try {
      await api.post(`/cases/${caseId}/assign-owner`, {
        owner_email: selectedEmail,
      });
      toast.success(`Ownership assigned to ${selectedEmail.split('@')[0]}`);
      if (onAssigned) {
        onAssigned();
      }
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to assign owner');
    } finally {
      setAssigning(false);
    }
  };

  return (
    <div
      className="flex gap-2 items-center flex-wrap"
      data-testid="ownership-assigner"
    >
      <Select value={selectedEmail} onValueChange={setSelectedEmail}>
        <SelectTrigger className="w-56" data-testid="owner-select-trigger">
          <SelectValue placeholder="Select owner" />
        </SelectTrigger>
        <SelectContent>
          {users.map((user) => (
            <SelectItem key={user.email} value={user.email}>
              {user.email}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
      <Button
        data-testid="assign-owner-button"
        onClick={handleAssign}
        disabled={assigning || selectedEmail === currentOwner}
        className="flex items-center gap-2"
      >
        <UserPlus className="w-4 h-4" />
        {currentOwner ? 'Reassign' : 'Assign'}
      </Button>
    </div>
  );
};
