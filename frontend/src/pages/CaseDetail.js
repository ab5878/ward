import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import { ArrowLeft, Loader2, AlertTriangle, Check, Lock, Unlock } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

export default function CaseDetail() {
  const { caseId } = useParams();
  const [caseData, setCaseData] = useState(null);
  const [draft, setDraft] = useState(null);
  const [approvals, setApprovals] = useState([]);
  const [decision, setDecision] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [selectedAlternative, setSelectedAlternative] = useState('');
  const [overrideRationale, setOverrideRationale] = useState('');
  const [showOverrideModal, setShowOverrideModal] = useState(false);
  const [finalizing, setFinalizing] = useState(false);

  useEffect(() => {
    loadCase();
  }, [caseId]);

  const loadCase = async () => {
    try {
      const response = await api.get(`/cases/${caseId}`);
      setCaseData(response.data.case);
      setDraft(response.data.draft);
      setApprovals(response.data.approvals || []);
      setDecision(response.data.decision);
    } catch (error) {
      console.error('Failed to load case:', error);
    } finally {
      setLoading(false);
    }
  };

  const generateDraft = async () => {
    setGenerating(true);
    try {
      const response = await api.post(`/cases/${caseId}/ai_draft`);
      setDraft(response.data);
      await loadCase();
    } catch (error) {
      alert('Failed to generate AI draft: ' + (error.response?.data?.detail || error.message));
    } finally {
      setGenerating(false);
    }
  };

  const approveSection = async (sectionKey) => {
    try {
      await api.post(`/cases/${caseId}/sections/${sectionKey}/approve`);
      await loadCase();
    } catch (error) {
      alert('Failed to approve section: ' + (error.response?.data?.detail || error.message));
    }
  };

  const isSectionApproved = (sectionKey) => {
    return approvals.some(a => a.section_key === sectionKey);
  };

  const handleFinalizeClick = () => {
    if (!selectedAlternative) {
      alert('Please select an alternative');
      return;
    }

    const recommendedChoice = draft?.recommendation?.choice || '';
    const isOverride = selectedAlternative.toLowerCase() !== recommendedChoice.toLowerCase();

    if (isOverride) {
      setShowOverrideModal(true);
    } else {
      finalize();
    }
  };

  const finalize = async () => {
    setFinalizing(true);
    try {
      await api.post(`/cases/${caseId}/finalize`, {
        selected_alternative: selectedAlternative,
        override_rationale: overrideRationale || null,
      });
      await loadCase();
      setShowOverrideModal(false);
    } catch (error) {
      alert('Failed to finalize decision: ' + (error.response?.data?.detail || error.message));
    } finally {
      setFinalizing(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-[hsl(var(--primary))]" />
      </div>
    );
  }

  if (!caseData) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <AlertTriangle className="h-12 w-12 mx-auto mb-4 text-[hsl(var(--muted-foreground))]" />
          <p className="text-[hsl(var(--muted-foreground))]">Case not found</p>
          <Link to="/dashboard" className="text-[hsl(var(--primary))] hover:underline mt-4 inline-block">
            Back to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-[hsl(var(--border))] bg-card sticky top-0 z-10">
        <div className="container mx-auto px-6 py-4">
          <Link
            to="/dashboard"
            className="inline-flex items-center gap-2 text-sm text-[hsl(var(--muted-foreground))] hover:text-foreground transition-colors mb-2"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Dashboard
          </Link>
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold">Case #{caseId.slice(-6).toUpperCase()}</h1>
              <p className="text-sm text-[hsl(var(--muted-foreground))]">
                Created {formatDistanceToNow(new Date(caseData.created_at), { addSuffix: true })}
              </p>
            </div>
            <div className="flex items-center gap-2">
              <span className={`px-3 py-1 rounded text-sm font-medium ${
                caseData.status === 'finalized'
                  ? 'bg-[hsl(var(--success))]/10 text-[hsl(var(--success))]'
                  : caseData.status === 'reviewing'
                  ? 'bg-[hsl(var(--info))]/10 text-[hsl(var(--info))]'
                  : 'bg-[hsl(var(--muted))] text-[hsl(var(--muted-foreground))]'
              }`}>
                {caseData.status?.toUpperCase() || 'DRAFT'}
              </span>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8">
        {/* Case Description */}
        <div className="bg-card border border-[hsl(var(--border))] rounded-lg p-6 mb-6">
          <h2 className="text-lg font-semibold mb-3">Disruption Description</h2>
          <p className="text-[hsl(var(--muted-foreground))]" data-testid="case-description">
            {caseData.description}
          </p>
          
          {/* Shipment Info */}
          {(caseData.shipment_identifiers?.ids?.length > 0 ||
            caseData.shipment_identifiers?.routes?.length > 0 ||
            caseData.shipment_identifiers?.carriers?.length > 0) && (
            <div className="mt-4 pt-4 border-t border-[hsl(var(--border))]">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                {caseData.shipment_identifiers?.ids?.length > 0 && (
                  <div>
                    <span className="font-medium">Shipments:</span>
                    <p className="text-[hsl(var(--muted-foreground))]">
                      {caseData.shipment_identifiers.ids.join(', ')}
                    </p>
                  </div>
                )}
                {caseData.shipment_identifiers?.routes?.length > 0 && (
                  <div>
                    <span className="font-medium">Routes:</span>
                    <p className="text-[hsl(var(--muted-foreground))]">
                      {caseData.shipment_identifiers.routes.join(', ')}
                    </p>
                  </div>
                )}
                {caseData.shipment_identifiers?.carriers?.length > 0 && (
                  <div>
                    <span className="font-medium">Carriers:</span>
                    <p className="text-[hsl(var(--muted-foreground))]">
                      {caseData.shipment_identifiers.carriers.join(', ')}
                    </p>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Generate AI Draft Button */}
        {!draft && !decision && (
          <div className="text-center py-8">
            <button
              onClick={generateDraft}
              disabled={generating}
              className="px-6 py-3 bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] rounded-md hover:bg-[hsl(var(--primary))]/90 transition-colors disabled:opacity-50 flex items-center gap-2 mx-auto"
              data-testid="generate-draft-button"
            >
              {generating ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Generating Decision Structure...
                </>
              ) : (
                'Generate Decision Structure'
              )}
            </button>
            <p className="text-sm text-[hsl(var(--muted-foreground))] mt-2">
              AI will generate a structured decision following the 6-step Ward protocol
            </p>
          </div>
        )}

        {/* Decision Draft */}
        {draft && !decision && (
          <div className="space-y-6">
            {/* 1. Decision Framing */}
            <SectionCard
              title="1. Decision Framing"
              sectionKey="decision_framing"
              approved={isSectionApproved('decision_framing')}
              onApprove={() => approveSection('decision_framing')}
              data-testid="section-decision-framing"
            >
              <div className="space-y-3">
                <div>
                  <h4 className="text-sm font-medium mb-1">What Decision?</h4>
                  <p className="text-sm text-[hsl(var(--muted-foreground))]">
                    {draft.decision_framing?.what_decision}
                  </p>
                </div>
                <div>
                  <h4 className="text-sm font-medium mb-1">Who Owns?</h4>
                  <p className="text-sm text-[hsl(var(--muted-foreground))]">
                    {draft.decision_framing?.who_owns}
                  </p>
                </div>
                <div>
                  <h4 className="text-sm font-medium mb-1">No Action Consequence</h4>
                  <p className="text-sm text-[hsl(var(--muted-foreground))]">
                    {draft.decision_framing?.no_action_consequence}
                  </p>
                </div>
              </div>
            </SectionCard>

            {/* 2. Known Inputs */}
            <SectionCard
              title="2. Known Inputs"
              sectionKey="known_inputs"
              approved={isSectionApproved('known_inputs')}
              onApprove={() => approveSection('known_inputs')}
              data-testid="section-known-inputs"
            >
              <div className="space-y-4">
                <div>
                  <h4 className="text-sm font-medium mb-2">Facts</h4>
                  <div className="space-y-2">
                    {draft.known_inputs?.facts?.map((fact, idx) => (
                      <div key={idx} className="p-3 bg-[hsl(var(--muted))]/30 rounded">
                        <p className="text-sm mb-2">{fact.fact}</p>
                        <div className="flex gap-2 flex-wrap">
                          <EvidenceBadge label="Source" value={fact.source} />
                          <EvidenceBadge label="Fresh" value={fact.freshness} />
                          <EvidenceBadge
                            label="Reliability"
                            value={fact.reliability}
                            color={fact.reliability === 'high' ? 'success' : fact.reliability === 'low' ? 'warning' : 'info'}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
                <div>
                  <h4 className="text-sm font-medium mb-2">Unknowns</h4>
                  <ul className="list-disc list-inside space-y-1">
                    {draft.known_inputs?.unknowns?.map((unknown, idx) => (
                      <li key={idx} className="text-sm text-[hsl(var(--muted-foreground))]">
                        {unknown}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </SectionCard>

            {/* 3. Declared Assumptions */}
            <SectionCard
              title="3. Declared Assumptions"
              sectionKey="declared_assumptions"
              approved={isSectionApproved('declared_assumptions')}
              onApprove={() => approveSection('declared_assumptions')}
              data-testid="section-assumptions"
            >
              <div className="space-y-3">
                {draft.declared_assumptions?.map((assumption, idx) => (
                  <div key={idx} className="p-3 bg-[hsl(var(--muted))]/30 rounded">
                    <p className="text-sm font-medium mb-2">{assumption.assumption}</p>
                    <p className="text-xs text-[hsl(var(--muted-foreground))] mb-1">
                      <span className="font-medium">Why reasonable:</span> {assumption.why_reasonable}
                    </p>
                    <p className="text-xs text-[hsl(var(--warning))]">
                      <span className="font-medium">Breaks if:</span> {assumption.breaks_if}
                    </p>
                  </div>
                ))}
              </div>
            </SectionCard>

            {/* 4. Alternatives */}
            <SectionCard
              title="4. Alternatives"
              sectionKey="alternatives"
              approved={isSectionApproved('alternatives')}
              onApprove={() => approveSection('alternatives')}
              data-testid="section-alternatives"
            >
              <div className="space-y-4">
                {draft.alternatives?.map((alt, idx) => (
                  <div
                    key={idx}
                    className="p-4 border border-[hsl(var(--border))] rounded-lg"
                    data-testid={`alternative-${idx}`}
                  >
                    <h4 className="text-base font-semibold mb-2">{alt.name}</h4>
                    <p className="text-sm text-[hsl(var(--muted-foreground))] mb-3">
                      {alt.description}
                    </p>
                    <div className="space-y-2 text-sm">
                      <div className="p-2 bg-[hsl(var(--destructive))]/10 border-l-2 border-[hsl(var(--destructive))] rounded">
                        <span className="font-medium text-[hsl(var(--destructive))]">Worst Case:</span>
                        <p className="text-[hsl(var(--destructive))]">{alt.worst_case}</p>
                      </div>
                      <p>
                        <span className="font-medium">Irreversible:</span> {alt.irreversible_consequences}
                      </p>
                      <p>
                        <span className="font-medium">Blast Radius:</span> {alt.blast_radius}
                      </p>
                      <div>
                        <span className="font-medium">Failure Signals:</span>
                        <ul className="list-disc list-inside mt-1">
                          {alt.failure_signals?.map((signal, sidx) => (
                            <li key={sidx} className="text-[hsl(var(--muted-foreground))]">
                              {signal}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </SectionCard>

            {/* 5. Recommendation */}
            <SectionCard
              title="5. Recommendation"
              sectionKey="recommendation"
              approved={isSectionApproved('recommendation')}
              onApprove={() => approveSection('recommendation')}
              data-testid="section-recommendation"
            >
              <div className="p-4 bg-[hsl(var(--info))]/10 border-l-4 border-[hsl(var(--info))] rounded">
                <h4 className="text-base font-semibold mb-2 text-[hsl(var(--info))]">
                  Recommended: {draft.recommendation?.choice}
                </h4>
                <p className="text-sm mb-3">{draft.recommendation?.rationale}</p>
                <div>
                  <span className="text-sm font-medium">Reversal Conditions:</span>
                  <ul className="list-disc list-inside mt-1">
                    {draft.recommendation?.reversal_conditions?.map((cond, idx) => (
                      <li key={idx} className="text-sm text-[hsl(var(--muted-foreground))]">
                        {cond}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </SectionCard>

            {/* Final Decision Selection */}
            <div className="bg-card border-2 border-[hsl(var(--primary))] rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-4">6. Make Your Decision</h3>
              <p className="text-sm text-[hsl(var(--muted-foreground))] mb-4">
                Select the alternative you choose to implement:
              </p>
              <div className="space-y-3">
                {draft.alternatives?.map((alt, idx) => (
                  <label
                    key={idx}
                    className="flex items-start gap-3 p-3 border border-[hsl(var(--border))] rounded cursor-pointer hover:border-[hsl(var(--primary))] transition-colors"
                  >
                    <input
                      type="radio"
                      name="alternative"
                      value={alt.name}
                      checked={selectedAlternative === alt.name}
                      onChange={(e) => setSelectedAlternative(e.target.value)}
                      className="mt-1"
                      data-testid={`select-alternative-${idx}`}
                    />
                    <div className="flex-1">
                      <span className="font-medium">{alt.name}</span>
                      <p className="text-sm text-[hsl(var(--muted-foreground))]">
                        {alt.description}
                      </p>
                    </div>
                  </label>
                ))}
              </div>

              <button
                onClick={handleFinalizeClick}
                disabled={!selectedAlternative || finalizing}
                className="mt-6 w-full bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] py-3 rounded-md hover:bg-[hsl(var(--primary))]/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium"
                data-testid="finalize-button"
              >
                {finalizing ? 'Finalizing...' : 'Finalize Decision'}
              </button>
            </div>
          </div>
        )}

        {/* Decision Finalized */}
        {decision && (
          <div className="bg-[hsl(var(--success))]/10 border-2 border-[hsl(var(--success))] rounded-lg p-6 text-center">
            <Check className="h-12 w-12 mx-auto mb-4 text-[hsl(var(--success))]" />
            <h2 className="text-xl font-bold mb-2">Decision Finalized</h2>
            <p className="text-sm text-[hsl(var(--muted-foreground))] mb-4">
              <span className="font-medium">Choice:</span> {decision.final_choice}
            </p>
            {decision.is_override && (
              <div className="mt-4 p-3 bg-[hsl(var(--warning))]/10 border border-[hsl(var(--warning))]/20 rounded">
                <p className="text-sm font-medium mb-1 text-[hsl(var(--warning))]">Override Rationale:</p>
                <p className="text-sm">{decision.override_rationale}</p>
              </div>
            )}
            <p className="text-xs text-[hsl(var(--muted-foreground))] mt-4">
              Decided by {decision.decided_by} on{' '}
              {new Date(decision.decided_at).toLocaleString()}
            </p>
          </div>
        )}
      </div>

      {/* Override Modal */}
      {showOverrideModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-card border border-[hsl(var(--border))] rounded-lg p-6 max-w-md w-full">
            <h3 className="text-lg font-semibold mb-4">Override Confirmation</h3>
            <p className="text-sm text-[hsl(var(--muted-foreground))] mb-4">
              You are choosing a different alternative than recommended. Please provide your rationale:
            </p>
            <textarea
              value={overrideRationale}
              onChange={(e) => setOverrideRationale(e.target.value)}
              rows={4}
              className="w-full px-3 py-2 border border-[hsl(var(--input))] rounded-md focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))] bg-background resize-none"
              placeholder="Explain why you chose a different option..."
              data-testid="override-rationale-input"
            />
            <div className="flex gap-3 mt-4">
              <button
                onClick={() => setShowOverrideModal(false)}
                className="flex-1 px-4 py-2 border border-[hsl(var(--border))] rounded-md hover:bg-[hsl(var(--secondary))] transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={finalize}
                disabled={!overrideRationale.trim() || finalizing}
                className="flex-1 px-4 py-2 bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] rounded-md hover:bg-[hsl(var(--primary))]/90 transition-colors disabled:opacity-50"
                data-testid="confirm-override-button"
              >
                {finalizing ? 'Finalizing...' : 'Confirm Override'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// Helper Components
function SectionCard({ title, children, sectionKey, approved, onApprove }) {
  return (
    <div className="bg-card border border-[hsl(var(--border))] rounded-lg overflow-hidden">
      <div className="flex justify-between items-center px-6 py-4 border-b border-[hsl(var(--border))] bg-[hsl(var(--muted))]/30">
        <h3 className="text-base font-semibold">{title}</h3>
        {approved ? (
          <span className="flex items-center gap-2 text-sm text-[hsl(var(--success))]">
            <Lock className="h-4 w-4" />
            Approved
          </span>
        ) : (
          <button
            onClick={onApprove}
            className="flex items-center gap-2 text-sm px-3 py-1 bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] rounded hover:bg-[hsl(var(--primary))]/90 transition-colors"
            data-testid={`approve-${sectionKey}`}
          >
            <Unlock className="h-4 w-4" />
            Approve
          </button>
        )}
      </div>
      <div className="p-6">{children}</div>
    </div>
  );
}

function EvidenceBadge({ label, value, color = 'info' }) {
  const colorClasses = {
    success: 'bg-[hsl(var(--success))]/10 text-[hsl(var(--success))]',
    warning: 'bg-[hsl(var(--warning))]/10 text-[hsl(var(--warning))]',
    info: 'bg-[hsl(var(--info))]/10 text-[hsl(var(--info))]',
  };

  return (
    <span className={`px-2 py-1 rounded text-xs ${colorClasses[color]}`}>
      {label}: {value}
    </span>
  );
}
