#!/usr/bin/env python3
"""
Test script to debug evidence scoring calculation
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from db_adapter import SupabaseAdapter
from db_compat import DBDatabase
from evidence_service import EvidenceService

load_dotenv()

SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")

async def test_evidence_scoring():
    print("=" * 70)
    print("EVIDENCE SCORING DEBUG TEST")
    print("=" * 70)
    
    if not SUPABASE_DB_URL:
        print("❌ SUPABASE_DB_URL not found")
        return
    
    adapter = SupabaseAdapter(SUPABASE_DB_URL)
    await adapter.connect()
    db = DBDatabase(adapter)
    
    # Find a test case
    print("\n1. Finding test cases...")
    cases_cursor = await db.cases.find({}, limit=5)
    cases = await cases_cursor.to_list(length=5)
    
    if not cases:
        print("❌ No cases found in database")
        await adapter.close()
        return
    
    test_case = cases[0]
    case_id = test_case.get("_id") or test_case.get("id")
    print(f"✅ Found test case: {case_id}")
    print(f"   Description: {test_case.get('description', 'N/A')[:50]}...")
    
    # Test timeline query
    print("\n2. Testing timeline query...")
    try:
        timeline_cursor = await db.timeline_events.find({"case_id": case_id})
        timeline = await timeline_cursor.to_list(length=100)
        print(f"✅ Timeline query successful: {len(timeline)} events found")
        if timeline:
            print(f"   First event: {timeline[0].get('content', 'N/A')[:50]}...")
    except Exception as e:
        print(f"❌ Timeline query failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test documents query
    print("\n3. Testing documents query...")
    try:
        docs_cursor = await db.documents.find({"case_id": case_id})
        docs = await docs_cursor.to_list(length=100)
        print(f"✅ Documents query successful: {len(docs)} documents found")
    except Exception as e:
        print(f"❌ Documents query failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test evidence service
    print("\n4. Testing EvidenceService...")
    try:
        evidence_service = EvidenceService(db)
        result = await evidence_service.calculate_and_update_score(case_id)
        
        if result:
            print(f"✅ Evidence score calculation successful!")
            print(f"   Score: {result.get('score', 0)}/100")
            print(f"   Breakdown: {len(result.get('breakdown', []))} items")
            print(f"   Missing: {len(result.get('missing_actions', []))} actions")
        else:
            print("❌ Evidence score calculation returned None")
    except Exception as e:
        print(f"❌ Evidence score calculation failed: {e}")
        import traceback
        traceback.print_exc()
    
    await adapter.close()
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(test_evidence_scoring())

