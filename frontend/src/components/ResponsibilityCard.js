import React, { useState } from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Loader2, Edit2, ShieldQuestion } from "lucide-react";
import { toast } from "sonner";
import api from '../services/api';

const ResponsibilityCard = ({ caseId, responsibility, onUpdate }) => {
  const [analyzing, setAnalyzing] = useState(false);
  const [showOverride, setShowOverride] = useState(false);
  const [overrideParty, setOverrideParty] = useState("");
  const [overrideReason, setOverrideReason] = useState("");
  const [saving, setSaving] = useState(false);

  const runAnalysis = async () => {
    setAnalyzing(true);
    try {
      await api.post(`/cases/${caseId}/responsibility/analyze`);
      toast.success("Responsibility attributed");
      onUpdate();
    } catch (e) {
      toast.error("Analysis failed");
    } finally {
      setAnalyzing(false);
    }
  };

  const handleOverride = async () => {
    if (!overrideParty || !overrideReason) return;
    setSaving(true);
    try {
      await api.post(`/cases/${caseId}/responsibility/override`, {
        primary_party: overrideParty,
        confidence: "High (Manual)",
        reasoning: overrideReason,
        override_reason: overrideReason
      });
      toast.success("Responsibility updated");
      setShowOverride(false);
      onUpdate();
    } catch (e) {
      toast.error("Update failed");
    } finally {
      setSaving(false);
    }
  };

  const getConfidenceColor = (conf) => {
    const c = conf?.toLowerCase();
    if (c?.includes("high")) return "bg-green-100 text-green-800 border-green-200";
    if (c?.includes("medium")) return "bg-yellow-100 text-yellow-800 border-yellow-200";
    return "bg-red-100 text-red-800 border-red-200";
  };

  if (!responsibility) {
    return (
      <Card className="border-dashed border-gray-300">
        <CardContent className="p-4 flex items-center justify-between">
          <div className="flex items-center gap-2 text-sm text-gray-500">
            <ShieldQuestion className="h-4 w-4" />
            <span>Responsibility not attributed</span>
          </div>
          <Button size="sm" variant="outline" onClick={runAnalysis} disabled={analyzing}>
            {analyzing ? <Loader2 className="h-3 w-3 animate-spin mr-2" /> : null}
            Analyze Responsibility
          </Button>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="border-purple-100 bg-purple-50/20">
      <CardContent className="p-4">
        <div className="flex justify-between items-start mb-2">
          <div>
            <h4 className="text-xs font-bold text-purple-900 uppercase tracking-wide mb-1">
              Primary Responsibility
            </h4>
            <div className="flex items-center gap-2">
              <span className="text-lg font-bold text-gray-900">
                {responsibility.primary_party}
              </span>
              <Badge variant="outline" className={`text-[10px] ${getConfidenceColor(responsibility.confidence)}`}>
                {responsibility.confidence} Confidence
              </Badge>
              {responsibility.is_override && (
                <Badge variant="outline" className="text-[10px] bg-gray-100 text-gray-600">Manual Override</Badge>
              )}
            </div>
          </div>
          
          <Dialog open={showOverride} onOpenChange={setShowOverride}>
            <DialogTrigger asChild>
              <Button variant="ghost" size="icon" className="h-6 w-6 text-gray-400 hover:text-purple-600">
                <Edit2 className="h-3 w-3" />
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Override Responsibility</DialogTitle>
              </DialogHeader>
              <div className="space-y-4 py-2">
                <div>
                  <Label>Responsible Party</Label>
                  <select 
                    className="flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                    value={overrideParty}
                    onChange={(e) => setOverrideParty(e.target.value)}
                  >
                    <option value="">Select Party...</option>
                    <option value="Driver">Driver</option>
                    <option value="Transporter">Transporter</option>
                    <option value="CHA">CHA</option>
                    <option value="Port">Port</option>
                    <option value="Customs">Customs</option>
                    <option value="Shipper">Shipper</option>
                  </select>
                </div>
                <div>
                  <Label>Reason for Override</Label>
                  <Input 
                    value={overrideReason}
                    onChange={(e) => setOverrideReason(e.target.value)}
                    placeholder="Why are you changing this?"
                  />
                </div>
                <Button onClick={handleOverride} disabled={saving} className="w-full">
                  {saving ? <Loader2 className="animate-spin" /> : "Save Override"}
                </Button>
              </div>
            </DialogContent>
          </Dialog>
        </div>
        
        <p className="text-sm text-gray-600 bg-white/50 p-2 rounded border border-purple-100 italic">
          "{responsibility.reasoning}"
        </p>
      </CardContent>
    </Card>
  );
};

export default ResponsibilityCard;
