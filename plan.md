# Ward v0 — Disruption Lifecycle Engine Build Plan

## Strategic Vision
Transform Ward from "Decision Support at a moment" to **"Disruption Lifecycle Owner"** — a system that owns the full lifecycle of a live disruption from REPORTED to RESOLVED, with explicit per-disruption ownership and multi-source timeline tracking.

**One-Line Build Test:** _"Can I answer: Who owned this disruption, what did we know at the time, and why did we move it forward?"_

---

## Phase 1: Disruption Lifecycle Engine (Status: In Progress)

### Objectives
Build the core lifecycle management system with:
- **6-state lifecycle**: REPORTED → CLARIFIED → DECISION_REQUIRED → DECIDED → IN_PROGRESS → RESOLVED
- **Per-disruption ownership**: Assigned explicitly, reassignable with audit trail
- **Multi-source timeline tracking**: Voice/text/system events with reliability tags
- **State transitions with authority**: Only decision owner can advance states
- **Manager-first web dashboard**: Desktop-optimized, responsive for mobile
- **India-first context**: IST timezone, ports, customs vocabulary

### Key Implementation Checklist

#### Backend Implementation
- [ ] **Database Schema Updates**
  - [ ] Add `status` field to cases collection (enum: REPORTED, CLARIFIED, DECISION_REQUIRED, DECIDED, IN_PROGRESS, RESOLVED)
  - [ ] Add `decision_owner_id` field (user ID, nullable)
  - [ ] Add `decision_owner_email` field
  - [ ] Create `timeline_events` collection
    - Structure: `{case_id, actor (user/phone/system), action (message/transcript/state_change), content, source_type (voice/text/system), reliability (low/medium/high), timestamp_ist, metadata}`

- [ ] **API Endpoints - Ownership**
  - [ ] `POST /api/cases/{case_id}/assign-owner` - Assign or reassign decision owner (with audit)
    - Body: `{owner_email}`
    - Response: Updated case with new owner
    - Audit: Log reassignment with who/when

- [ ] **API Endpoints - State Transitions**
  - [ ] `POST /api/cases/{case_id}/transition` - Advance state to next valid state
    - Body: `{next_state, reason (optional)}`
    - Auth: Verify current user is decision owner
    - Response: Updated case with new state
    - Side effect: Create timeline event for state change

- [ ] **API Endpoints - Timeline**
  - [ ] `POST /api/cases/{case_id}/timeline` - Add timeline event
    - Body: `{content, source_type, reliability}`
    - Auth: Any authenticated user can add
    - Response: Created timeline event
  - [ ] `GET /api/cases/{case_id}/timeline` - Get all timeline events for case
    - Response: Array of timeline events sorted by timestamp DESC

- [ ] **API Endpoints - Updated**
  - [ ] Update `POST /api/cases` - Initialize new cases with `status: REPORTED`
  - [ ] Update `GET /api/cases` - Add query params for filtering by status, owner, source_type
  - [ ] Update `GET /api/cases/{case_id}` - Include timeline events in response

#### Frontend Implementation
- [ ] **Design System Updates**
  - [ ] Add lifecycle state color tokens to `/app/frontend/src/App.css` (from design_guidelines.md)
  - [ ] Add reliability tag tokens
  - [ ] Add source type tokens
  - [ ] Implement utility classes: `.state-badge`, `.reliability-chip`, `.source-dot`

- [ ] **Utility Functions**
  - [ ] Create `/app/frontend/src/utils/datetime.js` with IST formatting helper
    - Use `date-fns-tz` to format timestamps to IST

- [ ] **New Components**
  - [ ] `/app/frontend/src/components/DisruptionRow.js`
    - Displays: state badge, title, owner badge, last event source + reliability, location, updated time, actions
    - Props: `{disruption, onSelect, onAssign}`
    - data-testid: `disruption-row-{id}`
  
  - [ ] `/app/frontend/src/components/TimelineEvent.js`
    - Displays: source icon, timestamp (IST), reliability chip, author, content, payload
    - Props: `{event}`
    - data-testid: `timeline-event-{id}`
  
  - [ ] `/app/frontend/src/components/StateTransitionBar.js`
    - Displays: Transition buttons for valid next states (if decision owner)
    - Shows disabled message if not decision owner
    - Props: `{currentState, nextStates, canAdvance, onAdvance}`
    - data-testid: `transition-actions`, `advance-to-{state}-button`
  
  - [ ] `/app/frontend/src/components/OwnershipAssigner.js`
    - Displays: Owner Select dropdown + Assign button
    - Props: `{owners, currentOwner, onChange, onSubmit}`
    - data-testid: `ownership-assigner`, `owner-select-trigger`, `assign-owner-button`

- [ ] **Page Updates**
  - [ ] **Dashboard.js**
    - [ ] Replace simple list with table view using `./components/ui/table`
    - [ ] Add state filter tabs (using `./components/ui/tabs`) for 6 states
    - [ ] Add quick filters: owner select, source type, reliability level
    - [ ] Show state badge, owner badge, last event info per row
    - [ ] data-testid: `dashboard`, `state-tab-{state}`, `filter-owner`, `filter-source`
  
  - [ ] **CaseDetail.js** (Major Rewrite)
    - [ ] Header section:
      - [ ] Show state badge
      - [ ] Show OwnershipAssigner component
      - [ ] Show created/updated timestamps (IST)
    - [ ] Main content (grid layout: 2 cols for timeline, 1 col for sidebar on lg):
      - [ ] Timeline view (left 2 cols):
        - [ ] Map timeline events using TimelineEvent component
        - [ ] Group by day with sticky day headers
        - [ ] Use `./components/ui/scroll-area` for scrolling
      - [ ] Sidebar (right 1 col):
        - [ ] StateTransitionBar component (visible only to decision owner)
        - [ ] Properties panel (disruption details, shipment info)
        - [ ] Quick actions (add timeline note button)
    - [ ] Add timeline note form:
      - [ ] Textarea for content
      - [ ] Select for source_type (text/voice/system)
      - [ ] Select for reliability (low/medium/high)
      - [ ] Submit button
      - [ ] data-testid: `add-timeline-note-form`, `timeline-content-input`

