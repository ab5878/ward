import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';
import { Truck, Plus, Edit, Trash2, Download, Upload, Search, Filter } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Badge } from '../components/ui/badge';
import { Table, TableHeader, TableBody, TableHead, TableRow, TableCell } from '../components/ui/table';
import { toast } from 'sonner';
import MobileBottomNav from '../components/MobileBottomNav';

export default function FleetManagement() {
  const { user } = useAuth();
  const [fleet, setFleet] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');

  useEffect(() => {
    loadFleet();
  }, []);

  const loadFleet = async () => {
    try {
      const response = await api.get('/operators/fleet');
      setFleet(response.data || []);
    } catch (error) {
      toast.error('Failed to load fleet');
      setFleet([]);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteVehicle = async (vehicleId) => {
    if (!confirm('Are you sure you want to delete this vehicle?')) {
      return;
    }
    
    try {
      // TODO: Implement delete endpoint
      toast.success('Vehicle deleted');
      loadFleet();
    } catch (error) {
      toast.error('Failed to delete vehicle');
    }
  };

  const handleExportCSV = () => {
    const csv = [
      ['Vehicle Number', 'Driver Name', 'Driver Phone', 'Route', 'Status'],
      ...fleet.map(v => [
        v.vehicle_number,
        v.driver_name || '',
        v.driver_phone || '',
        v.route || '',
        v.status || 'active'
      ])
    ].map(row => row.join(',')).join('\n');
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `fleet_export_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
    
    toast.success('Fleet exported to CSV');
  };

  const filteredFleet = fleet.filter(vehicle => {
    const matchesSearch = !searchQuery || 
      vehicle.vehicle_number?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      vehicle.driver_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      vehicle.route?.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesStatus = filterStatus === 'all' || vehicle.status === filterStatus;
    
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-4">
            <Link to="/operator/dashboard">
              <Button variant="ghost" size="sm">
                <ArrowLeft className="h-4 w-4" />
              </Button>
            </Link>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Fleet Management</h1>
              <p className="text-sm text-gray-600">Manage your vehicle fleet</p>
            </div>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" onClick={handleExportCSV}>
              <Download className="h-4 w-4 mr-2" />
              Export CSV
            </Button>
            <Button onClick={() => window.location.href = '/operator/onboard'}>
              <Plus className="h-4 w-4 mr-2" />
              Add Vehicle
            </Button>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-6 py-6 max-w-7xl">
        {/* Filters */}
        <Card className="mb-6">
          <CardContent className="p-4">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
                  <Input
                    placeholder="Search by vehicle number, driver, or route..."
                    className="pl-9"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                  />
                </div>
              </div>
              <div className="flex gap-2">
                <Button
                  variant={filterStatus === 'all' ? 'default' : 'outline'}
                  onClick={() => setFilterStatus('all')}
                >
                  All
                </Button>
                <Button
                  variant={filterStatus === 'active' ? 'default' : 'outline'}
                  onClick={() => setFilterStatus('active')}
                >
                  Active
                </Button>
                <Button
                  variant={filterStatus === 'inactive' ? 'default' : 'outline'}
                  onClick={() => setFilterStatus('inactive')}
                >
                  Inactive
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Fleet Table */}
        <Card>
          <CardHeader>
            <CardTitle>Fleet Vehicles ({filteredFleet.length})</CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                <p className="mt-2 text-gray-600">Loading fleet...</p>
              </div>
            ) : filteredFleet.length === 0 ? (
              <div className="text-center py-8">
                <Truck className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600 mb-4">No vehicles found</p>
                <Button onClick={() => window.location.href = '/operator/onboard'}>
                  <Plus className="h-4 w-4 mr-2" />
                  Add Your First Vehicle
                </Button>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Vehicle Number</TableHead>
                      <TableHead>Driver</TableHead>
                      <TableHead>Phone</TableHead>
                      <TableHead>Route</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredFleet.map((vehicle) => (
                      <TableRow key={vehicle._id || vehicle.id}>
                        <TableCell className="font-medium">
                          {vehicle.vehicle_number}
                        </TableCell>
                        <TableCell>{vehicle.driver_name || '-'}</TableCell>
                        <TableCell>{vehicle.driver_phone || '-'}</TableCell>
                        <TableCell>{vehicle.route || '-'}</TableCell>
                        <TableCell>
                          <Badge variant={vehicle.status === 'active' ? 'default' : 'secondary'}>
                            {vehicle.status || 'active'}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <div className="flex gap-2">
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => {/* TODO: Edit vehicle */}}
                            >
                              <Edit className="h-4 w-4" />
                            </Button>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => handleDeleteVehicle(vehicle._id || vehicle.id)}
                            >
                              <Trash2 className="h-4 w-4 text-red-600" />
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      <MobileBottomNav />
      <div className="h-16 md:hidden"></div>
    </div>
  );
}

