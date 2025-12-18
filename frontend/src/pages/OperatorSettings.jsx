import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';
import { Settings, Bell, Webhook, Palette, Save, CheckCircle2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Switch } from '../components/ui/switch';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { toast } from 'sonner';
import MobileBottomNav from '../components/MobileBottomNav';

export default function OperatorSettings() {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  
  // Notification settings
  const [notifications, setNotifications] = useState({
    email: true,
    whatsapp: false,
    sms: false
  });
  
  // Webhook settings
  const [webhookUrl, setWebhookUrl] = useState('');
  const [webhookEvents, setWebhookEvents] = useState({
    disruption_reported: true,
    evidence_ready: true,
    dispute_generated: false
  });
  
  // Branding settings
  const [branding, setBranding] = useState({
    logo_url: '',
    primary_color: '#2563eb'
  });

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      // TODO: Load operator settings from API
      // For now, use defaults
    } catch (error) {
      console.error('Failed to load settings:', error);
    }
  };

  const handleSaveNotifications = async () => {
    setSaving(true);
    try {
      await api.patch('/operators/settings', {
        notifications: notifications
      });
      toast.success('Notification settings saved!');
    } catch (error) {
      toast.error('Failed to save settings');
    } finally {
      setSaving(false);
    }
  };

  const handleSaveWebhook = async () => {
    setSaving(true);
    try {
      const events = Object.entries(webhookEvents)
        .filter(([_, enabled]) => enabled)
        .map(([event, _]) => event);
      
      await api.patch('/operators/settings', {
        webhook_url: webhookUrl,
        webhook_events: events
      });
      toast.success('Webhook configured!');
    } catch (error) {
      toast.error('Failed to configure webhook');
    } finally {
      setSaving(false);
    }
  };

  const handleSaveBranding = async () => {
    setSaving(true);
    try {
      await api.patch('/operators/settings', {
        branding: branding
      });
      toast.success('Branding updated!');
    } catch (error) {
      toast.error('Failed to update branding');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <h1 className="text-2xl font-bold text-gray-900">Operator Settings</h1>
        <p className="text-sm text-gray-600">Configure your operator account</p>
      </div>

      <div className="container mx-auto px-6 py-6 max-w-4xl">
        <Tabs defaultValue="notifications" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="notifications">
              <Bell className="h-4 w-4 mr-2" />
              Notifications
            </TabsTrigger>
            <TabsTrigger value="webhooks">
              <Webhook className="h-4 w-4 mr-2" />
              Webhooks
            </TabsTrigger>
            <TabsTrigger value="branding">
              <Palette className="h-4 w-4 mr-2" />
              Branding
            </TabsTrigger>
          </TabsList>

          {/* Notifications Tab */}
          <TabsContent value="notifications">
            <Card>
              <CardHeader>
                <CardTitle>Notification Preferences</CardTitle>
                <CardDescription>
                  Choose how you want to be notified about disruptions and cases
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label htmlFor="email-notifications">Email Notifications</Label>
                    <p className="text-sm text-gray-500">
                      Receive email alerts for new disruptions and case updates
                    </p>
                  </div>
                  <Switch
                    id="email-notifications"
                    checked={notifications.email}
                    onCheckedChange={(checked) => setNotifications({...notifications, email: checked})}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label htmlFor="whatsapp-notifications">WhatsApp Notifications</Label>
                    <p className="text-sm text-gray-500">
                      Receive WhatsApp messages for urgent disruptions
                    </p>
                  </div>
                  <Switch
                    id="whatsapp-notifications"
                    checked={notifications.whatsapp}
                    onCheckedChange={(checked) => setNotifications({...notifications, whatsapp: checked})}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label htmlFor="sms-notifications">SMS Notifications</Label>
                    <p className="text-sm text-gray-500">
                      Receive SMS alerts for critical disruptions
                    </p>
                  </div>
                  <Switch
                    id="sms-notifications"
                    checked={notifications.sms}
                    onCheckedChange={(checked) => setNotifications({...notifications, sms: checked})}
                  />
                </div>

                <Button onClick={handleSaveNotifications} disabled={saving} className="w-full">
                  {saving ? 'Saving...' : 'Save Notification Settings'}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Webhooks Tab */}
          <TabsContent value="webhooks">
            <Card>
              <CardHeader>
                <CardTitle>Webhook Integration</CardTitle>
                <CardDescription>
                  Connect Ward to your TMS/ERP system via webhooks
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="space-y-2">
                  <Label htmlFor="webhook-url">Webhook URL</Label>
                  <Input
                    id="webhook-url"
                    type="url"
                    placeholder="https://your-system.com/ward-webhook"
                    value={webhookUrl}
                    onChange={(e) => setWebhookUrl(e.target.value)}
                  />
                  <p className="text-sm text-gray-500">
                    We'll send POST requests to this URL when events occur
                  </p>
                </div>

                <div className="space-y-4">
                  <Label>Events to Subscribe</Label>
                  
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label htmlFor="event-disruption">Disruption Reported</Label>
                      <p className="text-sm text-gray-500">
                        When a driver reports a new disruption
                      </p>
                    </div>
                    <Switch
                      id="event-disruption"
                      checked={webhookEvents.disruption_reported}
                      onCheckedChange={(checked) => setWebhookEvents({...webhookEvents, disruption_reported: checked})}
                    />
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label htmlFor="event-evidence">Evidence Ready</Label>
                      <p className="text-sm text-gray-500">
                        When case evidence score reaches 70%+
                      </p>
                    </div>
                    <Switch
                      id="event-evidence"
                      checked={webhookEvents.evidence_ready}
                      onCheckedChange={(checked) => setWebhookEvents({...webhookEvents, evidence_ready: checked})}
                    />
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label htmlFor="event-dispute">Dispute Generated</Label>
                      <p className="text-sm text-gray-500">
                        When a dispute packet is generated
                      </p>
                    </div>
                    <Switch
                      id="event-dispute"
                      checked={webhookEvents.dispute_generated}
                      onCheckedChange={(checked) => setWebhookEvents({...webhookEvents, dispute_generated: checked})}
                    />
                  </div>
                </div>

                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <p className="text-sm text-blue-800">
                    <strong>Webhook Payload Format:</strong>
                  </p>
                  <pre className="text-xs text-blue-700 mt-2 overflow-x-auto">
{`{
  "event": "disruption_reported",
  "timestamp": "2024-12-15T10:30:00Z",
  "data": {
    "case_id": "uuid",
    "vehicle_number": "MH-12-AB-1234",
    "description": "..."
  }
}`}
                  </pre>
                </div>

                <Button onClick={handleSaveWebhook} disabled={saving || !webhookUrl} className="w-full">
                  {saving ? 'Saving...' : 'Configure Webhook'}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Branding Tab */}
          <TabsContent value="branding">
            <Card>
              <CardHeader>
                <CardTitle>Branding</CardTitle>
                <CardDescription>
                  Customize Ward's appearance for your company
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="space-y-2">
                  <Label htmlFor="logo-url">Company Logo URL</Label>
                  <Input
                    id="logo-url"
                    type="url"
                    placeholder="https://yourcompany.com/logo.png"
                    value={branding.logo_url}
                    onChange={(e) => setBranding({...branding, logo_url: e.target.value})}
                  />
                  <p className="text-sm text-gray-500">
                    URL to your company logo (will appear in driver app)
                  </p>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="primary-color">Primary Color</Label>
                  <div className="flex gap-4 items-center">
                    <Input
                      id="primary-color"
                      type="color"
                      value={branding.primary_color}
                      onChange={(e) => setBranding({...branding, primary_color: e.target.value})}
                      className="w-20 h-10"
                    />
                    <Input
                      type="text"
                      value={branding.primary_color}
                      onChange={(e) => setBranding({...branding, primary_color: e.target.value})}
                      placeholder="#2563eb"
                    />
                  </div>
                  <p className="text-sm text-gray-500">
                    Primary brand color (hex code)
                  </p>
                </div>

                <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                  <p className="text-sm text-gray-600">
                    <strong>Preview:</strong> Your branding will appear in the driver app and email notifications.
                  </p>
                </div>

                <Button onClick={handleSaveBranding} disabled={saving} className="w-full">
                  {saving ? 'Saving...' : 'Save Branding'}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>

      <MobileBottomNav />
      <div className="h-16 md:hidden"></div>
    </div>
  );
}

