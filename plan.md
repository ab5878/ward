# Ward v0 — Disruption Lifecycle Engine Build Plan

## Strategic Vision
Transform Ward from "Decision Support at a moment" to **"Disruption Lifecycle Owner"** — a system that owns the full lifecycle of a live disruption from REPORTED to RESOLVED, with explicit per-disruption ownership and multi-source timeline tracking.

**One-Line Build Test:** _"Can I answer: Who owned this disruption, what did we know at the time, and why did we move it forward?"_

---

## Phase 1: Disruption Lifecycle Engine (COMPLETED)
- ✅ 6-state lifecycle: REPORTED → CLARIFIED → DECISION_REQUIRED → DECIDED → IN_PROGRESS → RESOLVED
- ✅ Per-disruption ownership: Assigned explicitly, reassignable with audit trail
- ✅ Multi-source timeline tracking
- ✅ State transitions with authority
- ✅ Manager-first web dashboard
- ✅ India-first context

## Phase 2: Voice & Multilingual (COMPLETED)
- ✅ Sarvam AI integration for STT/TTS
- ✅ Multilingual support (Hindi, Tamil, etc.)
- ✅ Voice-first case reporting interface

## Phase 3: Active Coordination (COMPLETED - READY FOR DEMO)
- ✅ **AI Agent Architecture**: `CoordinationManager` orchestrating 5 specialized agents.
- ✅ **Stakeholder Identification**: Logic to identify CHA, Shipping Line, Port Ops based on disruption type.
- ✅ **Outreach Simulation**: Backend capability to "send" messages (mocked) and track status.
- ✅ **Enhanced RCA**: AI Agent that synthesizes data from initial reports + stakeholder responses.
- ✅ **Action Plan Execution**: Agent to execute approved plans (notify, remind).
- ✅ **Demo Tools**: "Simulate Response" UI built for the upcoming demo.

## Phase 4: Production Hardening (UPCOMING)
- [ ] Real WhatsApp Business API integration
- [ ] Role-based access control (RBAC) fine-tuning
- [ ] Analytics Dashboard (`/dashboard/analytics`)
- [ ] Post-Decision Learning ("Explain the Regret")

---

## Technical Architecture
- **Backend**: FastAPI (Python) + MongoDB + Motor
- **Frontend**: React + Tailwind CSS + Shadcn/UI
- **AI Agents**:
  - `StakeholderIdentifierAgent`: Who to call?
  - `OutreachAgent`: Sends messages (WhatsApp/SMS/API)
  - `ResponseCollectorAgent`: Gathers replies
  - `EnhancedRCAAgent`: Analyzes combined data (Gemini)
  - `ActionExecutorAgent`: Executes the fix
- **AI Services**: Google Gemini (Intelligence), Sarvam AI (Voice)

## Credentials
- **Emergent LLM Key**: Configured in `.env`
- **Sarvam AI Key**: User provided
