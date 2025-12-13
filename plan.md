# Ward v0 — Build Plan (Concise)

## 1) Objectives
- Deliver Ward v0 as a decision support tool (not planning/prediction/optimization/execution)
- Enforce fixed 6-step protocol on every decision (Framing → Known Inputs → Assumptions → Alternatives → Risk & Downside → Recommendation)
- Implement Hybrid AI-Assisted (Constrained) drafting with mandatory operator review/approval of each section
- Label evidence with source, freshness, reliability (low/medium/high), and relevance; surface unknowns explicitly
- Enforce counterfactual discipline and cognitive load limits (≤3 alternatives, worst-case first, plain language)
- Read-only context integrations only; no execution/syncing
- Simple email/password auth (JWT); full audit trail stored in MongoDB
- Backend: FastAPI; Frontend: React + shadcn/ui; DB: MongoDB; AI: Gemini 2.5 Flash via Emergent Universal LLM key

## 2) Implementation Steps (by Phase)

### Phase 1 — Core POC (Isolation): AI Decision Structuring
Goal: Prove Gemini reliably generates the 6-step structure with evidence labels, alternatives (≤3), counterfactuals, worst-case-first risks, and regret-minimizing recommendation, while refusing forbidden scopes.

User Stories (POC):
1. As a developer, I can call Gemini with a disruption description and get a 6-step draft.
2. As a developer, the draft includes known inputs with sources, freshness, reliability, and explicit unknowns.
3. As a developer, I see ≥2 and ≤3 realistic alternatives, including “do nothing/delay” when applicable.
4. As a developer, each alternative has worst-case, irreversible consequences, blast radius, failure signals.
5. As a developer, the recommendation minimizes regret and provides reversal conditions without optimizing for cost/ETA.
6. As a developer, the AI refuses planning/forecasting/network optimization or hypothetical futures.

Scope & Constraints:
- Inputs allowed: operator description, shipment IDs/routes/carriers, read-only historical disruptions (labeled)
- Forbidden: autonomous decisions, skipping steps, collapsing alternatives

Steps:
1. Integration playbook: request Gemini (text) via Emergent Universal LLM key; confirm model name and limits; note JSON-friendly prompting.
2. Secrets: fetch EMERGENT_LLM_KEY from environment (no user key needed).
3. Write single script /app/tests/test_core_ward_poc.py that:
   - Defines scenarios: (a) shipment delay at hub, (b) route closure, (c) carrier capacity failure
   - Sends prompt with strict output contract: JSON object { decision_framing, known_inputs, declared_assumptions, alternatives[], risk_and_downside[], recommendation }
   - Validates: keys present; ≤3 alternatives; each alternative has counterfactuals; evidence labels exist; worst-case first; recommendation has reversal conditions; refusal behavior on prohibited prompt
4. Run script; iterate prompts until all validations pass (Fix Until It Works). Persist final prompt.
5. Document POC result (structure examples) and finalize prompt template for backend use.

Deliverables:
- Proven prompt + working Gemini call
- Validated structured JSON that satisfies all checks

### Phase 1 — Core POC (Isolation): AI Decision Structuring ✅ COMPLETED
All 4 POC tests passed successfully. Gemini reliably generates 6-step decision structures with evidence labeling, 2-3 alternatives, and proper guardrails.

### Phase 2 — Full Application Development ✅ COMPLETED
All user stories implemented and tested. 100% test pass rate.

### Phase 3 — Critical Causal Locks Implementation ✅ COMPLETED

### Phase 4 — Voice-First Integration with Sarvam AI ✅ COMPLETED

**1. INDIA CONTEXT LOCK (Always On):**
- AI system prompt updated to assume India by default
- Indian ports: JNPT, Mundra, Chennai, Vizag, Kolkata
- Indian customs: CHA (Customs House Agent), documentation holds
- Indian realities: monsoon delays, strikes, congestion, manual processes
- Communication: phone calls, WhatsApp, broker updates
- Formats: IST timezone, DD/MM/YYYY dates, INR currency
- POC tests updated with Indian scenarios (customs hold at JNPT, monsoon blockage, truck breakdown)

**2. DISRUPTION FIRST HARD GATE:**
- Backend models updated: DisruptionDetails now mandatory (type, scope, identifier, time_discovered_ist, source)
- Backend validation: Cases without disruption details rejected with 422 error
- Frontend form updated: Mandatory disruption fields with dropdown for types (customs_hold, port_congestion, truck_breakdown, monsoon, CHA_delay, etc.)
- AI prompt enhanced: Disruption context passed explicitly to Gemini
- Validation confirmed: Test attempting to create case without disruption details properly rejected

**Testing Results:**
- Backend: 27/27 tests passed (100%)
- Frontend: 95% (all forms functional, disruption fields present)
- AI Integration: 4/4 POC tests passed with India-specific scenarios
- DISRUPTION FIRST gate validated: Properly rejects cases without required fields
- India context verified: AI responses include JNPT, CHA, Mumbai, INR, IST references
Goal: Complete app with auth, AI-assisted structuring, section approvals, override tracking, and audit trail.

