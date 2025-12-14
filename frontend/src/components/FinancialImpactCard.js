import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { IndianRupee, TrendingUp, AlertOctagon } from "lucide-react";

const FinancialImpactCard = ({ impact }) => {
  if (!impact) return null;

  const formattedAmount = new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: impact.currency || 'INR',
    maximumFractionDigits: 0
  }).format(impact.amount);

  const dailyIncrease = impact.estimated_daily_increase ? new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: impact.currency || 'INR',
    maximumFractionDigits: 0
  }).format(impact.estimated_daily_increase) : null;

  return (
    <Card className="border-red-200 bg-red-50/20">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium text-red-900 flex items-center gap-2">
          <IndianRupee className="h-4 w-4" />
          Financial Risk Exposure
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex justify-between items-end">
          <div>
            <p className="text-xs text-red-600 font-medium uppercase tracking-wider mb-1">
              {impact.category?.replace('_', ' ')} Cost
            </p>
            <h3 className="text-2xl font-bold text-red-950">{formattedAmount}</h3>
          </div>
          {dailyIncrease && (
            <div className="text-right">
              <div className="flex items-center gap-1 text-xs text-red-700 bg-red-100 px-2 py-1 rounded">
                <TrendingUp className="h-3 w-3" />
                +{dailyIncrease}/day
              </div>
            </div>
          )}
        </div>
        
        {impact.amount > 100000 && (
          <div className="mt-3 flex items-center gap-2 text-xs text-red-800 bg-red-100/50 p-2 rounded border border-red-200">
            <AlertOctagon className="h-3 w-3" />
            <span>High financial impact. Immediate resolution recommended.</span>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default FinancialImpactCard;
