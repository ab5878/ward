import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';
import { Plus, LogOut, AlertTriangle, FileText, Clock } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

export default function Dashboard() {
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const { logout, user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    loadCases();
  }, []);

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

  const getStatusBadge = (status) => {
    const styles = {
      draft: 'bg-[hsl(var(--muted))] text-[hsl(var(--muted-foreground))]',
      reviewing: 'bg-[hsl(var(--info))]/10 text-[hsl(var(--info))]',
      finalized: 'bg-[hsl(var(--success))]/10 text-[hsl(var(--success))]',
    };
    return (
      <span className={`px-2 py-1 rounded text-xs font-medium ${styles[status] || styles.draft}`}>
        {status?.toUpperCase() || 'DRAFT'}
      </span>
    );
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-[hsl(var(--border))] bg-card">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold">Ward v0</h1>
            <p className="text-sm text-[hsl(var(--muted-foreground))]">
              Logistics Decision Support
            </p>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-[hsl(var(--muted-foreground))]">
              {user?.email}
            </span>
            <button
              onClick={logout}
              className="flex items-center gap-2 text-sm text-[hsl(var(--muted-foreground))] hover:text-foreground transition-colors"
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
        <div className="flex justify-between items-center mb-8">
          <div>
            <h2 className="text-xl font-semibold">Active Disruptions</h2>
            <p className="text-sm text-[hsl(var(--muted-foreground))]">
              Manage ongoing disruption decisions
            </p>
          </div>
          <div className="flex gap-3">
            <Link
              to="/audit"
              className="flex items-center gap-2 px-4 py-2 text-sm border border-[hsl(var(--border))] rounded-md hover:bg-[hsl(var(--secondary))] transition-colors"
              data-testid="audit-trail-link"
            >
              <FileText className="h-4 w-4" />
              Audit Trail
            </Link>
            <Link
              to="/cases/new"
              className="flex items-center gap-2 px-4 py-2 text-sm border border-[hsl(var(--border))] rounded-md hover:bg-[hsl(var(--secondary))] transition-colors"
              data-testid="create-case-button"
            >
              <Plus className="h-4 w-4" />
              Type Disruption
            </Link>
            <Link
              to="/cases/voice"
              className="flex items-center gap-2 px-4 py-2 text-sm bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] rounded-md hover:bg-[hsl(var(--primary))]/90 transition-colors"
              data-testid="voice-case-button"
            >
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
              Voice Disruption
            </Link>
          </div>
        </div>

        {/* Cases List */}
        {loading ? (
          <div className="text-center py-12">
            <p className="text-[hsl(var(--muted-foreground))]">Loading cases...</p>
          </div>
        ) : cases.length === 0 ? (
          <div className="text-center py-12 bg-card border border-[hsl(var(--border))] rounded-lg">
            <AlertTriangle className="h-12 w-12 mx-auto mb-4 text-[hsl(var(--muted-foreground))]" />
            <h3 className="text-lg font-medium mb-2">No disruptions yet</h3>
            <p className="text-[hsl(var(--muted-foreground))] mb-4">
              Create your first disruption case to get started
            </p>
            <Link
              to="/cases/new"
              className="inline-flex items-center gap-2 px-4 py-2 text-sm bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] rounded-md hover:bg-[hsl(var(--primary))]/90 transition-colors"
            >
              <Plus className="h-4 w-4" />
              Create Disruption
            </Link>
          </div>
        ) : (
          <div className="grid gap-4">
            {cases.map((caseItem) => (
              <div
                key={caseItem._id}
                className="bg-card border border-[hsl(var(--border))] rounded-lg p-5 hover:border-[hsl(var(--primary))] transition-colors cursor-pointer"
                onClick={() => navigate(`/cases/${caseItem._id}`)}
                data-testid={`case-item-${caseItem._id}`}
              >
                <div className="flex justify-between items-start mb-3">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="font-semibold">
                        Case #{caseItem._id.slice(-6).toUpperCase()}
                      </h3>
                      {getStatusBadge(caseItem.status)}
                    </div>
                    <p className="text-sm text-[hsl(var(--muted-foreground))] line-clamp-2">
                      {caseItem.description}
                    </p>
                  </div>
                </div>

                <div className="flex items-center justify-between text-xs text-[hsl(var(--muted-foreground))]">
                  <div className="flex items-center gap-4">
                    {caseItem.shipment_identifiers?.ids?.length > 0 && (
                      <span>
                        Shipments: {caseItem.shipment_identifiers.ids.join(', ')}
                      </span>
                    )}
                    {caseItem.shipment_identifiers?.carriers?.length > 0 && (
                      <span>
                        Carriers: {caseItem.shipment_identifiers.carriers.join(', ')}
                      </span>
                    )}
                  </div>
                  <div className="flex items-center gap-1">
                    <Clock className="h-3 w-3" />
                    {formatDistanceToNow(new Date(caseItem.created_at), { addSuffix: true })}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
