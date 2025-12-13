import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import { ArrowLeft, Loader2, AlertTriangle, Plus } from 'lucide-react';
import { TimelineEvent } from '../components/TimelineEvent';
import { StateTransitionBar } from '../components/StateTransitionBar';
import { OwnershipAssigner } from '../components/OwnershipAssigner';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card';
import { Textarea } from '../components/ui/textarea';
import { Button } from '../components/ui/button';
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from '../components/ui/select';
import { Separator } from '../components/ui/separator';
import { ScrollArea } from '../components/ui/scroll-area';
import { toast } from 'sonner';
import { useAuth } from '../contexts/AuthContext';
import { toIST, getDayLabel } from '../utils/datetime';

export default function CaseDetail() {
  const { caseId } = useParams();
  const { user } = useAuth();
  const [caseData, setCaseData] = useState(null);
  const [timeline, setTimeline] = useState([]);
  const [loading, setLoading] = useState(true);
  const [addingNote, setAddingNote] = useState(false);
  
  // Add note form state
  const [noteContent, setNoteContent] = useState('');
  const [noteSourceType, setNoteSourceType] = useState('text');
  const [noteReliability, setNoteReliability] = useState('medium');

  useEffect(() => {
    loadCase();
  }, [caseId]);

  const loadCase = async () => {
    try {
      const response = await api.get(`/cases/${caseId}`);
      setCaseData(response.data.case);
      setTimeline(response.data.timeline || []);
    } catch (error) {
      console.error('Failed to load case:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTransition = async (nextState, reason) => {
    try {
      await api.post(`/cases/${caseId}/transition`, {
        next_state: nextState,
        reason: reason,
      });
      await loadCase();
    } catch (error) {
      throw error;
    }
  };

  const handleAddNote = async () => {
    if (!noteContent.trim()) {
      toast.error('Please enter note content');
      return;
    }

    setAddingNote(true);
    try {
      await api.post(`/cases/${caseId}/timeline`, {
        content: noteContent,
        source_type: noteSourceType,
        reliability: noteReliability,
      });
      toast.success('Note added to timeline');
      setNoteContent('');
      setNoteSourceType('text');
      setNoteReliability('medium');
      await loadCase();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to add note');
    } finally {
      setAddingNote(false);
    }
  };

  // Group timeline by day
  const groupedTimeline = timeline.reduce((groups, event) => {
    const dayLabel = getDayLabel(event.timestamp);
    if (!groups[dayLabel]) {
      groups[dayLabel] = [];
    }
    groups[dayLabel].push(event);
    return groups;
  }, {});

  if (loading) {
    return (
      <div className=\"min-h-screen bg-background flex items-center justify-center\">
        <Loader2 className=\"h-8 w-8 animate-spin text-primary\" />
      </div>
    );
  }

  if (!caseData) {
    return (
      <div className=\"min-h-screen bg-background flex items-center justify-center\">
        <div className=\"text-center\">
          <AlertTriangle className=\"h-12 w-12 mx-auto mb-4 text-muted-foreground\" />
          <p className=\"text-muted-foreground\">Case not found</p>
          <Link
            to=\"/dashboard\"
            className=\"text-primary hover:underline mt-4 inline-block\"
          >
            Back to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  const isDecisionOwner = caseData.decision_owner_email === user?.email;

  return (
    <div className=\"min-h-screen bg-background\">
      {/* Header */}
      <header className=\"border-b border-border bg-card sticky top-0 z-10\">
        <div className=\"container mx-auto px-6 py-4\">
          <Link
            to=\"/dashboard\"
            className=\"inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors mb-2\"
          >
            <ArrowLeft className=\"h-4 w-4\" />
            Back to Dashboard
          </Link>
          <div className=\"flex justify-between items-start\">
            <div className=\"space-y-2\">
              <div className=\"flex items-center gap-3\">
                <h1 className=\"text-2xl font-bold tracking-tight\">
                  Case #{caseId.slice(-6).toUpperCase()}
                </h1>
                <span className=\"state-badge\" data-state={caseData.status}>
                  {caseData.status.replace('_', ' ')}
                </span>
              </div>
              <div className=\"flex items-center gap-4 text-sm text-muted-foreground\">
                <span>Created {toIST(caseData.created_at)}</span>
                <span>•</span>
                <span>Updated {toIST(caseData.updated_at)}</span>
              </div>
            </div>
            <OwnershipAssigner
              caseId={caseId}
              currentOwner={caseData.decision_owner_email}
              onAssigned={loadCase}
            />
          </div>
        </div>
      </header>

      <div className=\"container mx-auto px-6 py-8\">
        <div className=\"grid grid-cols-1 lg:grid-cols-3 gap-6\">
          {/* Timeline - Left 2 columns */}
          <div className=\"lg:col-span-2 space-y-6\">
            {/* Disruption Description Card */}
            <Card>
              <CardHeader>
                <CardTitle className=\"text-lg\">Disruption Details</CardTitle>
              </CardHeader>
              <CardContent className=\"space-y-4\">
                <div>
                  <p className=\"text-sm leading-relaxed\" data-testid=\"case-description\">
                    {caseData.description}
                  </p>
                </div>
                <Separator />
                <div className=\"grid grid-cols-2 gap-4 text-sm\">
                  <div>
                    <span className=\"font-medium\">Type:</span>
                    <p className=\"text-muted-foreground\">
                      {caseData.disruption_details?.disruption_type || 'N/A'}
                    </p>
                  </div>
                  <div>
                    <span className=\"font-medium\">Scope:</span>
                    <p className=\"text-muted-foreground\">
                      {caseData.disruption_details?.scope || 'N/A'}
                    </p>
                  </div>
                  <div>
                    <span className=\"font-medium\">Location:</span>
                    <p className=\"text-muted-foreground\">
                      {caseData.disruption_details?.identifier || 'N/A'}
                    </p>
                  </div>
                  <div>
                    <span className=\"font-medium\">Discovered:</span>
                    <p className=\"text-muted-foreground\">
                      {caseData.disruption_details?.time_discovered_ist || 'N/A'}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Timeline */}
            <Card>
              <CardHeader>
                <CardTitle className=\"text-lg\">Timeline</CardTitle>
              </CardHeader>
              <CardContent>
                <ScrollArea className=\"h-[600px] pr-4\">
                  {timeline.length === 0 ? (
                    <div className=\"text-center py-8 text-muted-foreground\">
                      No timeline events yet
                    </div>
                  ) : (
                    <div className=\"space-y-6\">
                      {Object.entries(groupedTimeline).map(([day, events]) => (
                        <div key={day}>
                          <div className=\"sticky top-0 bg-background py-2 mb-4\">
                            <h3 className=\"text-xs uppercase tracking-wider text-muted-foreground font-medium\">
                              {day}
                            </h3>
                          </div>
                          <div className=\"space-y-4\">
                            {events.map((event) => (
                              <TimelineEvent key={event._id} event={event} />
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </ScrollArea>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar - Right column */}
          <div className=\"space-y-6\">
            {/* State Transition */}
            <Card>
              <CardHeader>
                <CardTitle className=\"text-lg\">State Transition</CardTitle>
              </CardHeader>
              <CardContent>
                <StateTransitionBar
                  currentState={caseData.status}
                  canAdvance={isDecisionOwner}
                  onAdvance={handleTransition}
                />
              </CardContent>
            </Card>

            {/* Add Timeline Note */}
            <Card>
              <CardHeader>
                <CardTitle className=\"text-lg\">Add Timeline Note</CardTitle>
              </CardHeader>
              <CardContent className=\"space-y-3\" data-testid=\"add-timeline-note-form\">
                <div>
                  <label className=\"text-sm font-medium mb-1 block\">Content</label>
                  <Textarea
                    value={noteContent}
                    onChange={(e) => setNoteContent(e.target.value)}
                    rows={4}
                    placeholder=\"What happened? What do we know?\"
                    data-testid=\"timeline-content-input\"
                  />
                </div>
                <div className=\"grid grid-cols-2 gap-3\">
                  <div>
                    <label className=\"text-sm font-medium mb-1 block\">Source</label>
                    <Select value={noteSourceType} onValueChange={setNoteSourceType}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value=\"text\">Text</SelectItem>
                        <SelectItem value=\"voice\">Voice</SelectItem>
                        <SelectItem value=\"system\">System</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <label className=\"text-sm font-medium mb-1 block\">Reliability</label>
                    <Select value={noteReliability} onValueChange={setNoteReliability}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value=\"low\">Low</SelectItem>
                        <SelectItem value=\"medium\">Medium</SelectItem>
                        <SelectItem value=\"high\">High</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
                <Button
                  onClick={handleAddNote}
                  disabled={addingNote || !noteContent.trim()}
                  className=\"w-full\"
                  data-testid=\"add-note-button\"
                >
                  <Plus className=\"w-4 h-4 mr-2\" />
                  {addingNote ? 'Adding...' : 'Add Note'}
                </Button>
              </CardContent>
            </Card>

            {/* Properties */}
            <Card>
              <CardHeader>
                <CardTitle className=\"text-lg\">Properties</CardTitle>
              </CardHeader>
              <CardContent className=\"space-y-3 text-sm\">
                <div>
                  <span className=\"font-medium\">Decision Owner:</span>
                  <p className=\"text-muted-foreground\">
                    {caseData.decision_owner_email || 'Unassigned'}
                  </p>
                </div>
                <Separator />
                <div>
                  <span className=\"font-medium\">Created By:</span>
                  <p className=\"text-muted-foreground\">{caseData.operator_email}</p>
                </div>
                <Separator />
                <div>
                  <span className=\"font-medium\">Shipments:</span>
                  <p className=\"text-muted-foreground\">
                    {caseData.shipment_identifiers?.ids?.join(', ') || 'None'}
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
