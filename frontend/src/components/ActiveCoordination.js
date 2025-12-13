import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Loader2, Send, CheckCircle2, Clock, Play, MessageSquare } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "sonner";
import api from '../services/api';

const ActiveCoordination = ({ caseId, caseData, onUpdate }) => {
  const [loading, setLoading] = useState(false);
  const [simulating, setSimulating] = useState(false);
  const [simActor, setSimActor] = useState("");
  const [simContent, setSimContent] = useState("");
  const [showSim, setShowSim] = useState(false);

  // Derive state from caseData
  const coordinationStatus = caseData?.coordination_status || "idle";
  const stakeholders = caseData?.stakeholders || [];
  const enhancedRca = caseData?.enhanced_rca;

  const startCoordination = async () => {
    setLoading(true);
    try {
      await api.post(`/api/cases/${caseId}/coordination/start`);
      toast.success("Active coordination started");
      if (onUpdate) onUpdate();
    } catch (error) {
      toast.error("Failed to start coordination");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const performRca = async () => {
    setLoading(true);
    try {
      await api.post(`/api/cases/${caseId}/coordination/rca`);
      toast.success("Enhanced RCA completed");
      if (onUpdate) onUpdate();
    } catch (error) {
      toast.error("Failed to perform RCA");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const executePlan = async (plan) => {
    setLoading(true);
    try {
      await api.post(`/api/cases/${caseId}/coordination/execute`, { action_plan: plan });
      toast.success("Action plan execution started");
      if (onUpdate) onUpdate();
    } catch (error) {
      toast.error("Failed to execute plan");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const submitSimulation = async () => {
    if (!simActor || !simContent) return;
    setSimulating(true);
    try {
      await api.post(`/api/cases/${caseId}/coordination/simulate-response`, {
        actor: simActor,
        content: simContent
      });
      toast.success("Response simulated");
      setSimContent("");
      if (onUpdate) onUpdate();
    } catch (error) {
      toast.error("Failed to simulate");
    } finally {
      setSimulating(false);
    }
  };

  if (!caseData) return null;

  return (
    <div className="space-y-6">
      {/* Active Coordination Panel */}
      <Card className="border-blue-100 bg-blue-50/20">
        <CardHeader className="pb-2">
          <div className="flex justify-between items-center">
            <CardTitle className="text-lg flex items-center gap-2 text-blue-800">
              <Send className="h-5 w-5" />
              Active Coordination
            </CardTitle>
            {coordinationStatus === "idle" && (
              <Button onClick={startCoordination} disabled={loading} size="sm">
                {loading ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : <Play className="h-4 w-4 mr-2" />}
                Start Outreach
              </Button>
            )}
          </div>
        </CardHeader>
        <CardContent>
          {coordinationStatus === "idle" ? (
            <p className="text-sm text-gray-500">
              Identify stakeholders and initiate outreach to gather data.
            </p>
          ) : (
            <div className="space-y-4">
              {/* Stakeholder Status */}
              <div>
                <h4 className="text-sm font-medium mb-2 text-gray-700">Stakeholder Outreach</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {stakeholders.map((s, idx) => (
                    <div key={idx} className="bg-white p-3 rounded border text-sm flex justify-between items-center">
                      <div>
                        <div className="font-medium">{s.role}</div>
                        <div className="text-xs text-gray-500">{s.contact?.name}</div>
                      </div>
                      <Badge variant="outline" className="bg-yellow-50 text-yellow-700 border-yellow-200">
                        <Clock className="h-3 w-3 mr-1" />
                        Waiting
                      </Badge>
                    </div>
                  ))}
                  {stakeholders.length === 0 && (
                    <div className="text-sm text-gray-500 italic">No stakeholders identified yet.</div>
                  )}
                </div>
              </div>

              {/* RCA Action */}
              {!enhancedRca && stakeholders.length > 0 && (
                <div className="flex justify-end pt-2">
                  <Button onClick={performRca} disabled={loading} variant="secondary" size="sm">
                    {loading ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
                    Analyze Responses & Plan Actions
                  </Button>
                </div>
              )}

              {/* Enhanced RCA Results & Action Plan */}
              {enhancedRca && (
                <div className="mt-4 pt-4 border-t border-blue-200">
                  <h4 className="text-sm font-medium mb-2 text-gray-700">Recommended Action Plan</h4>
                  <div className="space-y-2 mb-4">
                    {enhancedRca.action_plan?.map((action, idx) => (
                      <div key={idx} className="bg-white p-3 rounded border border-l-4 border-l-green-500 shadow-sm">
                        <div className="flex justify-between">
                          <span className="font-medium text-sm">{action.description}</span>
                          <Badge>{action.owner}</Badge>
                        </div>
                        <div className="text-xs text-gray-500 mt-1">Deadline: {action.deadline}</div>
                      </div>
                    ))}
                  </div>
                  <Button className="w-full" onClick={() => executePlan(enhancedRca.action_plan)} disabled={loading}>
                    {loading ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : <CheckCircle2 className="h-4 w-4 mr-2" />}
                    Approve & Execute Plan
                  </Button>
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Demo Simulation Tool (Collapsible) */}
      <div className="border border-dashed border-gray-300 rounded-lg p-4 bg-gray-50">
        <div 
          className="flex justify-between items-center cursor-pointer mb-2"
          onClick={() => setShowSim(!showSim)}
        >
          <h4 className="text-xs font-mono font-bold text-gray-500 uppercase tracking-wider flex items-center">
            <MessageSquare className="h-3 w-3 mr-2" />
            Demo: Simulate Responses
          </h4>
          <span className="text-xs text-blue-600 hover:underline">{showSim ? "Hide" : "Show"}</span>
        </div>
        
        {showSim && (
          <div className="space-y-3 pt-2">
            <div className="grid grid-cols-3 gap-2">
              <div className="col-span-1">
                <Label htmlFor="actor" className="text-xs">Actor</Label>
                <select 
                  id="actor"
                  className="w-full h-9 rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm transition-colors"
                  value={simActor}
                  onChange={(e) => setSimActor(e.target.value)}
                >
                  <option value="">Select...</option>
                  <option value="CHA Jagdish">CHA Jagdish</option>
                  <option value="Maersk Line">Maersk Line</option>
                  <option value="Port Operations">Port Ops</option>
                  <option value="Shipper">Shipper</option>
                </select>
              </div>
              <div className="col-span-2">
                <Label htmlFor="content" className="text-xs">Response</Label>
                <Input 
                  id="content" 
                  value={simContent} 
                  onChange={(e) => setSimContent(e.target.value)}
                  placeholder="e.g. Invoice corrected..."
                  className="h-9"
                />
              </div>
            </div>
            <div className="flex justify-end">
              <Button size="sm" variant="outline" onClick={submitSimulation} disabled={simulating}>
                {simulating ? <Loader2 className="h-3 w-3 animate-spin" /> : "Inject Response"}
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ActiveCoordination;
