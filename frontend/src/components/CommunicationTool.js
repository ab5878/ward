import React, { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Mail, MessageSquare, Send, Loader2 } from "lucide-react";
import { toast } from "sonner";
import api from '../services/api';

const CommunicationTool = () => {
  const [loading, setLoading] = useState(false);
  const [recipient, setRecipient] = useState("");
  const [message, setMessage] = useState("");
  const [channel, setChannel] = useState("sms");

  const handleSend = async () => {
    if (!recipient || !message) return;
    
    setLoading(true);
    try {
      await api.post("/integrations/send", {
        channel,
        recipient,
        content: message,
        subject: channel === "email" ? "Ward Disruption Alert" : undefined
      });
      toast.success(`${channel.toUpperCase()} sent successfully!`);
      setMessage("");
    } catch (error) {
      toast.error("Failed to send message");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline" size="sm" className="gap-2">
          <Send className="h-4 w-4" />
          Send Alert
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Send Real-World Alert</DialogTitle>
        </DialogHeader>
        <div className="space-y-4 pt-4">
          <div className="flex gap-2">
            <Button 
              variant={channel === "sms" ? "default" : "outline"} 
              onClick={() => setChannel("sms")}
              className="flex-1"
            >
              <MessageSquare className="h-4 w-4 mr-2" /> SMS
            </Button>
            <Button 
              variant={channel === "email" ? "default" : "outline"} 
              onClick={() => setChannel("email")}
              className="flex-1"
            >
              <Mail className="h-4 w-4 mr-2" /> Email
            </Button>
          </div>
          
          <div>
            <label className="text-sm font-medium mb-1 block">
              {channel === "sms" ? "Phone Number" : "Email Address"}
            </label>
            <Input 
              value={recipient}
              onChange={(e) => setRecipient(e.target.value)}
              placeholder={channel === "sms" ? "+919876543210" : "manager@company.com"}
            />
          </div>
          
          <div>
            <label className="text-sm font-medium mb-1 block">Message</label>
            <Textarea 
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Enter your alert message..."
              rows={4}
            />
          </div>
          
          <Button onClick={handleSend} disabled={loading} className="w-full">
            {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : "Send Now"}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default CommunicationTool;
