"""
Vercel Serverless Function for FastAPI Backend
Direct app export - Vercel natively supports ASGI
"""

import sys
import os

# Path setup - handle both local and Vercel deployment
_here = os.path.dirname(os.path.abspath(__file__))

# First, try backend in same directory (for Vercel deployment)
_api_backend = os.path.join(_here, "backend")
if os.path.exists(_api_backend):
    if _api_backend not in sys.path:
        sys.path.insert(0, _api_backend)

# Also try parent directory's backend (for local development)
_root = os.path.dirname(_here)  # Go up from api/ to project root
_backend = os.path.join(_root, "backend")
if os.path.exists(_backend) and _backend not in sys.path:
    sys.path.insert(0, _backend)
if _root not in sys.path:
    sys.path.insert(0, _root)

os.environ.setdefault("USE_SUPABASE", "true")

# Import and export the FastAPI app directly
# Vercel will automatically detect 'app' and handle it as ASGI
try:
    import importlib
    
    # Try importing from api/backend first (Vercel deployment)
    if os.path.exists(_api_backend) and os.path.exists(os.path.join(_api_backend, "server.py")):
        # Import directly from the backend directory
        import sys
        import importlib.util
        
        server_path = os.path.join(_api_backend, "server.py")
        spec = importlib.util.spec_from_file_location("server", server_path)
        server_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(server_module)
    elif os.path.exists(_backend) and os.path.exists(os.path.join(_backend, "server.py")):
        # Fallback to parent backend (local development)
        server_path = os.path.join(_backend, "server.py")
        spec = importlib.util.spec_from_file_location("server", server_path)
        server_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(server_module)
    else:
        # Last resort: try standard import
        server_module = importlib.import_module("server")
    
    app = server_module.app
except Exception as e:
    # Debug: print paths to help diagnose
    print(f"Error importing server module: {e}")
    print(f"Current directory: {os.getcwd()}")
    print(f"__file__ location: {__file__}")
    print(f"Python path: {sys.path}")
    print(f"Looking for api/backend at: {_api_backend}")
    print(f"api/backend exists: {os.path.exists(_api_backend)}")
    if os.path.exists(_api_backend):
        print(f"api/backend/server.py exists: {os.path.exists(os.path.join(_api_backend, 'server.py'))}")
        print(f"api/backend contents: {os.listdir(_api_backend)[:10]}")
    print(f"Looking for parent backend at: {_backend}")
    print(f"Parent backend exists: {os.path.exists(_backend)}")
    if os.path.exists(_backend):
        print(f"Parent backend/server.py exists: {os.path.exists(os.path.join(_backend, 'server.py'))}")
        print(f"Parent backend contents: {os.listdir(_backend)[:10]}")
    raise
