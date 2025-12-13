import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Loader2, Send, CheckCircle2, Clock, Play, MessageSquare, AlertCircle } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
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
      <Card className="border-blue-100 bg-blue-50/30 overflow-hidden relative">
        {/* Abstract background pattern for "Active" feel */}
        <div className="absolute top-0 right-0 w-32 h-32 bg-blue-100/50 rounded-full blur-3xl -mr-16 -mt-16 pointer-events-none" />
        
        <CardHeader className="pb-2 relative z-10">
          <div className="flex justify-between items-center">
            <CardTitle className="text-lg flex items-center gap-2 text-blue-900">
              <div className="p-1.5 bg-blue-100 rounded-md">
                <Send className="h-4 w-4 text-blue-700" />
              </div>
              Active Coordination
            </CardTitle>
            {coordinationStatus === "idle" && (
              <Button onClick={startCoordination} disabled={loading} size="sm" className="bg-blue-600 hover:bg-blue-700 shadow-md transition-all active:scale-95">
                {loading ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : <Play className="h-4 w-4 mr-2" />}
                Start Outreach
              </Button>
            )}
          </div>
        </CardHeader>
        <CardContent className="relative z-10">
          {coordinationStatus === "idle" ? (
            <div className="bg-white/60 p-4 rounded-lg border border-blue-100 text-center">
              <p className="text-sm text-gray-600">
                Identify stakeholders and initiate outreach to gather data automatically.
              </p>
            </div>
          ) : (
            <div className="space-y-5">
              {/* Stakeholder Status */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <h4 className="text-xs font-semibold text-blue-900 uppercase tracking-wide">Stakeholder Outreach</h4>
                  <Badge variant="outline" className="bg-white text-blue-600 border-blue-200 shadow-sm animate-pulse">
                    Live Tracking
                  </Badge>
                </div>
                <div className="grid grid-cols-1 gap-2">
                  {stakeholders.map((s, idx) => (
                    <div key={idx} className="bg-white p-3 rounded-lg border shadow-sm flex justify-between items-center group hover:border-blue-300 transition-colors">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-xs font-bold text-gray-500">
                          {s.role.substring(0, 2).toUpperCase()}
                        </div>
                        <div>
                          <div className="font-medium text-sm text-gray-900">{s.role}</div>
                          <div className="text-xs text-gray-500">{s.contact?.name}</div>
                        </div>
                      </div>
                      <Badge variant="outline" className="bg-yellow-50 text-yellow-700 border-yellow-200">
                        <Clock className="h-3 w-3 mr-1" />
                        Waiting
                      </Badge>
                    </div>
                  ))}
                  {stakeholders.length === 0 && (
                    <div className="text-sm text-gray-500 italic text-center py-4 bg-white/50 rounded border border-dashed">
                      No stakeholders identified yet.
                    </div>
                  )}
                </div>
              </div>

              {/* RCA Action */}
              {!enhancedRca && stakeholders.length > 0 && (
                <div className="flex justify-end pt-2 animate-in fade-in slide-in-from-bottom-2 duration-500">
                  <Button onClick={performRca} disabled={loading} className="bg-purple-600 hover:bg-purple-700 text-white shadow-md">
                    {loading ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : <Play className="h-4 w-4 mr-2" />}
                    Analyze Responses & Plan Actions
                  </Button>
                </div>
              )}

              {/* Enhanced RCA Results & Action Plan */}
              {enhancedRca && (
                <div className="mt-4 pt-4 border-t border-blue-200 animate-in zoom-in-95 duration-300">
                  <h4 className="text-xs font-semibold text-green-800 uppercase tracking-wide mb-3 flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4" />
                    Action Plan Generated
                  </h4>
                  <div className="space-y-2 mb-4">
                    {enhancedRca.action_plan?.map((action, idx) => (
                      <div key={idx} className="bg-white p-3 rounded-lg border-l-4 border-l-green-500 shadow-sm border border-gray-100">
                        <div className="flex justify-between items-start">
                          <div>
                            <span className="font-medium text-sm text-gray-900 block mb-1">{action.description}</span>
                            <div className="text-xs text-gray-500">Deadline: {action.deadline}</div>
                          </div>
                          <Badge variant="secondary" className="text-xs">{action.owner}</Badge>
                        </div>
                      </div>
                    ))}
                  </div>
                  <Button className="w-full bg-green-600 hover:bg-green-700 shadow-md" onClick={() => executePlan(enhancedRca.action_plan)} disabled={loading}>
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
      <div className="border border-dashed border-gray-300 rounded-lg p-4 bg-gray-50/50">
        <div 
          className="flex justify-between items-center cursor-pointer select-none"
          onClick={() => setShowSim(!showSim)}
        >
          <h4 className="text-xs font-mono font-bold text-gray-500 uppercase tracking-wider flex items-center gap-2">
            <MessageSquare className="h-3 w-3" />
            Demo Control: Inject Responses
          </h4>
          <span className="text-xs text-blue-600 hover:underline">{showSim ? "Hide" : "Show"}</span>
        </div>
        
        {showSim && (
          <div className="space-y-3 pt-3 animate-in slide-in-from-top-2">
            <div className="bg-white p-3 rounded border shadow-sm">
              <div className="grid grid-cols-1 gap-3">
                <div>
                  <Label htmlFor="actor" className="text-xs text-gray-600 mb-1.5 block">Stakeholder</Label>
                  <select 
                    id="actor"
                    className="w-full h-9 rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm transition-colors focus:ring-1 focus:ring-blue-500"
                    value={simActor}
                    onChange={(e) => setSimActor(e.target.value)}
                  >
                    <option value="">Select Stakeholder...</option>
                    <option value="CHA Jagdish">CHA Jagdish (Customs)</option>
                    <option value="Maersk Line">Maersk Line (Shipping)</option>
                    <option value="Port Operations">Port Ops (Terminal)</option>
                    <option value="Shipper">Shipper (Customer)</option>
                  </select>
                </div>
                <div>
                  <Label htmlFor="content" className="text-xs text-gray-600 mb-1.5 block">Response Message</Label>
                  <div className="flex gap-2">
                    <Input 
                      id="content" 
                      value={simContent} 
                      onChange={(e) => setSimContent(e.target.value)}
                      placeholder="e.g. Invoice corrected and submitted."
                      className="h-9 text-sm"
                    />
                    <Button size="sm" variant="default" onClick={submitSimulation} disabled={simulating || !simActor || !simContent}>
                      {simulating ? <Loader2 className="h-3 w-3 animate-spin" /> : <Send className="h-3 w-3" />}
                    </Button>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="flex gap-2 justify-end">
              <Button 
                variant="ghost" 
                size="sm" 
                className="text-xs text-gray-500 h-6"
                onClick={() => {
                  setSimActor("CHA Jagdish");
                  setSimContent("Sir, invoice mismatch detected. Shipper needs to amend value.");
                }}
              >
                Quick Fill: Discrepancy
              </Button>
              <Button 
                variant="ghost" 
                size="sm" 
                className="text-xs text-gray-500 h-6"
                onClick={() => {
                  setSimActor("Shipper");
                  setSimContent("Amended invoice sent to CHA.");
                }}
              >
                Quick Fill: Resolved
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ActiveCoordination;