- [ ] **Preserved Pages**
  - Landing.js - No changes
  - Login.js - No changes
  - Register.js - No changes
  - VoiceCase.js - No changes
  - AuditTrail.js - Minor update to show state changes

- [ ] **Toaster Integration**
  - [ ] Add `<Toaster />` from `./components/ui/sonner` to App.js root
  - [ ] Use `toast.success()`, `toast.error()`, `toast.info()` for:
    - State transitions
    - Owner assignments
    - Timeline additions

### Success Criteria
- [ ] User can create a disruption (automatically set to REPORTED)
- [ ] Manager can assign themselves or another user as decision owner
- [ ] Decision owner can advance state through the 6-state lifecycle with confirmation dialog
- [ ] Any user can add timeline context with source type and reliability
- [ ] Timeline displays with clear visual distinction (icons for source, chips for reliability)
- [ ] Non-owners see disabled transition buttons with tooltip: "Only the decision owner can advance the state"
- [ ] All state changes and owner assignments are logged in audit trail
- [ ] Dashboard filters disruptions by lifecycle state using tab navigation
- [ ] All timestamps display in IST with "IST" label
- [ ] UI matches design guidelines:
  - Control center aesthetic (serious, high-contrast)
  - No decorative gradients
  - Deep purposeful colors for states
  - Swiss layout discipline
  - Manager-first desktop UX, responsive for mobile

---

## Phase 2: Voice Hotline + PWA (Status: Not Started)
Voice-first ingestion via phone hotline, lightweight mobile-first PWA for field usage.

**Deferred until Phase 1 proves valuable.**

---

## Phase 3: Decision Patterns (Status: Not Started)
Suggest common alternatives and worst-cases for recurring disruption types, without being rigidly prescriptive.

**Deferred until Phase 1 proves valuable.**

---

## Phase 4: Post-Decision Learning (Status: Not Started)
"Explain the Regret" mode — capture human wisdom after RESOLVED to enrich Decision Patterns.

**Deferred until Phase 1 proves valuable.**

---

## Phase 5: WhatsApp Integration (Status: Deferred)
Bidirectional WhatsApp coordination for disruption reporting and updates.

**Explicitly deferred. Ward must earn the right to live inside WhatsApp. Product truth before distribution.**

---

## Previously Completed Work
- ✅ Initial MVP: User auth (JWT), decision construction protocol (6-step), audit trail
- ✅ AI Integration: Google Gemini for decision structuring (via Emergent LLM Key), validated in POC
- ✅ Voice Integration: Sarvam AI for multilingual STT/TTS (11+ Indian languages, tested end-to-end)
- ✅ Role-Based Architecture: Driver/Manager/Helper roles for voice interactions
- ✅ India-First Context: Ports, customs, IST timezone, INR currency
- ✅ Disruption First Hard Gate: All cases require disruption details (type, scope, identifier, time, source)
- ✅ Landing Page: Product philosophy ("Support human judgment, not automate it")
- ✅ Strategic Analysis: Deep analysis of "Disruption Lifecycle Owner" vision and implementation roadmap

---

## Tech Stack
- **Backend**: FastAPI (Python) + MongoDB + Motor (async driver)
- **Frontend**: React + Tailwind CSS + Shadcn/UI components
- **AI**: Google Gemini (via Emergent LLM Key), Sarvam AI (user-provided key for STT/TTS)
- **Auth**: JWT tokens
- **Deployment**: Kubernetes preview environment

## Key Files to Modify
- `/app/backend/server.py` - Add lifecycle endpoints, update schema logic
- `/app/frontend/src/pages/Dashboard.js` - Rewrite for table view with filters
- `/app/frontend/src/pages/CaseDetail.js` - Complete rewrite for timeline + transitions
- `/app/frontend/src/App.css` - Add design tokens from design_guidelines.md
- `/app/frontend/src/components/` - Create 4 new components (DisruptionRow, TimelineEvent, StateTransitionBar, OwnershipAssigner)

## Key Files to Preserve
- `/app/backend/ai_decision.py` - Decision structuring logic (used in DECISION_REQUIRED → DECIDED)
- `/app/backend/sarvam_service.py` - Voice service (Phase 2 integration)
- `/app/backend/voice_assistant.py` - Voice assistant logic (Phase 2)
- `/app/frontend/src/pages/Landing.js` - Product landing page
- `/app/frontend/src/pages/VoiceCase.js` - Voice capture UI (Phase 2)
- `/app/frontend/src/contexts/AuthContext.js` - Auth state management

## Design Reference
All design specifications are in `/app/design_guidelines.md`:
- Color tokens for 6 lifecycle states
- Reliability and source type styling
- Component patterns and examples
- India-first considerations (IST formatting, logistics vocabulary)
- Accessibility and testing conventions
