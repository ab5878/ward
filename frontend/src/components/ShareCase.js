import React from 'react';
import { Button } from "@/components/ui/button";
import { Link2, Copy, Check } from "lucide-react";
import { toast } from "sonner";
import api from '../services/api';

const ShareCase = ({ caseId }) => {
  const [loading, setLoading] = React.useState(false);
  const [copied, setCopied] = React.useState(false);

  const handleShare = async () => {
    setLoading(true);
    try {
      const response = await api.post(`/cases/${caseId}/magic-link`);
      const { url } = response.data;
      const fullUrl = `${window.location.origin}${url}`;
      
      await navigator.clipboard.writeText(fullUrl);
      setCopied(true);
      toast.success("Magic link copied to clipboard!");
      
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      toast.error("Failed to generate link");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Button 
      variant="outline" 
      size="sm" 
      onClick={handleShare}
      disabled={loading}
      className="gap-2"
    >
      {copied ? <Check className="h-4 w-4" /> : <Link2 className="h-4 w-4" />}
      {copied ? "Copied!" : "Share Case"}
    </Button>
  );
};

export default ShareCase;
