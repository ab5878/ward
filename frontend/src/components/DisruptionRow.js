import React from 'react';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Tooltip, TooltipTrigger, TooltipContent } from './ui/tooltip';
import { Phone, MessageSquareText, Server, UserCircle } from 'lucide-react';
import { toIST } from '../utils/datetime';

export const DisruptionRow = ({ disruption, onSelect }) => {
  const SourceIcon = disruption.last_event?.source_type === 'voice' 
    ? Phone 
    : disruption.last_event?.source_type === 'system' 
    ? Server 
    : MessageSquareText;

  const location = disruption.disruption_details?.identifier || 'N/A';
  const updatedAt = toIST(disruption.updated_at);

  return (
    <tr
      data-testid={`disruption-row-${disruption._id}`}
      className="group hover:bg-secondary/60 transition-colors"
    >
      <td className="px-4 py-3 whitespace-nowrap">
        <span className="state-badge" data-state={disruption.status}>
          {disruption.status.replace('_', ' ')}
        </span>
      </td>
      <td className="px-4 py-3">
        <div className="font-medium text-foreground/90">
          {disruption.description.length > 60
            ? disruption.description.substring(0, 60) + '...'
            : disruption.description}
        </div>
      </td>
      <td className="px-4 py-3 whitespace-nowrap">
        {disruption.decision_owner_email ? (
          <Badge variant="secondary" data-testid="owner-badge" className="flex items-center gap-1">
            <UserCircle className="w-3 h-3" />
            {disruption.decision_owner_email.split('@')[0]}
          </Badge>
        ) : (
          <span className="text-xs text-muted-foreground">Unassigned</span>
        )}
      </td>
      <td className="px-4 py-3">
        {disruption.last_event && (
          <div className="flex items-center gap-2">
            <SourceIcon className="w-4 h-4 text-muted-foreground" aria-hidden />
            <span
              className="reliability-chip"
              data-level={disruption.last_event.reliability}
            >
              {disruption.last_event.reliability}
            </span>
          </div>
        )}
      </td>
      <td className="px-4 py-3 text-muted-foreground">{location}</td>
      <td className="px-4 py-3 text-muted-foreground tabular-nums">{updatedAt}</td>
      <td className="px-4 py-3 text-right">
        <Tooltip>
          <TooltipTrigger asChild>
            <Button
              data-testid="row-open-button"
              size="sm"
              variant="outline"
              onClick={() => onSelect(disruption._id)}
            >
              Open
            </Button>
          </TooltipTrigger>
          <TooltipContent>View details and timeline</TooltipContent>
        </Tooltip>
      </td>
    </tr>
  );
};
