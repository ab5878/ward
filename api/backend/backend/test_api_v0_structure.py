"""
Test API v0 endpoint structure and imports
Tests that all endpoints are properly defined without requiring database connection
"""

import sys
import os
import inspect

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing imports...")
    try:
        from server import app
        print("✅ FastAPI app imported")
        
        from db_adapter import SupabaseAdapter
        print("✅ SupabaseAdapter imported")
        
        from db_compat import DBDatabase, DBCollection
        print("✅ DBDatabase and DBCollection imported")
        
        from dispute_service import DisputeBundleService
        print("✅ DisputeBundleService imported")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_endpoint_definitions():
    """Test that all API v0 endpoints are defined"""
    print("\n🔍 Testing endpoint definitions...")
    try:
        from server import app
        
        # Get all routes
        routes = []
        for route in app.routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                routes.append({
                    'path': route.path,
                    'methods': list(route.methods)
                })
        
        # Expected API v0 endpoints
        expected_endpoints = [
            # Movements
            ('/api/v0/movements', ['POST']),
            ('/api/v0/movements', ['GET']),
            ('/api/v0/movements/{movement_id}', ['GET']),
            # Events
            ('/api/v0/events', ['POST']),
            # Attachments
            ('/api/v0/attachments', ['POST']),
            ('/api/v0/attachments/{attachment_id}', ['GET']),
            ('/api/v0/events/{event_id}/attachments', ['GET']),
            # DisputePackets
            ('/api/v0/movements/{movement_id}/dispute-packets', ['POST']),
            ('/api/v0/movements/{movement_id}/dispute-packets', ['GET']),
            ('/api/v0/dispute-packets/{packet_id}', ['GET']),
            ('/api/v0/dispute-packets/{packet_id}/export', ['POST']),
            ('/api/v0/dispute-packets/{packet_id}', ['PATCH']),
            # Facilities
            ('/api/v0/facilities', ['POST']),
            ('/api/v0/facilities', ['GET']),
            ('/api/v0/facilities/{facility_id}', ['GET']),
            # Parties
            ('/api/v0/parties', ['POST']),
            ('/api/v0/parties', ['GET']),
            ('/api/v0/parties/{party_id}', ['GET']),
        ]
        
        found_endpoints = []
        missing_endpoints = []
        
        for expected_path, expected_methods in expected_endpoints:
            found = False
            for route in routes:
                # Normalize path (FastAPI uses {param} format)
                route_path = route['path'].replace('<', '{').replace('>', '}')
                if route_path == expected_path:
                    # Check if at least one method matches
                    if any(m in route['methods'] for m in expected_methods):
                        found = True
                        found_endpoints.append((expected_path, expected_methods))
                        print(f"✅ Found: {expected_methods[0]} {expected_path}")
                        break
            
            if not found:
                missing_endpoints.append((expected_path, expected_methods))
                print(f"❌ Missing: {expected_methods[0]} {expected_path}")
        
        if missing_endpoints:
            print(f"\n❌ {len(missing_endpoints)} endpoints missing")
            return False
        else:
            print(f"\n✅ All {len(found_endpoints)} expected endpoints found")
            return True
            
    except Exception as e:
        print(f"❌ Endpoint definition test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pydantic_models():
    """Test that Pydantic models are defined"""
    print("\n🔍 Testing Pydantic models...")
    try:
        from server import (
            CreateFacility, CreateParty, CreateDisputePacket, 
            UpdateDisputePacket, CreateMovement, CreateEvent
        )
        
        print("✅ CreateFacility model imported")
        print("✅ CreateParty model imported")
        print("✅ CreateDisputePacket model imported")
        print("✅ UpdateDisputePacket model imported")
        
        # Test model instantiation
        facility = CreateFacility(
            name="Test Facility",
            type="port"
        )
        print("✅ CreateFacility can be instantiated")
        
        party = CreateParty(
            name="Test Party",
            type="forwarder"
        )
        print("✅ CreateParty can be instantiated")
        
        packet = CreateDisputePacket(
            invoice_id="INV-123"
        )
        print("✅ CreateDisputePacket can be instantiated")
        
        update = UpdateDisputePacket(
            status="generated"
        )
        print("✅ UpdateDisputePacket can be instantiated")
        
        movement = CreateMovement(
            container_id="TEST-123",
            lane="JNPT-Delhi"
        )
        print("✅ CreateMovement can be instantiated")
        
        event = CreateEvent(
            movement_id="test-id",
            event_type="incident"
        )
        print("✅ CreateEvent can be instantiated")
        
        return True
        
    except Exception as e:
        print(f"❌ Pydantic model test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database_adapter_methods():
    """Test that database adapter methods exist"""
    print("\n🔍 Testing database adapter methods...")
    try:
        from db_adapter import SupabaseAdapter
        
        adapter = SupabaseAdapter("dummy://connection")
        
        # Check for required methods
        required_methods = [
            'facilities_find_one',
            'facilities_find',
            'facilities_insert_one',
            'facilities_update_one',
            'parties_find_one',
            'parties_find',
            'parties_insert_one',
            'parties_update_one',
            'dispute_packets_find_one',
            'dispute_packets_find',
            'dispute_packets_insert_one',
            'dispute_packets_update_one',
            'attachments_find_one',
            'attachments_find',
            'attachments_insert_one',
            'attachments_delete_one',
        ]
        
        missing_methods = []
        for method_name in required_methods:
            if hasattr(adapter, method_name):
                print(f"✅ Method exists: {method_name}")
            else:
                missing_methods.append(method_name)
                print(f"❌ Method missing: {method_name}")
        
        if missing_methods:
            print(f"\n❌ {len(missing_methods)} methods missing")
            return False
        else:
            print(f"\n✅ All {len(required_methods)} required methods exist")
            return True
            
    except Exception as e:
        print(f"❌ Database adapter method test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_db_compat_collections():
    """Test that db_compat supports new collections"""
    print("\n🔍 Testing db_compat collections...")
    try:
        from db_compat import DBDatabase
        from db_adapter import SupabaseAdapter
        
        # Create dummy adapter
        adapter = SupabaseAdapter("dummy://connection")
        db = DBDatabase(adapter)
        
        # Check collections exist
        collections = ['facilities', 'parties', 'dispute_packets', 'attachments']
        for collection_name in collections:
            collection = db[collection_name]
            if collection:
                print(f"✅ Collection accessible: {collection_name}")
            else:
                print(f"❌ Collection not accessible: {collection_name}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ db_compat collection test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("Ward API v0 Structure Test")
    print("=" * 60)
    print()
    
    tests = [
        ("Imports", test_imports),
        ("Endpoint Definitions", test_endpoint_definitions),
        ("Pydantic Models", test_pydantic_models),
        ("Database Adapter Methods", test_database_adapter_methods),
        ("DB Compat Collections", test_db_compat_collections),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ All structure tests passed! Code is properly structured.")
        print("\n💡 Next: Test against deployed API with HTTP requests")
        return 0
    else:
        print("\n❌ Some structure tests failed. Fix issues before deployment.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

