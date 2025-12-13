"""
Analytics Dashboard Service
Aggregates case data into strategic metrics.
"""

from datetime import datetime, timedelta, timezone
import statistics

class AnalyticsService:
    def __init__(self, db):
        self.db = db

    async def get_dashboard_metrics(self, days=30):
        """
        Calculate key metrics for the last N days.
        """
        start_date = datetime.now(timezone.utc) - timedelta(days=days)
        
        # 1. Fetch relevant cases
        cursor = self.db.cases.find({
            "created_at": {"$gte": start_date}
        })
        cases = await cursor.to_list(length=1000)
        
        if not cases:
            return self._empty_metrics()

        # 2. Calculate Metrics
        total_cases = len(cases)
        resolved_cases = [c for c in cases if c.get("status") == "RESOLVED"]
        open_cases = total_cases - len(resolved_cases)
        
        # Resolution Time
        resolution_times = []
        for c in resolved_cases:
            created = c.get("created_at")
            updated = c.get("updated_at")
            if created and updated:
                # Ensure timezone awareness match
                if created.tzinfo is None: created = created.replace(tzinfo=timezone.utc)
                if updated.tzinfo is None: updated = updated.replace(tzinfo=timezone.utc)
                hours = (updated - created).total_seconds() / 3600
                resolution_times.append(hours)
        
        avg_resolution_time = statistics.mean(resolution_times) if resolution_times else 0
        
        # Disruption Types Breakdown
        type_counts = {}
        for c in cases:
            dtype = c.get("disruption_details", {}).get("disruption_type", "unknown")
            type_counts[dtype] = type_counts.get(dtype, 0) + 1
            
        # Top 5 types
        top_disruptions = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "period": f"Last {days} Days",
            "kpis": {
                "total_disruptions": total_cases,
                "open_cases": open_cases,
                "avg_resolution_hours": round(avg_resolution_time, 1),
                "resolution_rate": round((len(resolved_cases) / total_cases * 100), 1) if total_cases else 0
            },
            "breakdown": [
                {"name": k, "value": v} for k, v in top_disruptions
            ],
            "trends": await self._get_daily_trends(start_date)
        }

    async def _get_daily_trends(self, start_date):
        """Aggregate cases by day"""
        pipeline = [
            {"$match": {"created_at": {"$gte": start_date}}},
            {
                "$group": {
                    "_id": {
                        "$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"}
                    },
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"_id": 1}}
        ]
        result = await self.db.cases.aggregate(pipeline).to_list(length=30)
        return [{"date": r["_id"], "count": r["count"]} for r in result]

    def _empty_metrics(self):
        return {
            "period": "Last 30 Days",
            "kpis": {"total_disruptions": 0, "open_cases": 0, "avg_resolution_hours": 0, "resolution_rate": 0},
            "breakdown": [],
            "trends": []
        }
