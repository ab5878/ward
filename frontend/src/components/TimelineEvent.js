import React, { useState } from 'react';
import { Card } from './ui/card';
import { Separator } from './ui/separator';
import { Phone, MessageSquareText, Server, ChevronDown, ChevronUp } from 'lucide-react';
import { toIST } from '../utils/datetime';

export const TimelineEvent = ({ event }) => {
  const [expanded, setExpanded] = useState(false);
  
  const Icon = event.source_type === 'voice'
    ? Phone
    : event.source_type === 'system'
    ? Server
    : MessageSquareText;

  const hasMetadata = event.metadata && Object.keys(event.metadata).length > 0;

  return (
    <div
      className="grid grid-cols-[20px_1fr] gap-3"
      data-testid={`timeline-event-${event._id}`}
    >
      <div className="relative flex justify-center pt-1">
        <span className="source-dot" data-type={event.source_type} />
      </div>
      <Card className="p-3 shadow-sm border border-border">
        <div className="flex items-center gap-2 text-xs text-muted-foreground tabular-nums flex-wrap">
          <Icon className="w-3.5 h-3.5" aria-hidden />
          <span>{toIST(event.timestamp)}</span>
          <span>•</span>
          <span className="reliability-chip" data-level={event.reliability}>
            {event.reliability}
          </span>
          {event.actor && (
            <>
              <span>•</span>
              <span>by {event.actor.split('@')[0]}</span>
            </>
          )}
        </div>
        <Separator className="my-2" />
        <div className="text-sm leading-relaxed text-foreground/90">
          {event.content}
        </div>
        {hasMetadata && (
          <div className="mt-2">
            <button
              onClick={() => setExpanded(!expanded)}
              className="flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground transition-colors"
              data-testid="toggle-metadata"
            >
              {expanded ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
              {expanded ? 'Hide' : 'Show'} details
            </button>
            {expanded && (
              <pre
                className="mt-2 bg-secondary/60 p-2 rounded-md text-xs overflow-x-auto"
                data-testid="timeline-payload"
              >
                {JSON.stringify(event.metadata, null, 2)}
              </pre>
            )}
          </div>
        )}
      </Card>
    </div>
  );
};
