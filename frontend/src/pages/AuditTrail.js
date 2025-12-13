import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { ArrowLeft, FileText } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

export default function AuditTrail() {
  const [auditEntries, setAuditEntries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAuditTrail();
  }, []);

  const loadAuditTrail = async () => {
    try {
      const response = await api.get('/audit');
      setAuditEntries(response.data);
    } catch (error) {
      console.error('Failed to load audit trail:', error);
    } finally {
      setLoading(false);
    }
  };

  const getActionBadge = (action) => {
    const styles = {
      CASE_CREATED: 'bg-[hsl(var(--info))]/10 text-[hsl(var(--info))]',
      AI_DRAFT_GENERATED: 'bg-[hsl(var(--primary))]/10 text-[hsl(var(--primary))]',
      SECTION_EDITED: 'bg-[hsl(var(--warning))]/10 text-[hsl(var(--warning))]',
      SECTION_APPROVED: 'bg-[hsl(var(--success))]/10 text-[hsl(var(--success))]',
      DECISION_FINALIZED: 'bg-[hsl(var(--success))] text-[hsl(var(--success-foreground))]',
    };
    return (
      <span className={`px-2 py-1 rounded text-xs font-medium ${styles[action] || styles.CASE_CREATED}`}>
        {action.replace(/_/g, ' ')}
      </span>
    );
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-[hsl(var(--border))] bg-card">
        <div className="container mx-auto px-6 py-4">
          <Link
            to="/dashboard"
            className="inline-flex items-center gap-2 text-sm text-[hsl(var(--muted-foreground))] hover:text-foreground transition-colors mb-2"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Dashboard
          </Link>
          <h1 className="text-2xl font-bold">Audit Trail</h1>
          <p className="text-sm text-[hsl(var(--muted-foreground))]">
            Complete history of all decisions and actions
          </p>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8 max-w-4xl">
        {loading ? (
          <div className="text-center py-12">
            <p className="text-[hsl(var(--muted-foreground))]">Loading audit trail...</p>
          </div>
        ) : auditEntries.length === 0 ? (
          <div className="text-center py-12 bg-card border border-[hsl(var(--border))] rounded-lg">
            <FileText className="h-12 w-12 mx-auto mb-4 text-[hsl(var(--muted-foreground))]" />
            <h3 className="text-lg font-medium mb-2">No audit entries yet</h3>
            <p className="text-[hsl(var(--muted-foreground))]">Activity will appear here as you work</p>
          </div>
        ) : (
          <div className="space-y-4">
            {auditEntries.map((entry) => (
              <div
                key={entry._id}
                className="bg-card border border-[hsl(var(--border))] rounded-lg p-4"
                data-testid={`audit-entry-${entry._id}`}
              >
                <div className="flex justify-between items-start mb-2">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-1">
                      {getActionBadge(entry.action)}
                      <span className="text-sm font-medium">
                        Case #{entry.case_id.slice(-6).toUpperCase()}
                      </span>
                    </div>
                    <p className="text-sm text-[hsl(var(--muted-foreground))]">
                      by {entry.actor}
                    </p>
                  </div>
                  <span className="text-xs text-[hsl(var(--muted-foreground))]">
                    {formatDistanceToNow(new Date(entry.timestamp), { addSuffix: true })}
                  </span>
                </div>

                {entry.payload && Object.keys(entry.payload).length > 0 && (
                  <div className="mt-3 p-3 bg-[hsl(var(--muted))]/30 rounded text-xs">
                    {Object.entries(entry.payload).map(([key, value]) => (
                      <div key={key} className="mb-1">
                        <span className="font-medium">{key}:</span>{' '}
                        <span className="text-[hsl(var(--muted-foreground))]">
                          {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
