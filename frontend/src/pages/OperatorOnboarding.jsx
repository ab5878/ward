import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';
import { Building2, Truck, Upload, Link as LinkIcon, QrCode, CheckCircle2, ArrowRight } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { toast } from 'sonner';

export default function OperatorOnboarding() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  
  // Step 1: Company Info
  const [companyName, setCompanyName] = useState('');
  const [phone, setPhone] = useState('');
  const [fleetSize, setFleetSize] = useState('');
  
  // Step 2: Fleet Upload
  const [uploadMethod, setUploadMethod] = useState('manual'); // manual, csv, api
  const [vehicles, setVehicles] = useState([{ vehicle_number: '', driver_name: '', driver_phone: '', route: '' }]);
  const [csvFile, setCsvFile] = useState(null);
  
  // Step 3: Driver Onboarding
  const [onboardingMethod, setOnboardingMethod] = useState('magic_link'); // magic_link, qr_code

  const handleCompanySubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      // Create operator account
      const response = await api.post('/operators/create', {
        company_name: companyName,
        phone: phone,
        fleet_size: parseInt(fleetSize) || 0
      });
      
      toast.success('Company profile created!');
      setStep(2);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to create company profile');
    } finally {
      setLoading(false);
    }
  };

  const handleAddVehicle = () => {
    setVehicles([...vehicles, { vehicle_number: '', driver_name: '', driver_phone: '', route: '' }]);
  };

  const handleVehicleChange = (index, field, value) => {
    const updated = [...vehicles];
    updated[index][field] = value;
    setVehicles(updated);
  };

  const handleRemoveVehicle = (index) => {
    setVehicles(vehicles.filter((_, i) => i !== index));
  };

  const handleFleetSubmit = async () => {
    setLoading(true);
    
    try {
      if (uploadMethod === 'manual') {
        // Add vehicles one by one
        for (const vehicle of vehicles) {
          if (vehicle.vehicle_number) {
            await api.post('/operators/fleet/add', vehicle);
          }
        }
        toast.success(`${vehicles.length} vehicles added!`);
      } else if (uploadMethod === 'csv' && csvFile) {
        // Upload CSV
        const formData = new FormData();
        formData.append('file', csvFile);
        const response = await api.post('/operators/fleet/bulk-upload', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        toast.success(`Uploaded: ${response.data.success} vehicles`);
      }
      
      setStep(3);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to add fleet');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateLinks = async () => {
    setLoading(true);
    
    try {
      const response = await api.post('/operators/drivers/generate-links', {
        method: onboardingMethod
      });
      
      toast.success('Driver links generated!');
      // Show links/QR codes
      navigate('/operator/dashboard');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to generate links');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-6 max-w-4xl">
        {/* Progress Steps */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            {[1, 2, 3].map((s) => (
              <div key={s} className="flex items-center flex-1">
                <div className={`flex items-center justify-center w-10 h-10 rounded-full ${
                  s <= step ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-500'
                }`}>
                  {s < step ? <CheckCircle2 className="h-6 w-6" /> : s}
                </div>
                {s < 3 && (
                  <div className={`flex-1 h-1 mx-2 ${
                    s < step ? 'bg-blue-600' : 'bg-gray-200'
                  }`} />
                )}
              </div>
            ))}
          </div>
          <div className="flex justify-between text-sm text-gray-600">
            <span>Company Info</span>
            <span>Add Fleet</span>
            <span>Onboard Drivers</span>
          </div>
        </div>

        {/* Step 1: Company Info */}
        {step === 1 && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Building2 className="h-6 w-6" />
                Company Information
              </CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleCompanySubmit} className="space-y-4">
                <div>
                  <Label htmlFor="companyName">Company Name *</Label>
                  <Input
                    id="companyName"
                    value={companyName}
                    onChange={(e) => setCompanyName(e.target.value)}
                    required
                    placeholder="ABC Transporters Pvt Ltd"
                  />
                </div>
                
                <div>
                  <Label htmlFor="phone">Phone Number *</Label>
                  <Input
                    id="phone"
                    type="tel"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    required
                    placeholder="+91-98765-43210"
                  />
                </div>
                
                <div>
                  <Label htmlFor="fleetSize">Approximate Fleet Size</Label>
                  <Input
                    id="fleetSize"
                    type="number"
                    value={fleetSize}
                    onChange={(e) => setFleetSize(e.target.value)}
                    placeholder="50"
                  />
                </div>
                
                <Button type="submit" disabled={loading} className="w-full">
                  Continue <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </form>
            </CardContent>
          </Card>
        )}

        {/* Step 2: Add Fleet */}
        {step === 2 && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Truck className="h-6 w-6" />
                Add Your Fleet
              </CardTitle>
            </CardHeader>
            <CardContent>
              <Tabs value={uploadMethod} onValueChange={setUploadMethod}>
                <TabsList className="grid w-full grid-cols-3">
                  <TabsTrigger value="manual">Manual Entry</TabsTrigger>
                  <TabsTrigger value="csv">CSV Upload</TabsTrigger>
                  <TabsTrigger value="api">API Integration</TabsTrigger>
                </TabsList>
                
                <TabsContent value="manual" className="space-y-4">
                  {vehicles.map((vehicle, index) => (
                    <div key={index} className="grid grid-cols-4 gap-2 p-4 border rounded-lg">
                      <Input
                        placeholder="Vehicle Number"
                        value={vehicle.vehicle_number}
                        onChange={(e) => handleVehicleChange(index, 'vehicle_number', e.target.value)}
                      />
                      <Input
                        placeholder="Driver Name"
                        value={vehicle.driver_name}
                        onChange={(e) => handleVehicleChange(index, 'driver_name', e.target.value)}
                      />
                      <Input
                        placeholder="Driver Phone"
                        value={vehicle.driver_phone}
                        onChange={(e) => handleVehicleChange(index, 'driver_phone', e.target.value)}
                      />
                      <div className="flex gap-2">
                        <Input
                          placeholder="Route"
                          value={vehicle.route}
                          onChange={(e) => handleVehicleChange(index, 'route', e.target.value)}
                        />
                        {vehicles.length > 1 && (
                          <Button
                            type="button"
                            variant="ghost"
                            onClick={() => handleRemoveVehicle(index)}
                          >
                            ×
                          </Button>
                        )}
                      </div>
                    </div>
                  ))}
                  <Button type="button" variant="outline" onClick={handleAddVehicle}>
                    + Add Another Vehicle
                  </Button>
                </TabsContent>
                
                <TabsContent value="csv" className="space-y-4">
                  <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                    <Upload className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                    <Label htmlFor="csvFile" className="cursor-pointer">
                      <span className="text-blue-600 hover:underline">Click to upload CSV</span>
                      <Input
                        id="csvFile"
                        type="file"
                        accept=".csv"
                        onChange={(e) => setCsvFile(e.target.files[0])}
                        className="hidden"
                      />
                    </Label>
                    <p className="text-sm text-gray-500 mt-2">
                      Format: vehicle_number,driver_name,driver_phone,route
                    </p>
                  </div>
                  {csvFile && (
                    <div className="text-sm text-green-600">
                      ✓ {csvFile.name} selected
                    </div>
                  )}
                </TabsContent>
                
                <TabsContent value="api" className="space-y-4">
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                    <h3 className="font-semibold mb-2">API Integration</h3>
                    <p className="text-sm text-gray-600 mb-4">
                      Connect your TMS/ERP to Ward via API. Get your API key from Settings after onboarding.
                    </p>
                    <Button variant="outline" onClick={() => window.open('/docs/api', '_blank')}>
                      View API Documentation
                    </Button>
                  </div>
                </TabsContent>
              </Tabs>
              
              <div className="flex gap-4 mt-6">
                <Button variant="outline" onClick={() => setStep(1)}>
                  Back
                </Button>
                <Button onClick={handleFleetSubmit} disabled={loading} className="flex-1">
                  Continue <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Step 3: Onboard Drivers */}
        {step === 3 && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <LinkIcon className="h-6 w-6" />
                Onboard Your Drivers
              </CardTitle>
            </CardHeader>
            <CardContent>
              <Tabs value={onboardingMethod} onValueChange={setOnboardingMethod}>
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="magic_link">Magic Links</TabsTrigger>
                  <TabsTrigger value="qr_code">QR Codes</TabsTrigger>
                </TabsList>
                
                <TabsContent value="magic_link" className="space-y-4">
                  <div className="bg-green-50 border border-green-200 rounded-lg p-6">
                    <h3 className="font-semibold mb-2">Magic Links (Recommended)</h3>
                    <p className="text-sm text-gray-600 mb-4">
                      Generate unique links for each driver. Share via WhatsApp/SMS. No login required!
                    </p>
                    <ul className="text-sm space-y-2 mb-4">
                      <li>✓ One link per vehicle</li>
                      <li>✓ Works for 30 days</li>
                      <li>✓ No app installation needed</li>
                      <li>✓ Works on any smartphone</li>
                    </ul>
                  </div>
                </TabsContent>
                
                <TabsContent value="qr_code" className="space-y-4">
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                    <h3 className="font-semibold mb-2">QR Codes</h3>
                    <p className="text-sm text-gray-600 mb-4">
                      Print QR codes and stick them in vehicles. Driver scans to open Ward app.
                    </p>
                    <ul className="text-sm space-y-2 mb-4">
                      <li>✓ One QR code per vehicle</li>
                      <li>✓ No internet needed to scan</li>
                      <li>✓ Works offline</li>
                      <li>✓ Easy to replace</li>
                    </ul>
                  </div>
                </TabsContent>
              </Tabs>
              
              <div className="flex gap-4 mt-6">
                <Button variant="outline" onClick={() => setStep(2)}>
                  Back
                </Button>
                <Button onClick={handleGenerateLinks} disabled={loading} className="flex-1">
                  Generate {onboardingMethod === 'magic_link' ? 'Links' : 'QR Codes'}
                </Button>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}

