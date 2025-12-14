# Ward v0 - Master Product Document

**Version:** 1.0  
**Status:** MVP Live  
**Date:** December 13, 2025  

---

## 1. Executive Summary

**Ward** is the AI-powered **Disruption Lifecycle Layer** for modern logistics. 

While existing platforms (SAP TM, Oracle OTM, Project44) focus on *planning* and *visibility* ("Where is my shipment?"), Ward focuses on **execution** and **resolution** ("The shipment is stuck. How do I fix it?").

Ward bridges the gap between rigid ERP systems and the chaotic reality of logistics operations (voice calls, WhatsApp, paper documents) by using AI to:
1.  **Capture** unstructured data via voice/text in local languages.
2.  **Structure** it into actionable formats.
3.  **Coordinate** resolution actively with stakeholders.
4.  **Learn** from every incident to prevent recurrence.

**Target Market:** The **$184 Billion** annual loss from global supply chain disruptions, starting with the **$349 Billion** Indian logistics market.

---

## 2. The Problem

Logistics operations in emerging markets are broken at the "Last Mile of Coordination":

1.  **The Information Gap:** 90% of field intelligence (drivers, port staff) is locked in phone calls and unstructured WhatsApp chats, never reaching the TMS/ERP.
2.  **The Coordination Tax:** Operations managers spend 40% of their day on low-value follow-ups ("Where is the invoice?", "Did the truck leave?").
3.  **The "Unorganized" Barrier:** Legacy software cannot be used by the 85% of the sector that is unorganized (small fleet owners, independent CHAs) due to language and literacy barriers.
4.  **Financial Bleed:** Delays result in tangible losses—Demurrage, Detention, and Production Line stoppages—that are often accepted as "business as usual."

---

## 3. The Solution: Ward v0

Ward is not another dashboard. It is an **Active Intelligence Engine**.

### 3.1 Core Pillars

| Pillar | Feature Set | Value Prop |
| :--- | :--- | :--- |
| **Voice-First Ingestion** | • Multilingual STT (Sarvam AI)<br>• 10+ Indian Languages<br>• Zero-typing interface | Captures 100% of field data. No training required for drivers. |
| **Active Coordination** | • Autonomous AI Agents<br>• Stakeholder Identification<br>• Automated Outreach (WhatsApp/SMS) | Reduces manager workload by 70%. Fixes problems while you sleep. |
| **Deep Intelligence** | • Document Vision AI (Invoice/BL)<br>• Enhanced RCA (Root Cause Analysis)<br>• Financial Risk Tracking | Turns data into decisions. Stops the financial bleed. |
| **Platform-First** | • API/Webhooks<br>• "Magic Links" for external guests<br>• Embeddable Widgets | Zero friction adoption. Works with existing tech stacks. |

---

## 4. User Personas & User Journeys

### 🚚 **Persona A: The Driver (Ramesh)**
*   **Context:** Stuck at JNPT gate. Speaks only Hindi. No laptop.
*   **Journey:**
    1.  Opens Ward on phone (no login).
    2.  Taps Mic button.
    3.  Speaks: *"Madam, gate pe rok diya. Documents match nahi ho raha."*
    4.  Ward confirms: *"Reported. Case #123 created."*
*   **Benefit:** Zero friction reporting.

### 👔 **Persona B: The Ops Manager (Priya)**
*   **Context:** Handling 50 shipments. Overwhelmed by emails.
*   **Journey:**
    1.  Receives alert: "High Risk Disruption at JNPT."
    2.  Opens Dashboard. Sees "Financial Risk: ₹50,000 Demurrage."
    3.  Checks RCA: "Root Cause: HS Code Mismatch."
    4.  Approves AI Action Plan: "Notify CHA, Request Correction."
*   **Benefit:** From chaos to control in 2 minutes.

### 🚢 **Persona C: The CHA / Vendor (Jagdish)**
*   **Context:** Independent agent. Uses WhatsApp. Won't login to your portal.
*   **Journey:**
    1.  Receives WhatsApp/SMS with a **Magic Link**.
    2.  Clicks link -> Sees specific case details.
    3.  Uploads corrected Bill of Entry.
    4.  Done.
*   **Benefit:** No onboarding friction.

---

## 5. Technical Architecture

### **Stack: FARM (FastAPI, React, MongoDB)**

*   **Backend:** Python 3.11 + FastAPI (Async)
    *   **Orchestrator:** `CoordinationManager` manages agent workflows.
    *   **Services:** `MasterDataService`, `IntegrationService`, `AnalyticsService`.
    *   **Database:** MongoDB (Motor) for flexible schema (Documents + Relational logic).

*   **Frontend:** React 18 + Tailwind CSS + Shadcn/UI
    *   **UX Philosophy:** "Control Tower" aesthetic. High information density, low clutter.
    *   **Components:** `VoiceCase` (Audio logic), `ActiveCoordination` (Agent UI), `Analytics` (Recharts).

*   **AI Layer:**
    *   **Reasoning/RCA:** Google Gemini 2.5 Flash (via Emergent Integrations).
    *   **Voice:** Sarvam AI (Best-in-class for Indian languages).
    *   **Vision:** Gemini Vision (Document analysis).

*   **Integration Layer:**
    *   **Webhooks:** Outbound events (`case.created`, `status.changed`) for ERP sync.
    *   **API:** RESTful endpoints for custom integrations.

---

## 6. Product Roadmap

### **Phase 1: The "Fixer" (MVP - Completed)**
*   ✅ Voice Reporting (Multilingual)
*   ✅ Active Coordination Agents
*   ✅ Document Intelligence (OCR/Diff)
*   ✅ Basic Analytics & Financials

### **Phase 2: The "Predictor" (Q1 2026)**
*   🔲 **Predictive Alerts:** "Based on weather, Mundra will be congested tomorrow."
*   🔲 **Dynamic Routing:** Suggest alternative routes based on live disruption data.
*   🔲 **WhatsApp Native Bot:** Allow drivers to report directly inside WhatsApp (no web app).

### **Phase 3: The "Network" (Q3 2026)**
*   🔲 **Inter-Company Collaboration:** Shared workspaces for Shipper + Transporter + Consignee.
*   🔲 **Benchmarking:** "Your detention costs are 20% higher than industry average."

---

## 7. Go-to-Market (GTM) Strategy

**Positioning:** "The API-first Disruption Layer."

1.  **The "Wedge":** Sell to Ops Managers as a **Productivity Tool** to reduce calls/emails. Free pilot for 30 days.
2.  **The "Moat":** Once Ward captures proprietary field data (via Voice), it becomes the **System of Record** for truth, making it sticky.
3.  **The "Scale":** Sell to ERP/TMS vendors (Partnerships) to embed Ward as their "AI Module."

---

## 8. Success Metrics (KPIs)

1.  **Mean Time to Resolve (MTTR):** Target reduction > 40%.
2.  **Data Capture Rate:** % of disruptions reported via Ward vs. phone calls.
3.  **Financial Savings:** Total Demurrage/Detention saved (displayed on dashboard).
4.  **Adoption:** Daily Active Users (DAU) / Monthly Active Users (MAU).

---

## 9. Appendix: Key Assets

*   **Codebase:** `/app`
*   **Demo Script:** `/app/DEMO_SCRIPT.md`
*   **Market Analysis:** `/app/TAM_ANALYSIS.md`
*   **API Docs:** `/settings/developer` (In-app)
*   **Design System:** `/app/design_guidelines.md`

---
*Confidential Property of Ward AI Inc.*
