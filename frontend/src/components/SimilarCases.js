import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { History, ArrowRight, Sparkles } from "lucide-react";
import { Skeleton } from "@/components/ui/skeleton";
import api from '../services/api';

const SimilarCases = ({ caseId }) => {
  const [similarCases, setSimilarCases] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSimilar();
  }, [caseId]);

  const loadSimilar = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/cases/${caseId}/similar`);
      setSimilarCases(response.data);
    } catch (error) {
      console.error("Failed to load similar cases", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
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
            {[1, 2].map((i) => (
              <div key={i} className="bg-white p-3 rounded border border-amber-100 shadow-sm">
                <div className="flex justify-between items-start mb-2">
                  <Skeleton className="h-4 w-20" />
                  <Skeleton className="h-3 w-3" />
                </div>
                <Skeleton className="h-3 w-full mb-2" />
                <Skeleton className="h-3 w-3/4 mb-3" />
                <Skeleton className="h-5 w-32 rounded" />
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!similarCases.length) return null;

  return (
    <Card className="border-amber-200 bg-amber-50/30">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium text-amber-900 flex items-center gap-2">
          <History className="h-4 w-4" />
          Institutional Memory
          <Badge variant="secondary" className="ml-auto bg-amber-100 text-amber-800 text-[10px] font-normal">
            {similarCases.length} Matches
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {similarCases.map((c, idx) => (
            <div key={idx} className="bg-white p-3 rounded border border-amber-100 shadow-sm hover:shadow-md transition-shadow group">
              <div className="flex justify-between items-start mb-1">
                <div className="flex items-center gap-2">
                  <Badge variant="outline" className="text-[10px] bg-gray-100 text-gray-600 border-gray-200">
                    Resolved in {c.resolution_time}
                  </Badge>
                  {idx === 0 && (
                    <span className="text-[10px] flex items-center text-amber-600 font-medium">
                      <Sparkles className="h-3 w-3 mr-1" /> Best Match
                    </span>
                  )}
                </div>
                <a href={`/cases/${c.case_id}`} className="text-gray-400 hover:text-blue-600 transition-colors">
                  <ArrowRight className="h-3 w-3" />
                </a>
              </div>
              <p className="text-xs text-gray-700 line-clamp-2 mb-2 font-medium leading-relaxed">
                "{c.description}"
              </p>
              <div className="text-xs font-medium text-green-800 bg-green-50 px-2 py-1.5 rounded border border-green-100">
                <span className="opacity-70 font-normal mr-1">Fix:</span> {c.resolution || "Manual intervention"}
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default SimilarCases;
