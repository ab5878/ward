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
        # Note: PostgreSQL doesn't support $gte directly, we'll filter in Python for now
        cursor = await self.db.cases.find({}, sort=[("created_at", -1)], limit=1000)
        all_cases = await cursor.to_list(length=1000)
        # Filter by date in Python
        cases = [c for c in all_cases if c.get("created_at") and c.get("created_at") >= start_date]
        
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
        
        # --- NEW: Time to Defensible Evidence (TTDE) ---
        ttde_values = []
        for c in cases:
            created = c.get("created_at")
            ready = c.get("evidence_ready_at")
            
            # Fallback for demo data: if resolved but no specific ready time, assume 50% of resolution time
            if not ready and c.get("status") == "RESOLVED" and c.get("updated_at"):
                 ready = created + (c.get("updated_at") - created) / 2
            
            if created and ready:
                if created.tzinfo is None: created = created.replace(tzinfo=timezone.utc)
                if ready.tzinfo is None: ready = ready.replace(tzinfo=timezone.utc)
                minutes = (ready - created).total_seconds() / 60
                ttde_values.append(minutes)
                
        avg_ttde_minutes = statistics.mean(ttde_values) if ttde_values else 0

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
                "avg_ttde_minutes": round(avg_ttde_minutes, 0), # NEW METRIC
                "resolution_rate": round((len(resolved_cases) / total_cases * 100), 1) if total_cases else 0
            },
            "breakdown": [
                {"name": k, "value": v} for k, v in top_disruptions
            ],
            "trends": await self._get_daily_trends(start_date)
        }

    async def _get_daily_trends(self, start_date):
        """Aggregate cases by day"""
        # PostgreSQL doesn't support MongoDB aggregation pipeline
        # Fetch all cases and group in Python
        cursor = await self.db.cases.find({}, sort=[("created_at", -1)], limit=1000)
        all_cases = await cursor.to_list(length=1000)
        cases = [c for c in all_cases if c.get("created_at") and c.get("created_at") >= start_date]
        
        # Group by date
        daily_counts = {}
        for case in cases:
            created = case.get("created_at")
            if created:
                date_str = created.strftime("%Y-%m-%d")
                daily_counts[date_str] = daily_counts.get(date_str, 0) + 1
        
        # Convert to list and sort
        trends = [{"date": date, "count": count} for date, count in sorted(daily_counts.items())]
        return trends

    def _empty_metrics(self):
        return {
            "period": "Last 30 Days",
            "kpis": {"total_disruptions": 0, "open_cases": 0, "avg_resolution_hours": 0, "avg_ttde_minutes": 0, "resolution_rate": 0},
            "breakdown": [],
            "trends": []
        }
