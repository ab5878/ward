import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';
import { 
  Plus, LogOut, AlertTriangle, Mic, 
  LayoutList, Clock, AlertCircle, CheckCircle2, 
  Search, Filter, Code
} from 'lucide-react';
import { DisruptionRow } from '../components/DisruptionRow';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '../components/ui/tabs';
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from '../components/ui/select';
import {
  Table,
  TableHeader,
  TableBody,
  TableHead,
  TableRow,
} from '../components/ui/table';
import { Input } from '../components/ui/input';
import { Badge } from '../components/ui/badge';
import { Card, CardContent } from '../components/ui/card';
import { TooltipProvider } from '../components/ui/tooltip';

// Simplified Smart Views for Supply Chain "Exception Management"
const SMART_VIEWS = [
  { 
    id: 'needs_attention', 
    label: 'Needs Attention', 
    icon: AlertCircle,
    description: 'Cases waiting for your decision or action'
  },
  { 
    id: 'awaiting_stakeholders', 
    label: 'Waiting on Others', 
    icon: Clock,
    description: 'Outreach sent, waiting for replies'
  },
  { 
    id: 'all_active', 
    label: 'All Active', 
    icon: LayoutList,
    description: 'Full operational visibility'
  },
  { 
    id: 'resolved', 
    label: 'Resolved', 
    icon: CheckCircle2,
    description: 'Historical archive'
  }
];

