"""
Database Adapter for Supabase PostgreSQL
Replaces MongoDB operations with PostgreSQL/Supabase
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import asyncpg
import json
from uuid import UUID, uuid4
import os
from contextlib import asynccontextmanager


class SupabaseAdapter:
    """Adapter to replace MongoDB operations with Supabase PostgreSQL"""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.pool: Optional[asyncpg.Pool] = None
    
    async def connect(self):
        """Create connection pool"""
        # Disable prepared statements for pgbouncer compatibility
        # pgbouncer in transaction/statement mode doesn't support prepared statements
        self.pool = await asyncpg.create_pool(
            self.connection_string,
            min_size=1,
            max_size=10,
            command_timeout=60,
            statement_cache_size=0  # Disable prepared statements for pgbouncer
        )
        print("Connected to Supabase PostgreSQL")
    
    async def close(self):
        """Close connection pool"""
        if self.pool:
            await self.pool.close()
            print("Closed Supabase connection")
    
    def _serialize_value(self, value: Any) -> Any:
        """Convert Python types to PostgreSQL-compatible types"""
        if isinstance(value, datetime):
            return value
        if isinstance(value, dict):
            return json.dumps(value)
        if isinstance(value, list):
            return json.dumps(value)
        if isinstance(value, UUID):
            return str(value)
        return value
    
    def _deserialize_doc(self, row: asyncpg.Record) -> Dict[str, Any]:
        """Convert PostgreSQL row to dict (similar to MongoDB document)"""
        doc = {}
        for key, value in row.items():
            if isinstance(value, str):
                # Try to parse JSON fields
                if key in ['disruption_details', 'shipment_identifiers', 'financial_impact', 
                          'structured_context', 'responsibility', 'rca', 'enhanced_rca',
                          'metadata', 'analysis', 'stakeholders', 'evidence_score_breakdown',
                          'decision_framing', 'known_inputs', 'declared_assumptions',
                          'alternatives', 'risk_and_downside', 'recommendation', 'content_snapshot',
                          'payload', 'data', 'address', 'location', 'contact_info', 'gps', 'settings']:
                    try:
                        doc[key] = json.loads(value) if value else {}
                    except:
                        doc[key] = value
                else:
                    doc[key] = value
            elif isinstance(value, UUID):
                doc[key] = str(value)
            elif isinstance(value, datetime):
                doc[key] = value
            else:
                doc[key] = value
        
        # Always set _id from id for MongoDB compatibility
        if "id" in doc and "_id" not in doc:
            doc["_id"] = doc["id"]
        
        return doc
    
    # Users operations
    async def users_find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find one user"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        try:
            async with self.pool.acquire() as conn:
                if "_id" in query or "id" in query:
                    # Handle both _id (MongoDB-style) and id (PostgreSQL-style)
                    user_id = query.get("_id") or query.get("id")
                    if isinstance(user_id, str):
                        try:
                            user_id = UUID(user_id)
                        except ValueError:
                            # Invalid UUID format
                            return None
                    row = await conn.fetchrow(
                        "SELECT * FROM users WHERE id = $1",
                        user_id
                    )
                elif "email" in query:
                    row = await conn.fetchrow(
                        "SELECT * FROM users WHERE email = $1",
                        query["email"]
                    )
                else:
                    return None
                
                if row:
                    result = self._deserialize_doc(row)
                    # Ensure _id is set for compatibility (MongoDB-style)
                    # PostgreSQL uses 'id' (UUID), but code expects '_id'
                    if "id" in result:
                        result["_id"] = result["id"]  # Always set _id from id
                    return result
                return None
        except Exception as e:
            print(f"users_find_one error: {e}, query: {query}")
            import traceback
            traceback.print_exc()
            raise
    
    async def users_insert_one(self, doc: Dict[str, Any]) -> str:
        """Insert one user, return ID"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        try:
            async with self.pool.acquire() as conn:
                user_id = uuid4()
                await conn.execute(
                    """INSERT INTO users (id, email, password_hash, created_at)
                       VALUES ($1, $2, $3, $4)""",
                    user_id,
                    doc["email"],
                    doc["password_hash"],
                    doc.get("created_at", datetime.now(timezone.utc))
                )
                return str(user_id)
        except Exception as e:
            print(f"users_insert_one error: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    # Cases operations
    async def cases_find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find one case"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            conditions = []
            params = []
            param_idx = 1
            
            if "_id" in query:
                conditions.append(f"id = ${param_idx}")
                params.append(UUID(query["_id"]))
                param_idx += 1
            if "operator_id" in query:
                conditions.append(f"operator_id = ${param_idx}")
                params.append(UUID(query["operator_id"]))
                param_idx += 1
            if "status" in query:
                conditions.append(f"status = ${param_idx}")
                params.append(query["status"])
                param_idx += 1
            if "decision_owner_email" in query:
                conditions.append(f"decision_owner_email = ${param_idx}")
                params.append(query["decision_owner_email"])
                param_idx += 1
            
            if not conditions:
                return None
            
            sql = f"SELECT * FROM cases WHERE {' AND '.join(conditions)} LIMIT 1"
            row = await conn.fetchrow(sql, *params)
            return self._deserialize_doc(row) if row else None
    
    async def cases_find(self, query: Dict[str, Any], sort: Optional[List] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Find cases"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            conditions = []
            params = []
            param_idx = 1
            
            if "operator_id" in query:
                conditions.append(f"operator_id = ${param_idx}")
                params.append(UUID(query["operator_id"]))
                param_idx += 1
            if "status" in query:
                conditions.append(f"status = ${param_idx}")
                params.append(query["status"])
                param_idx += 1
            if "decision_owner_email" in query:
                conditions.append(f"decision_owner_email = ${param_idx}")
                params.append(query["decision_owner_email"])
                param_idx += 1
            
            where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
            
            order_clause = ""
            if sort:
                for field, direction in sort:
                    dir_str = "DESC" if direction == -1 else "ASC"
                    order_clause = f"ORDER BY {field} {dir_str}"
            
            limit_clause = f"LIMIT {limit}" if limit else ""
            
            sql = f"SELECT * FROM cases {where_clause} {order_clause} {limit_clause}"
            rows = await conn.fetch(sql, *params)
            return [self._deserialize_doc(row) for row in rows]
    
    async def cases_insert_one(self, doc: Dict[str, Any]) -> str:
        """Insert one case, return ID"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            case_id = uuid4()
            await conn.execute(
                """INSERT INTO cases (
                    id, operator_id, operator_email, description, status,
                    disruption_details, shipment_identifiers, financial_impact,
                    structured_context, created_at, updated_at,
                    decision_owner_id, decision_owner_email, voice_transcript,
                    created_via, coordination_status, stakeholders
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17)""",
                case_id,
                UUID(doc["operator_id"]) if doc.get("operator_id") else None,
                doc["operator_email"],
                doc["description"],
                doc.get("status", "REPORTED"),
                json.dumps(doc.get("disruption_details", {})),
                json.dumps(doc.get("shipment_identifiers", {})),
                json.dumps(doc.get("financial_impact")) if doc.get("financial_impact") else None,
                json.dumps(doc.get("structured_context")) if doc.get("structured_context") else None,
                doc.get("created_at", datetime.now(timezone.utc)),
                doc.get("updated_at", datetime.now(timezone.utc)),
                UUID(doc["decision_owner_id"]) if doc.get("decision_owner_id") else None,
                doc.get("decision_owner_email"),
                doc.get("voice_transcript"),
                doc.get("created_via"),
                doc.get("coordination_status"),
                json.dumps(doc.get("stakeholders")) if doc.get("stakeholders") else None
            )
            return str(case_id)
    
    async def cases_update_one(self, query: Dict[str, Any], update: Dict[str, Any]) -> bool:
        """Update one case"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            # Build WHERE clause
            where_conditions = []
            params = []
            param_idx = 1
            
            if "_id" in query:
                where_conditions.append(f"id = ${param_idx}")
                params.append(UUID(query["_id"]))
                param_idx += 1
            
            if not where_conditions:
                return False
            
            # Build SET clause
            set_clauses = []
            set_values = update.get("$set", {})
            
            for key, value in set_values.items():
                if key in ['disruption_details', 'shipment_identifiers', 'financial_impact',
                          'structured_context', 'responsibility', 'rca', 'enhanced_rca',
                          'stakeholders', 'evidence_score_breakdown']:
                    set_clauses.append(f"{key} = ${param_idx}")
                    params.append(json.dumps(value) if value else None)
                else:
                    set_clauses.append(f"{key} = ${param_idx}")
                    params.append(value)
                param_idx += 1
            
            if not set_clauses:
                return False
            
            sql = f"UPDATE cases SET {', '.join(set_clauses)} WHERE {' AND '.join(where_conditions)}"
            result = await conn.execute(sql, *params)
            return result != "UPDATE 0"
    
    # Timeline events operations
    async def timeline_events_find(self, query: Dict[str, Any], sort: Optional[List] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Find timeline events"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            conditions = []
            params = []
            param_idx = 1
            
            if "case_id" in query:
                conditions.append(f"case_id = ${param_idx}")
                params.append(UUID(query["case_id"]))
                param_idx += 1
            
            where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
            
            order_clause = ""
            if sort:
                for field, direction in sort:
                    dir_str = "DESC" if direction == -1 else "ASC"
                    order_clause = f"ORDER BY {field} {dir_str}"
            
            limit_clause = f"LIMIT {limit}" if limit else ""
            
            sql = f"SELECT * FROM timeline_events {where_clause} {order_clause} {limit_clause}"
            rows = await conn.fetch(sql, *params)
            return [self._deserialize_doc(row) for row in rows]
    
    async def timeline_events_find_one(self, query: Dict[str, Any], sort: Optional[List] = None) -> Optional[Dict[str, Any]]:
        """Find one timeline event"""
        results = await self.timeline_events_find(query, sort=sort, limit=1)
        return results[0] if results else None
    
    async def timeline_events_insert_one(self, doc: Dict[str, Any]) -> str:
        """Insert one timeline event"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            event_id = uuid4()
            await conn.execute(
                """INSERT INTO timeline_events (
                    id, case_id, actor, action, content, source_type,
                    reliability, metadata, timestamp
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)""",
                event_id,
                UUID(doc["case_id"]),
                doc["actor"],
                doc["action"],
                doc["content"],
                doc["source_type"],
                doc["reliability"],
                json.dumps(doc.get("metadata", {})),
                doc.get("timestamp", datetime.now(timezone.utc))
            )
            return str(event_id)
    
    # Audit entries operations
    async def audit_entries_insert_one(self, doc: Dict[str, Any]) -> str:
        """Insert one audit entry"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            entry_id = uuid4()
            await conn.execute(
                """INSERT INTO audit_entries (id, case_id, actor, action, payload, timestamp)
                   VALUES ($1, $2, $3, $4, $5, $6)""",
                entry_id,
                doc["case_id"],
                doc["actor"],
                doc["action"],
                json.dumps(doc.get("payload", {})),
                doc.get("timestamp", datetime.now(timezone.utc))
            )
            return str(entry_id)
    
    async def audit_entries_find(self, query: Dict[str, Any], sort: Optional[List] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Find audit entries"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            conditions = []
            params = []
            param_idx = 1
            
            if "case_id" in query:
                if isinstance(query["case_id"], dict) and "$in" in query["case_id"]:
                    # Handle $in operator
                    case_ids = [str(cid) for cid in query["case_id"]["$in"]]
                    placeholders = [f"${i}" for i in range(param_idx, param_idx + len(case_ids))]
                    conditions.append(f"case_id IN ({', '.join(placeholders)})")
                    params.extend(case_ids)
                    param_idx += len(case_ids)
                else:
                    conditions.append(f"case_id = ${param_idx}")
                    params.append(str(query["case_id"]))
                    param_idx += 1
            
            where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
            
            order_clause = ""
            if sort:
                for field, direction in sort:
                    dir_str = "DESC" if direction == -1 else "ASC"
                    order_clause = f"ORDER BY {field} {dir_str}"
            
            limit_clause = f"LIMIT {limit}" if limit else ""
            
            sql = f"SELECT * FROM audit_entries {where_clause} {order_clause} {limit_clause}"
            rows = await conn.fetch(sql, *params)
            return [self._deserialize_doc(row) for row in rows]
    
    # Documents operations
    async def documents_find(self, query: Dict[str, Any], sort: Optional[List] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Find documents"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            conditions = []
            params = []
            param_idx = 1
            
            if "case_id" in query:
                conditions.append(f"case_id = ${param_idx}")
                params.append(UUID(query["case_id"]))
                param_idx += 1
            
            where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
            
            order_clause = ""
            if sort:
                for field, direction in sort:
                    dir_str = "DESC" if direction == -1 else "ASC"
                    order_clause = f"ORDER BY {field} {dir_str}"
            
            limit_clause = f"LIMIT {limit}" if limit else ""
            
            sql = f"SELECT * FROM documents {where_clause} {order_clause} {limit_clause}"
            rows = await conn.fetch(sql, *params)
            return [self._deserialize_doc(row) for row in rows]
    
    async def documents_find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find one document"""
        results = await self.documents_find(query, limit=1)
        return results[0] if results else None
    
    async def documents_insert_one(self, doc: Dict[str, Any]) -> str:
        """Insert one document"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            doc_id = uuid4()
            await conn.execute(
                """INSERT INTO documents (
                    id, case_id, filename, doc_type, analysis, uploaded_at, uploaded_by
                ) VALUES ($1, $2, $3, $4, $5, $6, $7)""",
                doc_id,
                UUID(doc["case_id"]),
                doc["filename"],
                doc.get("doc_type"),
                json.dumps(doc.get("analysis", {})) if doc.get("analysis") else None,
                doc.get("uploaded_at", datetime.now(timezone.utc)),
                doc["uploaded_by"]
            )
            return str(doc_id)
    
    async def documents_count_documents(self, query: Dict[str, Any]) -> int:
        """Count documents"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            conditions = []
            params = []
            param_idx = 1
            
            if "case_id" in query:
                conditions.append(f"case_id = ${param_idx}")
                params.append(UUID(query["case_id"]))
                param_idx += 1
            
            where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
            sql = f"SELECT COUNT(*) FROM documents {where_clause}"
            count = await conn.fetchval(sql, *params)
            return count
    
    # Drafts, approvals, decisions operations (similar pattern)
    async def drafts_find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find one draft"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            if "case_id" in query:
                row = await conn.fetchrow(
                    "SELECT * FROM drafts WHERE case_id = $1",
                    UUID(query["case_id"])
                )
                return self._deserialize_doc(row) if row else None
            return None
    
    async def drafts_insert_one(self, doc: Dict[str, Any]) -> str:
        """Insert one draft"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            draft_id = uuid4()
            await conn.execute(
                """INSERT INTO drafts (
                    id, case_id, decision_framing, known_inputs, declared_assumptions,
                    alternatives, risk_and_downside, recommendation, ai_model, created_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)""",
                draft_id,
                UUID(doc["case_id"]),
                json.dumps(doc.get("decision_framing")) if doc.get("decision_framing") else None,
                json.dumps(doc.get("known_inputs")) if doc.get("known_inputs") else None,
                json.dumps(doc.get("declared_assumptions")) if doc.get("declared_assumptions") else None,
                json.dumps(doc.get("alternatives")) if doc.get("alternatives") else None,
                json.dumps(doc.get("risk_and_downside")) if doc.get("risk_and_downside") else None,
                json.dumps(doc.get("recommendation")) if doc.get("recommendation") else None,
                doc.get("ai_model"),
                doc.get("created_at", datetime.now(timezone.utc))
            )
            return str(draft_id)
    
    async def drafts_update_one(self, query: Dict[str, Any], update: Dict[str, Any]) -> bool:
        """Update one draft"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            where_conditions = []
            params = []
            param_idx = 1
            
            if "case_id" in query:
                where_conditions.append(f"case_id = ${param_idx}")
                params.append(UUID(query["case_id"]))
                param_idx += 1
            
            if not where_conditions:
                return False
            
            set_clauses = []
            set_values = update.get("$set", {})
            
            for key, value in set_values.items():
                if key in ['decision_framing', 'known_inputs', 'declared_assumptions',
                          'alternatives', 'risk_and_downside', 'recommendation']:
                    set_clauses.append(f"{key} = ${param_idx}")
                    params.append(json.dumps(value) if value else None)
                else:
                    set_clauses.append(f"{key} = ${param_idx}")
                    params.append(value)
                param_idx += 1
            
            if not set_clauses:
                return False
            
            sql = f"UPDATE drafts SET {', '.join(set_clauses)} WHERE {' AND '.join(where_conditions)}"
            result = await conn.execute(sql, *params)
            return result != "UPDATE 0"
    
    async def approvals_find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find one approval"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            conditions = []
            params = []
            param_idx = 1
            
            if "case_id" in query:
                conditions.append(f"case_id = ${param_idx}")
                params.append(UUID(query["case_id"]))
                param_idx += 1
            if "section_key" in query:
                conditions.append(f"section_key = ${param_idx}")
                params.append(query["section_key"])
                param_idx += 1
            
            if not conditions:
                return None
            
            sql = f"SELECT * FROM approvals WHERE {' AND '.join(conditions)} LIMIT 1"
            row = await conn.fetchrow(sql, *params)
            return self._deserialize_doc(row) if row else None
    
    async def approvals_insert_one(self, doc: Dict[str, Any]) -> str:
        """Insert one approval"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            approval_id = uuid4()
            await conn.execute(
                """INSERT INTO approvals (
                    id, case_id, section_key, approved_by, approved_at, content_snapshot
                ) VALUES ($1, $2, $3, $4, $5, $6)""",
                approval_id,
                UUID(doc["case_id"]),
                doc["section_key"],
                doc["approved_by"],
                doc.get("approved_at", datetime.now(timezone.utc)),
                json.dumps(doc.get("content_snapshot")) if doc.get("content_snapshot") else None
            )
            return str(approval_id)
    
    async def approvals_find(self, query: Dict[str, Any], sort: Optional[List] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Find approvals"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            conditions = []
            params = []
            param_idx = 1
            
            if "case_id" in query:
                conditions.append(f"case_id = ${param_idx}")
                params.append(UUID(query["case_id"]))
                param_idx += 1
            
            where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
            
            order_clause = ""
            if sort:
                for field, direction in sort:
                    dir_str = "DESC" if direction == -1 else "ASC"
                    order_clause = f"ORDER BY {field} {dir_str}"
            
            limit_clause = f"LIMIT {limit}" if limit else ""
            
            sql = f"SELECT * FROM approvals {where_clause} {order_clause} {limit_clause}"
            rows = await conn.fetch(sql, *params)
            return [self._deserialize_doc(row) for row in rows]
    
    async def decisions_find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find one decision"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            if "case_id" in query:
                row = await conn.fetchrow(
                    "SELECT * FROM decisions WHERE case_id = $1",
                    UUID(query["case_id"])
                )
                return self._deserialize_doc(row) if row else None
            return None
    
    async def decisions_insert_one(self, doc: Dict[str, Any]) -> str:
        """Insert one decision"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            decision_id = uuid4()
            await conn.execute(
                """INSERT INTO decisions (
                    id, case_id, final_choice, is_override, override_rationale,
                    recommended_choice, decided_by, decided_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)""",
                decision_id,
                UUID(doc["case_id"]),
                doc["final_choice"],
                doc.get("is_override", False),
                doc.get("override_rationale"),
                doc.get("recommended_choice"),
                doc["decided_by"],
                doc.get("decided_at", datetime.now(timezone.utc))
            )
            return str(decision_id)
    
    async def historical_find(self, sort: Optional[List] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Find historical entries"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            order_clause = ""
            if sort:
                for field, direction in sort:
                    dir_str = "DESC" if direction == -1 else "ASC"
                    order_clause = f"ORDER BY {field} {dir_str}"
            
            limit_clause = f"LIMIT {limit}" if limit else ""
            
            sql = f"SELECT * FROM historical {order_clause} {limit_clause}"
            rows = await conn.fetch(sql)
            return [self._deserialize_doc(row) for row in rows]
    
    async def historical_find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find one historical entry"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            if "_id" in query:
                row = await conn.fetchrow(
                    "SELECT * FROM historical WHERE id = $1",
                    UUID(query["_id"])
                )
                return self._deserialize_doc(row) if row else None
            return None
    
    # MongoDB-like interface for compatibility
    @property
    def users(self):
        return self
    
    @property
    def cases(self):
        return self
    
    @property
    def timeline_events(self):
        return self
    
    @property
    def audit_entries(self):
        return self
    
    @property
    def documents(self):
        return self
    
    @property
    def drafts(self):
        return self
    
    @property
    def approvals(self):
        return self
    
    @property
    def decisions(self):
        return self
    
    @property
    def historical(self):
        return self
    
    # Operator operations
    async def operators_find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find one operator"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        async with self.pool.acquire() as conn:
            if "_id" in query or "id" in query:
                operator_id = UUID(query.get("_id") or query.get("id"))
                row = await conn.fetchrow("SELECT * FROM operators WHERE id = $1", operator_id)
            elif "email" in query:
                row = await conn.fetchrow("SELECT * FROM operators WHERE email = $1", query["email"])
            else:
                return None
            return self._deserialize_doc(row) if row else None

    async def operators_insert_one(self, doc: Dict[str, Any]) -> str:
        """Insert operator"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        async with self.pool.acquire() as conn:
            operator_id = UUID(doc.get("id") or uuid4())
            await conn.execute(
                """INSERT INTO operators (
                    id, company_name, email, phone, fleet_size, account_type, settings, created_at, updated_at, created_by
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)""",
                operator_id, doc["company_name"], doc["email"], doc.get("phone"),
                doc.get("fleet_size", 0), doc.get("account_type", "pilot"),
                json.dumps(doc.get("settings", {})),
                doc.get("created_at", datetime.now(timezone.utc)),
                doc.get("updated_at", datetime.now(timezone.utc)),
                UUID(doc["created_by"]) if doc.get("created_by") else None
            )
            return str(operator_id)

    async def fleet_vehicles_find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find one fleet vehicle"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        async with self.pool.acquire() as conn:
            if "_id" in query or "id" in query:
                vehicle_id = UUID(query.get("_id") or query.get("id"))
                row = await conn.fetchrow("SELECT * FROM fleet_vehicles WHERE id = $1", vehicle_id)
            else:
                return None
            return self._deserialize_doc(row) if row else None

    async def fleet_vehicles_find(self, query: Dict[str, Any], sort: Optional[List] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Find fleet vehicles"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        async with self.pool.acquire() as conn:
            sql = "SELECT * FROM fleet_vehicles WHERE 1=1"
            params = []
            param_idx = 1
            
            if "operator_id" in query:
                sql += f" AND operator_id = ${param_idx}"
                params.append(UUID(query["operator_id"]))
                param_idx += 1
            
            if "vehicle_number" in query:
                sql += f" AND vehicle_number = ${param_idx}"
                params.append(query["vehicle_number"])
                param_idx += 1
            
            if sort:
                order_clause = self._build_order_clause(sort)
                sql += f" ORDER BY {order_clause}"
            else:
                sql += " ORDER BY created_at DESC"
            
            if limit:
                sql += f" LIMIT {limit}"
            
            rows = await conn.fetch(sql, *params)
            return [self._deserialize_doc(row) for row in rows]

    async def fleet_vehicles_insert_one(self, doc: Dict[str, Any]) -> str:
        """Insert fleet vehicle"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        async with self.pool.acquire() as conn:
            vehicle_id = UUID(doc.get("id") or uuid4())
            await conn.execute(
                """INSERT INTO fleet_vehicles (
                    id, operator_id, vehicle_number, vehicle_type, driver_name, driver_phone, route, status, metadata, created_at, updated_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)""",
                vehicle_id, UUID(doc["operator_id"]), doc["vehicle_number"], doc.get("vehicle_type", "truck"),
                doc.get("driver_name"), doc.get("driver_phone"), doc.get("route"),
                doc.get("status", "active"), json.dumps(doc.get("metadata", {})),
                doc.get("created_at", datetime.now(timezone.utc)),
                doc.get("updated_at", datetime.now(timezone.utc))
            )
            return str(vehicle_id)

    async def magic_links_find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find one magic link"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        async with self.pool.acquire() as conn:
            if "token" in query:
                row = await conn.fetchrow("SELECT * FROM magic_links WHERE token = $1", query["token"])
            elif "_id" in query or "id" in query:
                link_id = UUID(query.get("_id") or query.get("id"))
                row = await conn.fetchrow("SELECT * FROM magic_links WHERE id = $1", link_id)
            else:
                return None
            return self._deserialize_doc(row) if row else None

    async def magic_links_insert_one(self, doc: Dict[str, Any]) -> str:
        """Insert magic link"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        async with self.pool.acquire() as conn:
            link_id = UUID(doc.get("id") or uuid4())
            await conn.execute(
                """INSERT INTO magic_links (
                    id, operator_id, vehicle_id, token, expires_at, used_count, max_uses, created_at, last_used_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)""",
                link_id, UUID(doc["operator_id"]), UUID(doc["vehicle_id"]), doc["token"],
                doc["expires_at"], doc.get("used_count", 0), doc.get("max_uses"),
                doc.get("created_at", datetime.now(timezone.utc)), doc.get("last_used_at")
            )
            return str(link_id)

    async def magic_links_update_one(self, query: Dict[str, Any], update: Dict[str, Any]) -> bool:
        """Update magic link (e.g., increment used_count)"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        async with self.pool.acquire() as conn:
            where_conditions = []
            params = []
            param_idx = 1
            
            if "token" in query:
                where_conditions.append(f"token = ${param_idx}")
                params.append(query["token"])
                param_idx += 1
            
            if not where_conditions:
                return False
            
            set_clauses = []
            set_values = update.get("$set", {})
            for key, value in set_values.items():
                set_clauses.append(f"{key} = ${param_idx}")
                params.append(value)
                param_idx += 1
            
            if not set_clauses:
                return False
            
            sql = f"UPDATE magic_links SET {', '.join(set_clauses)} WHERE {' AND '.join(where_conditions)}"
            result = await conn.execute(sql, *params)
            return result != "UPDATE 0"
    
    async def operators_update_one(self, query: Dict[str, Any], update: Dict[str, Any]) -> bool:
        """Update operator"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        async with self.pool.acquire() as conn:
            where_conditions = []
            params = []
            param_idx = 1
            
            if "_id" in query or "id" in query:
                operator_id = UUID(query.get("_id") or query.get("id"))
                where_conditions.append(f"id = ${param_idx}")
                params.append(operator_id)
                param_idx += 1
            
            if not where_conditions:
                return False
            
            set_clauses = []
            set_values = update.get("$set", {})
            for key, value in set_values.items():
                if key == "settings":
                    set_clauses.append(f"{key} = ${param_idx}")
                    params.append(json.dumps(value) if value else "{}")
                else:
                    set_clauses.append(f"{key} = ${param_idx}")
                    params.append(value)
                param_idx += 1
            
            if not set_clauses:
                return False
            
            sql = f"UPDATE operators SET {', '.join(set_clauses)} WHERE {' AND '.join(where_conditions)}"
            result = await conn.execute(sql, *params)
            return result != "UPDATE 0"
    
    async def fleet_vehicles_update_one(self, query: Dict[str, Any], update: Dict[str, Any]) -> bool:
        """Update fleet vehicle"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        async with self.pool.acquire() as conn:
            where_conditions = []
            params = []
            param_idx = 1
            
            if "_id" in query or "id" in query:
                vehicle_id = UUID(query.get("_id") or query.get("id"))
                where_conditions.append(f"id = ${param_idx}")
                params.append(vehicle_id)
                param_idx += 1
            
            if not where_conditions:
                return False
            
            set_clauses = []
            set_values = update.get("$set", {})
            for key, value in set_values.items():
                if key == "metadata":
                    set_clauses.append(f"{key} = ${param_idx}")
                    params.append(json.dumps(value) if value else "{}")
                else:
                    set_clauses.append(f"{key} = ${param_idx}")
                    params.append(value)
                param_idx += 1
            
            if not set_clauses:
                return False
            
            sql = f"UPDATE fleet_vehicles SET {', '.join(set_clauses)} WHERE {' AND '.join(where_conditions)}"
            result = await conn.execute(sql, *params)
            return result != "UPDATE 0"
    
    # Facilities operations
    async def facilities_find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find one facility"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            if "_id" in query or "id" in query:
                facility_id = query.get("_id") or query.get("id")
                if isinstance(facility_id, str):
                    try:
                        facility_id = UUID(facility_id)
                    except ValueError:
                        return None
                row = await conn.fetchrow("SELECT * FROM facilities WHERE id = $1", facility_id)
                return self._deserialize_doc(row) if row else None
            elif "code" in query:
                row = await conn.fetchrow("SELECT * FROM facilities WHERE code = $1", query["code"])
                return self._deserialize_doc(row) if row else None
            return None
    
    async def facilities_find(self, query: Dict[str, Any], sort: Optional[List] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Find facilities"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            conditions = []
            params = []
            param_idx = 1
            
            if "type" in query:
                conditions.append(f"type = ${param_idx}")
                params.append(query["type"])
                param_idx += 1
            
            where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
            order_clause = "ORDER BY name ASC"
            if sort:
                for field, direction in sort:
                    dir_str = "DESC" if direction == -1 else "ASC"
                    order_clause = f"ORDER BY {field} {dir_str}"
            
            limit_clause = f"LIMIT {limit}" if limit else ""
            sql = f"SELECT * FROM facilities {where_clause} {order_clause} {limit_clause}"
            rows = await conn.fetch(sql, *params)
            return [self._deserialize_doc(row) for row in rows]
    
    async def facilities_insert_one(self, doc: Dict[str, Any]) -> str:
        """Insert one facility"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            facility_id = uuid4()
            await conn.execute(
                """INSERT INTO facilities (
                    id, external_id, name, type, code, address, location, metadata, created_by
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)""",
                facility_id,
                doc.get("external_id"),
                doc["name"],
                doc["type"],
                doc.get("code"),
                json.dumps(doc.get("address")) if doc.get("address") else None,
                json.dumps(doc.get("location")) if doc.get("location") else None,
                json.dumps(doc.get("metadata", {})) if doc.get("metadata") else "{}",
                UUID(doc["created_by"]) if doc.get("created_by") else None
            )
            return str(facility_id)
    
    async def facilities_update_one(self, query: Dict[str, Any], update: Dict[str, Any]) -> bool:
        """Update one facility"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            facility_id = query.get("_id") or query.get("id")
            if isinstance(facility_id, str):
                facility_id = UUID(facility_id)
            
            # Extract $set from MongoDB-style update
            set_values = update.get("$set", update)
            
            set_clauses = []
            params = []
            param_idx = 1
            
            for key, value in set_values.items():
                if key in ["address", "location", "metadata"]:
                    set_clauses.append(f"{key} = ${param_idx}")
                    params.append(json.dumps(value) if value else None)
                else:
                    set_clauses.append(f"{key} = ${param_idx}")
                    params.append(value)
                param_idx += 1
            
            if not set_clauses:
                return False
            
            params.append(facility_id)
            sql = f"UPDATE facilities SET {', '.join(set_clauses)} WHERE id = ${param_idx}"
            result = await conn.execute(sql, *params)
            return result == "UPDATE 1"
    
    # Parties operations
    async def parties_find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find one party"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            if "_id" in query or "id" in query:
                party_id = query.get("_id") or query.get("id")
                if isinstance(party_id, str):
                    try:
                        party_id = UUID(party_id)
                    except ValueError:
                        return None
                row = await conn.fetchrow("SELECT * FROM parties WHERE id = $1", party_id)
                return self._deserialize_doc(row) if row else None
            elif "code" in query:
                row = await conn.fetchrow("SELECT * FROM parties WHERE code = $1", query["code"])
                return self._deserialize_doc(row) if row else None
            return None
    
    async def parties_find(self, query: Dict[str, Any], sort: Optional[List] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Find parties"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            conditions = []
            params = []
            param_idx = 1
            
            if "type" in query:
                conditions.append(f"type = ${param_idx}")
                params.append(query["type"])
                param_idx += 1
            
            where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
            order_clause = "ORDER BY name ASC"
            if sort:
                for field, direction in sort:
                    dir_str = "DESC" if direction == -1 else "ASC"
                    order_clause = f"ORDER BY {field} {dir_str}"
            
            limit_clause = f"LIMIT {limit}" if limit else ""
            sql = f"SELECT * FROM parties {where_clause} {order_clause} {limit_clause}"
            rows = await conn.fetch(sql, *params)
            return [self._deserialize_doc(row) for row in rows]
    
    async def parties_insert_one(self, doc: Dict[str, Any]) -> str:
        """Insert one party"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            party_id = uuid4()
            await conn.execute(
                """INSERT INTO parties (
                    id, external_id, name, type, code, contact_info, metadata, created_by
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)""",
                party_id,
                doc.get("external_id"),
                doc["name"],
                doc["type"],
                doc.get("code"),
                json.dumps(doc.get("contact_info")) if doc.get("contact_info") else None,
                json.dumps(doc.get("metadata", {})) if doc.get("metadata") else "{}",
                UUID(doc["created_by"]) if doc.get("created_by") else None
            )
            return str(party_id)
    
    async def parties_update_one(self, query: Dict[str, Any], update: Dict[str, Any]) -> bool:
        """Update one party"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            party_id = query.get("_id") or query.get("id")
            if isinstance(party_id, str):
                party_id = UUID(party_id)
            
            # Extract $set from MongoDB-style update
            set_values = update.get("$set", update)
            
            set_clauses = []
            params = []
            param_idx = 1
            
            for key, value in set_values.items():
                if key in ["contact_info", "metadata"]:
                    set_clauses.append(f"{key} = ${param_idx}")
                    params.append(json.dumps(value) if value else None)
                else:
                    set_clauses.append(f"{key} = ${param_idx}")
                    params.append(value)
                param_idx += 1
            
            if not set_clauses:
                return False
            
            params.append(party_id)
            sql = f"UPDATE parties SET {', '.join(set_clauses)} WHERE id = ${param_idx}"
            result = await conn.execute(sql, *params)
            return result == "UPDATE 1"
    
    # DisputePackets operations
    async def dispute_packets_find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find one dispute packet"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            if "_id" in query or "id" in query:
                packet_id = query.get("_id") or query.get("id")
                if isinstance(packet_id, str):
                    try:
                        packet_id = UUID(packet_id)
                    except ValueError:
                        return None
                row = await conn.fetchrow("SELECT * FROM dispute_packets WHERE id = $1", packet_id)
                return self._deserialize_doc(row) if row else None
            return None
    
    async def dispute_packets_find(self, query: Dict[str, Any], sort: Optional[List] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Find dispute packets"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            conditions = []
            params = []
            param_idx = 1
            
            if "movement_id" in query:
                conditions.append(f"movement_id = ${param_idx}")
                params.append(UUID(query["movement_id"]))
                param_idx += 1
            
            if "status" in query:
                conditions.append(f"status = ${param_idx}")
                params.append(query["status"])
                param_idx += 1
            
            where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
            order_clause = "ORDER BY created_at DESC"
            if sort:
                for field, direction in sort:
                    dir_str = "DESC" if direction == -1 else "ASC"
                    order_clause = f"ORDER BY {field} {dir_str}"
            
            limit_clause = f"LIMIT {limit}" if limit else ""
            sql = f"SELECT * FROM dispute_packets {where_clause} {order_clause} {limit_clause}"
            rows = await conn.fetch(sql, *params)
            return [self._deserialize_doc(row) for row in rows]
    
    async def dispute_packets_insert_one(self, doc: Dict[str, Any]) -> str:
        """Insert one dispute packet"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            packet_id = uuid4()
            # Convert UUID arrays
            selected_events = [UUID(e) for e in doc.get("selected_events", [])] if doc.get("selected_events") else []
            selected_attachments = [UUID(a) for a in doc.get("selected_attachments", [])] if doc.get("selected_attachments") else []
            
            await conn.execute(
                """INSERT INTO dispute_packets (
                    id, movement_id, external_id, invoice_id, template_type, status,
                    selected_events, selected_attachments, narrative, generated_at,
                    submitted_at, resolved_at, outcome, outcome_amount, metadata, created_by
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16)""",
                packet_id,
                UUID(doc["movement_id"]),
                doc.get("external_id"),
                doc.get("invoice_id"),
                doc.get("template_type"),
                doc.get("status", "draft"),
                selected_events,
                selected_attachments,
                doc.get("narrative"),
                doc.get("generated_at"),
                doc.get("submitted_at"),
                doc.get("resolved_at"),
                doc.get("outcome"),
                doc.get("outcome_amount"),
                json.dumps(doc.get("metadata", {})) if doc.get("metadata") else "{}",
                UUID(doc["created_by"]) if doc.get("created_by") else None
            )
            return str(packet_id)
    
    async def dispute_packets_update_one(self, query: Dict[str, Any], update: Dict[str, Any]) -> bool:
        """Update one dispute packet"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            packet_id = query.get("_id") or query.get("id")
            if isinstance(packet_id, str):
                packet_id = UUID(packet_id)
            
            # Extract $set from MongoDB-style update
            set_values = update.get("$set", update)
            
            set_clauses = []
            params = []
            param_idx = 1
            
            for key, value in set_values.items():
                if key == "selected_events" and value:
                    set_clauses.append(f"{key} = ${param_idx}")
                    params.append([UUID(e) for e in value])
                elif key == "selected_attachments" and value:
                    set_clauses.append(f"{key} = ${param_idx}")
                    params.append([UUID(a) for a in value])
                elif key == "metadata":
                    set_clauses.append(f"{key} = ${param_idx}")
                    params.append(json.dumps(value) if value else "{}")
                else:
                    set_clauses.append(f"{key} = ${param_idx}")
                    params.append(value)
                param_idx += 1
            
            if not set_clauses:
                return False
            
            params.append(packet_id)
            sql = f"UPDATE dispute_packets SET {', '.join(set_clauses)} WHERE id = ${param_idx}"
            result = await conn.execute(sql, *params)
            return result == "UPDATE 1"
    
    # Attachments operations
    async def attachments_find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find one attachment"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            if "_id" in query or "id" in query:
                attachment_id = query.get("_id") or query.get("id")
                if isinstance(attachment_id, str):
                    try:
                        attachment_id = UUID(attachment_id)
                    except ValueError:
                        return None
                row = await conn.fetchrow("SELECT * FROM attachments WHERE id = $1", attachment_id)
                return self._deserialize_doc(row) if row else None
            return None
    
    async def attachments_find(self, query: Dict[str, Any], sort: Optional[List] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Find attachments"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            conditions = []
            params = []
            param_idx = 1
            
            if "event_id" in query:
                conditions.append(f"event_id = ${param_idx}")
                params.append(UUID(query["event_id"]))
                param_idx += 1
            
            if "movement_id" in query:
                conditions.append(f"movement_id = ${param_idx}")
                params.append(UUID(query["movement_id"]))
                param_idx += 1
            
            where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
            order_clause = "ORDER BY created_at DESC"
            if sort:
                for field, direction in sort:
                    dir_str = "DESC" if direction == -1 else "ASC"
                    order_clause = f"ORDER BY {field} {dir_str}"
            
            limit_clause = f"LIMIT {limit}" if limit else ""
            sql = f"SELECT * FROM attachments {where_clause} {order_clause} {limit_clause}"
            rows = await conn.fetch(sql, *params)
            return [self._deserialize_doc(row) for row in rows]
    
    async def attachments_insert_one(self, doc: Dict[str, Any]) -> str:
        """Insert one attachment"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            attachment_id = uuid4()
            await conn.execute(
                """INSERT INTO attachments (
                    id, event_id, movement_id, filename, file_type, mime_type,
                    file_size, storage_url, storage_key, metadata, uploaded_by
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)""",
                attachment_id,
                UUID(doc["event_id"]) if doc.get("event_id") else None,
                UUID(doc["movement_id"]) if doc.get("movement_id") else None,
                doc["filename"],
                doc["file_type"],
                doc.get("mime_type"),
                doc.get("file_size"),
                doc.get("storage_url"),
                doc.get("storage_key"),
                json.dumps(doc.get("metadata", {})) if doc.get("metadata") else "{}",
                UUID(doc["uploaded_by"]) if doc.get("uploaded_by") else None
            )
            return str(attachment_id)
    
    async def attachments_delete_one(self, query: Dict[str, Any]) -> bool:
        """Delete one attachment"""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            attachment_id = query.get("_id") or query.get("id")
            if isinstance(attachment_id, str):
                attachment_id = UUID(attachment_id)
            
            result = await conn.execute("DELETE FROM attachments WHERE id = $1", attachment_id)
            return result == "DELETE 1"

