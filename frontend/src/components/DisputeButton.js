import React, { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Download, Loader2, FileArchive, CheckSquare, AlertCircle } from "lucide-react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import api from '../services/api';

const DisputeButton = ({ caseId, status, financialImpact, evidenceScore }) => {
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);

  // Visibility Logic: Resolved OR High Risk (>100k) AND Score > 70 (or override logic)
  const isHighRisk = (financialImpact?.amount || 0) > 100000;
  const isResolved = status === 'RESOLVED';
  const hasStrongEvidence = (evidenceScore?.score || 0) >= 70;

  // For demo, we might relax this slightly or show disabled
  if (!isResolved && !isHighRisk) return null;

  const handleDownload = async () => {
    setLoading(true);
    try {
      const response = await api.get(`/cases/${caseId}/dispute/bundle`, {
        responseType: 'blob'
      });
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      
      // Extract filename from header if possible, else default
      const contentDisposition = response.headers['content-disposition'];
      let filename = `Demurrage_Dispute_${caseId}.zip`;
      if (contentDisposition) {
        const match = contentDisposition.match(/filename="?([^"]+)"?/);
        if (match) filename = match[1];
      }
      
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      toast.success("Dispute Bundle downloaded");
      setOpen(false);
    } catch (error) {
      toast.error("Failed to generate bundle");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button 
          variant={hasStrongEvidence ? "default" : "secondary"} 
          className={`gap-2 ${hasStrongEvidence ? "bg-red-700 hover:bg-red-800 text-white" : ""}`}
          disabled={!hasStrongEvidence}
        >
          <FileArchive className="h-4 w-4" />
          Export Dispute Bundle
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <FileArchive className="h-5 w-5 text-red-600" />
            Generate Dispute Defense Package
          </DialogTitle>
        </DialogHeader>
        
        <div className="space-y-4 py-4">
          <div className="bg-slate-50 p-4 rounded-lg border text-sm space-y-3">
            <p className="font-semibold text-slate-700">The following evidence will be zipped:</p>
            <ul className="space-y-2">
              <li className="flex items-center gap-2">
                <CheckSquare className="h-4 w-4 text-green-600" />
                <span>Original Voice Recording & Transcript</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckSquare className="h-4 w-4 text-green-600" />
                <span>Responsibility Attribution Report</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckSquare className="h-4 w-4 text-green-600" />
                <span>Full Timeline of Actions</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckSquare className="h-4 w-4 text-green-600" />
                <span>Extracted Document Data (JSON)</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckSquare className="h-4 w-4 text-green-600" />
                <span>Evidence Completeness Certificate</span>
              </li>
            </ul>
          </div>

          {!hasStrongEvidence && (
            <div className="flex items-center gap-2 text-amber-600 bg-amber-50 p-3 rounded text-xs">
              <AlertCircle className="h-4 w-4" />
              Evidence score is below 70%. Bundle may be weak.
            </div>
          )}

          <Button onClick={handleDownload} disabled={loading} className="w-full bg-red-700 hover:bg-red-800">
            {loading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin mr-2" />
                Packaging Evidence...
              </>
            ) : (
              <>
                <Download className="h-4 w-4 mr-2" />
                Download .ZIP
              </>
            )}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default DisputeButton;
