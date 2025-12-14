import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { ShieldAlert, CheckCircle, Lock } from "lucide-react";
import { toast } from "sonner";

// Initial feature list (simulating a database/backlog)
const INITIAL_FEATURES = [
  { id: 1, name: "Voice Transcription", justification: "Captures verbatim driver testimony as primary evidence.", status: "Live" },
  { id: 2, name: "Evidence Score", justification: "Quantifies the strength of the defense dossier.", status: "Live" },
  { id: 3, name: "Dispute Bundle Export", justification: "Creates the physical artifact sent to opposing legal/finance teams.", status: "Live" },
  { id: 4, name: "Responsibility Attribution", justification: "Uses AI to objectively pinpoint third-party fault.", status: "Live" },
  { id: 5, name: "Predictive ETA", justification: "", status: "Planned" },
  { id: 6, name: "Driver Leaderboard", justification: "", status: "Planned" },
  { id: 7, name: "Dark Mode", justification: "", status: "Planned" },
];

export default function AlignmentCheck() {
  const [features, setFeatures] = useState(INITIAL_FEATURES);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [password, setPassword] = useState("");

  const handleLogin = () => {
    if (password === "ward-core") { // Simple client-side gate for this internal tool
      setIsAuthenticated(true);
    } else {
      toast.error("Incorrect password");
    }
  };

  const updateJustification = (id, text) => {
    setFeatures(features.map(f => f.id === id ? { ...f, justification: text } : f));
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <Card className="w-96 border-gray-800 bg-gray-950 text-white">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Lock className="h-5 w-5 text-red-500" /> Internal Access Only
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Input 
              type="password" 
              placeholder="Enter Access Code" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="bg-gray-900 border-gray-800 text-white"
            />
            <Button onClick={handleLogin} className="w-full bg-red-600 hover:bg-red-700">Unlock</Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8 font-sans">
      <div className="max-w-6xl mx-auto space-y-8">
        
        {/* The Mantra */}
        <div className="bg-slate-900 text-white p-8 rounded-lg shadow-lg border-l-8 border-red-500 text-center">
          <h1 className="text-3xl font-bold italic font-serif leading-relaxed tracking-wide">
            "If it doesn’t strengthen our customer’s argument in a dispute, we don’t build it."
          </h1>
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="text-xl flex items-center gap-2">
              <ShieldAlert className="h-5 w-5 text-red-600" />
              Feature Alignment Audit
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-1/4">Feature Name</TableHead>
                  <TableHead className="w-1/6">Status</TableHead>
                  <TableHead className="w-1/2">
                    Direct Alignment Justification
                    <span className="block text-xs font-normal text-gray-500 mt-1">
                      (Mandatory: How does this stop the meter or win a dispute?)
                    </span>
                  </TableHead>
                  <TableHead className="w-1/12 text-center">Verdict</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {features.map((feature) => {
                  const isMissing = !feature.justification || feature.justification.trim() === "";
                  return (
                    <TableRow key={feature.id} className={isMissing ? "bg-red-50" : ""}>
                      <TableCell className="font-medium">{feature.name}</TableCell>
                      <TableCell>
                        <Badge variant={feature.status === "Live" ? "default" : "secondary"}>
                          {feature.status}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <Input 
                          value={feature.justification}
                          onChange={(e) => updateJustification(feature.id, e.target.value)}
                          placeholder="Explain dispute value..."
                          className={`w-full ${isMissing ? "border-red-300 bg-white placeholder:text-red-300" : ""}`}
                        />
                        {isMissing && (
                          <p className="text-xs text-red-600 mt-1 font-bold">⚠️ Alignment Missing: Do not build.</p>
                        )}
                      </TableCell>
                      <TableCell className="text-center">
                        {isMissing ? (
                          <ShieldAlert className="h-5 w-5 text-red-500 mx-auto" />
                        ) : (
                          <CheckCircle className="h-5 w-5 text-green-500 mx-auto" />
                        )}
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        {/* Feature Ticket Schema Reminder */}
        <Card className="bg-blue-50 border-blue-200">
          <CardHeader>
            <CardTitle className="text-sm font-bold uppercase tracking-wider text-blue-800">
              New Ticket Schema Enforcement
            </CardTitle>
          </CardHeader>
          <CardContent className="text-sm text-blue-900">
            <p>All new PRs and Jira tickets MUST include the following field:</p>
            <pre className="bg-white p-3 rounded mt-2 border border-blue-200 font-mono text-xs">
              **Dispute Value:** [Explain exactly how this feature serves as evidence]
            </pre>
          </CardContent>
        </Card>

      </div>
    </div>
  );
}