Backend (FastAPI) — Endpoints (all under /api):
- Auth: POST /auth/register, POST /auth/login (JWT), GET /auth/me
- Cases: POST /cases (create with description, shipment IDs/routes/carrier), GET /cases, GET /cases/{id}
- AI Draft: POST /cases/{id}/ai_draft (calls Gemini with POC prompt; stores draft)
- Sections: PATCH /cases/{id}/sections/{sectionKey} (edit), POST /cases/{id}/sections/{sectionKey}/approve (lock)
- Finalize: POST /cases/{id}/finalize (select alternative; require override rationale if not AI recommendation)
- Audit: GET /audit (list); GET /cases/{id}/audit (detail)
- Historical: GET /historical (read-only list), GET /historical/{id}

Backend Data Model (MongoDB):
- users: { email, password_hash, created_at }
- cases: { operator_id, description, shipment_identifiers{ids,routes,carriers}, status, created_at }
- drafts: { case_id, decision_framing, known_inputs{facts,unknowns,evidence[]}, declared_assumptions[], alternatives[max3], risk_and_downside[by alt], recommendation{choice, rationale, reversal_signals}, ai_model, ai_prompt, created_at }
- approvals: { case_id, section_key, approved_by, approved_at, content_snapshot }
- decisions: { case_id, final_choice, override{exists, rationale}, decided_by, decided_at }
- audit_entries: { case_id, actor, action, payload, ts }
- historical: { title, summary, labels, content, created_at } (read-only seed)

Backend Rules/Guards:
- Enforce ≤3 alternatives; reject more
- Serialize datetime/ObjectId safely; consistent evidence labeling schema
- Guardrails: refuse requests violating scope; return 400 with reason
- Use environment variables (MONGO_URL); bind 0.0.0.0:8001

Frontend (React + shadcn/ui):
- Auth pages: Login/Register (simple, reliable)
- Dashboard: list active cases and recent decisions
- New Case: form for description + shipment IDs/routes/carriers, option to reference historical
- Case Detail: 6-step view/editor with:
  - “Generate Decision Structure” (shows loading)
  - Section editors (textareas) with approve/lock per section
  - Alternatives card list (≤3) with worst-case-first risk display
  - Final decision chooser (radio); override rationale prompt if not AI recommendation
  - Evidence labels displayed inline
- Audit Trail: chronological view with filters
- Historical: read-only viewer; link to reference in a case
- All interactive elements include data-testid

Frontend States & UX:
- Clear loading/error/empty states; non-transparent backgrounds; plain operational language
- Warning/alert styling for risks; lock icons for approved sections

Build/Dev Steps:
1. After POC, call design_agent for UI guidelines; install any UI deps
2. Implement backend + frontend in parallel using bulk_file_writer; ensure route/contract match
3. Add JWT auth middleware; protect case operations
4. Validate AI output server-side (schema + constraints) before persisting
5. Test images/files: N/A in v0; ensure all text flows work
6. Logs sanity check; fix until clean

Testing (end of Phase 2):
- Use testing_agent_v3 for end-to-end on all Phase 1 & 2 user stories (skip drag/drop/camera)
- Lint Python/JS; verify no import/runtime errors

User Stories (Phase 2 — at least 10):
1. As an operator, I can register and login to get a JWT.
2. As an operator, I can create a new disruption case with description and shipment details.
3. As an operator, I can trigger AI to draft the 6-step structure and see a working indicator.
4. As an operator, I can edit and approve each section individually and see locked state.
5. As an operator, I can view ≤3 alternatives with worst-case-first risks.
6. As an operator, I can choose a final decision via radio buttons.
7. As an operator, I must provide override rationale if my choice differs from AI recommendation.
8. As an operator, I can view a complete audit trail of actions on a case.
9. As an operator, I can browse historical disruptions (read-only) and reference them in a case.
10. As an operator, I see evidence labels and explicit unknowns in the UI.

## 3) Next Actions (Immediate)
1. Request Gemini integration playbook (text gen) via Emergent Universal LLM key; confirm model identifier and SDK usage.
2. Implement Phase 1 single test script with 3 scenarios + guardrail test; iterate prompt until all assertions pass.
3. After POC success, call design_agent; then scaffold backend and frontend in parallel (bulk_file_writer) following this plan.
4. Run end-to-end tests with testing_agent_v3; fix all reported issues (high → low); re-run until green.

## 4) Success Criteria
- Phase 1: Single script produces valid structured JSON for all 3 scenarios; guardrail refusal works; ≤3 alternatives; evidence labels present; recommendation includes reversal conditions; zero unhandled exceptions.
- Phase 2: 
  - Auth works; protected endpoints enforce JWT
  - AI drafting endpoint returns validated structure; UI displays and allows edits/approvals
  - Finalization enforces override rationale when needed; audit entries complete and queryable
  - Historical data readable and clearly labeled
  - All backend routes prefixed with /api; no hardcoded envs; server bound to 0.0.0.0:8001
  - All interactive UI elements have data-testid; clear loading/error states; no red screens
  - Testing agent passes all user stories from Phases 1 & 2; fixed regressions
- Global: Adheres to product identity and hard rules; uncertainty surfaced; regrets-minimizing logic (not cost/ETA optimization); weak evidence clearly labeled.
