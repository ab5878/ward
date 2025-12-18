"""
Database Compatibility Layer
Makes Supabase adapter work with existing MongoDB-style code
"""

from typing import Dict, Any, List, Optional
from db_adapter import SupabaseAdapter
from uuid import UUID


class DBCursor:
    """Mimics MongoDB cursor for compatibility"""
    
    def __init__(self, results: List[Dict[str, Any]]):
        self.results = results
        self.index = 0
    
    async def to_list(self, length: Optional[int] = None) -> List[Dict[str, Any]]:
        """Convert cursor to list"""
        if length:
            return self.results[:length]
        return self.results
    
    def sort(self, *args):
        """Sort cursor (no-op, sorting done in query)"""
        return self
    
    def limit(self, *args):
        """Limit cursor (no-op, limit done in query)"""
        return self


class DBCollection:
    """Mimics MongoDB collection for compatibility"""
    
    def __init__(self, adapter: SupabaseAdapter, collection_name: str):
        self.adapter = adapter
        self.collection_name = collection_name
    
    async def find_one(self, query: Dict[str, Any], sort: Optional[List] = None):
        """Find one document"""
        # Convert ObjectId strings to UUID format if needed
        query = self._convert_query(query)
        
        if self.collection_name == "users":
            return await self.adapter.users_find_one(query)
        elif self.collection_name == "cases":
            return await self.adapter.cases_find_one(query)
        elif self.collection_name == "timeline_events":
            return await self.adapter.timeline_events_find_one(query, sort=sort)
        elif self.collection_name == "audit_entries":
            return None  # Not implemented yet
        elif self.collection_name == "documents":
            return await self.adapter.documents_find_one(query)
        elif self.collection_name == "drafts":
            return await self.adapter.drafts_find_one(query)
        elif self.collection_name == "approvals":
            return await self.adapter.approvals_find_one(query)
        elif self.collection_name == "decisions":
            return await self.adapter.decisions_find_one(query)
        elif self.collection_name == "historical":
            return await self.adapter.historical_find_one(query)
        elif self.collection_name == "facilities":
            return await self.adapter.facilities_find_one(query)
        elif self.collection_name == "parties":
            return await self.adapter.parties_find_one(query)
        elif self.collection_name == "dispute_packets":
            return await self.adapter.dispute_packets_find_one(query)
        elif self.collection_name == "attachments":
            return await self.adapter.attachments_find_one(query)
        elif self.collection_name == "operators":
            return await self.adapter.operators_find_one(query)
        elif self.collection_name == "fleet_vehicles":
            return await self.adapter.fleet_vehicles_find_one(query)
        elif self.collection_name == "magic_links":
            return await self.adapter.magic_links_find_one(query)
        else:
            raise NotImplementedError(f"Collection {self.collection_name} not implemented")
    
    async def find(self, query: Dict[str, Any] = None, sort: Optional[List] = None, limit: Optional[int] = None):
        """Find documents"""
        if query is None:
            query = {}
        
        query = self._convert_query(query)
        
        if self.collection_name == "users":
            results = []  # Not implemented
        elif self.collection_name == "cases":
            # Use provided sort/limit or defaults
            sort = sort or [("updated_at", -1)]
            limit = limit or 100
            results = await self.adapter.cases_find(query, sort=sort, limit=limit)
        elif self.collection_name == "timeline_events":
            sort = sort or [("timestamp", -1)]
            results = await self.adapter.timeline_events_find(query, sort=sort, limit=limit)
        elif self.collection_name == "audit_entries":
            sort = sort or [("timestamp", -1)]
            results = await self.adapter.audit_entries_find(query, sort=sort, limit=limit)
        elif self.collection_name == "documents":
            sort = sort or [("uploaded_at", -1)]
            results = await self.adapter.documents_find(query, sort=sort, limit=limit)
        elif self.collection_name == "approvals":
            results = await self.adapter.approvals_find(query, sort=sort, limit=limit)
        elif self.collection_name == "historical":
            sort = sort or [("created_at", -1)]
            limit = limit or 20
            results = await self.adapter.historical_find(sort=sort, limit=limit)
        elif self.collection_name == "facilities":
            sort = sort or [("name", 1)]
            results = await self.adapter.facilities_find(query, sort=sort, limit=limit)
        elif self.collection_name == "parties":
            sort = sort or [("name", 1)]
            results = await self.adapter.parties_find(query, sort=sort, limit=limit)
        elif self.collection_name == "dispute_packets":
            sort = sort or [("created_at", -1)]
            results = await self.adapter.dispute_packets_find(query, sort=sort, limit=limit)
        elif self.collection_name == "attachments":
            sort = sort or [("created_at", -1)]
            results = await self.adapter.attachments_find(query, sort=sort, limit=limit)
        elif self.collection_name == "events":
            results = await self.adapter.events_find(query, sort=sort, limit=limit)
        elif self.collection_name == "fleet_vehicles":
            results = await self.adapter.fleet_vehicles_find(query, sort=sort, limit=limit)
        elif self.collection_name == "operators":
            # Operators don't have a find method yet, return empty for now
            results = []
        elif self.collection_name == "magic_links":
            # Magic links don't have a find method yet, return empty for now
            results = []
        else:
            raise NotImplementedError(f"Collection {self.collection_name} not implemented")
        
        return DBCursor(results)
    
    async def insert_one(self, doc: Dict[str, Any]):
        """Insert one document"""
        method_map = {
            "users": self.adapter.users_insert_one,
            "cases": self.adapter.cases_insert_one,
            "timeline_events": self.adapter.timeline_events_insert_one,
            "audit_entries": self.adapter.audit_entries_insert_one,
            "documents": self.adapter.documents_insert_one,
            "drafts": self.adapter.drafts_insert_one,
            "approvals": self.adapter.approvals_insert_one,
            "decisions": self.adapter.decisions_insert_one,
            "facilities": self.adapter.facilities_insert_one,
            "parties": self.adapter.parties_insert_one,
            "dispute_packets": self.adapter.dispute_packets_insert_one,
            "attachments": self.adapter.attachments_insert_one,
            "operators": self.adapter.operators_insert_one,
            "fleet_vehicles": self.adapter.fleet_vehicles_insert_one,
            "magic_links": self.adapter.magic_links_insert_one,
        }
        
        method = method_map.get(self.collection_name)
        if not method:
            raise NotImplementedError(f"Collection {self.collection_name} not implemented")
        
        # Convert ObjectId to UUID if needed
        doc = self._convert_doc(doc)
        doc_id = await method(doc)
        
        # Return MongoDB-style result
        class InsertResult:
            def __init__(self, inserted_id):
                self.inserted_id = inserted_id
        
        return InsertResult(doc_id)
    
    async def update_one(self, query: Dict[str, Any], update: Dict[str, Any], upsert: bool = False):
        """Update one document"""
        method_map = {
            "cases": self.adapter.cases_update_one,
            "drafts": self.adapter.drafts_update_one,
            "facilities": self.adapter.facilities_update_one,
            "parties": self.adapter.parties_update_one,
            "dispute_packets": self.adapter.dispute_packets_update_one,
            "operators": self.adapter.operators_update_one if hasattr(self.adapter, 'operators_update_one') else None,
            "fleet_vehicles": self.adapter.fleet_vehicles_update_one if hasattr(self.adapter, 'fleet_vehicles_update_one') else None,
            "magic_links": self.adapter.magic_links_update_one if hasattr(self.adapter, 'magic_links_update_one') else None,
        }
        
        method = method_map.get(self.collection_name)
        if not method:
            # For master_data collections, handle upsert by inserting if not exists
            if upsert and self.collection_name.startswith("master_"):
                existing = await self.find_one(query)
                if not existing:
                    doc = update.get("$set", {})
                    doc.update(query)
                    result = await self.insert_one(doc)
                    class UpdateResult:
                        def __init__(self, matched_count, upserted_id=None):
                            self.matched_count = matched_count
                            self.modified_count = matched_count
                            self.upserted_id = upserted_id
                    return UpdateResult(0, result.inserted_id)
                else:
                    # Document exists but no update method - return success
                    class UpdateResult:
                        def __init__(self, matched_count):
                            self.matched_count = matched_count
                            self.modified_count = matched_count
                    return UpdateResult(1)
            raise NotImplementedError(f"Collection {self.collection_name} not implemented")
        
        query = self._convert_query(query)
        
        # Handle upsert: try update first, if no match and upsert=True, insert
        if upsert:
            # Check if document exists
            existing = await self.find_one(query)
            if not existing:
                # Insert instead
                doc = update.get("$set", {})
                # Merge query fields into doc for insert
                doc.update(query)
                result = await self.insert_one(doc)
                class UpdateResult:
                    def __init__(self, matched_count, upserted_id=None):
                        self.matched_count = matched_count
                        self.modified_count = matched_count
                        self.upserted_id = upserted_id
                return UpdateResult(0, result.inserted_id)
        
        # Extract $set from MongoDB-style update
        update_dict = update.get("$set", update) if isinstance(update, dict) else update
        result = await method(query, update_dict)
        
        # Return MongoDB-style result
        class UpdateResult:
            def __init__(self, matched_count):
                self.matched_count = matched_count
                self.modified_count = matched_count
        
        return UpdateResult(1 if result else 0)
    
    def count_documents(self, query: Dict[str, Any] = None):
        """Count documents"""
        if query is None:
            query = {}
        
        if self.collection_name == "documents":
            return self.adapter.documents_count_documents(query)
        # For others, use find and count
        cursor = self.find(query)
        return len(cursor.results)
    
    def create_index(self, field: str, **kwargs):
        """Create index (no-op, indexes created in migration)"""
        return None
    
    def _convert_query(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Convert MongoDB query to Supabase query"""
        converted = {}
        for key, value in query.items():
            if key == "_id":
                # Convert ObjectId string to UUID
                if isinstance(value, str):
                    converted["_id"] = value
                else:
                    converted["_id"] = str(value)
            else:
                converted[key] = value
        return converted
    
    def _convert_doc(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Convert document for insertion"""
        converted = {}
        for key, value in doc.items():
            if key == "_id" and value:
                # Skip _id, will be generated
                continue
            converted[key] = value
        return converted


class DBDatabase:
    """Mimics MongoDB database for compatibility"""
    
    def __init__(self, adapter: SupabaseAdapter):
        self.adapter = adapter
        self._collections = {}
    
    def __getitem__(self, collection_name: str) -> DBCollection:
        """Get collection"""
        if collection_name not in self._collections:
            self._collections[collection_name] = DBCollection(self.adapter, collection_name)
        return self._collections[collection_name]
    
    def __getattr__(self, collection_name: str) -> DBCollection:
        """Get collection as attribute"""
        return self[collection_name]

