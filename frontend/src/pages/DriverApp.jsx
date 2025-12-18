import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';
import VoiceRecorder from '../components/VoiceRecorder';
import { Mic, CheckCircle2, Loader2, AlertCircle } from 'lucide-react';
import { Card, CardContent } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { toast } from 'sonner';

/**
 * Driver Mobile App (No Login Required)
 * Accessed via magic link: /driver/{token}
 * Zero-friction interface for drivers to report disruptions
 */
export default function DriverApp() {
  const { token } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [vehicleInfo, setVehicleInfo] = useState(null);
  const [reporting, setReporting] = useState(false);
  const [lastReport, setLastReport] = useState(null);

  useEffect(() => {
    loadVehicleInfo();
  }, [token]);

  const loadVehicleInfo = async () => {
    try {
      const response = await api.get(`/driver/verify/${token}`);
      setVehicleInfo(response.data);
    } catch (error) {
      toast.error('Invalid or expired link');
      // Redirect to error page or show error
    } finally {
      setLoading(false);
    }
  };

  const handleVoiceRecording = async (audioData) => {
    setReporting(true);
    try {
      const response = await api.post('/driver/report', {
        token: token,
        audio_base64: audioData.audio_base64,
        audio_format: audioData.audio_format,
        language_code: audioData.language_code
      });
      
      setLastReport({
        case_id: response.data.case_id,
        timestamp: new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' })
      });
      
      toast.success('Report submitted successfully!');
    } catch (error) {
      toast.error('Failed to submit report. Please try again.');
    } finally {
      setReporting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
      </div>
    );
  }

  if (!vehicleInfo) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
        <Card className="max-w-md w-full">
          <CardContent className="p-6 text-center">
            <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
            <h2 className="text-xl font-bold mb-2">Link Expired</h2>
            <p className="text-gray-600 mb-4">
              This link has expired or is invalid. Please contact your operator for a new link.
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-md mx-auto">
          <h1 className="text-2xl font-bold text-gray-900">Ward</h1>
          <p className="text-sm text-gray-600">Report Disruption</p>
        </div>
      </div>

      {/* Vehicle Info */}
      <div className="px-6 py-4">
        <div className="max-w-md mx-auto">
          <Card className="bg-white">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Vehicle</p>
                  <p className="text-lg font-semibold">{vehicleInfo.vehicle_number}</p>
                </div>
                {vehicleInfo.driver_name && (
                  <div className="text-right">
                    <p className="text-sm text-gray-500">Driver</p>
                    <p className="text-lg font-semibold">{vehicleInfo.driver_name}</p>
                  </div>
                )}
              </div>
              {vehicleInfo.route && (
                <div className="mt-2 pt-2 border-t">
                  <p className="text-sm text-gray-500">Route</p>
                  <p className="text-sm font-medium">{vehicleInfo.route}</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Main Content */}
      <div className="px-6 py-6">
        <div className="max-w-md mx-auto">
          <Card className="bg-white">
            <CardContent className="p-6">
              <div className="text-center mb-6">
                <Mic className="h-16 w-16 text-blue-600 mx-auto mb-4" />
                <h2 className="text-2xl font-bold text-gray-900 mb-2">
                  Report a Problem
                </h2>
                <p className="text-gray-600">
                  Tap the button below and speak in your language. We'll capture everything automatically.
                </p>
              </div>

              <VoiceRecorder
                onRecordingComplete={handleVoiceRecording}
                language="hi-IN" // Default to Hindi, can be changed
              />

              {lastReport && (
                <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
                  <div className="flex items-start gap-3">
                    <CheckCircle2 className="h-5 w-5 text-green-600 mt-0.5" />
                    <div>
                      <p className="font-semibold text-green-900">Report Submitted!</p>
                      <p className="text-sm text-green-700 mt-1">
                        Case ID: {lastReport.case_id}
                      </p>
                      <p className="text-xs text-green-600 mt-1">
                        {lastReport.timestamp}
                      </p>
                    </div>
                  </div>
                </div>
              )}

              <div className="mt-6 text-center">
                <p className="text-xs text-gray-500">
                  Your location and vehicle details are automatically captured.
                  No typing required.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Footer */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-6 py-3">
        <p className="text-xs text-center text-gray-500">
          Powered by Ward • No login required
        </p>
      </div>
    </div>
  );
}

