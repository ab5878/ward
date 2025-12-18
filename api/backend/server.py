from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta, timezone
from enum import Enum
import os
import jwt
import bcrypt
from dotenv import load_dotenv
import asyncio
from contextlib import asynccontextmanager
from uuid import UUID

# Import AI modules
from ai_decision import generate_decision_structure
from sarvam_service import sarvam_service
from voice_assistant import voice_assistant
from rca_engine import RCAEngine
from coordination_manager import CoordinationManager
from master_data_service import MasterDataService
from integration_service import integration_service
from similarity_engine import SimilarityEngine
from analytics_service import AnalyticsService
from fastapi import UploadFile, File
from document_processor import document_processor
import aiofiles
import base64
import io
from dispute_service import DisputeBundleService
from evidence_service import EvidenceService
from responsibility_agent import ResponsibilityAgent
from operator_service import OperatorService
from operator_service import OperatorService

# Import Supabase database adapter
from db_adapter import SupabaseAdapter
from db_compat import DBDatabase

# Initialize voice assistant and RCA engine (lazy initialization)
rca_engine = None
coordination_manager = None  # Will be initialized in lifespan

def get_rca_engine():
    """Lazy initialization of RCA engine"""
    global rca_engine
    if rca_engine is None:
        rca_engine = RCAEngine()
    return rca_engine

# Load environment variables
load_dotenv()

# Configuration
# Use SUPABASE_DB_URL for PostgreSQL connection string
SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL") or os.getenv("DATABASE_URL")
# Fallback to MongoDB if Supabase not configured
USE_SUPABASE = bool(SUPABASE_DB_URL)
MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

# Debug: Log environment variable status at startup
print(f"🔧 Environment Check:")
print(f"   SUPABASE_DB_URL set: {bool(SUPABASE_DB_URL)}")
print(f"   USE_SUPABASE: {USE_SUPABASE}")
if SUPABASE_DB_URL:
    # Parse and log safe URL (without password)
    try:
        from urllib.parse import urlparse
        _parsed = urlparse(SUPABASE_DB_URL)
        print(f"   DB Host: {_parsed.hostname}")
        print(f"   DB Port: {_parsed.port or 5432}")
        print(f"   DB User: {_parsed.username}")
    except Exception as e:
        print(f"   Could not parse DB URL: {e}")
else:
    print(f"   ⚠️ SUPABASE_DB_URL not set! Check Vercel environment variables.")

