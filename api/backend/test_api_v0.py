"""
Test script for API v0 endpoints
Tests Facilities, Parties, and DisputePackets endpoints
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
from datetime import datetime, timezone
from uuid import uuid4

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

async def test_database_connection():
    """Test database connection and new tables"""
    print("🔍 Testing database connection and new tables...")
    try:
        from db_adapter import SupabaseAdapter
        
        db_url = os.getenv("SUPABASE_DB_URL")
        if not db_url:
            print("❌ SUPABASE_DB_URL not found in environment")
            return False, None
        
        adapter = SupabaseAdapter(db_url)
        await adapter.connect()
        print("✅ Database connected")
        
        # Check if new tables exist
        import asyncpg
        async with adapter.pool.acquire() as conn:
            tables_to_check = ['facilities', 'parties', 'dispute_packets', 'attachments']
            for table in tables_to_check:
                result = await conn.fetchval(f"""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = '{table}'
                    );
                """)
                if result:
                    print(f"✅ Table '{table}' exists")
                else:
                    print(f"❌ Table '{table}' does NOT exist")
                    return False, None
        
        return True, adapter
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None

async def test_facilities_crud(adapter):
    """Test Facilities CRUD operations"""
    print("\n🔍 Testing Facilities CRUD...")
    try:
        from db_compat import DBDatabase
        db = DBDatabase(adapter)
        
        # Create a test facility
        test_facility = {
            "name": f"Test Port {uuid4().hex[:8]}",
            "type": "port",
            "code": f"TEST{uuid4().hex[:4].upper()}",
            "address": {"city": "Mumbai", "state": "Maharashtra"},
            "location": {"latitude": 18.9, "longitude": 72.8},
            "metadata": {"test": True},
            "created_by": str(uuid4())  # Dummy user ID
        }
        
        result = await db.facilities.insert_one(test_facility)
        facility_id = str(result.inserted_id)
        print(f"✅ Created facility: {facility_id}")
        
        # Read facility
        facility = await db.facilities.find_one({"_id": facility_id})
        if facility and facility.get("name") == test_facility["name"]:
            print(f"✅ Read facility: {facility.get('name')}")
        else:
            print(f"❌ Failed to read facility")
            return False
        
        # List facilities
        cursor = await db.facilities.find({"type": "port"}, sort=[("name", 1)], limit=10)
        facilities = await cursor.to_list(length=10)
        print(f"✅ Listed {len(facilities)} facilities")
        
        # Update facility
        await db.facilities.update_one(
            {"_id": facility_id},
            {"$set": {"code": "UPDATED"}}
        )
        updated = await db.facilities.find_one({"_id": facility_id})
        if updated and updated.get("code") == "UPDATED":
            print(f"✅ Updated facility")
        else:
            print(f"❌ Failed to update facility")
            return False
        
        print("✅ Facilities CRUD test passed")
        return True, facility_id
        
    except Exception as e:
        print(f"❌ Facilities CRUD test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None

async def test_parties_crud(adapter):
    """Test Parties CRUD operations"""
    print("\n🔍 Testing Parties CRUD...")
    try:
        from db_compat import DBDatabase
        db = DBDatabase(adapter)
        
        # Create a test party
        test_party = {
            "name": f"Test Forwarder {uuid4().hex[:8]}",
            "type": "forwarder",
            "code": f"FWD{uuid4().hex[:4].upper()}",
            "contact_info": {"email": "test@example.com", "phone": "+91-1234567890"},
            "metadata": {"test": True},
            "created_by": str(uuid4())  # Dummy user ID
        }
        
        result = await db.parties.insert_one(test_party)
        party_id = str(result.inserted_id)
        print(f"✅ Created party: {party_id}")
        
        # Read party
        party = await db.parties.find_one({"_id": party_id})
        if party and party.get("name") == test_party["name"]:
            print(f"✅ Read party: {party.get('name')}")
        else:
            print(f"❌ Failed to read party")
            return False
        
        # List parties
        cursor = await db.parties.find({"type": "forwarder"}, sort=[("name", 1)], limit=10)
        parties = await cursor.to_list(length=10)
        print(f"✅ Listed {len(parties)} parties")
        
        # Update party
        await db.parties.update_one(
            {"_id": party_id},
            {"$set": {"code": "UPDATED"}}
        )
        updated = await db.parties.find_one({"_id": party_id})
        if updated and updated.get("code") == "UPDATED":
            print(f"✅ Updated party")
        else:
            print(f"❌ Failed to update party")
            return False
        
        print("✅ Parties CRUD test passed")
        return True, party_id
        
    except Exception as e:
        print(f"❌ Parties CRUD test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None

async def test_dispute_packets_crud(adapter):
    """Test DisputePackets CRUD operations"""
    print("\n🔍 Testing DisputePackets CRUD...")
    try:
        from db_compat import DBDatabase
        db = DBDatabase(adapter)
        
        # First, we need a case/movement to link to
        # Create a test case
        test_case = {
            "operator_id": str(uuid4()),
            "operator_email": "test@example.com",
            "description": "Test case for dispute packet",
            "status": "REPORTED",
            "disruption_details": {"disruption_type": "delay"},
            "shipment_identifiers": {},
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        
        case_result = await db.cases.insert_one(test_case)
        case_id = str(case_result.inserted_id)
        print(f"✅ Created test case: {case_id}")
        
        # Create a test dispute packet
        test_packet = {
            "movement_id": case_id,
            "invoice_id": f"INV-{uuid4().hex[:8]}",
            "template_type": "jnpt_demurrage",
            "status": "draft",
            "selected_events": [],
            "selected_attachments": [],
            "narrative": "Test dispute packet",
            "metadata": {"test": True},
            "created_by": str(uuid4())  # Dummy user ID
        }
        
        result = await db.dispute_packets.insert_one(test_packet)
        packet_id = str(result.inserted_id)
        print(f"✅ Created dispute packet: {packet_id}")
        
        # Read packet
        packet = await db.dispute_packets.find_one({"_id": packet_id})
        if packet and packet.get("invoice_id") == test_packet["invoice_id"]:
            print(f"✅ Read dispute packet: {packet.get('invoice_id')}")
        else:
            print(f"❌ Failed to read dispute packet")
            return False
        
        # List packets for movement
        cursor = await db.dispute_packets.find({"movement_id": case_id}, sort=[("created_at", -1)], limit=10)
        packets = await cursor.to_list(length=10)
        print(f"✅ Listed {len(packets)} dispute packets")
        
        # Update packet
        await db.dispute_packets.update_one(
            {"_id": packet_id},
            {"$set": {"status": "generated", "generated_at": datetime.now(timezone.utc)}}
        )
        updated = await db.dispute_packets.find_one({"_id": packet_id})
        if updated and updated.get("status") == "generated":
            print(f"✅ Updated dispute packet")
        else:
            print(f"❌ Failed to update dispute packet")
            return False
        
        print("✅ DisputePackets CRUD test passed")
        return True, (case_id, packet_id)
        
    except Exception as e:
        print(f"❌ DisputePackets CRUD test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None

async def main():
    print("=" * 60)
    print("Ward API v0 Endpoints Test")
    print("=" * 60)
    print()
    
    # Test database connection
    db_ok, adapter = await test_database_connection()
    
    if not db_ok:
        print("\n❌ Database connection failed. Cannot continue tests.")
        print("\nNext steps:")
        print("1. Run migration: supabase/migrations/002_api_v0_tables.sql")
        print("2. Check SUPABASE_DB_URL is correct")
        return 1
    
    # Test Facilities
    facilities_ok, facility_id = await test_facilities_crud(adapter)
    
    # Test Parties
    parties_ok, party_id = await test_parties_crud(adapter)
    
    # Test DisputePackets
    packets_ok, packet_data = await test_dispute_packets_crud(adapter)
    
    # Close connection
    await adapter.close()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Database Connection: {'✅ PASS' if db_ok else '❌ FAIL'}")
    print(f"Facilities CRUD: {'✅ PASS' if facilities_ok else '❌ FAIL'}")
    print(f"Parties CRUD: {'✅ PASS' if parties_ok else '❌ FAIL'}")
    print(f"DisputePackets CRUD: {'✅ PASS' if packets_ok else '❌ FAIL'}")
    print()
    
    if db_ok and facilities_ok and parties_ok and packets_ok:
        print("✅ All tests passed! API v0 endpoints are working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Check errors above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

