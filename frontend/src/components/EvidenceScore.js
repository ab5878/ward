import React, { useState, useEffect } from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { CheckCircle, AlertTriangle, XCircle, ChevronRight, FileText, Mic, User } from "lucide-react";
import { Progress } from "@/components/ui/progress";
import api from '../services/api';

const EvidenceScore = ({ caseId, caseData, onUpdate }) => {
  const [scoreData, setScoreData] = useState(null);
  const [loading, setLoading] = useState(true);

  // Recalculate or fetch score on mount or when caseData changes
  useEffect(() => {
    fetchScore();
  }, [caseId, caseData]);

  const fetchScore = async () => {
    try {
      // We can trigger a recalc to ensure it's fresh
      const response = await api.post(`/cases/${caseId}/evidence/recalc`);
      setScoreData(response.data);
    } catch (error) {
      console.error("Failed to fetch evidence score", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading || !scoreData) return null;

  const { score, breakdown, missing_actions } = scoreData;

  let scoreColor = "text-red-600";
  let ringColor = "stroke-red-500";
  if (score >= 80) {
    scoreColor = "text-green-600";
    ringColor = "stroke-green-500";
  } else if (score >= 60) {
    scoreColor = "text-yellow-600";
    ringColor = "stroke-yellow-500";
  }

  // SVG Gauge
  const radius = 30;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <Card className="border-l-4 border-l-blue-600 shadow-sm mb-6">
      <CardContent className="p-6">
        <div className="flex flex-col md:flex-row gap-6 items-center">
          
          {/* Gauge Section */}
          <div className="flex flex-col items-center justify-center min-w-[120px]">
            <div className="relative w-24 h-24">
              <svg className="w-full h-full transform -rotate-90">
                <circle
                  className="text-gray-200"
                  strokeWidth="8"
                  stroke="currentColor"
                  fill="transparent"
                  r={radius}
                  cx="48"
                  cy="48"
                />
                <circle
                  className={`${ringColor} transition-all duration-1000 ease-out`}
                  strokeWidth="8"
                  strokeDasharray={circumference}
                  strokeDashoffset={strokeDashoffset}
                  strokeLinecap="round"
                  stroke="currentColor"
                  fill="transparent"
                  r={radius}
                  cx="48"
                  cy="48"
                />
              </svg>
              <div className="absolute top-0 left-0 w-full h-full flex flex-col items-center justify-center">
                <span className={`text-2xl font-bold ${scoreColor}`}>{score}%</span>
                <span className="text-[10px] text-gray-500 font-medium uppercase">Score</span>
              </div>
            </div>
            <p className="text-xs font-semibold text-gray-600 mt-2 text-center uppercase tracking-wide">
              Evidence Strength
            </p>
          </div>

          {/* Breakdown Section */}
          <div className="flex-1 grid grid-cols-1 md:grid-cols-2 gap-4 w-full">
            
            {/* What we have */}
            <div className="space-y-2">
              <h4 className="text-sm font-semibold text-gray-700 flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-green-500" /> Secured Evidence
              </h4>
              {breakdown.length === 0 && <p className="text-xs text-gray-400 italic">No significant evidence yet.</p>}
              <ul className="space-y-1">
                {breakdown.map((item, i) => (
                  <li key={i} className="text-xs text-gray-600 flex items-start gap-2 bg-green-50 p-1.5 rounded border border-green-100">
                    <span className="text-green-600 font-bold">•</span> {item}
                  </li>
                ))}
              </ul>
            </div>

            {/* What is missing */}
            <div className="space-y-2">
              <h4 className="text-sm font-semibold text-gray-700 flex items-center gap-2">
                <AlertTriangle className="h-4 w-4 text-amber-500" /> Missing Items
              </h4>
              {missing_actions.length === 0 && <p className="text-xs text-green-600 font-medium">All evidence requirements met!</p>}
              <ul className="space-y-1">
                {missing_actions.map((action, i) => (
                  <li key={i} className="text-xs text-gray-600 flex items-start gap-2 bg-amber-50 p-1.5 rounded border border-amber-100">
                    <span className="text-amber-600 font-bold">→</span> {action}
                  </li>
                ))}
              </ul>
            </div>

          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default EvidenceScore;
