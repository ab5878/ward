import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Copy, Plus, Trash2, Key, Webhook } from "lucide-react";
import { toast } from "sonner";
import api from '../services/api';
import { Link } from 'react-router-dom';

export default function DeveloperSettings() {
  const [keys, setKeys] = useState([]);
  const [webhooks, setWebhooks] = useState([]);
  const [newKeyName, setNewKeyName] = useState("");
  const [newWebhookUrl, setNewWebhookUrl] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [k, w] = await Promise.all([
        api.get('/developer/keys'),
        api.get('/developer/webhooks')
      ]);
      setKeys(k.data);
      setWebhooks(w.data);
    } catch (e) {
      console.error(e);
    }
  };

  const createKey = async () => {
    if (!newKeyName) return;
    setLoading(true);
    try {
      const res = await api.post('/developer/keys', { name: newKeyName });
      toast.success("API Key Created: " + res.data.api_key); // Show once!
      setNewKeyName("");
      loadData();
    } catch (e) {
      toast.error("Failed to create key");
    } finally {
      setLoading(false);
    }
  };

  const createWebhook = async () => {
    if (!newWebhookUrl) return;
    setLoading(true);
    try {
      await api.post('/developer/webhooks', { 
        url: newWebhookUrl,
        events: ["case.created", "status.changed"]
      });
      toast.success("Webhook registered");
      setNewWebhookUrl("");
      loadData();
    } catch (e) {
      toast.error("Failed to register webhook");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50/50 p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Developer Settings</h1>
            <p className="text-gray-500">Manage API access and integrations</p>
          </div>
          <Link to="/dashboard" className="text-blue-600 hover:underline">Back to Dashboard</Link>
        </div>

        {/* API Keys */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Key className="h-5 w-5" /> API Keys
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex gap-4">
              <Input 
                placeholder="Key Name (e.g. SAP Integration)" 
                value={newKeyName}
                onChange={(e) => setNewKeyName(e.target.value)}
              />
              <Button onClick={createKey} disabled={loading}>Generate Key</Button>
            </div>

            <div className="space-y-2">
              {keys.map((key) => (
                <div key={key._id} className="flex justify-between items-center p-3 bg-white border rounded-lg">
                  <div>
                    <div className="font-medium">{key.name}</div>
                    <div className="font-mono text-xs text-gray-500">{key.key_hash}</div>
                  </div>
                  <Badge variant="outline" className="bg-green-50 text-green-700">Active</Badge>
                </div>
              ))}
              {keys.length === 0 && <div className="text-sm text-gray-500 italic">No API keys generated.</div>}
            </div>
          </CardContent>
        </Card>

        {/* Webhooks */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Webhook className="h-5 w-5" /> Webhooks
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex gap-4">
              <Input 
                placeholder="https://api.your-company.com/webhook" 
                value={newWebhookUrl}
                onChange={(e) => setNewWebhookUrl(e.target.value)}
              />
              <Button onClick={createWebhook} disabled={loading}>Register URL</Button>
            </div>

            <div className="space-y-2">
              {webhooks.map((hook) => (
                <div key={hook._id} className="flex justify-between items-center p-3 bg-white border rounded-lg">
                  <div className="overflow-hidden">
                    <div className="font-mono text-sm truncate">{hook.url}</div>
                    <div className="flex gap-2 mt-1">
                      {hook.events.map(e => (
                        <Badge key={e} variant="secondary" className="text-[10px]">{e}</Badge>
                      ))}
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-gray-400">Secret: {hook.secret.substring(0, 8)}...</span>
                    <Button variant="ghost" size="sm" className="text-red-500"><Trash2 className="h-4 w-4" /></Button>
                  </div>
                </div>
              ))}
              {webhooks.length === 0 && <div className="text-sm text-gray-500 italic">No webhooks configured.</div>}
            </div>
          </CardContent>
        </Card>

      </div>
    </div>
  );
}
