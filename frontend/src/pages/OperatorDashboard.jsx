import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';
import { Truck, AlertCircle, TrendingUp, DollarSign, CheckCircle2, BarChart3, Settings, Plus } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Button } from '../components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import MobileBottomNav from '../components/MobileBottomNav';

export default function OperatorDashboard() {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [dashboard, setDashboard] = useState(null);
  const [fleet, setFleet] = useState([]);
  const [days, setDays] = useState(7);

  useEffect(() => {
    loadDashboard();
    loadFleet();
  }, [days]);

  const loadDashboard = async () => {
    try {
      const response = await api.get(`/operators/dashboard?days=${days}`);
      setDashboard(response.data);
    } catch (error) {
      console.error('Failed to load dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadFleet = async () => {
    try {
      const response = await api.get('/operators/fleet');
      setFleet(response.data || []);
    } catch (error) {
      console.error('Failed to load fleet:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (!dashboard) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
        <Card>
          <CardContent className="p-6 text-center">
            <p className="text-gray-600">No operator account found. Please complete onboarding.</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Operator Dashboard</h1>
            <p className="text-sm text-gray-600">Fleet operations overview</p>
          </div>
          <div className="flex gap-2">
            <Link to="/operator/fleet">
              <Button variant="outline" size="sm">
                <Truck className="h-4 w-4 mr-2" />
                Fleet
              </Button>
            </Link>
            <Link to="/operator/settings">
              <Button variant="outline" size="sm">
                <Settings className="h-4 w-4" />
              </Button>
            </Link>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-6 py-6 max-w-7xl">
        {/* Key Metrics */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Fleet Size</p>
                  <p className="text-2xl font-bold">{dashboard.fleet_size}</p>
                </div>
                <Truck className="h-8 w-8 text-blue-600" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Active Cases</p>
                  <p className="text-2xl font-bold">{dashboard.active_cases}</p>
                </div>
                <AlertCircle className="h-8 w-8 text-orange-600" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Financial Impact</p>
                  <p className="text-2xl font-bold">₹{dashboard.total_financial_impact?.toLocaleString() || 0}</p>
                </div>
                <DollarSign className="h-8 w-8 text-green-600" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Evidence Ready</p>
                  <p className="text-2xl font-bold">{dashboard.evidence_ready_cases}</p>
                  <p className="text-xs text-gray-500">
                    {dashboard.evidence_readiness_rate?.toFixed(0) || 0}%
                  </p>
                </div>
                <CheckCircle2 className="h-8 w-8 text-green-600" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Tabs */}
        <Tabs defaultValue="overview" className="space-y-4">
          <TabsList>
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="fleet">Fleet</TabsTrigger>
            <TabsTrigger value="drivers">Drivers</TabsTrigger>
            <TabsTrigger value="routes">Routes</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Cases by Route</CardTitle>
              </CardHeader>
              <CardContent>
                {Object.entries(dashboard.cases_by_route || {}).length > 0 ? (
                  <div className="space-y-2">
                    {Object.entries(dashboard.cases_by_route).map(([route, count]) => (
                      <div key={route} className="flex justify-between items-center p-2 border rounded">
                        <span className="font-medium">{route || "Unknown"}</span>
                        <Badge>{count} cases</Badge>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500 text-center py-4">No cases yet</p>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="fleet" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Fleet Vehicles ({fleet.length})</CardTitle>
              </CardHeader>
              <CardContent>
                {fleet.length > 0 ? (
                  <div className="space-y-2">
                    {fleet.map((vehicle) => (
                      <div key={vehicle._id || vehicle.id} className="flex justify-between items-center p-3 border rounded">
                        <div>
                          <p className="font-semibold">{vehicle.vehicle_number}</p>
                          {vehicle.driver_name && (
                            <p className="text-sm text-gray-600">{vehicle.driver_name}</p>
                          )}
                          {vehicle.route && (
                            <p className="text-xs text-gray-500">{vehicle.route}</p>
                          )}
                        </div>
                        <Badge variant={vehicle.status === 'active' ? 'default' : 'secondary'}>
                          {vehicle.status}
                        </Badge>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500 text-center py-4">No vehicles added yet</p>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="routes" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Route Performance</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-500 text-center py-4">Route analytics coming soon</p>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="drivers" className="space-y-4">
            <DriverLinksManager />
          </TabsContent>
        </Tabs>
      </div>

      <MobileBottomNav />
      <div className="h-16 md:hidden"></div>
    </div>
  );
}

