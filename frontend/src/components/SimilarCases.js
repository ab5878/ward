import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Loader2, History, ArrowRight } from "lucide-react";
import api from '../services/api';

const SimilarCases = ({ caseId }) => {
  const [similarCases, setSimilarCases] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSimilar();
  }, [caseId]);

  const loadSimilar = async () => {
    try {
      const response = await api.get(`/cases/${caseId}/similar`);
      setSimilarCases(response.data);
    } catch (error) {
      console.error("Failed to load similar cases", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="p-4"><Loader2 className="h-4 w-4 animate-spin text-gray-400" /></div>;
  if (!similarCases.length) return null;

  return (
    <Card className="border-amber-200 bg-amber-50/30">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium text-amber-900 flex items-center gap-2">
          <History className="h-4 w-4" />
          Institutional Memory
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {similarCases.map((c, idx) => (
            <div key={idx} className="bg-white p-3 rounded border border-amber-100 shadow-sm">
              <div className="flex justify-between items-start mb-1">
                <Badge variant="outline" className="text-[10px] bg-gray-100 text-gray-600">Resolved in {c.resolution_time}</Badge>
                <a href={`/cases/${c.case_id}`} className="text-blue-600 hover:text-blue-800">
                  <ArrowRight className="h-3 w-3" />
                </a>
              </div>
              <p className="text-xs text-gray-600 line-clamp-2 mb-2">{c.description}</p>
              <div className="text-xs font-medium text-green-700 bg-green-50 px-2 py-1 rounded">
                Fix: {c.resolution || "Manual intervention"}
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default SimilarCases;