JWT_SECRET = os.getenv("JWT_SECRET", "ward-v0-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

# Global database client
db_adapter = None
db = None

# For ObjectId compatibility (convert to UUID)
class ObjectId:
    """Compatibility class for ObjectId"""
    def __init__(self, value=None):
        if value is None:
            import uuid
            self.value = str(uuid.uuid4())
        else:
            self.value = str(value)
    
    def __str__(self):
        return self.value

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global db_adapter, db, coordination_manager
    
    # Check if already initialized (for Vercel serverless)
    if db_adapter is None and USE_SUPABASE and SUPABASE_DB_URL:
        # Use Supabase PostgreSQL
        try:
            db_adapter = SupabaseAdapter(SUPABASE_DB_URL)
            await db_adapter.connect()
            db = DBDatabase(db_adapter)
            print(f"✅ Connected to Supabase PostgreSQL")
        except Exception as e:
            print(f"❌ Failed to connect to Supabase: {e}")
            print(f"💡 Check your SUPABASE_DB_URL environment variable")
            print(f"💡 Run: python3 backend/test_db_connection.py to diagnose")
            # Don't raise - allow server to start but database operations will fail
            # This allows health check to work even if DB is down
    elif db is None and not USE_SUPABASE:
        # Fallback to MongoDB
        from motor.motor_asyncio import AsyncIOMotorClient
        from bson import ObjectId as MongoObjectId
        global ObjectId
        ObjectId = MongoObjectId
        
        client = AsyncIOMotorClient(MONGO_URL)
        db = client[DB_NAME]
        print(f"Connected to MongoDB: {DB_NAME}")
        
        # Create indexes
        await db.users.create_index("email", unique=True)
        await db.cases.create_index("created_at")
        await db.cases.create_index("status")
        await db.cases.create_index("decision_owner_email")
        await db.audit_entries.create_index("case_id")
        await db.timeline_events.create_index("case_id")
        await db.timeline_events.create_index("timestamp")
    
    # Initialize Coordination Manager
    coordination_manager = CoordinationManager(db)
    
    yield
    
    # Shutdown
    if USE_SUPABASE and db_adapter:
        await db_adapter.close()
        print("Closed Supabase connection")
    elif not USE_SUPABASE:
        client.close()
        print("Closed MongoDB connection")

# Create FastAPI app
# For Vercel serverless, we'll initialize DB on each request, so lifespan is optional

# Check if we're in a serverless environment (Vercel sets VERCEL env var, or AWS_LAMBDA for Lambda)
is_serverless = os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME") or os.getenv("_HANDLER")
if is_serverless:
    # Serverless: don't use lifespan, initialize DB on each request via ensure_db_initialized()
    app = FastAPI(title="Ward v0 API")
else:
    # Local development: use lifespan for proper startup/shutdown
    app = FastAPI(title="Ward v0 API", lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGINS", "*")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add monitoring middleware (if available)
try:
    from middleware import MonitoringMiddleware, ErrorHandlingMiddleware
    app.add_middleware(MonitoringMiddleware)
    app.add_middleware(ErrorHandlingMiddleware)
except ImportError:
    # Middleware not critical, continue without it
    pass

security = HTTPBearer()

# ============================================================================
# MODELS
# ============================================================================

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ShipmentIdentifiers(BaseModel):
    ids: List[str] = []
    routes: List[str] = []
    carriers: List[str] = []

class DisruptionDetails(BaseModel):
    disruption_type: str = Field(min_length=3)  # e.g., "customs hold", "port congestion"
    scope: str = Field(min_length=3)  # e.g., "shipment", "corridor", "container"
    identifier: str = Field(min_length=1)  # shipment ID, container number, etc.
    time_discovered_ist: str = Field(min_length=5)  # IST time
    source: str = Field(min_length=3)  # call, WhatsApp, CHA, transporter, etc.

class FinancialImpact(BaseModel):
    amount: float
    currency: str = "INR"
    category: str = Field(description="demurrage, detention, production_loss, penalty")
    estimated_daily_increase: Optional[float] = 0.0

class StructuredContext(BaseModel):
    """Links to Master Data"""
    carrier_code: Optional[str] = None
    location_code: Optional[str] = None
class Responsibility(BaseModel):
    primary_party: str
    confidence: str
    reasoning: str
    is_override: Optional[bool] = False
    override_reason: Optional[str] = None
    vendor_id: Optional[str] = None
    reason_code: Optional[str] = None

class CreateCase(BaseModel):
    responsibility: Optional[Responsibility] = None
    description: str = Field(min_length=10)
    disruption_details: DisruptionDetails
    shipment_identifiers: ShipmentIdentifiers
    financial_impact: Optional[FinancialImpact] = None
    structured_context: Optional[StructuredContext] = None

class EvidenceFact(BaseModel):
    fact: str
    source: str
    freshness: str
    reliability: str
    relevance: str

class Assumption(BaseModel):
    assumption: str
    why_reasonable: str
    breaks_if: str

class Alternative(BaseModel):
    name: str
    description: str
    worst_case: str
    irreversible_consequences: str
    blast_radius: str
    failure_signals: List[str]

class UpdateSection(BaseModel):
    content: Dict[str, Any]

class FinalizeDecision(BaseModel):
    selected_alternative: str
    override_rationale: Optional[str] = None

class VoiceTranscript(BaseModel):
    audio_base64: str
    audio_format: str = "wav"
    language_code: str = "hi-IN"  # Default to Hindi, but frontend should specify

class VoiceResponse(BaseModel):
    response_text: str
    language_code: Optional[str] = "hi-IN"  # Default to Hindi
    context: str = "clarity"  # clarity, guidance, confirmation

# ============================================================================
# LIFECYCLE MODELS
# ============================================================================

class DisruptionStatus(str, Enum):
    REPORTED = "REPORTED"
    CLARIFIED = "CLARIFIED"
    DECISION_REQUIRED = "DECISION_REQUIRED"
    DECIDED = "DECIDED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"

class SourceType(str, Enum):
    TEXT = "text"
    VOICE = "voice"
    SYSTEM = "system"

class ReliabilityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class AssignOwner(BaseModel):
    owner_email: EmailStr

class TransitionState(BaseModel):
    target_status: str

# API v0 Models
class CreateFacility(BaseModel):
    external_id: Optional[str] = None
    name: str
    type: str  # 'port', 'icd', 'cfs', 'warehouse', 'logistics_park'
    code: Optional[str] = None
    address: Optional[Dict[str, Any]] = None
    location: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

class CreateParty(BaseModel):
    external_id: Optional[str] = None
    name: str
    type: str  # 'shipper', 'forwarder', 'cha', 'transporter', 'consignee', etc.
    code: Optional[str] = None
    contact_info: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

class CreateDisputePacket(BaseModel):
    invoice_id: Optional[str] = None
    template_type: Optional[str] = None  # 'jnpt_demurrage', 'warehouse_waiting_charge', etc.
    selected_events: Optional[List[str]] = []  # List of event IDs
    selected_attachments: Optional[List[str]] = []  # List of attachment IDs
    narrative: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class UpdateDisputePacket(BaseModel):
    status: Optional[str] = None
    narrative: Optional[str] = None
    outcome: Optional[str] = None
    outcome_amount: Optional[float] = None
    submitted_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None

class CreateMovement(BaseModel):
    external_id: Optional[str] = None
    container_id: Optional[str] = None
    truck_id: Optional[str] = None
    bill_of_lading: Optional[str] = None
    route: Optional[Dict[str, Any]] = None  # {origin_facility_id, destination_facility_id, intermediate_facilities}
    lane: Optional[str] = None
    planned_start_date: Optional[datetime] = None
    planned_end_date: Optional[datetime] = None
    parties: Optional[Dict[str, Any]] = None  # {shipper_id, forwarder_id, cha_id, transporter_id, consignee_id}
    metadata: Optional[Dict[str, Any]] = None

class CreateEvent(BaseModel):
    movement_id: str
    facility_id: Optional[str] = None
    event_type: str = "incident"  # 'incident', 'edit', 'note'
    incident_type: Optional[str] = None  # 'stuck_at_port_gate', 'cfs_yard_full', etc.
    timestamp_captured: Optional[datetime] = None  # System timestamp (immutable)
    timestamp_incident: Optional[datetime] = None  # When incident actually occurred
    original_event_id: Optional[str] = None  # For edits
    actor_id: Optional[str] = None
    actor_role: Optional[str] = None
    device_id: Optional[str] = None
    location: Optional[Dict[str, Any]] = None  # {latitude, longitude, accuracy_meters, source}
    content: Optional[Dict[str, Any]] = None  # {text, voice_transcript, voice_recording_url, language}
    reliability: str = "medium"  # 'high', 'medium', 'low'
    metadata: Optional[Dict[str, Any]] = None

class AddTimelineEvent(BaseModel):
    content: str = Field(min_length=1)
    source_type: SourceType
    reliability: ReliabilityLevel
    metadata: Optional[Dict[str, Any]] = None

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def serialize_doc(doc: dict) -> dict:
    """Convert database document to JSON-serializable dict"""
    if doc is None:
        return None
    
    serialized = {}
    for key, value in doc.items():
        if isinstance(value, (ObjectId, UUID)):
            serialized[key] = str(value)
        elif isinstance(value, datetime):
            serialized[key] = value.isoformat()
        elif isinstance(value, dict):
            serialized[key] = serialize_doc(value)
        elif isinstance(value, list):
            serialized[key] = [serialize_doc(item) if isinstance(item, dict) else item for item in value]
        else:
            serialized[key] = value
    return serialized

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_jwt_token(user_id: str, email: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS)
    payload = {
        "user_id": user_id,
        "email": email,
        "exp": exp
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Ensure database is initialized
    await ensure_db_initialized()
    
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("user_id")
        email = payload.get("email")
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Verify user exists - try both _id and id fields
        user = await db.users.find_one({"_id": user_id})
        if not user:
            # Try with id field as fallback
            user = await db.users.find_one({"id": user_id})
        
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        # Ensure we return the correct user_id format
        actual_user_id = str(user.get("_id") or user.get("id") or user_id)
        
        return {
            "user_id": actual_user_id,
            "email": email or user.get("email")
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def ensure_db_initialized():
    """Ensure database is initialized (for serverless functions)"""
    global db_adapter, db, coordination_manager
    
    if db is None:
        if USE_SUPABASE and SUPABASE_DB_URL:
            try:
                db_adapter = SupabaseAdapter(SUPABASE_DB_URL)
                await db_adapter.connect()
                db = DBDatabase(db_adapter)
                coordination_manager = CoordinationManager(db)
                print("Database initialized in serverless function")
            except Exception as e:
                print(f"Failed to initialize Supabase: {e}")
                import traceback
                traceback.print_exc()
                raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
        elif not USE_SUPABASE and MONGO_URL:
            try:
                from motor.motor_asyncio import AsyncIOMotorClient
                from bson import ObjectId as MongoObjectId
                global ObjectId
                ObjectId = MongoObjectId
                
                client = AsyncIOMotorClient(MONGO_URL)
                db = client[DB_NAME]
                coordination_manager = CoordinationManager(db)
                print("Database initialized in serverless function (MongoDB)")
            except Exception as e:
                print(f"Failed to initialize MongoDB: {e}")
                import traceback
                traceback.print_exc()
                raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
        else:
            error_msg = "Database not configured. Set SUPABASE_DB_URL or MONGO_URL environment variable."
            print(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
    
    return db

async def log_audit(case_id: str, actor: str, action: str, payload: dict):
    """Log audit entry"""
    await db.audit_entries.insert_one({
        "case_id": case_id,
        "actor": actor,
        "action": action,
        "payload": payload,
        "timestamp": datetime.now(timezone.utc)
    })

# ============================================================================
# AUTH ROUTES
# ============================================================================

@app.post("/api/auth/register", response_model=Token)
async def register(user_data: UserRegister):
    try:
        # Ensure database is initialized
        print(f"Register: Initializing database...")
        await ensure_db_initialized()
        print(f"Register: Database initialized, checking for existing user...")
        
        # Check if user exists
        existing = await db.users.find_one({"email": user_data.email})
        print(f"Register: Existing user check result: {existing is not None}")
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create user
        print(f"Register: Creating new user...")
        hashed_pw = hash_password(user_data.password)
        result = await db.users.insert_one({
            "email": user_data.email,
            "password_hash": hashed_pw,
            "created_at": datetime.now(timezone.utc)
        })
        print(f"Register: User created, inserted_id: {result.inserted_id}, type: {type(result.inserted_id)}")
        
        # Ensure inserted_id is a string
        user_id = str(result.inserted_id) if result.inserted_id else None
        if not user_id:
            raise HTTPException(status_code=500, detail="Failed to create user: no ID returned")
        
        token = create_jwt_token(user_id, user_data.email)
        print(f"Register: Token created for user_id: {user_id}, returning response")
        
        return {"access_token": token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Registration error: {e}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@app.post("/api/auth/login", response_model=Token)
async def login(credentials: UserLogin):
    try:
        # Ensure database is initialized
        print(f"Login: Initializing database...")
        await ensure_db_initialized()
        print(f"Login: Database initialized, looking up user...")
        
        user = await db.users.find_one({"email": credentials.email})
        print(f"Login: User lookup result: {user is not None}")
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Verify user has required fields
        if "_id" not in user and "id" not in user:
            print(f"Login: ERROR - User missing ID field. User keys: {list(user.keys())}")
            raise HTTPException(status_code=500, detail="User data corrupted")
        
        # Get user_id from _id or id
        user_id = str(user.get("_id") or user.get("id"))
        if not user_id:
            print(f"Login: ERROR - User ID is None. User: {user}")
            raise HTTPException(status_code=500, detail="User ID not found")
        
        if "password_hash" not in user:
            print(f"Login: ERROR - User missing password_hash. User keys: {list(user.keys())}")
            raise HTTPException(status_code=500, detail="User data corrupted")
        
        print(f"Login: Verifying password for user_id: {user_id}...")
        if not verify_password(credentials.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        token = create_jwt_token(user_id, credentials.email)
        print(f"Login: Token created for user_id: {user_id}, returning response")
        
        return {"access_token": token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Login error: {e}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@app.get("/api/auth/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    user = await db.users.find_one({"_id": current_user["user_id"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Ensure _id is set
    user_id = str(user.get("_id") or user.get("id"))
    return serialize_doc({
        "_id": user_id,
        "email": user.get("email"),
        "created_at": user.get("created_at")
    })

# ============================================================================
# CASE ROUTES
# ============================================================================

@app.post("/api/cases")
async def create_case(case_data: CreateCase, current_user: dict = Depends(get_current_user)):
    now = datetime.now(timezone.utc)
    case = {
        "operator_id": current_user["user_id"],
        "operator_email": current_user["email"],
        "description": case_data.description,
        "disruption_details": case_data.disruption_details.dict(),
        "shipment_identifiers": case_data.shipment_identifiers.dict(),
        "status": DisruptionStatus.REPORTED.value,
        "decision_owner_id": None,
        "decision_owner_email": None,
        "created_at": now,
        "updated_at": now
    }
    
    # Add optional financial and structured context if provided
    if case_data.financial_impact:
        case["financial_impact"] = case_data.financial_impact.dict()
    if case_data.structured_context:
        case["structured_context"] = case_data.structured_context.dict()
    
    result = await db.cases.insert_one(case)
    case_id = str(result.inserted_id)
    case["_id"] = result.inserted_id
    
    await log_audit(case_id, current_user["email"], "CASE_CREATED", {"description": case_data.description})
    
    # Create initial timeline event
    await db.timeline_events.insert_one({
        "case_id": case_id,
        "actor": current_user["email"],
        "action": "DISRUPTION_REPORTED",
        "content": case_data.description,
        "source_type": SourceType.TEXT.value,
        "reliability": ReliabilityLevel.HIGH.value,
        "timestamp": now,
        "metadata": case_data.disruption_details.dict()
    })
    
    return serialize_doc(case)

@app.get("/api/cases")
async def list_cases(
    current_user: dict = Depends(get_current_user),
    status: Optional[str] = None,
    owner_email: Optional[str] = None,
    source_type: Optional[str] = None
):
    query = {"operator_id": current_user["user_id"]}
    
    if status:
        query["status"] = status
    if owner_email:
        query["decision_owner_email"] = owner_email
    
    cursor = await db.cases.find(query, sort=[("updated_at", -1)], limit=100)
    cases = await cursor.to_list(length=100)
    
    # Get last timeline event for each case
    for case in cases:
        # Ensure _id exists
        case_id = str(case.get("_id") or case.get("id"))
        if not case_id:
            continue  # Skip cases without ID
        
        try:
            last_event = await db.timeline_events.find_one(
                {"case_id": case_id},
                sort=[("timestamp", -1)]
            )
            case["last_event"] = serialize_doc(last_event) if last_event else None
        except Exception as e:
            print(f"Error fetching timeline event for case {case_id}: {e}")
            case["last_event"] = None
    
    return [serialize_doc(case) for case in cases]

@app.get("/api/cases/{case_id}")
async def get_case(case_id: str, current_user: dict = Depends(get_current_user)):
    try:
        case = await db.cases.find_one({"_id": case_id, "operator_id": current_user["user_id"]})
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        
        # Get timeline events
        timeline_cursor = await db.timeline_events.find({"case_id": case_id}, sort=[("timestamp", -1)], limit=500)
        timeline_events = await timeline_cursor.to_list(length=500)
        
        # Get draft if exists (for legacy decision flow)
        draft = await db.drafts.find_one({"case_id": case_id})
        
        # Get approvals (for legacy decision flow)
        approvals_cursor = await db.approvals.find({"case_id": case_id}, limit=100)
        approvals = await approvals_cursor.to_list(length=100)
        
        # Get decision if exists (for legacy decision flow)
        decision = await db.decisions.find_one({"case_id": case_id})
        
        return serialize_doc({
            "case": case,
            "timeline": timeline_events,
            "draft": draft,
            "approvals": approvals,
            "decision": decision
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============================================================================
# AI DRAFT ROUTES
# ============================================================================

@app.post("/api/cases/{case_id}/ai_draft")
async def generate_ai_draft(case_id: str, current_user: dict = Depends(get_current_user)):
    try:
        case = await db.cases.find_one({"_id": case_id, "operator_id": current_user["user_id"]})
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        
        # Check if draft already exists
        existing_draft = await db.drafts.find_one({"case_id": case_id})
        if existing_draft:
            return serialize_doc(existing_draft)
        
        # Generate decision structure using AI
        decision_structure = await generate_decision_structure(
            description=case["description"],
            disruption_details=case["disruption_details"],
            shipment_data=case["shipment_identifiers"]
        )
        
        # Store draft
        draft = {
            "case_id": case_id,
            "decision_framing": decision_structure.get("decision_framing"),
            "known_inputs": decision_structure.get("known_inputs"),
            "declared_assumptions": decision_structure.get("declared_assumptions"),
            "alternatives": decision_structure.get("alternatives"),
            "risk_and_downside": decision_structure.get("alternatives", []),  # Same as alternatives for now
            "recommendation": decision_structure.get("recommendation"),
            "ai_model": "gemini-2.5-flash",
            "created_at": datetime.now(timezone.utc)
        }
        
        result = await db.drafts.insert_one(draft)
        draft["_id"] = result.inserted_id
        
        await log_audit(case_id, current_user["email"], "AI_DRAFT_GENERATED", {"model": "gemini-2.5-flash"})
        await db.cases.update_one({"_id": case_id}, {"$set": {"status": "reviewing", "updated_at": datetime.utcnow()}})
        
        return serialize_doc(draft)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")

# ============================================================================
# SECTION EDIT & APPROVAL ROUTES
# ============================================================================

@app.patch("/api/cases/{case_id}/sections/{section_key}")
async def update_section(case_id: str, section_key: str, update_data: UpdateSection, current_user: dict = Depends(get_current_user)):
    try:
        draft = await db.drafts.find_one({"case_id": case_id})
        if not draft:
            raise HTTPException(status_code=404, detail="Draft not found")
        
        # Update the section
        await db.drafts.update_one(
            {"case_id": case_id},
            {"$set": {section_key: update_data.content, "updated_at": datetime.utcnow()}}
        )
        
        await log_audit(case_id, current_user["email"], "SECTION_EDITED", {"section": section_key})
        
        return {"message": "Section updated", "section_key": section_key}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/cases/{case_id}/sections/{section_key}/approve")
async def approve_section(case_id: str, section_key: str, current_user: dict = Depends(get_current_user)):
    try:
        draft = await db.drafts.find_one({"case_id": case_id})
        if not draft:
            raise HTTPException(status_code=404, detail="Draft not found")
        
        # Get section content
        section_content = draft.get(section_key)
        if not section_content:
            raise HTTPException(status_code=400, detail="Section not found in draft")
        
        # Check if already approved
        existing = await db.approvals.find_one({"case_id": case_id, "section_key": section_key})
        if existing:
            return serialize_doc(existing)
        
        # Create approval
        approval = {
            "case_id": case_id,
            "section_key": section_key,
            "approved_by": current_user["email"],
            "approved_at": datetime.utcnow(),
            "content_snapshot": section_content
        }
        
        result = await db.approvals.insert_one(approval)
        approval["_id"] = result.inserted_id
        
        await log_audit(case_id, current_user["email"], "SECTION_APPROVED", {"section": section_key})
        
        return serialize_doc(approval)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============================================================================
# FINALIZE DECISION ROUTE
# ============================================================================

@app.post("/api/cases/{case_id}/finalize")
async def finalize_decision(case_id: str, finalize_data: FinalizeDecision, current_user: dict = Depends(get_current_user)):
    try:
        draft = await db.drafts.find_one({"case_id": case_id})
        if not draft:
            raise HTTPException(status_code=404, detail="Draft not found")
        
        # Check if already finalized
        existing = await db.decisions.find_one({"case_id": case_id})
        if existing:
            raise HTTPException(status_code=400, detail="Decision already finalized")
        
        # Determine if this is an override
        recommended_choice = draft.get("recommendation", {}).get("choice", "")
        is_override = finalize_data.selected_alternative.lower() != recommended_choice.lower()
        
        # Create decision
        decision = {
            "case_id": case_id,
            "final_choice": finalize_data.selected_alternative,
            "is_override": is_override,
            "override_rationale": finalize_data.override_rationale if is_override else None,
            "recommended_choice": recommended_choice,
            "decided_by": current_user["email"],
            "decided_at": datetime.utcnow()
        }
        
        result = await db.decisions.insert_one(decision)
        decision["_id"] = result.inserted_id
        
        await log_audit(case_id, current_user["email"], "DECISION_FINALIZED", {
            "choice": finalize_data.selected_alternative,
            "override": is_override
        })
        await db.cases.update_one({"_id": case_id}, {"$set": {"status": "finalized", "updated_at": datetime.utcnow()}})
        
        return serialize_doc(decision)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============================================================================
# AUDIT TRAIL ROUTES
# ============================================================================

@app.get("/api/audit")
async def list_audit_trail(current_user: dict = Depends(get_current_user)):
    # Get all cases for this user
    cases_cursor = await db.cases.find({"operator_id": current_user["user_id"]})
    cases = await cases_cursor.to_list(length=None)
    case_ids = [str(case.get("_id") or case.get("id")) for case in cases if case.get("_id") or case.get("id")]
    
    # Get audit entries for these cases
    cursor = await db.audit_entries.find({"case_id": {"$in": case_ids}}, sort=[("timestamp", -1)], limit=100)
    entries = await cursor.to_list(length=100)
    return [serialize_doc(entry) for entry in entries]

@app.get("/api/cases/{case_id}/audit")
async def get_case_audit(case_id: str, current_user: dict = Depends(get_current_user)):
    # Verify case belongs to user
    case = await db.cases.find_one({"_id": case_id, "operator_id": current_user["user_id"]})
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    cursor = await db.audit_entries.find({"case_id": case_id}, sort=[("timestamp", 1)])
    entries = await cursor.to_list(length=None)
    return [serialize_doc(entry) for entry in entries]

# ============================================================================
# EVIDENCE SCORING ENDPOINTS
# ============================================================================

@app.post("/api/cases/{case_id}/evidence/recalc")
async def recalculate_evidence_score(case_id: str, current_user: dict = Depends(get_current_user)):
    """
    Manually recalculate evidence completeness score for a case.
    """
    try:
        # Verify case belongs to user
        case = await db.cases.find_one({"_id": case_id, "operator_id": current_user["user_id"]})
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        
        # Calculate and update score
        try:
            evidence_service = EvidenceService(db)
            evidence_data = await evidence_service.calculate_and_update_score(case_id)
            
            if not evidence_data:
                # Return default if calculation fails
                evidence_data = {"score": 0, "breakdown": [], "missing_actions": []}
            
            return evidence_data
        except Exception as calc_error:
            print(f"Error calculating evidence score: {calc_error}")
            import traceback
            traceback.print_exc()
            # Return default on calculation error instead of failing
            return {"score": 0, "breakdown": [], "missing_actions": []}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in recalculate_evidence_score: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to recalculate evidence score: {str(e)}")

@app.get("/api/cases/{case_id}/evidence")
async def get_evidence_score(case_id: str, current_user: dict = Depends(get_current_user)):
    """
    Get current evidence completeness score for a case.
    """
    try:
        # Verify case belongs to user
        case = await db.cases.find_one({"_id": case_id, "operator_id": current_user["user_id"]})
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        
        # Return existing score or calculate if missing
        evidence_score = case.get("evidence_score")
        if not evidence_score:
            # Calculate if missing
            try:
                evidence_service = EvidenceService(db)
                evidence_score = await evidence_service.calculate_and_update_score(case_id)
                if not evidence_score:
                    # If calculation returns None, return default
                    evidence_score = {"score": 0, "breakdown": [], "missing_actions": []}
            except Exception as calc_error:
                print(f"Error calculating evidence score: {calc_error}")
                import traceback
                traceback.print_exc()
                # Return default on calculation error
                evidence_score = {"score": 0, "breakdown": [], "missing_actions": []}
        
        return evidence_score or {"score": 0, "breakdown": [], "missing_actions": []}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_evidence_score: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to get evidence score: {str(e)}")

# ============================================================================
# RESPONSIBILITY ATTRIBUTION ENDPOINTS
# ============================================================================

@app.post("/api/cases/{case_id}/responsibility/analyze")
async def analyze_responsibility(case_id: str, current_user: dict = Depends(get_current_user)):
    """
    Analyze and attribute responsibility for a disruption.
    """
    try:
        # Verify case belongs to user
        case = await db.cases.find_one({"_id": case_id, "operator_id": current_user["user_id"]})
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        
        # Analyze responsibility
        responsibility_agent = ResponsibilityAgent(db)
        responsibility_data = await responsibility_agent.analyze_responsibility(case_id)
        
        if not responsibility_data:
            raise HTTPException(status_code=500, detail="Failed to analyze responsibility")
        
        # Update case with responsibility data
        await db.cases.update_one(
            {"_id": case_id},
            {"$set": {"responsibility": responsibility_data, "updated_at": datetime.now(timezone.utc)}}
        )
        
        await log_audit(case_id, current_user["email"], "RESPONSIBILITY_ANALYZED", {
            "responsible_party": responsibility_data.get("responsible_party")
        })
        
        return responsibility_data
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze responsibility: {str(e)}")

@app.get("/api/cases/{case_id}/responsibility")
async def get_responsibility(case_id: str, current_user: dict = Depends(get_current_user)):
    """
    Get current responsibility attribution for a case.
    """
    try:
        # Verify case belongs to user
        case = await db.cases.find_one({"_id": case_id, "operator_id": current_user["user_id"]})
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        
        # Return existing responsibility or analyze if missing
        responsibility = case.get("responsibility")
        if not responsibility:
            # Analyze if missing
            responsibility_agent = ResponsibilityAgent(db)
            responsibility = await responsibility_agent.analyze_responsibility(case_id)
            if responsibility:
                await db.cases.update_one(
                    {"_id": case_id},
                    {"$set": {"responsibility": responsibility, "updated_at": datetime.now(timezone.utc)}}
                )
        
        return responsibility or {"responsible_party": "Unknown", "confidence": "low", "reasoning": "Insufficient evidence"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get responsibility: {str(e)}")

# ============================================================================
# HISTORICAL DISRUPTIONS (READ-ONLY)
# ============================================================================

@app.get("/api/historical")
async def list_historical(current_user: dict = Depends(get_current_user)):
    cursor = await db.historical.find(sort=[("created_at", -1)], limit=20)
    entries = await cursor.to_list(length=20)
    return [serialize_doc(entry) for entry in entries]

@app.get("/api/historical/{historical_id}")
async def get_historical(historical_id: str, current_user: dict = Depends(get_current_user)):
    try:
        entry = await db.historical.find_one({"_id": historical_id})
        if not entry:
            raise HTTPException(status_code=404, detail="Historical entry not found")
        return serialize_doc(entry)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============================================================================
# LIFECYCLE MANAGEMENT ENDPOINTS
# ============================================================================

@app.post("/api/cases/{case_id}/assign-owner")
async def assign_owner(case_id: str, assignment: AssignOwner, current_user: dict = Depends(get_current_user)):
    """
    Assign or reassign decision owner for a disruption.
    Anyone can assign ownership - this supports the fluid Indian ops reality.
    """
    try:
        case = await db.cases.find_one({"_id": case_id, "operator_id": current_user["user_id"]})
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        
        # Find the user being assigned
        assigned_user = await db.users.find_one({"email": assignment.owner_email})
        if not assigned_user:
            raise HTTPException(status_code=404, detail="Assigned user not found")
        
        assigned_user_id = str(assigned_user.get("_id") or assigned_user.get("id"))
        previous_owner = case.get("decision_owner_email")
        now = datetime.now(timezone.utc)
        
        # Update case
        await db.cases.update_one(
            {"_id": case_id},
            {
                "$set": {
                    "decision_owner_id": assigned_user_id,
                    "decision_owner_email": assignment.owner_email,
                    "updated_at": now
                }
            }
        )
        
        # Create audit log
        await log_audit(case_id, current_user["email"], "OWNER_ASSIGNED", {
            "previous_owner": previous_owner,
            "new_owner": assignment.owner_email,
            "assigned_by": current_user["email"]
        })
        
        # Create timeline event
        action_text = f"Ownership assigned to {assignment.owner_email}"
        if previous_owner:
            action_text = f"Ownership reassigned from {previous_owner} to {assignment.owner_email}"
        
        await db.timeline_events.insert_one({
            "case_id": case_id,
            "actor": current_user["email"],
            "action": "OWNER_ASSIGNED",
            "content": action_text,
            "source_type": SourceType.SYSTEM.value,
            "reliability": ReliabilityLevel.HIGH.value,
            "timestamp": now,
            "metadata": {
                "previous_owner": previous_owner,
                "new_owner": assignment.owner_email,
                "assigned_by": current_user["email"]
            }
        })
        
        # Get updated case
        updated_case = await db.cases.find_one({"_id": case_id})
        return serialize_doc(updated_case)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to assign owner: {str(e)}")

@app.post("/api/cases/{case_id}/transition")
async def transition_state(case_id: str, transition: TransitionState, current_user: dict = Depends(get_current_user)):
    """
    Transition disruption to next state.
    ONLY the decision owner can advance states.
    """
    try:
        case = await db.cases.find_one({"_id": case_id, "operator_id": current_user["user_id"]})
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        
        # Check if user is decision owner
        if case.get("decision_owner_email") != current_user["email"]:
            raise HTTPException(
                status_code=403,
                detail="Only the decision owner can advance the state"
            )
        
        current_state = case.get("status", DisruptionStatus.REPORTED.value)
        next_state = transition.next_state.value
        
        # Validate state transition
        valid_transitions = {
            DisruptionStatus.REPORTED.value: [DisruptionStatus.CLARIFIED.value],
            DisruptionStatus.CLARIFIED.value: [DisruptionStatus.DECISION_REQUIRED.value],
            DisruptionStatus.DECISION_REQUIRED.value: [DisruptionStatus.DECIDED.value],
            DisruptionStatus.DECIDED.value: [DisruptionStatus.IN_PROGRESS.value],
            DisruptionStatus.IN_PROGRESS.value: [DisruptionStatus.RESOLVED.value],
            DisruptionStatus.RESOLVED.value: []
        }
        
        if next_state not in valid_transitions.get(current_state, []):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid transition from {current_state} to {next_state}"
            )
        
        now = datetime.now(timezone.utc)
        
        # Update case status
        await db.cases.update_one(
            {"_id": case_id},
            {
                "$set": {
                    "status": next_state,
                    "updated_at": now
                }
            }
        )
        
        # Create audit log
        await log_audit(case_id, current_user["email"], "STATE_TRANSITION", {
            "from_state": current_state,
            "to_state": next_state,
            "reason": transition.reason
        })
        
        # Create timeline event
        content = f"State advanced from {current_state} to {next_state}"
        if transition.reason:
            content += f": {transition.reason}"
        
        await db.timeline_events.insert_one({
            "case_id": case_id,
            "actor": current_user["email"],
            "action": "STATE_TRANSITION",
            "content": content,
            "source_type": SourceType.SYSTEM.value,
            "reliability": ReliabilityLevel.HIGH.value,
            "timestamp": now,
            "metadata": {
                "from_state": current_state,
                "to_state": next_state,
                "reason": transition.reason
            }
        })
        
        # Get updated case
        updated_case = await db.cases.find_one({"_id": case_id})
        return serialize_doc(updated_case)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to transition state: {str(e)}")

@app.post("/api/cases/{case_id}/timeline")
async def add_timeline_event(case_id: str, event_data: AddTimelineEvent, current_user: dict = Depends(get_current_user)):
    """
    Add a timeline event to a disruption.
    Anyone can add context - supports fluid Indian ops where information comes from many sources.
    """
    try:
        case = await db.cases.find_one({"_id": case_id, "operator_id": current_user["user_id"]})
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        
        now = datetime.now(timezone.utc)
        
        # Create timeline event
        event = {
            "case_id": case_id,
            "actor": current_user["email"],
            "action": "CONTEXT_ADDED",
            "content": event_data.content,
            "source_type": event_data.source_type.value,
            "reliability": event_data.reliability.value,
            "timestamp": now,
            "metadata": event_data.metadata or {}
        }
        
        result = await db.timeline_events.insert_one(event)
        event["_id"] = result.inserted_id
        
        # Update case timestamp
        await db.cases.update_one(
            {"_id": case_id},
            {"$set": {"updated_at": now}}
        )
        
        # Auto-calculate evidence score when new event is added
        try:
            evidence_service = EvidenceService(db)
            await evidence_service.calculate_and_update_score(case_id)
        except Exception as e:
            print(f"Warning: Failed to calculate evidence score: {e}")
        
        # Create audit log
        await log_audit(case_id, current_user["email"], "TIMELINE_EVENT_ADDED", {
            "source_type": event_data.source_type.value,
            "reliability": event_data.reliability.value
        })
        
        return serialize_doc(event)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add timeline event: {str(e)}")

@app.get("/api/cases/{case_id}/timeline")
async def get_timeline(case_id: str, current_user: dict = Depends(get_current_user)):
    """
    Get all timeline events for a disruption.
    """
    try:
        case = await db.cases.find_one({"_id": case_id, "operator_id": current_user["user_id"]})
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        
        cursor = await db.timeline_events.find({"case_id": case_id}, sort=[("timestamp", -1)], limit=1000)
        events = await cursor.to_list(length=1000)
        
        return [serialize_doc(event) for event in events]
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get timeline: {str(e)}")

# ============================================================================
# ROOT CAUSE ANALYSIS ENDPOINTS
# ============================================================================

@app.post("/api/cases/{case_id}/rca")
async def perform_rca(case_id: str, current_user: dict = Depends(get_current_user)):
    """
    Perform Root Cause Analysis on a disruption
    Analyzes timeline and suggests root cause, actions, preventive measures
    """
    try:
        case = await db.cases.find_one({"_id": case_id, "operator_id": current_user["user_id"]})
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        
        # Get timeline events
        timeline_cursor = await db.timeline_events.find({"case_id": case_id}, sort=[("timestamp", 1)], limit=500)
        timeline_events = await timeline_cursor.to_list(length=500)
        
        # Perform RCA
        rca_result = await get_rca_engine().analyze_disruption(
            serialize_doc(case),
            [serialize_doc(event) for event in timeline_events]
        )
        
        # Store RCA in case
        now = datetime.now(timezone.utc)
        await db.cases.update_one(
            {"_id": case_id},
            {
                "$set": {
                    "rca": rca_result,
                    "rca_performed_at": now,
                    "rca_performed_by": current_user["email"],
                    "updated_at": now
                }
            }
        )
        
        # Create timeline event for RCA
        await db.timeline_events.insert_one({
            "case_id": case_id,
            "actor": "Ward AI",
            "action": "RCA_PERFORMED",
            "content": f"Root Cause Analysis completed: {rca_result.get('root_cause', 'Analysis in progress')}",
            "source_type": SourceType.SYSTEM.value,
            "reliability": ReliabilityLevel.HIGH.value,
            "timestamp": now,
            "metadata": rca_result
        })
        
        # Log audit
        await log_audit(case_id, current_user["email"], "RCA_PERFORMED", {
            "root_cause": rca_result.get("root_cause"),
            "confidence": rca_result.get("confidence")
        })
        
        return rca_result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RCA failed: {str(e)}")

@app.get("/api/cases/{case_id}/similar-resolutions")
async def get_similar_resolutions(case_id: str, current_user: dict = Depends(get_current_user)):
    """
    Get similar disruptions and how they were resolved
    Helps with pattern recognition and learning
    """
    try:
        case = await db.cases.find_one({"_id": case_id, "operator_id": current_user["user_id"]})
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        
        disruption_type = case.get("disruption_details", {}).get("disruption_type", "")
        location = case.get("disruption_details", {}).get("identifier", "")
        
        similar = await get_rca_engine().suggest_similar_resolutions(disruption_type, location)
        
        return {
            "case_id": case_id,
            "disruption_type": disruption_type,
            "similar_resolutions": similar,
            "count": len(similar)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get similar resolutions: {str(e)}")

# ============================================================================
# VOICE-FIRST ENDPOINTS (Sarvam AI Integration)
# ============================================================================

@app.post("/api/voice/transcribe")
async def transcribe_voice(voice_data: VoiceTranscript, current_user: dict = Depends(get_current_user)):
    """
    Transcribe voice to text using Sarvam AI
    Supports 10+ Indian languages (hi-IN, en-IN, ta-IN, te-IN, kn-IN, ml-IN, mr-IN, gu-IN, pa-IN, bn-IN, od-IN)
    IMPORTANT: language_code is REQUIRED for Sarvam AI saarika:v1 model
    """
    try:
        # Decode base64 audio
        audio_bytes = base64.b64decode(voice_data.audio_base64)
        
        # Save temporarily
        temp_file_path = f"/tmp/voice_{current_user['user_id']}_{datetime.utcnow().timestamp()}.{voice_data.audio_format}"
        async with aiofiles.open(temp_file_path, 'wb') as f:
            await f.write(audio_bytes)
        
        # Transcribe using Sarvam AI with explicit language code
        result = await sarvam_service.speech_to_text(
            temp_file_path, 
            language_code=voice_data.language_code
        )
        
        # Clean up temp file
        os.remove(temp_file_path)
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error", "Transcription failed"))
        
        return {
            "transcript": result["transcript"],
            "language_code": result.get("language_code"),
            "duration": result.get("duration")
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice transcription failed: {str(e)}")

@app.post("/api/voice/driver-response")
async def generate_driver_response(request: dict, current_user: dict = Depends(get_current_user)):
    """
    Generate safe response for DRIVER role
    Only acknowledgment, clarification, or safe coordination - NO DECISIONS
    """
    try:
        driver_input = request.get("driver_input", "")
        conversation_history = request.get("conversation_history", [])
        
        if not driver_input:
            raise HTTPException(status_code=400, detail="Driver input is required")
        
        response = await voice_assistant.generate_driver_response(driver_input, conversation_history)
        
        return {
            "response": response,
            "role": "driver",
            "safe": True  # Flag indicating this is a safe, non-decision response
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate driver response: {str(e)}")

@app.post("/api/voice/helper-questions")
async def generate_helper_questions(request: dict, current_user: dict = Depends(get_current_user)):
    """
    Generate context-harvesting questions for HELPER role (CHA, senior ops)
    NOT asking for advice, asking for domain knowledge
    """
    try:
        context = request.get("context", "")
        if not context:
            raise HTTPException(status_code=400, detail="Context is required")
        
        questions = await voice_assistant.generate_helper_questions(context)
        
        return {
            "questions": questions,
            "role": "helper",
            "count": len(questions)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate helper questions: {str(e)}")

@app.post("/api/voice/clarity-questions")
async def generate_clarity_questions(transcript: dict, current_user: dict = Depends(get_current_user)):
    """
    Generate clarity-enforcing questions for MANAGER role
    Ward clarifies - it does not decide
    """
    try:
        initial_transcript = transcript.get("transcript", "")
        if not initial_transcript:
            raise HTTPException(status_code=400, detail="Transcript is required")
        
        questions = await voice_assistant.generate_clarity_questions(initial_transcript)
        
        return {
            "questions": questions,
            "role": "manager",
            "count": len(questions)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate questions: {str(e)}")

@app.post("/api/voice/extract-disruption")
async def extract_disruption_from_conversation(conversation: dict, current_user: dict = Depends(get_current_user)):
    """
    Extract structured disruption details from voice conversation
    Operator must approve before decision creation
    """
    try:
        conversation_transcript = conversation.get("conversation_transcript", "")
        if not conversation_transcript:
            raise HTTPException(status_code=400, detail="Conversation transcript is required")
        
        disruption = await voice_assistant.extract_disruption_details(conversation_transcript)
        
        if "error" in disruption:
            raise HTTPException(status_code=500, detail=disruption["error"])
        
        return disruption
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract disruption: {str(e)}")

@app.post("/api/voice/text-to-speech")
async def synthesize_speech(voice_response: VoiceResponse, current_user: dict = Depends(get_current_user)):
    """
    Convert text to speech using Sarvam AI Bulbul v2
    Returns base64 encoded audio for playback in the user's chosen language
    """
    try:
        text = voice_response.response_text
        if not text:
            raise HTTPException(status_code=400, detail="Text is required")
        
        # Use the language specified by the user (defaults to Hindi)
        language_code = voice_response.language_code or "hi-IN"
        
        # Use Anushka voice (clear, professional)
        audio_bytes = await sarvam_service.text_to_speech(
            text=text,
            language_code=language_code,
            speaker="anushka"
        )
        
        if not audio_bytes:
            raise HTTPException(status_code=500, detail="Speech synthesis failed")
        
        # Return base64 encoded audio
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        return {
            "audio_base64": audio_base64,
            "format": "wav",
            "text": text
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Speech synthesis failed: {str(e)}")

@app.post("/api/voice/decision-guidance")
async def generate_voice_guidance(disruption: dict, current_user: dict = Depends(get_current_user)):
    """
    Generate voice guidance for decision protocol steps
    Ward guides through the 6-step protocol
    """
    try:
        disruption_summary = disruption.get("summary", "")
        if not disruption_summary:
            raise HTTPException(status_code=400, detail="Disruption summary is required")
        
        guidance = await voice_assistant.generate_decision_guidance(disruption_summary)
        
        return guidance
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate guidance: {str(e)}")

@app.post("/api/cases/voice-create")
async def create_case_from_voice(voice_case: dict, current_user: dict = Depends(get_current_user)):
    """
    Create case from voice conversation
    Includes full voice transcript in audit trail
    """
    try:
        # Extract data
        disruption_details = voice_case.get("disruption_details")
        description = voice_case.get("description")
        shipment_identifiers = voice_case.get("shipment_identifiers", {})
        voice_transcript = voice_case.get("voice_transcript", "")
        
        if not disruption_details or not description:
            raise HTTPException(status_code=400, detail="Disruption details and description required")
        
        # Create case
        case = {
            "operator_id": current_user["user_id"],
            "operator_email": current_user["email"],
            "description": description,
            "disruption_details": disruption_details,
            "shipment_identifiers": shipment_identifiers,
            "voice_transcript": voice_transcript,  # Store full transcript
            "created_via": "voice",
            "status": "draft",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        
        result = await db.cases.insert_one(case)
        case_id = str(result.inserted_id)
        
        await log_audit(case_id, current_user["email"], "VOICE_CASE_CREATED", {
            "description": description[:100],
            "voice_enabled": True,
            "transcript_length": len(voice_transcript)
        })
        
        case["_id"] = result.inserted_id
        return serialize_doc(case)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create case from voice: {str(e)}")

# ============================================================================
# ACTIVE COORDINATION ENDPOINTS
# ============================================================================

class SimulateResponseRequest(BaseModel):
    actor: str
    content: str

class ExecutePlanRequest(BaseModel):
    action_plan: List[Dict[str, Any]]

@app.post("/api/cases/{case_id}/coordination/start")
async def start_coordination(case_id: str, current_user: dict = Depends(get_current_user)):
    """
    Start the active coordination process: Identify stakeholders and send outreach.
    """
    try:
        case = await db.cases.find_one({"_id": case_id})
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        
        disruption_type = case.get("disruption_details", {}).get("disruption_type", "unknown")
        location = case.get("disruption_details", {}).get("identifier", "unknown")
        summary = case.get("description", "")
        
        result = await coordination_manager.start_coordination(
            case_id=case_id,
            disruption_summary=summary,
            disruption_type=disruption_type,
            location=location
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start coordination: {str(e)}")

@app.post("/api/cases/{case_id}/coordination/simulate-response")
async def simulate_response(case_id: str, request: SimulateResponseRequest, current_user: dict = Depends(get_current_user)):
    """
    DEMO TOOL: Simulate a response from a stakeholder.
    """
    try:
        event = await coordination_manager.simulate_response(
            case_id=case_id,
            actor=request.actor,
            content=request.content
        )
        return serialize_doc(event)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to simulate response: {str(e)}")

@app.post("/api/cases/{case_id}/coordination/rca")
async def perform_enhanced_rca(case_id: str, current_user: dict = Depends(get_current_user)):
    """
    Perform RCA using collected stakeholder data.
    """
    try:
        result = await coordination_manager.perform_enhanced_rca(case_id)
        
        # Update case with enhanced RCA
        now = datetime.now(timezone.utc)
        await db.cases.update_one(
            {"_id": case_id},
            {
                "$set": {
                    "enhanced_rca": result,
                    "rca_performed_at": now,
                    "updated_at": now
                }
            }
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to perform enhanced RCA: {str(e)}")

@app.post("/api/cases/{case_id}/coordination/execute")
async def execute_action_plan(case_id: str, request: ExecutePlanRequest, current_user: dict = Depends(get_current_user)):
    """
    Execute the approved action plan.
    """
    try:
        result = await coordination_manager.execute_plan(case_id, request.action_plan)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to execute plan: {str(e)}")

# ============================================================================
# MASTER DATA ENDPOINTS
# ============================================================================

@app.post("/api/admin/seed-master-data")
async def seed_master_data(current_user: dict = Depends(get_current_user)):
    """
    Seed the database with standardized logistics master data.
    """
    service = MasterDataService(db)
    await service.seed_master_data()
    return {"status": "Master data seeded"}

@app.get("/api/master/lookup")
async def lookup_entity(query: str, current_user: dict = Depends(get_current_user)):
    """
    Find structured entities (Port, Carrier) from a text query.
    """
    service = MasterDataService(db)
    return await service.lookup_entity(query)

# ============================================================================
# INTEGRATION ENDPOINTS
# ============================================================================

class CommunicationRequest(BaseModel):
    channel: str = "sms" # or email
    recipient: str
    content: str
    subject: Optional[str] = None

@app.post("/api/integrations/send")
async def send_communication(request: CommunicationRequest, current_user: dict = Depends(get_current_user)):
    """
    Send a real-world communication (SMS/Email).
    """
    try:
        if request.channel == "sms":
            result = await integration_service.send_sms(request.recipient, request.content)
        elif request.channel == "email":
            result = await integration_service.send_email(request.recipient, request.subject or "Ward Alert", request.content)
        else:
            raise HTTPException(status_code=400, detail="Invalid channel")
            
        # Audit log
        await log_audit("system", current_user["email"], "COMMUNICATION_SENT", {
            "channel": request.channel, 
            "recipient": request.recipient,
            "status": result["status"]
        })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# INSTITUTIONAL MEMORY ENDPOINTS
# ============================================================================

@app.get("/api/cases/{case_id}/similar")
async def get_similar_cases(case_id: str, current_user: dict = Depends(get_current_user)):
    """
    Find historically similar cases to help make better decisions.
    """
    case = await db.cases.find_one({"_id": case_id, "operator_id": current_user["user_id"]})
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
        
    engine = SimilarityEngine(db)
    return await engine.find_similar_cases(case)

# ============================================================================
# ANALYTICS ENDPOINTS
# ============================================================================

@app.get("/api/analytics/dashboard")
async def get_analytics_dashboard(days: int = 30, current_user: dict = Depends(get_current_user)):
    """
    Get strategic analytics for the dashboard.
    """
    service = AnalyticsService(db)
    return await service.get_dashboard_metrics(days)

# ============================================================================
# DOCUMENT INTELLIGENCE ENDPOINTS
# ============================================================================

@app.post("/api/cases/{case_id}/documents/analyze")
async def analyze_document(
    case_id: str, 
    file: UploadFile = File(...),
    doc_type: str = "unknown",
    current_user: dict = Depends(get_current_user)
):
    """
    Upload and analyze a document (Invoice, BL, etc.) using Gemini Vision.
    """
    try:
        content = await file.read()
        analysis = await document_processor.analyze_document(content, file.filename, doc_type)
        
        # Store in DB
        doc_record = {
            "case_id": case_id,
            "filename": file.filename,
            "doc_type": doc_type,
            "analysis": analysis,
            "uploaded_at": datetime.utcnow(),
            "uploaded_by": current_user["email"]
        }
        await db.documents.insert_one(doc_record)
        
        # Auto-calculate evidence score when document is added
        try:
            evidence_service = EvidenceService(db)
            await evidence_service.calculate_and_update_score(case_id)
        except Exception as e:
            print(f"Warning: Failed to calculate evidence score: {e}")
        
        # Log to timeline
        await db.timeline_events.insert_one({
            "case_id": case_id,
            "actor": current_user["email"],
            "action": "DOCUMENT_UPLOADED",
            "content": f"Uploaded {doc_type}: {file.filename}",
            "source_type": "system",
            "reliability": "high",
            "timestamp": datetime.now(timezone.utc),
            "metadata": {"analysis_summary": str(analysis)[:200]}
        })
        
        return serialize_doc(doc_record)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/cases/{case_id}/documents/compare")
async def compare_documents_endpoint(
    case_id: str, 
    doc1_id: str, 
    doc2_id: str, 
    current_user: dict = Depends(get_current_user)
):
    """
    Compare two previously uploaded documents for discrepancies.
    """
    try:
        doc1 = await db.documents.find_one({"_id": doc1_id})
        doc2 = await db.documents.find_one({"_id": doc2_id})
        
        if not doc1 or not doc2:
            raise HTTPException(status_code=404, detail="Documents not found")
            
        comparison = await document_processor.compare_documents(doc1["analysis"], doc2["analysis"])
        
        # Log if mismatch found
        if comparison.get("match") is False:
             await db.timeline_events.insert_one({
                "case_id": case_id,
                "actor": "Ward AI",
                "action": "DISCREPANCY_DETECTED",
                "content": f"Document Mismatch detected: {comparison.get('summary')}",
                "source_type": "system",
                "reliability": "high",
                "timestamp": datetime.now(timezone.utc),
                "metadata": comparison
            })
            
        return comparison
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")

@app.get("/api/cases/{case_id}/documents")
async def list_documents(case_id: str, current_user: dict = Depends(get_current_user)):
    cursor = await db.documents.find({"case_id": case_id}, sort=[("uploaded_at", -1)], limit=100)
    docs = await cursor.to_list(length=100)
    return [serialize_doc(doc) for doc in docs]

# ============================================================================
# API v0 ENDPOINTS
# ============================================================================

# DisputePacket Endpoints
@app.post("/api/v0/movements/{movement_id}/dispute-packets")
async def create_dispute_packet(
    movement_id: str,
    packet_data: CreateDisputePacket,
    current_user: dict = Depends(get_current_user)
):
    """Create a dispute packet for a movement"""
    try:
        # Verify movement exists and belongs to user
        movement = await db.cases.find_one({"_id": movement_id, "operator_id": current_user["user_id"]})
        if not movement:
            raise HTTPException(status_code=404, detail="Movement not found")
        
        now = datetime.now(timezone.utc)
        packet = {
            "movement_id": movement_id,
            "invoice_id": packet_data.invoice_id,
            "template_type": packet_data.template_type,
            "status": "draft",
            "selected_events": packet_data.selected_events or [],
            "selected_attachments": packet_data.selected_attachments or [],
            "narrative": packet_data.narrative,
            "metadata": packet_data.metadata or {},
            "created_by": current_user["user_id"]
        }
        
        packet_id = await db.dispute_packets.insert_one(packet)
        packet["_id"] = packet_id.inserted_id
        
        await log_audit(movement_id, current_user["email"], "DISPUTE_PACKET_CREATED", {
            "packet_id": str(packet_id.inserted_id),
            "invoice_id": packet_data.invoice_id
        })
        
        return serialize_doc(packet)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create dispute packet: {str(e)}")

@app.get("/api/v0/movements/{movement_id}/dispute-packets")
async def list_dispute_packets(
    movement_id: str,
    current_user: dict = Depends(get_current_user)
):
    """List dispute packets for a movement"""
    try:
        # Verify movement exists and belongs to user
        movement = await db.cases.find_one({"_id": movement_id, "operator_id": current_user["user_id"]})
        if not movement:
            raise HTTPException(status_code=404, detail="Movement not found")
        
        cursor = await db.dispute_packets.find({"movement_id": movement_id}, sort=[("created_at", -1)], limit=100)
        packets = await cursor.to_list(length=100)
        
        return [serialize_doc(packet) for packet in packets]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list dispute packets: {str(e)}")

@app.get("/api/v0/dispute-packets/{packet_id}")
async def get_dispute_packet(
    packet_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a dispute packet"""
    try:
        packet = await db.dispute_packets.find_one({"_id": packet_id})
        if not packet:
            raise HTTPException(status_code=404, detail="Dispute packet not found")
        
        # Verify movement belongs to user
        movement = await db.cases.find_one({"_id": packet["movement_id"], "operator_id": current_user["user_id"]})
        if not movement:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return serialize_doc(packet)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get dispute packet: {str(e)}")

@app.post("/api/v0/dispute-packets/{packet_id}/export")
async def export_dispute_packet(
    packet_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Export dispute packet as PDF/ZIP"""
    try:
        packet = await db.dispute_packets.find_one({"_id": packet_id})
        if not packet:
            raise HTTPException(status_code=404, detail="Dispute packet not found")
        
        # Verify movement belongs to user
        movement = await db.cases.find_one({"_id": packet["movement_id"], "operator_id": current_user["user_id"]})
        if not movement:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Use existing DisputeBundleService to generate bundle
        movement_id = packet.get("movement_id")
        if not movement_id:
            raise HTTPException(status_code=400, detail="Dispute packet missing movement_id")
        
        bundle_service = DisputeBundleService(db)
        zip_buffer, filename = await bundle_service.generate_bundle(movement_id)
        
        # Update packet status
        await db.dispute_packets.update_one(
            {"_id": packet_id},
            {"$set": {
                "status": "generated",
                "generated_at": datetime.now(timezone.utc)
            }}
        )
        
        from fastapi.responses import StreamingResponse
        return StreamingResponse(
            io.BytesIO(zip_buffer.read()),
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export dispute packet: {str(e)}")

@app.patch("/api/v0/dispute-packets/{packet_id}")
async def update_dispute_packet(
    packet_id: str,
    update_data: UpdateDisputePacket,
    current_user: dict = Depends(get_current_user)
):
    """Update a dispute packet"""
    try:
        packet = await db.dispute_packets.find_one({"_id": packet_id})
        if not packet:
            raise HTTPException(status_code=404, detail="Dispute packet not found")
        
        # Verify movement belongs to user
        movement = await db.cases.find_one({"_id": packet["movement_id"], "operator_id": current_user["user_id"]})
        if not movement:
            raise HTTPException(status_code=403, detail="Access denied")
        
        update_dict = {}
        if update_data.status is not None:
            update_dict["status"] = update_data.status
        if update_data.narrative is not None:
            update_dict["narrative"] = update_data.narrative
        if update_data.outcome is not None:
            update_dict["outcome"] = update_data.outcome
        if update_data.outcome_amount is not None:
            update_dict["outcome_amount"] = update_data.outcome_amount
        if update_data.submitted_at is not None:
            update_dict["submitted_at"] = update_data.submitted_at
        if update_data.resolved_at is not None:
            update_dict["resolved_at"] = update_data.resolved_at
        
        if update_dict:
            # db_compat expects MongoDB-style update with $set
            await db.dispute_packets.update_one({"_id": packet_id}, {"$set": update_dict})
            await log_audit(packet["movement_id"], current_user["email"], "DISPUTE_PACKET_UPDATED", {
                "packet_id": packet_id,
                "updates": update_dict
            })
        
        updated_packet = await db.dispute_packets.find_one({"_id": packet_id})
        return serialize_doc(updated_packet)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update dispute packet: {str(e)}")

# Facility Endpoints
@app.post("/api/v0/facilities")
async def create_facility(
    facility_data: CreateFacility,
    current_user: dict = Depends(get_current_user)
):
    """Create a facility"""
    try:
        facility = {
            "external_id": facility_data.external_id,
            "name": facility_data.name,
            "type": facility_data.type,
            "code": facility_data.code,
            "address": facility_data.address,
            "location": facility_data.location,
            "metadata": facility_data.metadata or {},
            "created_by": current_user["user_id"]
        }
        
        facility_id = await db.facilities.insert_one(facility)
        facility["_id"] = facility_id.inserted_id
        
        return serialize_doc(facility)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create facility: {str(e)}")

@app.get("/api/v0/facilities")
async def list_facilities(
    type: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """List facilities"""
    try:
        query = {}
        if type:
            query["type"] = type
        
        cursor = await db.facilities.find(query, sort=[("name", 1)], limit=1000)
        facilities = await cursor.to_list(length=1000)
        
        return [serialize_doc(facility) for facility in facilities]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list facilities: {str(e)}")

@app.get("/api/v0/facilities/{facility_id}")
async def get_facility(
    facility_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a facility"""
    try:
        facility = await db.facilities.find_one({"_id": facility_id})
        if not facility:
            raise HTTPException(status_code=404, detail="Facility not found")
        
        return serialize_doc(facility)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get facility: {str(e)}")

# Party Endpoints
@app.post("/api/v0/parties")
async def create_party(
    party_data: CreateParty,
    current_user: dict = Depends(get_current_user)
):
    """Create a party"""
    try:
        party = {
            "external_id": party_data.external_id,
            "name": party_data.name,
            "type": party_data.type,
            "code": party_data.code,
            "contact_info": party_data.contact_info,
            "metadata": party_data.metadata or {},
            "created_by": current_user["user_id"]
        }
        
        party_id = await db.parties.insert_one(party)
        party["_id"] = party_id.inserted_id
        
        return serialize_doc(party)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create party: {str(e)}")

@app.get("/api/v0/parties")
async def list_parties(
    type: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """List parties"""
    try:
        query = {}
        if type:
            query["type"] = type
        
        cursor = await db.parties.find(query, sort=[("name", 1)], limit=1000)
        parties = await cursor.to_list(length=1000)
        
        return [serialize_doc(party) for party in parties]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list parties: {str(e)}")

@app.get("/api/v0/parties/{party_id}")
async def get_party(
    party_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a party"""
    try:
        party = await db.parties.find_one({"_id": party_id})
        if not party:
            raise HTTPException(status_code=404, detail="Party not found")
        
        return serialize_doc(party)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get party: {str(e)}")

# Movement Endpoints (API v0)
@app.post("/api/v0/movements")
async def create_movement(
    movement_data: CreateMovement,
    current_user: dict = Depends(get_current_user)
):
    """Create or upsert a Movement"""
    try:
        # Check if movement exists with same external_id (upsert behavior)
        existing_movement = None
        if movement_data.external_id:
            cursor = await db.cases.find({"external_id": movement_data.external_id, "operator_id": current_user["user_id"]}, limit=1)
            existing_list = await cursor.to_list(length=1)
            if existing_list:
                existing_movement = existing_list[0]
        
        now = datetime.now(timezone.utc)
        
        if existing_movement:
            # Update existing movement
            update_dict = {
                "updated_at": now
            }
            if movement_data.container_id:
                update_dict["container_id"] = movement_data.container_id
            if movement_data.truck_id:
                update_dict["truck_id"] = movement_data.truck_id
            if movement_data.bill_of_lading:
                update_dict["bill_of_lading"] = movement_data.bill_of_lading
            if movement_data.lane:
                update_dict["lane"] = movement_data.lane
            if movement_data.planned_start_date:
                update_dict["planned_start_date"] = movement_data.planned_start_date
            if movement_data.planned_end_date:
                update_dict["planned_end_date"] = movement_data.planned_end_date
            if movement_data.metadata:
                update_dict["metadata"] = movement_data.metadata
            
            await db.cases.update_one({"_id": existing_movement["_id"]}, {"$set": update_dict})
            movement_id = str(existing_movement["_id"])
        else:
            # Create new movement (as a case)
            movement = {
                "operator_id": current_user["user_id"],
                "operator_email": current_user["email"],
                "description": f"Movement: {movement_data.container_id or movement_data.truck_id or movement_data.external_id or 'Unknown'}",
                "status": "active",
                "external_id": movement_data.external_id,
                "container_id": movement_data.container_id,
                "truck_id": movement_data.truck_id,
                "bill_of_lading": movement_data.bill_of_lading,
                "lane": movement_data.lane,
                "planned_start_date": movement_data.planned_start_date,
                "planned_end_date": movement_data.planned_end_date,
                "disruption_details": {},
                "shipment_identifiers": {},
                "metadata": movement_data.metadata or {},
                "created_at": now,
                "updated_at": now
            }
            
            result = await db.cases.insert_one(movement)
            movement_id = str(result.inserted_id)
            movement["_id"] = result.inserted_id
            
            # Create initial timeline event
            await db.timeline_events.insert_one({
                "case_id": movement_id,
                "actor": current_user["email"],
                "action": "MOVEMENT_CREATED",
                "content": f"Movement created: {movement_data.container_id or movement_data.truck_id or 'Unknown'}",
                "source_type": "system",
                "reliability": "high",
                "timestamp": now,
                "metadata": {}
            })
        
        # Get the movement to return
        movement = await db.cases.find_one({"_id": movement_id})
        return serialize_doc(movement)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create movement: {str(e)}")

@app.get("/api/v0/movements")
async def list_movements(
    container_id: Optional[str] = None,
    truck_id: Optional[str] = None,
    external_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: dict = Depends(get_current_user)
):
    """List movements with filters"""
    try:
        query = {"operator_id": current_user["user_id"]}
        
        if container_id:
            query["container_id"] = container_id
        if truck_id:
            query["truck_id"] = truck_id
        if external_id:
            query["external_id"] = external_id
        if status:
            query["status"] = status
        
        cursor = await db.cases.find(query, sort=[("updated_at", -1)], limit=min(limit, 100))
        movements = await cursor.to_list(length=min(limit, 100))
        
        return {
            "items": [serialize_doc(m) for m in movements[offset:offset+limit]],
            "total": len(movements),
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list movements: {str(e)}")

@app.get("/api/v0/movements/{movement_id}")
async def get_movement(
    movement_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a movement"""
    try:
        movement = await db.cases.find_one({"_id": movement_id, "operator_id": current_user["user_id"]})
        if not movement:
            raise HTTPException(status_code=404, detail="Movement not found")
        
        return serialize_doc(movement)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get movement: {str(e)}")

# Event Endpoints (API v0)
@app.post("/api/v0/events")
async def create_event(
    event_data: CreateEvent,
    current_user: dict = Depends(get_current_user)
):
    """Create an event for a movement (with GPS, device_id, captured_at)"""
    try:
        # Verify movement exists and belongs to user
        movement = await db.cases.find_one({"_id": event_data.movement_id, "operator_id": current_user["user_id"]})
        if not movement:
            raise HTTPException(status_code=404, detail="Movement not found")
        
        now = datetime.now(timezone.utc)
        captured_at = event_data.timestamp_captured or now
        
        # Determine action type
        action = "CONTEXT_ADDED"
        if event_data.event_type == "incident":
            action = "DISRUPTION_REPORTED"
        elif event_data.event_type == "edit":
            action = "EVENT_EDITED"
        
        # Extract content text
        content_text = ""
        if event_data.content:
            content_text = event_data.content.get("text") or event_data.content.get("voice_transcript") or ""
        
        # Determine source type
        source_type = "system"
        if event_data.device_id:
            source_type = "mobile"
        elif event_data.content and event_data.content.get("voice_recording_url"):
            source_type = "voice"
        
        # Determine reliability
        reliability = event_data.reliability or "medium"
        if event_data.location and event_data.device_id:
            reliability = "high"  # GPS + device ID = high reliability
        
        event = {
            "case_id": event_data.movement_id,
            "actor": current_user["email"],
            "action": action,
            "content": content_text,
            "source_type": source_type,
            "reliability": reliability,
            "timestamp": captured_at,
            "gps": event_data.location,  # Store GPS in new column
            "device_id": event_data.device_id,  # Store device_id in new column
            "captured_at": captured_at,  # Store captured_at (immutable)
            "metadata": {
                **(event_data.metadata or {}),
                "event_type": event_data.event_type,
                "incident_type": event_data.incident_type,
                "facility_id": event_data.facility_id,
                "actor_id": event_data.actor_id,
                "actor_role": event_data.actor_role,
                "timestamp_incident": event_data.timestamp_incident.isoformat() if event_data.timestamp_incident else None,
                "original_event_id": event_data.original_event_id,
                "content": event_data.content
            }
        }
        
        # If this is an edit, mark the original event
        if event_data.original_event_id:
            event["metadata"]["original_event_id"] = event_data.original_event_id
            event["edited_at"] = now  # Store edited_at timestamp
        
        result = await db.timeline_events.insert_one(event)
        event["_id"] = result.inserted_id
        
        # Update movement timestamp
        await db.cases.update_one(
            {"_id": event_data.movement_id},
            {"$set": {"updated_at": now}}
        )
        
        await log_audit(event_data.movement_id, current_user["email"], "EVENT_CREATED", {
            "event_id": str(result.inserted_id),
            "event_type": event_data.event_type
        })
        
        return serialize_doc(event)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create event: {str(e)}")

# Attachment Endpoints (API v0)
@app.post("/api/v0/attachments")
async def create_attachment(
    file: UploadFile = File(...),
    event_id: Optional[str] = None,
    movement_id: Optional[str] = None,
    file_type: str = "photo",  # 'photo', 'video', 'audio', 'document'
    description: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Upload an attachment and associate it with an event"""
    try:
        # Validate file size (10MB limit)
        file_content = await file.read()
        file_size = len(file_content)
        if file_size > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")
        
        # Validate file type
        mime_type = file.content_type or "application/octet-stream"
        allowed_types = [
            "image/jpeg", "image/png", "image/jpg",
            "application/pdf",
            "audio/mpeg", "audio/mp3", "audio/wav",
            "video/mp4", "video/mpeg"
        ]
        if mime_type not in allowed_types:
            raise HTTPException(status_code=400, detail=f"File type {mime_type} not supported")
        
        # Verify event exists if provided
        if event_id:
            event = await db.timeline_events.find_one({"_id": event_id})
            if not event:
                raise HTTPException(status_code=404, detail="Event not found")
            movement_id = event.get("case_id")
        
        # Verify movement exists and belongs to user
        if movement_id:
            movement = await db.cases.find_one({"_id": movement_id, "operator_id": current_user["user_id"]})
            if not movement:
                raise HTTPException(status_code=404, detail="Movement not found")
        
        # For now, store file metadata (actual file storage would go to S3/Supabase Storage)
        # In production, upload to storage service and get URL
        storage_url = f"https://storage.ward.ai/{file_type}s/{file.filename}"  # Placeholder
        storage_key = f"{file_type}s/{file.filename}"  # Placeholder
        
        attachment = {
            "event_id": event_id,
            "movement_id": movement_id,
            "filename": file.filename,
            "file_type": file_type,
            "mime_type": mime_type,
            "file_size": file_size,
            "storage_url": storage_url,
            "storage_key": storage_key,
            "metadata": {
                "description": description,
                "uploaded_at": datetime.now(timezone.utc).isoformat()
            },
            "uploaded_by": current_user["user_id"]
        }
        
        result = await db.attachments.insert_one(attachment)
        attachment["_id"] = result.inserted_id
        
        # Log to timeline if event_id provided
        if event_id:
            await db.timeline_events.insert_one({
                "case_id": movement_id,
                "actor": current_user["email"],
                "action": "ATTACHMENT_UPLOADED",
                "content": f"Uploaded {file_type}: {file.filename}",
                "source_type": "system",
                "reliability": "high",
                "timestamp": datetime.now(timezone.utc),
                "metadata": {"attachment_id": str(result.inserted_id)}
            })
        
        return serialize_doc(attachment)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload attachment: {str(e)}")

@app.get("/api/v0/events/{event_id}/attachments")
async def list_attachments(
    event_id: str,
    current_user: dict = Depends(get_current_user)
):
    """List attachments for an event"""
    try:
        # Verify event exists
        event = await db.timeline_events.find_one({"_id": event_id})
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        movement_id = event.get("case_id")
        # Verify movement belongs to user
        movement = await db.cases.find_one({"_id": movement_id, "operator_id": current_user["user_id"]})
        if not movement:
            raise HTTPException(status_code=403, detail="Access denied")
        
        cursor = await db.attachments.find({"event_id": event_id}, sort=[("created_at", -1)], limit=100)
        attachments = await cursor.to_list(length=100)
        
        return [serialize_doc(att) for att in attachments]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list attachments: {str(e)}")

@app.get("/api/v0/attachments/{attachment_id}")
async def get_attachment(
    attachment_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get an attachment"""
    try:
        attachment = await db.attachments.find_one({"_id": attachment_id})
        if not attachment:
            raise HTTPException(status_code=404, detail="Attachment not found")
        
        # Verify movement belongs to user
        movement_id = attachment.get("movement_id")
        if movement_id:
            movement = await db.cases.find_one({"_id": movement_id, "operator_id": current_user["user_id"]})
            if not movement:
                raise HTTPException(status_code=403, detail="Access denied")
        
        return serialize_doc(attachment)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get attachment: {str(e)}")

# ============================================================================
# OPERATOR ENDPOINTS (Transport Operator Plug & Play)
# ============================================================================

class CreateOperator(BaseModel):
    company_name: str
    email: EmailStr
    phone: Optional[str] = None
    fleet_size: Optional[int] = 0
    account_type: Optional[str] = "pilot"

class AddVehicle(BaseModel):
    vehicle_number: str
    vehicle_type: Optional[str] = "truck"
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None
    route: Optional[str] = None

@app.post("/api/operators/create")
async def create_operator_account(
    operator_data: CreateOperator,
    current_user: dict = Depends(get_current_user)
):
    """Create transport operator account"""
    try:
        operator_service = OperatorService(db)
        operator_id = await operator_service.create_operator_account({
            "company_name": operator_data.company_name,
            "email": operator_data.email,
            "phone": operator_data.phone,
            "fleet_size": operator_data.fleet_size,
            "account_type": operator_data.account_type,
            "created_by": current_user["user_id"]
        })
        return {"operator_id": operator_id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create operator account: {str(e)}")

@app.post("/api/operators/fleet/add")
async def add_fleet_vehicle(
    vehicle_data: AddVehicle,
    current_user: dict = Depends(get_current_user)
):
    """Add a vehicle to operator's fleet"""
    try:
        await ensure_db_initialized()
        
        # Find operator by user email
        operator = await db.operators.find_one({"email": current_user["email"]})
        if not operator:
            # Create operator account for user if doesn't exist
            operator_service = OperatorService(db)
            operator_id = await operator_service.create_operator_account({
                "company_name": current_user.get("email", "Unknown Company"),
                "email": current_user["email"],
                "fleet_size": 0,
                "account_type": "pilot",
                "created_by": current_user["user_id"]
            })
        else:
            operator_id = operator.get("_id") or operator.get("id")
        
        operator_service = OperatorService(db)
        vehicle_id = await operator_service.add_fleet_vehicle(operator_id, vehicle_data.dict())
        return {"vehicle_id": vehicle_id, "status": "added", "operator_id": operator_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add vehicle: {str(e)}")

@app.post("/api/operators/fleet/bulk-upload")
async def bulk_upload_fleet(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Bulk upload fleet from CSV"""
    try:
        await ensure_db_initialized()
        
        # Find operator by user email
        operator = await db.operators.find_one({"email": current_user["email"]})
        if not operator:
            raise HTTPException(status_code=404, detail="Operator account not found. Please create one first.")
        
        operator_id = operator.get("_id") or operator.get("id")
        content = await file.read()
        csv_content = content.decode('utf-8')
        
        operator_service = OperatorService(db)
        results = await operator_service.bulk_upload_fleet(operator_id, csv_content)
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload fleet: {str(e)}")

@app.get("/api/operators/fleet")
async def get_operator_fleet(current_user: dict = Depends(get_current_user)):
    """Get all vehicles for operator"""
    try:
        await ensure_db_initialized()
        
        # Find operator by user email
        operator = await db.operators.find_one({"email": current_user["email"]})
        if not operator:
            return []
        
        operator_id = operator.get("_id") or operator.get("id")
        operator_service = OperatorService(db)
        vehicles = await operator_service.get_operator_vehicles(operator_id)
        return vehicles
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get fleet: {str(e)}")

@app.get("/api/operators/dashboard")
async def get_operator_dashboard(
    days: int = 7,
    current_user: dict = Depends(get_current_user)
):
    """Get operator dashboard metrics"""
    try:
        await ensure_db_initialized()
        
        # Find operator by user email
        operator = await db.operators.find_one({"email": current_user["email"]})
        if not operator:
            return {
                "fleet_size": 0,
                "total_cases": 0,
                "active_cases": 0,
                "total_financial_impact": 0,
                "evidence_ready_cases": 0,
                "evidence_readiness_rate": 0,
                "cases_by_route": {},
                "period_days": days
            }
        
        operator_id = operator.get("_id") or operator.get("id")
        operator_service = OperatorService(db)
        dashboard = await operator_service.get_operator_dashboard(operator_id, days)
        return dashboard
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get dashboard: {str(e)}")

@app.get("/api/operators/settings")
async def get_operator_settings(current_user: dict = Depends(get_current_user)):
    """Get operator settings"""
    try:
        await ensure_db_initialized()
        
        operator = await db.operators.find_one({"email": current_user["email"]})
        if not operator:
            raise HTTPException(status_code=404, detail="Operator account not found")
        
        settings = operator.get("settings", {})
        return {
            "notifications": settings.get("notifications", {"email": True, "whatsapp": False, "sms": False}),
            "webhook_url": settings.get("webhook_url"),
            "branding": settings.get("branding", {"logo_url": "", "primary_color": "#2563eb"})
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get settings: {str(e)}")

class UpdateOperatorSettings(BaseModel):
    notifications: Optional[Dict[str, bool]] = None
    webhook_url: Optional[str] = None
    branding: Optional[Dict[str, str]] = None

@app.patch("/api/operators/settings")
async def update_operator_settings(
    settings_data: UpdateOperatorSettings,
    current_user: dict = Depends(get_current_user)
):
    """Update operator settings"""
    try:
        await ensure_db_initialized()
        
        operator = await db.operators.find_one({"email": current_user["email"]})
        if not operator:
            raise HTTPException(status_code=404, detail="Operator account not found")
        
        operator_id = operator.get("_id") or operator.get("id")
        operator_service = OperatorService(db)
        
        # Get current settings
        current_settings = operator.get("settings", {})
        
        # Update settings
        if settings_data.notifications:
            current_settings["notifications"] = settings_data.notifications
        if settings_data.webhook_url is not None:
            current_settings["webhook_url"] = settings_data.webhook_url
        if settings_data.branding:
            current_settings["branding"] = {**current_settings.get("branding", {}), **settings_data.branding}
        
        # Save settings
        await operator_service.update_operator_settings(operator_id, current_settings)
        
        return {"status": "updated", "settings": current_settings}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update settings: {str(e)}")

@app.post("/api/operators/drivers/generate-links")
async def generate_driver_links(
    method: str = "magic_link",  # magic_link or qr_code
    current_user: dict = Depends(get_current_user)
):
    """Generate magic links or QR codes for drivers"""
    try:
        await ensure_db_initialized()
        
        # Find operator by user email
        operator = await db.operators.find_one({"email": current_user["email"]})
        if not operator:
            raise HTTPException(status_code=404, detail="Operator account not found. Please create one first.")
        
        operator_id = operator.get("_id") or operator.get("id")
        operator_service = OperatorService(db)
        
        # Get all vehicles
        vehicles = await operator_service.get_operator_vehicles(operator_id)
        
        if not vehicles or len(vehicles) == 0:
            return {"links": [], "method": method, "message": "No vehicles found. Add vehicles first."}
        
        links = []
        for vehicle in vehicles:
            vehicle_id = vehicle.get("_id") or vehicle.get("id")
            if not vehicle_id:
                continue
                
            try:
                if method == "magic_link":
                    link = await operator_service.generate_driver_magic_link(operator_id, vehicle_id)
                    links.append({
                        "vehicle_number": vehicle.get("vehicle_number", "Unknown"),
                        "driver_name": vehicle.get("driver_name"),
                        "link": link
                    })
                elif method == "qr_code":
                    qr_data = await operator_service.generate_driver_qr_code(operator_id, vehicle_id)
                    links.append({
                        "vehicle_number": vehicle.get("vehicle_number", "Unknown"),
                        "driver_name": vehicle.get("driver_name"),
                        "qr_url": qr_data["qr_url"],
                        "link": qr_data["qr_data"]
                    })
            except Exception as e:
                print(f"Warning: Failed to generate link for vehicle {vehicle_id}: {e}")
                continue
        
        return {"links": links, "method": method, "count": len(links)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate links: {str(e)}")

# Driver endpoints (no auth required - magic link based)
@app.get("/api/driver/verify/{token}")
async def verify_driver_token(token: str):
    """Verify magic link token and return vehicle info"""
    try:
        await ensure_db_initialized()
        
        # Find magic link
        magic_link = await db.magic_links.find_one({"token": token})
        if not magic_link:
            raise HTTPException(status_code=404, detail="Invalid token")
        
        # Check if expired
        expires_at = magic_link.get("expires_at")
        if expires_at and datetime.now(timezone.utc) > expires_at:
            raise HTTPException(status_code=410, detail="Token expired")
        
        # Get vehicle info
        vehicle_id = magic_link.get("vehicle_id")
        vehicle = await db.fleet_vehicles.find_one({"_id": vehicle_id})
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        
        # Increment used count
        await db.magic_links.update_one(
            {"token": token},
            {"$set": {"used_count": magic_link.get("used_count", 0) + 1, "last_used_at": datetime.now(timezone.utc)}}
        )
        
        return {
            "vehicle_number": vehicle.get("vehicle_number"),
            "driver_name": vehicle.get("driver_name"),
            "route": vehicle.get("route"),
            "valid": True
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to verify token: {str(e)}")

class DriverReport(BaseModel):
    token: str
    audio_base64: str
    audio_format: str = "webm"
    language_code: str = "hi-IN"

@app.post("/api/driver/report")
async def driver_report_disruption(report_data: DriverReport):
    """Driver reports disruption via voice (no auth required - token based)"""
    try:
        await ensure_db_initialized()
        
        # Verify token
        magic_link = await db.magic_links.find_one({"token": report_data.token})
        if not magic_link:
            raise HTTPException(status_code=404, detail="Invalid token")
        
        # Get vehicle info
        vehicle_id = magic_link.get("vehicle_id")
        vehicle = await db.fleet_vehicles.find_one({"_id": vehicle_id})
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        
        operator_id = magic_link.get("operator_id")
        
        # Transcribe voice (if audio provided)
        transcript = ""
        if report_data.audio_base64:
            try:
                import base64
                import aiofiles
                import os
                
                # Decode base64 audio
                audio_bytes = base64.b64decode(report_data.audio_base64)
                
                # Save temporarily
                temp_file_path = f"/tmp/driver_voice_{vehicle_id}_{datetime.now(timezone.utc).timestamp()}.{report_data.audio_format}"
                async with aiofiles.open(temp_file_path, 'wb') as f:
                    await f.write(audio_bytes)
                
                # Transcribe using Sarvam AI
                result = await sarvam_service.speech_to_text(
                    temp_file_path,
                    language_code=report_data.language_code
                )
                
                # Clean up temp file
                try:
                    os.remove(temp_file_path)
                except:
                    pass
                
                if result.get("success"):
                    transcript = result.get("transcript", "")
                else:
                    transcript = "Voice report (transcription failed)"
            except Exception as e:
                print(f"Warning: Voice transcription failed: {e}")
                transcript = "Voice report (transcription failed)"
        
        # Create case
        case_data = {
            "operator_id": operator_id,
            "operator_email": f"driver-{vehicle_id}@ward.local",  # Placeholder
            "description": transcript or "Driver reported disruption via voice",
            "disruption_details": {
                "disruption_type": "reported",
                "source": "Driver Voice Report",
                "identifier": vehicle.get("vehicle_number")
            },
            "shipment_identifiers": {
                "ids": [vehicle.get("vehicle_number")]
            },
            "voice_transcript": transcript,
            "vehicle_id": vehicle_id,
            "status": "REPORTED",
            "created_via": "driver_app"
        }
        
        result = await db.cases.insert_one(case_data)
        case_id = result.inserted_id
        
        # Create timeline event
        await db.timeline_events.insert_one({
            "case_id": case_id,
            "actor": vehicle.get("driver_name") or "Driver",
            "action": "DISRUPTION_REPORTED",
            "content": transcript,
            "source_type": "voice",
            "reliability": "high",
            "timestamp": datetime.now(timezone.utc),
            "metadata": {
                "vehicle_id": vehicle_id,
                "vehicle_number": vehicle.get("vehicle_number")
            }
        })
        
        # Trigger webhook if configured
        try:
            from webhook_service import WebhookService
            webhook_service = WebhookService(db)
            await webhook_service.trigger_webhook(
                operator_id,
                "disruption_reported",
                {
                    "case_id": str(case_id),
                    "vehicle_number": vehicle.get("vehicle_number"),
                    "description": transcript or "Driver reported disruption",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
        except Exception as e:
            print(f"Warning: Webhook trigger failed: {e}")
        
        return {
            "case_id": str(case_id),
            "status": "created",
            "message": "Disruption reported successfully",
            "vehicle_number": vehicle.get("vehicle_number")
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to report disruption: {str(e)}")

@app.get("/api/health")
async def health():
    """Health check endpoint for monitoring"""
    try:
        await ensure_db_initialized()
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

@app.get("/api/health/detailed")
async def detailed_health_check():
    """Detailed health check with system information"""
    try:
        await ensure_db_initialized()
        
        # Check database connection
        db_status = "connected"
        try:
            await db.users.find_one({})
        except:
            db_status = "disconnected"
        
        return {
            "status": "healthy" if db_status == "connected" else "degraded",
            "database": db_status,
            "api_version": "v0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "environment": os.getenv("ENVIRONMENT", "production")
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

# ============================================================================
# DEVELOPER API ENDPOINTS
# ============================================================================

from developer_service import DeveloperService

class WebhookCreate(BaseModel):
    url: str
    events: List[str]

class ApiKeyCreate(BaseModel):
    name: str

@app.post("/api/developer/keys")
async def create_api_key(request: ApiKeyCreate, current_user: dict = Depends(get_current_user)):
    service = DeveloperService(db)
    return await service.generate_api_key(current_user["user_id"], request.name)

@app.get("/api/developer/keys")
async def list_api_keys(current_user: dict = Depends(get_current_user)):
    service = DeveloperService(db)
    return await service.list_api_keys(current_user["user_id"])

@app.post("/api/developer/webhooks")
async def create_webhook(request: WebhookCreate, current_user: dict = Depends(get_current_user)):
    service = DeveloperService(db)
    return await service.register_webhook(current_user["user_id"], request.url, request.events)

@app.get("/api/developer/webhooks")
async def list_webhooks(current_user: dict = Depends(get_current_user)):
    service = DeveloperService(db)
    return await service.list_webhooks(current_user["user_id"])


# Only run uvicorn if this is the main module (local development)
# Don't import uvicorn at module level to avoid Vercel handler detection issues
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
# Force deployment Thu Dec 18 23:47:30 IST 2025
