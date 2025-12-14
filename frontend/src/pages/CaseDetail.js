import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import { ArrowLeft, Loader2, AlertTriangle, Plus, LayoutList, Brain, History, FileText, Send } from 'lucide-react';
import EvidenceScore from '../components/EvidenceScore';
import ResponsibilityCard from '../components/ResponsibilityCard';
import CommunicationTool from '../components/CommunicationTool';
import ShareCase from '../components/ShareCase';
import DisputeButton from '../components/DisputeButton';
import { TimelineEvent } from '../components/TimelineEvent';
import { StateTransitionBar } from '../components/StateTransitionBar';
import { OwnershipAssigner } from '../components/OwnershipAssigner';
import ActiveCoordination from '../components/ActiveCoordination';
import SimilarCases from '../components/SimilarCases';
import DocumentManager from '../components/DocumentManager';
import FinancialImpactCard from '../components/FinancialImpactCard';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card';
import { Textarea } from '../components/ui/textarea';
import { Button } from '../components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
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
  const [activeTab, setActiveTab] = useState("timeline");
  
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
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!caseData) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <AlertTriangle className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
          <p className="text-muted-foreground">Case not found</p>
          <Link
            to="/dashboard"
            className="text-primary hover:underline mt-4 inline-block"
          >
            Back to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  const isDecisionOwner = caseData.decision_owner_email === user?.email;

  return (
    <div className="min-h-screen bg-gray-50/30">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10 shadow-sm">
        <div className="container mx-auto px-6 py-4">
          <div className="flex justify-between items-start">
            <div className="space-y-1">
              <Link
                to="/dashboard"
                className="inline-flex items-center gap-2 text-xs font-medium text-gray-500 hover:text-gray-900 transition-colors mb-1"
              >
                <ArrowLeft className="h-3 w-3" />
                Back to Dashboard
              </Link>
              <div className="flex items-center gap-3">
                <h1 className="text-xl font-bold tracking-tight text-gray-900">
                  Case #{caseId.slice(-6).toUpperCase()}
                </h1>
                <span className="state-badge" data-state={caseData.status}>
                  {caseData.status.replace('_', ' ')}
                </span>
              </div>
              <div className="flex items-center gap-4 text-xs text-gray-500">
                <span>Created {toIST(caseData.created_at)}</span>
                <span>•</span>
                <span>Updated {toIST(caseData.updated_at)}</span>
              </div>
            </div>
            
            <div className="flex items-center gap-3">
              <OwnershipAssigner
                caseId={caseId}
                currentOwner={caseData.decision_owner_email}
                onAssigned={loadCase}
              />
              <DisputeButton 
                caseId={caseId}
                status={caseData.status}
                financialImpact={caseData.financial_impact}
                evidenceScore={caseData.evidence_score}
              />
              <ShareCase caseId={caseId} />
              <CommunicationTool />
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Main Content Area - Left 2 columns */}
          <div className="lg:col-span-2 space-y-6">
            
            {/* Evidence Score Card (New) */}
            <EvidenceScore 
              caseId={caseId} 
              caseData={caseData} 
              onUpdate={loadCase} 
            />

            {/* Responsibility Attribution (New) */}
            <ResponsibilityCard
              caseId={caseId}
              responsibility={caseData.responsibility}
              onUpdate={loadCase}
            />

            {/* Case Description - Always Visible */}
            <Card className="border-none shadow-sm bg-white">
              <CardContent className="pt-6">
                <p className="text-sm text-gray-800 leading-relaxed font-medium">
                  {caseData.description}
                </p>
                <div className="mt-4 flex flex-wrap gap-4 text-xs text-gray-500 border-t pt-4">
                  <div>
                    <span className="font-semibold text-gray-700 block">Type</span>
                    {caseData.disruption_details?.disruption_type || 'N/A'}
                  </div>
                  <div>
                    <span className="font-semibold text-gray-700 block">Location</span>
                    <div className="flex items-center gap-1">
                      {caseData.structured_context?.location_code && (
                        <Badge variant="outline" className="text-[10px] font-mono h-4 px-1">{caseData.structured_context.location_code}</Badge>
                      )}
                      {caseData.disruption_details?.identifier || 'N/A'}
                    </div>
                  </div>
                  <div>
                    <span className="font-semibold text-gray-700 block">Source</span>
                    {caseData.disruption_details?.source || 'N/A'}
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Tabbed Interface for Tools */}
            <Tabs defaultValue="timeline" className="w-full" onValueChange={setActiveTab}>
              <TabsList className="grid w-full grid-cols-3 mb-4">
                <TabsTrigger value="timeline" className="flex items-center gap-2">
                  <LayoutList className="h-4 w-4" /> Timeline
                </TabsTrigger>
                <TabsTrigger value="intelligence" className="flex items-center gap-2">
                  <Brain className="h-4 w-4" /> Intelligence
                </TabsTrigger>
                <TabsTrigger value="action" className="flex items-center gap-2">
                  <Send className="h-4 w-4" /> Action Center
                </TabsTrigger>
              </TabsList>

              <TabsContent value="timeline" className="space-y-4">
                <Card className="border-gray-200">
                  <CardHeader className="py-4 px-6 border-b bg-gray-50/50">
                    <div className="flex justify-between items-center">
                      <CardTitle className="text-sm font-medium text-gray-700">Chronological Events</CardTitle>
                      <Button variant="ghost" size="sm" className="h-8 text-xs" onClick={() => document.getElementById('note-input')?.focus()}>
                        <Plus className="h-3 w-3 mr-1" /> Add Note
                      </Button>
                    </div>
                  </CardHeader>
                  <CardContent className="p-0">
                    <ScrollArea className="h-[500px] px-6 py-4">
                      {timeline.length === 0 ? (
                        <div className="text-center py-12 text-gray-400 text-sm">No events recorded yet.</div>
                      ) : (
                        <div className="space-y-6">
                          {Object.entries(groupedTimeline).map(([day, events]) => (
                            <div key={day}>
                              <div className="sticky top-0 bg-white/95 backdrop-blur py-2 mb-4 z-10 border-b border-gray-100">
                                <h3 className="text-xs font-semibold uppercase tracking-wider text-gray-500">
                                  {day}
                                </h3>
                              </div>
                              <div className="space-y-4 pl-2">
                                {events.map((event) => (
                                  <TimelineEvent key={event._id} event={event} />
                                ))}
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </ScrollArea>
                    
                    {/* Quick Note Input */}
                    <div className="p-4 border-t bg-gray-50">
                      <div className="flex gap-2">
                        <Textarea
                          id="note-input"
                          value={noteContent}
                          onChange={(e) => setNoteContent(e.target.value)}
                          rows={1}
                          placeholder="Type a quick update..."
                          className="min-h-[40px] text-sm resize-none bg-white"
                        />
                        <Button size="icon" onClick={handleAddNote} disabled={addingNote || !noteContent.trim()}>
                          {addingNote ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="intelligence" className="space-y-6">
                <div className="grid grid-cols-1 gap-6">
                  {/* RCA Section */}
                  <Card>
                    <CardHeader className="pb-2">
                      <CardTitle className="text-base flex items-center gap-2">
                        <Brain className="h-4 w-4 text-purple-600" />
                        Root Cause Analysis
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      {caseData.rca ? (
                        <div className="space-y-4">
                          <div className="bg-purple-50 p-4 rounded-lg border border-purple-100">
                            <span className="text-xs font-bold text-purple-700 uppercase">Root Cause</span>
                            <p className="mt-1 text-sm font-medium text-gray-900">{caseData.rca.root_cause}</p>
                          </div>
                          
                          <div className="grid grid-cols-2 gap-4">
                            <div>
                              <h4 className="text-xs font-semibold text-gray-500 mb-2 uppercase">Recommended Actions</h4>
                              <ul className="space-y-2">
                                {caseData.rca.recommended_actions?.map((action, idx) => (
                                  <li key={idx} className="text-sm flex gap-2 items-start">
                                    <span className="text-purple-600 font-bold">•</span>
                                    <span className="text-gray-700">{action.action}</span>
                                  </li>
                                ))}
                              </ul>
                            </div>
                            <div>
                              <h4 className="text-xs font-semibold text-gray-500 mb-2 uppercase">Preventive Measures</h4>
                              <ul className="space-y-2">
                                {caseData.rca.preventive_measures?.map((measure, idx) => (
                                  <li key={idx} className="text-sm text-gray-600 bg-gray-50 p-2 rounded">
                                    {measure}
                                  </li>
                                ))}
                              </ul>
                            </div>
                          </div>
                        </div>
                      ) : (
                        <div className="text-center py-8">
                          <p className="text-sm text-gray-500 mb-4">No analysis performed yet.</p>
                          <Button 
                            variant="outline" 
                            onClick={async () => {
                              toast.info('Analyzing...');
                              await api.post(`/cases/${caseId}/rca`);
                              loadCase();
                            }}
                          >
                            Run AI Analysis
                          </Button>
                        </div>
                      )}
                    </CardContent>
                  </Card>

                  {/* Document Intelligence */}
                  <DocumentManager caseId={caseId} />
                  
                  {/* Institutional Memory */}
                  <SimilarCases caseId={caseId} />
                </div>
              </TabsContent>

              <TabsContent value="action" className="space-y-6">
                <ActiveCoordination 
                  caseId={caseId} 
                  caseData={caseData} 
                  onUpdate={loadCase} 
                />
              </TabsContent>
            </Tabs>
          </div>

          {/* Sidebar - Right column */}
          <div className="space-y-6">
            {/* Financial Impact (Enterprise) */}
            <FinancialImpactCard impact={caseData.financial_impact} />

            {/* State Transition Control */}
            <Card className="border-l-4 border-l-blue-600 shadow-sm">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-gray-900">Current Status</CardTitle>
              </CardHeader>
              <CardContent>
                <StateTransitionBar
                  currentState={caseData.status}
                  canAdvance={isDecisionOwner}
                  onAdvance={handleTransition}
                />
              </CardContent>
            </Card>

            {/* Quick Properties */}
            <Card>
              <CardHeader className="pb-2 border-b bg-gray-50/50">
                <CardTitle className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Case Properties</CardTitle>
              </CardHeader>
              <CardContent className="pt-4 space-y-4 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-500">Decision Owner</span>
                  <span className="font-medium text-gray-900 truncate max-w-[150px]" title={caseData.decision_owner_email}>
                    {caseData.decision_owner_email || 'Unassigned'}
                  </span>
                </div>
                <Separator />
                <div className="flex justify-between">
                  <span className="text-gray-500">Created By</span>
                  <span className="font-medium text-gray-900 truncate max-w-[150px]">
                    {caseData.operator_email}
                  </span>
                </div>
                <Separator />
                <div>
                  <span className="text-gray-500 block mb-1">Shipment IDs</span>
                  <div className="flex flex-wrap gap-1">
                    {caseData.shipment_identifiers?.ids?.map(id => (
                      <span key={id} className="bg-gray-100 px-2 py-0.5 rounded text-xs font-mono text-gray-700 border">
                        {id}
                      </span>
                    )) || <span className="text-gray-400 italic">None</span>}
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

        </div>
      </div>
    </div>
  );
}
