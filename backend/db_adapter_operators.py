"""
Database Adapter Methods for Operator Tables
Add these methods to db_adapter.py
"""

# Add these methods to SupabaseAdapter class in db_adapter.py

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

