import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Link as LinkIcon, QrCode, Copy, CheckCircle2, RefreshCw } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Badge } from '../components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { toast } from 'sonner';

export default function DriverLinksManager() {
  const [links, setLinks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [copiedId, setCopiedId] = useState(null);

  const generateLinks = async (method = 'magic_link') => {
    setLoading(true);
    try {
      const response = await api.post(`/operators/drivers/generate-links?method=${method}`);
      setLinks(response.data.links || []);
      toast.success(`Generated ${response.data.links?.length || 0} ${method === 'magic_link' ? 'links' : 'QR codes'}`);
    } catch (error) {
      toast.error('Failed to generate links');
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    toast.success('Link copied to clipboard!');
    setTimeout(() => setCopiedId(null), 2000);
  };

  const shareViaWhatsApp = (link, vehicleNumber) => {
    const message = `Ward Driver App Link for ${vehicleNumber}:\n${link}`;
    const whatsappUrl = `https://wa.me/?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank');
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Driver Links</CardTitle>
        <p className="text-sm text-gray-600">Generate magic links or QR codes for your drivers</p>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="magic_link" className="space-y-4">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="magic_link">
              <LinkIcon className="h-4 w-4 mr-2" />
              Magic Links
            </TabsTrigger>
            <TabsTrigger value="qr_code">
              <QrCode className="h-4 w-4 mr-2" />
              QR Codes
            </TabsTrigger>
          </TabsList>

          <TabsContent value="magic_link" className="space-y-4">
            <Button 
              onClick={() => generateLinks('magic_link')} 
              disabled={loading}
              className="w-full"
            >
              {loading ? 'Generating...' : 'Generate Magic Links'}
            </Button>

            {links.length > 0 && (
              <div className="space-y-3">
                {links.map((linkData, index) => (
                  <div key={index} className="border rounded-lg p-4 space-y-2">
                    <div className="flex justify-between items-start">
                      <div>
                        <p className="font-semibold">{linkData.vehicle_number}</p>
                        {linkData.driver_name && (
                          <p className="text-sm text-gray-600">{linkData.driver_name}</p>
                        )}
                      </div>
                      <Badge variant="outline">Active</Badge>
                    </div>
                    
                    <div className="flex gap-2">
                      <Input
                        value={linkData.link}
                        readOnly
                        className="flex-1 text-sm"
                      />
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => copyToClipboard(linkData.link, index)}
                      >
                        {copiedId === index ? (
                          <CheckCircle2 className="h-4 w-4 text-green-600" />
                        ) : (
                          <Copy className="h-4 w-4" />
                        )}
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => shareViaWhatsApp(linkData.link, linkData.vehicle_number)}
                      >
                        WhatsApp
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </TabsContent>

          <TabsContent value="qr_code" className="space-y-4">
            <Button 
              onClick={() => generateLinks('qr_code')} 
              disabled={loading}
              className="w-full"
            >
              {loading ? 'Generating...' : 'Generate QR Codes'}
            </Button>

            {links.length > 0 && (
              <div className="grid grid-cols-2 gap-4">
                {links.map((linkData, index) => (
                  <div key={index} className="border rounded-lg p-4 space-y-2 text-center">
                    <p className="font-semibold text-sm">{linkData.vehicle_number}</p>
                    {linkData.qr_url && (
                      <img 
                        src={linkData.qr_url} 
                        alt={`QR Code for ${linkData.vehicle_number}`}
                        className="w-full h-auto"
                      />
                    )}
                    <Button
                      variant="outline"
                      size="sm"
                      className="w-full"
                      onClick={() => window.open(linkData.qr_url, '_blank')}
                    >
                      Download QR
                    </Button>
                  </div>
                ))}
              </div>
            )}
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
}

