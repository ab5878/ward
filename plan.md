# Ward v0 — Disruption Lifecycle Engine Build Plan

## Strategic Vision
Transform Ward from "Decision Support at a moment" to **"Disruption Lifecycle Owner"** — a system that owns the full lifecycle of a live disruption from REPORTED to RESOLVED.

---

## Phase 1: Disruption Lifecycle Engine (COMPLETED)
- ✅ 6-state lifecycle & ownership
- ✅ Multi-source timeline & audit trail
- ✅ Manager-first dashboard

## Phase 2: Voice & Multilingual (COMPLETED)
- ✅ Sarvam AI integration (STT/TTS)
- ✅ Multilingual support

## Phase 3: Active Coordination (COMPLETED)
- ✅ AI Agent Architecture (`CoordinationManager`)
- ✅ Stakeholder Identification & Outreach Simulation
- ✅ Enhanced RCA & Action Execution
- ✅ Demo Tools ("Simulate Response")

## Phase 4: Product Depth (CURRENT FOCUS)
**Goal:** Deepen the product functionality to "Real World" standards.

### 4.1. AI Document Intelligence (The "Proof" Layer) - **IN PROGRESS**
- [ ] **Document Processor Service:** Use Gemini Vision to OCR and analyze PDFs/Images.
- [ ] **Comparison Logic:** Auto-detect discrepancies (e.g., Invoice vs Bill of Lading).
- [ ] **UI Integration:** File upload in Case Detail + "Discrepancy Alert".

### 4.2. Institutional Memory (The "Learning" Layer)
- [ ] **Similarity Engine:** Find historical cases with matching embedding/tags.
- [ ] **Resolution Recommender:** "Last time this happened, we did X."

### 4.3. Real World Comms (The "Integration" Layer)
- [ ] **Twilio Integration:** Real SMS for "Urgent" alerts.
- [ ] **SendGrid Integration:** Email summaries for stakeholders.

### 4.4. Strategic Analytics (The "Value" Layer)
- [ ] **Analytics Dashboard:** Time to Resolve, Vendor Scorecards.
- [ ] **Export Reports:** PDF/CSV download for management.

---

## Technical Architecture
- **Backend**: FastAPI + MongoDB
- **AI**: Gemini (Text & Vision), Sarvam (Voice)
- **Integrations**: Twilio (SMS), SendGrid (Email)
