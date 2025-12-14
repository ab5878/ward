import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, Legend } from 'recharts';
import { ArrowUpRight, Clock, AlertOctagon, CheckCircle, Loader2, ShieldCheck } from 'lucide-react';
import api from '../services/api';
import { Link } from 'react-router-dom';

export default function AnalyticsDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        const response = await api.get('/analytics/dashboard?days=30');
        setData(response.data);
      } catch (error) {
        console.error("Failed to load analytics", error);
        setError("Failed to load analytics data.");
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50/50">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin text-blue-600 mx-auto mb-2" />
          <p className="text-gray-500">Calculating strategic metrics...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50/50">
        <div className="text-center text-red-600">
          <AlertOctagon className="h-8 w-8 mx-auto mb-2" />
          <p>{error}</p>
          <button onClick={() => window.location.reload()} className="text-blue-600 underline mt-2">Retry</button>
        </div>
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="min-h-screen bg-gray-50/50 p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Strategic Analytics</h1>
            <p className="text-gray-500">Performance metrics for the last 30 days</p>
          </div>
          <Link to="/dashboard" className="text-blue-600 hover:underline">Back to Operations</Link>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <KpiCard 
            title="Avg Time to Evidence" 
            value={`${data.kpis.avg_ttde_minutes} min`} 
            icon={ShieldCheck}
            trend="Target: <60 min"
            color="text-emerald-600"
            bg="bg-emerald-50"
          />
          <KpiCard 
            title="Avg Resolution Time" 
            value={`${data.kpis.avg_resolution_hours}h`} 
            icon={Clock}
            trend="-8% faster"
            color="text-amber-600"
            bg="bg-amber-50"
          />
          <KpiCard 
            title="Resolution Rate" 
            value={`${data.kpis.resolution_rate}%`} 
            icon={CheckCircle}
            trend="Steady"
            color="text-blue-600"
            bg="bg-blue-50"
          />
          <KpiCard 
            title="Open Cases" 
            value={data.kpis.open_cases} 
            icon={ArrowUpRight}
            trend="Active now"
            color="text-purple-600"
            bg="bg-purple-50"
          />
        </div>

        {/* Charts Row 1 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <Card className="shadow-sm border-gray-200">
            <CardHeader>
              <CardTitle className="text-gray-800">Disruptions by Type</CardTitle>
            </CardHeader>
            <CardContent>
              <div style={{ width: '100%', height: 300 }}>
                <ResponsiveContainer>
                  <BarChart data={data.breakdown} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} stroke="#e5e7eb" />
                    <XAxis type="number" hide />
                    <YAxis 
                      dataKey="name" 
                      type="category" 
                      width={120} 
                      tick={{fontSize: 11, fill: '#6b7280'}} 
                      tickFormatter={(val) => val.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    />
                    <Tooltip 
                      contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}}
                      cursor={{fill: '#f3f4f6'}}
                    />
                    <Bar dataKey="value" fill="#3b82f6" radius={[0, 4, 4, 0]} barSize={24} name="Count" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          <Card className="shadow-sm border-gray-200">
            <CardHeader>
              <CardTitle className="text-gray-800">Daily Incident Volume</CardTitle>
            </CardHeader>
            <CardContent>
              <div style={{ width: '100%', height: 300 }}>
                <ResponsiveContainer>
                  <LineChart data={data.trends} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
                    <XAxis 
                      dataKey="date" 
                      tick={{fontSize: 10, fill: '#6b7280'}} 
                      tickFormatter={(val) => val.slice(8)} // Show DD only
                      interval={2}
                    />
                    <YAxis tick={{fontSize: 11, fill: '#6b7280'}} />
                    <Tooltip 
                      contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="count" 
                      stroke="#8b5cf6" 
                      strokeWidth={3} 
                      dot={false}
                      activeDot={{r: 6}}
                      name="Incidents"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

function KpiCard({ title, value, icon: Icon, trend, color, bg }) {
  return (
    <Card className="border-gray-200 shadow-sm hover:shadow-md transition-shadow">
      <CardContent className="p-6">
        <div className="flex justify-between items-start">
          <div>
            <p className="text-sm font-medium text-gray-500 uppercase tracking-wide">{title}</p>
            <h3 className="text-3xl font-extrabold mt-2 text-gray-900">{value}</h3>
          </div>
          <div className={`p-3 rounded-xl ${bg} ${color}`}>
            <Icon className="h-6 w-6" />
          </div>
        </div>
        <div className="mt-4 flex items-center text-xs text-gray-500">
          <span className="text-green-600 font-bold mr-2 bg-green-50 px-1.5 py-0.5 rounded">{trend}</span>
          <span>from previous period</span>
        </div>
      </CardContent>
    </Card>
  );
}
