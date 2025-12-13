from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta, timezone
from enum import Enum
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
import jwt
import bcrypt
from dotenv import load_dotenv
import asyncio
from contextlib import asynccontextmanager

# Import AI modules
from ai_decision import generate_decision_structure
from sarvam_service import sarvam_service
from voice_assistant import voice_assistant
from rca_engine import RCAEngine
from coordination_manager import CoordinationManager
import aiofiles
import base64

# Initialize voice assistant and RCA engine
rca_engine = RCAEngine()
coordination_manager = None  # Will be initialized in lifespan

# Load environment variables
load_dotenv()

# Configuration
MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME", "ward_v0")
JWT_SECRET = os.getenv("JWT_SECRET", "ward-v0-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

# Global MongoDB client
client = None
db = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global client, db, coordination_manager
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    print(f"Connected to MongoDB: {DB_NAME}")
    
    # Initialize Coordination Manager
    coordination_manager = CoordinationManager(db)

    # Create indexes
    await db.users.create_index("email", unique=True)
    await db.cases.create_index("created_at")
    await db.cases.create_index("status")
    await db.cases.create_index("decision_owner_email")
    await db.audit_entries.create_index("case_id")
    await db.timeline_events.create_index("case_id")
    await db.timeline_events.create_index("timestamp")
    
    yield
    
    # Shutdown
    client.close()
    print("Closed MongoDB connection")

app = FastAPI(title="Ward v0 API", lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGINS", "*")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

class CreateCase(BaseModel):
    description: str = Field(min_length=10)
    disruption_details: DisruptionDetails
    shipment_identifiers: ShipmentIdentifiers

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
    next_state: DisruptionStatus
    reason: Optional[str] = None

class AddTimelineEvent(BaseModel):
    content: str = Field(min_length=1)
    source_type: SourceType
    reliability: ReliabilityLevel
    metadata: Optional[Dict[str, Any]] = None

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def serialize_doc(doc: dict) -> dict:
    """Convert MongoDB document to JSON-serializable dict"""
    if doc is None:
        return None
    
    serialized = {}
    for key, value in doc.items():
        if isinstance(value, ObjectId):
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
    exp = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    payload = {
        "user_id": user_id,
        "email": email,
        "exp": exp
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("user_id")
        email = payload.get("email")
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Verify user exists
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return {"user_id": user_id, "email": email}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def log_audit(case_id: str, actor: str, action: str, payload: dict):
    """Log audit entry"""
    await db.audit_entries.insert_one({
        "case_id": case_id,
        "actor": actor,
        "action": action,
        "payload": payload,
        "timestamp": datetime.utcnow()
    })

# ============================================================================
# AUTH ROUTES
# ============================================================================

@app.post("/api/auth/register", response_model=Token)
async def register(user_data: UserRegister):
    # Check if user exists
    existing = await db.users.find_one({"email": user_data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    hashed_pw = hash_password(user_data.password)
    result = await db.users.insert_one({
        "email": user_data.email,
        "password_hash": hashed_pw,
        "created_at": datetime.utcnow()
    })
    
    user_id = str(result.inserted_id)
    token = create_jwt_token(user_id, user_data.email)
    
    return {"access_token": token, "token_type": "bearer"}

@app.post("/api/auth/login", response_model=Token)
async def login(credentials: UserLogin):
    user = await db.users.find_one({"email": credentials.email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user_id = str(user["_id"])
    token = create_jwt_token(user_id, credentials.email)
    
    return {"access_token": token, "token_type": "bearer"}

@app.get("/api/auth/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    user = await db.users.find_one({"_id": ObjectId(current_user["user_id"])})
    return serialize_doc({
        "_id": user["_id"],
        "email": user["email"],
        "created_at": user["created_at"]
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
    
    result = await db.cases.insert_one(case)
    case_id = str(result.inserted_id)
    
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
    
    case["_id"] = result.inserted_id
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
    
    cursor = db.cases.find(query).sort("updated_at", -1).limit(100)
    cases = await cursor.to_list(length=100)
    
    # Get last timeline event for each case
    for case in cases:
        case_id = str(case["_id"])
        last_event = await db.timeline_events.find_one(
            {"case_id": case_id},
            sort=[("timestamp", -1)]
        )
        case["last_event"] = serialize_doc(last_event) if last_event else None
    
    return [serialize_doc(case) for case in cases]

@app.get("/api/cases/{case_id}")
async def get_case(case_id: str, current_user: dict = Depends(get_current_user)):
    try:
        case = await db.cases.find_one({"_id": ObjectId(case_id), "operator_id": current_user["user_id"]})
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        
        # Get timeline events
        timeline_cursor = db.timeline_events.find({"case_id": case_id}).sort("timestamp", -1)
        timeline_events = await timeline_cursor.to_list(length=500)
        
        # Get draft if exists (for legacy decision flow)
        draft = await db.drafts.find_one({"case_id": case_id})
        
        # Get approvals (for legacy decision flow)
        approvals_cursor = db.approvals.find({"case_id": case_id})
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
        case = await db.cases.find_one({"_id": ObjectId(case_id), "operator_id": current_user["user_id"]})
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
            "created_at": datetime.utcnow()
        }
        
        result = await db.drafts.insert_one(draft)
        draft["_id"] = result.inserted_id
        
        await log_audit(case_id, current_user["email"], "AI_DRAFT_GENERATED", {"model": "gemini-2.5-flash"})
        await db.cases.update_one({"_id": ObjectId(case_id)}, {"$set": {"status": "reviewing", "updated_at": datetime.utcnow()}})
        
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
        await db.cases.update_one({"_id": ObjectId(case_id)}, {"$set": {"status": "finalized", "updated_at": datetime.utcnow()}})
        
        return serialize_doc(decision)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============================================================================
# AUDIT TRAIL ROUTES
# ============================================================================

@app.get("/api/audit")
async def list_audit_trail(current_user: dict = Depends(get_current_user)):
    # Get all cases for this user
    cases_cursor = db.cases.find({"operator_id": current_user["user_id"]})
    cases = await cases_cursor.to_list(length=None)
    case_ids = [str(case["_id"]) for case in cases]
    
    # Get audit entries for these cases
    cursor = db.audit_entries.find({"case_id": {"$in": case_ids}}).sort("timestamp", -1).limit(100)
    entries = await cursor.to_list(length=100)
    return [serialize_doc(entry) for entry in entries]

@app.get("/api/cases/{case_id}/audit")
async def get_case_audit(case_id: str, current_user: dict = Depends(get_current_user)):
    # Verify case belongs to user
    case = await db.cases.find_one({"_id": ObjectId(case_id), "operator_id": current_user["user_id"]})
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    cursor = db.audit_entries.find({"case_id": case_id}).sort("timestamp", 1)
    entries = await cursor.to_list(length=None)
    return [serialize_doc(entry) for entry in entries]

# ============================================================================
# HISTORICAL DISRUPTIONS (READ-ONLY)
# ============================================================================

@app.get("/api/historical")
async def list_historical(current_user: dict = Depends(get_current_user)):
    cursor = db.historical.find().sort("created_at", -1).limit(20)
    entries = await cursor.to_list(length=20)
    return [serialize_doc(entry) for entry in entries]

@app.get("/api/historical/{historical_id}")
async def get_historical(historical_id: str, current_user: dict = Depends(get_current_user)):
    try:
        entry = await db.historical.find_one({"_id": ObjectId(historical_id)})
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
        case = await db.cases.find_one({"_id": ObjectId(case_id), "operator_id": current_user["user_id"]})
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        
        # Find the user being assigned
        assigned_user = await db.users.find_one({"email": assignment.owner_email})
        if not assigned_user:
            raise HTTPException(status_code=404, detail="Assigned user not found")
        
        assigned_user_id = str(assigned_user["_id"])
        previous_owner = case.get("decision_owner_email")
        now = datetime.now(timezone.utc)
        
        # Update case
        await db.cases.update_one(
            {"_id": ObjectId(case_id)},
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
        updated_case = await db.cases.find_one({"_id": ObjectId(case_id)})
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
        case = await db.cases.find_one({"_id": ObjectId(case_id), "operator_id": current_user["user_id"]})
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
            {"_id": ObjectId(case_id)},
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
        updated_case = await db.cases.find_one({"_id": ObjectId(case_id)})
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
        case = await db.cases.find_one({"_id": ObjectId(case_id), "operator_id": current_user["user_id"]})
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
            {"_id": ObjectId(case_id)},
            {"$set": {"updated_at": now}}
        )
        
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
        case = await db.cases.find_one({"_id": ObjectId(case_id), "operator_id": current_user["user_id"]})
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        
        cursor = db.timeline_events.find({"case_id": case_id}).sort("timestamp", -1)
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
        case = await db.cases.find_one({"_id": ObjectId(case_id), "operator_id": current_user["user_id"]})
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        
        # Get timeline events
        timeline_cursor = db.timeline_events.find({"case_id": case_id}).sort("timestamp", 1)
        timeline_events = await timeline_cursor.to_list(length=500)
        
        # Perform RCA
        rca_result = await rca_engine.analyze_disruption(
            serialize_doc(case),
            [serialize_doc(event) for event in timeline_events]
        )
        
        # Store RCA in case
        now = datetime.now(timezone.utc)
        await db.cases.update_one(
            {"_id": ObjectId(case_id)},
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
        case = await db.cases.find_one({"_id": ObjectId(case_id), "operator_id": current_user["user_id"]})
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        
        disruption_type = case.get("disruption_details", {}).get("disruption_type", "")
        location = case.get("disruption_details", {}).get("identifier", "")
        
        similar = await rca_engine.suggest_similar_resolutions(disruption_type, location)
        
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
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
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
        case = await db.cases.find_one({"_id": ObjectId(case_id)})
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
            {"_id": ObjectId(case_id)},
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

# Health check
@app.get("/api/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
