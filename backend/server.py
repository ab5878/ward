from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
import jwt
import bcrypt
from dotenv import load_dotenv
import asyncio
from contextlib import asynccontextmanager

# Import AI module
from ai_decision import generate_decision_structure

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
    global client, db
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    print(f"Connected to MongoDB: {DB_NAME}")
    
    # Create indexes
    await db.users.create_index("email", unique=True)
    await db.cases.create_index("created_at")
    await db.audit_entries.create_index("case_id")
    
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

class CreateCase(BaseModel):
    description: str = Field(min_length=10)
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
    case = {
        "operator_id": current_user["user_id"],
        "operator_email": current_user["email"],
        "description": case_data.description,
        "shipment_identifiers": case_data.shipment_identifiers.dict(),
        "status": "draft",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await db.cases.insert_one(case)
    case_id = str(result.inserted_id)
    
    await log_audit(case_id, current_user["email"], "CASE_CREATED", {"description": case_data.description})
    
    case["_id"] = result.inserted_id
    return serialize_doc(case)

@app.get("/api/cases")
async def list_cases(current_user: dict = Depends(get_current_user)):
    cursor = db.cases.find({"operator_id": current_user["user_id"]}).sort("created_at", -1).limit(50)
    cases = await cursor.to_list(length=50)
    return [serialize_doc(case) for case in cases]

@app.get("/api/cases/{case_id}")
async def get_case(case_id: str, current_user: dict = Depends(get_current_user)):
    try:
        case = await db.cases.find_one({"_id": ObjectId(case_id), "operator_id": current_user["user_id"]})
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        
        # Get draft if exists
        draft = await db.drafts.find_one({"case_id": case_id})
        
        # Get approvals
        approvals_cursor = db.approvals.find({"case_id": case_id})
        approvals = await approvals_cursor.to_list(length=100)
        
        # Get decision if exists
        decision = await db.decisions.find_one({"case_id": case_id})
        
        return serialize_doc({
            "case": case,
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

@app.get("/api/historical/{historical_id}", data-testid="get-historical-endpoint")
async def get_historical(historical_id: str, current_user: dict = Depends(get_current_user)):
    try:
        entry = await db.historical.find_one({"_id": ObjectId(historical_id)})
        if not entry:
            raise HTTPException(status_code=404, detail="Historical entry not found")
        return serialize_doc(entry)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Health check
@app.get("/api/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
