import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';
import { Plus, LogOut, AlertTriangle, Mic } from 'lucide-react';
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
import { TooltipProvider } from '../components/ui/tooltip';

const LIFECYCLE_STATES = [
  { value: 'ALL', label: 'All States' },
  { value: 'REPORTED', label: 'Reported' },
  { value: 'CLARIFIED', label: 'Clarified' },
  { value: 'DECISION_REQUIRED', label: 'Decision Required' },
  { value: 'DECIDED', label: 'Decided' },
  { value: 'IN_PROGRESS', label: 'In Progress' },
  { value: 'RESOLVED', label: 'Resolved' },
];

export default function Dashboard() {
  const [cases, setCases] = useState([]);
  const [filteredCases, setFilteredCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('ALL');
  const [ownerFilter, setOwnerFilter] = useState('all');
  const { logout, user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    loadCases();
  }, []);

  useEffect(() => {
    filterCases();
  }, [cases, activeTab, ownerFilter]);

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

    // Filter by state
    if (activeTab !== 'ALL') {
      filtered = filtered.filter((c) => c.status === activeTab);
    }

    // Filter by owner
    if (ownerFilter === 'mine') {
      filtered = filtered.filter(
        (c) => c.decision_owner_email === user?.email
      );
    } else if (ownerFilter === 'unassigned') {
      filtered = filtered.filter((c) => !c.decision_owner_email);
    }

    setFilteredCases(filtered);
  };

  const handleSelectCase = (caseId) => {
    navigate(`/cases/${caseId}`);
  };

  return (
    <TooltipProvider>
      <div className="min-h-screen bg-background" data-testid="dashboard">
        {/* Header */}
        <header className="border-b border-border bg-card sticky top-0 z-10">
          <div className="container mx-auto px-6 py-4 flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold tracking-tight">Ward v0</h1>
              <p className="text-sm text-muted-foreground">
                Disruption Lifecycle Management
              </p>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-muted-foreground">
                {user?.email}
              </span>
              <button
                onClick={logout}
                className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
                data-testid="logout-button"
              >
                <LogOut className="h-4 w-4" />
                Logout
              </button>
            </div>
          </div>
        </header>

        <div className="container mx-auto px-6 py-8">
          {/* Actions Bar */}
          <div className="flex justify-between items-center mb-6">
            <div>
              <h2 className="text-xl font-semibold tracking-tight">Active Disruptions</h2>
              <p className="text-sm text-muted-foreground">
                {filteredCases.length} disruption{filteredCases.length !== 1 ? 's' : ''}
              </p>
            </div>
            <div className="flex gap-3">
              <Link
                to="/cases/new"
                className="flex items-center gap-2 px-4 py-2 text-sm border border-border rounded-md hover:bg-secondary transition-colors"
                data-testid="create-case-button"
              >
                <Plus className="h-4 w-4" />
                New Disruption
              </Link>
              <Link
                to="/cases/voice"
                className="flex items-center gap-2 px-4 py-2 text-sm bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
                data-testid="voice-case-button"
              >
                <Mic className="h-4 w-4" />
                Voice Report
              </Link>
            </div>
          </div>

          {/* Filters */}
          <div className="mb-6 space-y-4">
            <Tabs value={activeTab} onValueChange={setActiveTab}>
              <TabsList className="grid w-full grid-cols-7">
                {LIFECYCLE_STATES.map((state) => (
                  <TabsTrigger
                    key={state.value}
                    value={state.value}
                    data-testid={`state-tab-${state.value}`}
                  >
                    {state.label}
                  </TabsTrigger>
                ))}
              </TabsList>
            </Tabs>

            <div className="flex gap-3">
              <Select value={ownerFilter} onValueChange={setOwnerFilter}>
                <SelectTrigger className="w-48" data-testid="filter-owner">
                  <SelectValue placeholder="Filter by owner" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All owners</SelectItem>
                  <SelectItem value="mine">My disruptions</SelectItem>
                  <SelectItem value="unassigned">Unassigned</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Cases Table */}
          {loading ? (
            <div className="text-center py-12">
              <p className="text-muted-foreground">Loading disruptions...</p>
            </div>
          ) : filteredCases.length === 0 ? (
            <div className="text-center py-12 bg-card border border-border rounded-lg">
              <AlertTriangle className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
              <h3 className="text-lg font-medium mb-2">No disruptions found</h3>
              <p className="text-muted-foreground mb-4">
                {activeTab === 'ALL'
                  ? 'Create your first disruption to get started'
                  : `No disruptions in ${activeTab.replace('_', ' ')} state`}
              </p>
              <Link
                to="/cases/new"
                className="inline-flex items-center gap-2 px-4 py-2 text-sm bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
              >
                <Plus className="h-4 w-4" />
                Create Disruption
              </Link>
            </div>
          ) : (
            <div className="bg-card border border-border rounded-lg overflow-hidden">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-32">State</TableHead>
                    <TableHead>Description</TableHead>
                    <TableHead className="w-40">Owner</TableHead>
                    <TableHead className="w-32">Last Event</TableHead>
                    <TableHead className="w-32">Location</TableHead>
                    <TableHead className="w-48">Updated (IST)</TableHead>
                    <TableHead className="w-24 text-right">Actions</TableHead>
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
        </div>
      </div>
    </TooltipProvider>
  );
}