export default function Dashboard() {
  const [cases, setCases] = useState([]);
  const [filteredCases, setFilteredCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeView, setActiveView] = useState('needs_attention');
  const [searchQuery, setSearchQuery] = useState('');
  const { logout, user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    loadCases();
  }, []);

  useEffect(() => {
    filterCases();
  }, [cases, activeView, searchQuery]);

  const loadCases = async () => {
    try {
      const response = await api.get('/cases');
      setCases(response.data);
    } catch (error) {
      console.error('Failed to load cases:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterCases = () => {
    let filtered = cases;

    // 1. Search Filter
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      filtered = filtered.filter(c => 
        c.description.toLowerCase().includes(q) ||
        c.disruption_details?.identifier?.toLowerCase().includes(q) ||
        c.disruption_details?.disruption_type?.toLowerCase().includes(q)
      );
    }

    // 2. Smart View Filters (The "Supply Chain Exception" Logic)
    switch (activeView) {
      case 'needs_attention':
        // Show cases where:
        // - User is owner AND state is DECISION_REQUIRED
        // - OR status is REPORTED (needs triage)
        filtered = filtered.filter(c => 
          (c.status === 'DECISION_REQUIRED' && c.decision_owner_email === user?.email) ||
          c.status === 'REPORTED' ||
          c.status === 'CLARIFIED'
        );
        break;
      
      case 'awaiting_stakeholders':
        // Active coordination implies waiting
        // Or specific states like IN_PROGRESS
        filtered = filtered.filter(c => 
          c.status === 'IN_PROGRESS' || 
          (c.coordination_status === 'outreach_sent')
        );
        break;

      case 'resolved':
        filtered = filtered.filter(c => c.status === 'RESOLVED');
        break;

      case 'all_active':
      default:
        filtered = filtered.filter(c => c.status !== 'RESOLVED');
        break;
    }

    setFilteredCases(filtered);
  };

  const handleSelectCase = (caseId) => {
    navigate(`/cases/${caseId}`);
  };

  // Calculate counts for badges
  const getCount = (viewId) => {
    if (!cases.length) return 0;
    
    switch (viewId) {
      case 'needs_attention':
        return cases.filter(c => 
          (c.status === 'DECISION_REQUIRED' && c.decision_owner_email === user?.email) ||
          c.status === 'REPORTED' ||
          c.status === 'CLARIFIED'
        ).length;
      case 'awaiting_stakeholders':
        return cases.filter(c => 
          c.status === 'IN_PROGRESS' || 
          (c.coordination_status === 'outreach_sent')
        ).length;
      case 'all_active':
        return cases.filter(c => c.status !== 'RESOLVED').length;
      case 'resolved':
        return cases.filter(c => c.status === 'RESOLVED').length;
      default: return 0;
    }
  };

  return (
    <TooltipProvider>
      <div className="min-h-screen bg-gray-50/50" data-testid="dashboard">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 sticky top-0 z-10 shadow-sm">
          <div className="container mx-auto px-6 h-16 flex justify-between items-center">
            <div className="flex items-center gap-2">
              <div className="bg-blue-600 w-8 h-8 rounded-lg flex items-center justify-center text-white font-bold">W</div>
              <h1 className="text-xl font-bold tracking-tight text-gray-900">Ward</h1>
            </div>
            
            <div className="flex items-center gap-6">
              <div className="relative w-64">
                <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-gray-400" />
                <Input 
                  placeholder="Search identifiers, types..." 
                  className="pl-9 h-9 bg-gray-100 border-none focus-visible:bg-white focus-visible:ring-1 focus-visible:ring-blue-600 transition-all"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
              
              <div className="h-6 w-px bg-gray-200"></div>

              <div className="flex items-center gap-3">
                <span className="text-sm font-medium text-gray-700">
                  {user?.email}
                </span>
                <button
                  onClick={logout}
                  className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-full transition-colors"
                  title="Logout"
                  data-testid="logout-button"
                >
                  <LogOut className="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>
        </header>

        <div className="container mx-auto px-6 py-8">
          {/* Top Actions & KPI Area */}
          <div className="flex justify-between items-end mb-8">
            <div>
              <h2 className="text-2xl font-semibold text-gray-900">Disruption Control</h2>
              <p className="text-sm text-gray-500 mt-1">
                Manage and coordinate active supply chain exceptions
              </p>
            </div>
            <div className="flex gap-3">
              <Link
                to="/settings/developer"
                className="flex items-center gap-2 px-4 py-2.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg shadow-sm hover:bg-gray-50 hover:text-gray-900 transition-all"
              >
                <Code className="h-4 w-4" />
                API
              </Link>
              <Link
                to="/dashboard/analytics"
                className="flex items-center gap-2 px-4 py-2.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg shadow-sm hover:bg-gray-50 hover:text-gray-900 transition-all"
              >
                <LayoutList className="h-4 w-4" />
                Analytics
              </Link>
              <Link
                to="/cases/voice"
                className="flex items-center gap-2 px-4 py-2.5 text-sm font-medium text-white bg-blue-600 rounded-lg shadow-sm hover:bg-blue-700 hover:shadow-md transition-all active:scale-95"
                data-testid="voice-case-button"
              >
                <Mic className="h-4 w-4" />
                Voice Report
              </Link>
              <Link
                to="/cases/new"
                className="flex items-center gap-2 px-4 py-2.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg shadow-sm hover:bg-gray-50 hover:text-gray-900 transition-all"
                data-testid="create-case-button"
              >
                <Plus className="h-4 w-4" />
                Manual Entry
              </Link>
            </div>
          </div>

          {/* Smart Views (Replaces 7 Tabs) */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            {SMART_VIEWS.map((view) => {
              const isActive = activeView === view.id;
              const count = getCount(view.id);
              const Icon = view.icon;
              
              return (
                <button
                  key={view.id}
                  onClick={() => setActiveView(view.id)}
                  className={`relative p-4 rounded-xl border text-left transition-all duration-200 ${
                    isActive 
                      ? 'bg-white border-blue-600 ring-1 ring-blue-600 shadow-md' 
                      : 'bg-white border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  <div className="flex justify-between items-start mb-2">
                    <div className={`p-2 rounded-lg ${isActive ? 'bg-blue-50 text-blue-600' : 'bg-gray-100 text-gray-500'}`}>
                      <Icon className="h-5 w-5" />
                    </div>
                    <Badge variant={isActive ? "default" : "secondary"} className="text-xs font-bold">
                      {count}
                    </Badge>
                  </div>
                  <h3 className={`font-semibold ${isActive ? 'text-gray-900' : 'text-gray-700'}`}>
                    {view.label}
                  </h3>
                  <p className="text-xs text-gray-500 mt-1 truncate">
                    {view.description}
                  </p>
                </button>
              );
            })}
          </div>

          {/* Main List Area */}
          <Card className="border-gray-200 shadow-sm overflow-hidden bg-white">
            <CardContent className="p-0">
              {loading ? (
                <div className="text-center py-20">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
                  <p className="text-gray-500">Loading disruptions...</p>
                </div>
              ) : filteredCases.length === 0 ? (
                <div className="text-center py-20 bg-gray-50/50">
                  <div className="bg-gray-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                    <CheckCircle2 className="h-8 w-8 text-gray-400" />
                  </div>
                  <h3 className="text-lg font-medium text-gray-900 mb-1">All clear</h3>
                  <p className="text-gray-500 mb-6">No disruptions found in this view.</p>
                  {activeView === 'all_active' && (
                    <Link
                      to="/cases/new"
                      className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded-md transition-colors"
                    >
                      Create your first disruption
                    </Link>
                  )}
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow className="bg-gray-50/50 hover:bg-gray-50/50">
                        <TableHead className="w-32 py-3 pl-6">State</TableHead>
                        <TableHead className="py-3">Description</TableHead>
                        <TableHead className="w-40 py-3">Owner</TableHead>
                        <TableHead className="w-40 py-3">Last Update</TableHead>
                        <TableHead className="w-24 text-right py-3 pr-6">Action</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {filteredCases.map((disruption) => (
                        <DisruptionRow
                          key={disruption._id}
                          disruption={disruption}
                          onSelect={handleSelectCase}
                        />
                      ))}
                    </TableBody>
                  </Table>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </TooltipProvider>
  );
}
