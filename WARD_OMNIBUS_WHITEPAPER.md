# Ward v0: The Omnibus Whitepaper
**The Complete Operating Manual & Strategic Manifesto**

---

## Table of Contents

1.  [The Ward Manifesto](#1-the-ward-manifesto)
2.  [Market Intelligence & Opportunity](#2-market-intelligence--opportunity)
3.  [Product Architecture (Deep Dive)](#3-product-architecture-deep-dive)
4.  [Technical Reference & Schemas](#4-technical-reference--schemas)
5.  [AI & Intelligence Logic](#5-ai--intelligence-logic)
6.  [User Experience & Design System](#6-user-experience--design-system)
7.  [Commercial Strategy](#7-commercial-strategy)
8.  [Future Roadmap](#8-future-roadmap)

---

## 1. The Ward Manifesto

### 1.1 The Fundamental Truth
Logistics technology has spent the last decade obsessed with **Visibility** ("Where is my truck?"). Billions were invested in GPS, IoT, and API aggregators (Project44, FourKites).

Yet, the industry still loses **$184 Billion annually** to disruptions. Why?

Because **knowing** a truck is stopped doesn't **fix** the problem. And it certainly doesn't pay the demurrage bill.

### 1.2 The Pivot: From "Tracking" to "Defense"
Ward asserts that the critical gap is not *location data*, but **Operational Evidence**.
- When a driver is stuck at a gate, the GPS says "Stopped."
- Ward says "Stopped because the guard demanded a bribe and the e-way bill server is down."

The first is a dot on a map. The second is **Defense**. It is the evidence required to stop the financial meter (Demurrage/Detention) and win the inevitable dispute.

### 1.3 The Mission
> **"To immunize supply chains against the financial cost of chaos by turning unstructured field reality into audit-grade legal evidence."**

---

## 2. Market Intelligence & Opportunity

### 2.1 The "Cost of Chaos" (TAM)
*   **Global Disruption Cost:** $184 Billion / Year (Swiss Re).
*   **Demurrage & Detention (D&D):** Estimated at $20B+ globally. In India, D&D often exceeds the cost of freight for delayed shipments.
*   **Human Capital:** 40% of a Logistics Manager's time is spent on "Coordination Calls" (non-productive work).

### 2.2 The Indian Context (SAM)
India is the perfect crucible for Ward because:
1.  **High Friction:** 14% of GDP spent on logistics (vs 8% in USA).
2.  **Fragmented:** 85% of trucking is "Unorganized" (Small fleet owners).
3.  **Language Barrier:** Drivers speak Hindi, Tamil, Gujarati. Managers speak English. ERPs speak English. **Data is lost in translation.**
4.  **Litigious Culture:** Disputes over "Who pays for the delay?" are standard business practice.

### 2.3 Competitive Landscape

| Capability | **Incumbents** (Project44, FourKites) | **Challengers** (GoComet, Shiprocket) | **Ward v0** |
| :--- | :--- | :--- | :--- |
| **Core Value** | Visibility (GPS/API) | Procurement/Rates | **Dispute Defense** |
| **Data Source** | Telematics / Carrier APIs | RFQ / Bidding Data | **Voice / Field Audio** |
| **Target User** | VP Supply Chain (HQ) | Procurement Manager | **Ops Manager / Finance** |
| **Evidence Quality** | Low (Lat/Long only) | Medium (Audit logs) | **High (Audio + Docs)** |
| **Input Method** | Passive (Sensors) | Web Portals | **Active (Voice/Whatsapp)** |

---

## 3. Product Architecture (Deep Dive)

Ward is built on four interconnected engines.

### 3.1 The Voice Capture Engine
*   **Purpose:** Bridge the literacy/language gap to capture "Ground Truth".
*   **Technology:** Sarvam AI (Speech-to-Text for Indic Languages) + Custom Translation Layer.
*   **Workflow:**
    1.  **Input:** User speaks in Hindi/Tamil/Gujarati.
    2.  **Transcription:** Converted to native script text.
    3.  **Translation:** Converted to English for the ERP.
    4.  **Extraction:** LLM extracts `Location`, `Issue_Type`, `Entities`.
    5.  **Validation:** System reads it back (TTS) for confirmation.

### 3.2 The Evidence Scoring Engine
*   **Purpose:** Quantify "Defensibility". Can we win in court?
*   **Algorithm (0-100 Score):**
    *   `+30` **Voice Report:** Verbatim testimony is the strongest evidence.
    *   `+20` **Document Proof:** Uploaded Invoice/BL/Notice.
    *   `+15` **Attribution:** Specifically naming *who* caused it (e.g., "Officer Sharma").
    *   `+15` **Counterparty:** Linking to a specific Vendor ID in Master Data.
    *   `+10` **Timestamp:** Cryptographic proof of *when* we knew.
    *   `+10` **Consistency:** RCA matches the timeline.
*   **Visual:** Red (<60%), Yellow (60-80%), Green (>80%).

### 3.3 The Responsibility Attribution Agent
*   **Purpose:** Objectivity. Removing "He said/She said".
*   **Logic:** Uses Gemini 2.5 Flash to analyze the *entire* context (Timeline + Transcript + Docs).
*   **Prompt Strategy:** "Act as an arbitrator. Based ONLY on the provided facts, who is primarily responsible? Cite the specific evidence."
*   **Output:** `Primary Party` (e.g., CHA), `Confidence` (High), `Reasoning` ("CHA admitted oversight in timestamped voice note").

### 3.4 The Dispute Bundle Service
*   **Purpose:** The "Kill Shot" for finance teams.
*   **Deliverable:** A ZIP file generated on-the-fly containing:
    1.  `audio_original.wav` (The raw truth)
    2.  `transcript_certified.txt` (The translation)
    3.  `timeline_audit.log` (The sequence of events)
    4.  `responsibility_report.pdf` (The AI verdict)
    5.  `documents/` (All attached proofs)

---

## 4. Technical Reference & Schemas

### 4.1 Core Database Schema (MongoDB)

#### `cases` Collection
```json
{
  "_id": "ObjectId",
  "status": "Enum(REPORTED, CLARIFIED, DECISION_REQUIRED, DECIDED, IN_PROGRESS, RESOLVED)",
  "description": "String (English summary)",
  "disruption_details": {
    "type": "Enum(customs, truck, port...)",
    "scope": "container/shipment",
    "identifier": "String (Container ID)",
    "source": "String (Driver Call/API)"
  },
  "financial_impact": {
    "amount": "Float",
    "currency": "INR",
    "category": "demurrage/detention",
    "daily_increase": "Float"
  },
  "evidence_score": {
    "score": "Int (0-100)",
    "breakdown": ["List of satisfied criteria"],
    "missing": ["List of missing items"]
  },
  "responsibility": {
    "primary_party": "String",
    "confidence": "High/Med/Low",
    "reasoning": "String",
    "is_override": "Boolean"
  },
  "structured_context": {
    "carrier_code": "MAEU",
    "location_code": "INNSA"
  },
  "created_at": "ISODate",
  "evidence_ready_at": "ISODate (When score crossed 70%)"
}
```

#### `timeline_events` Collection
```json
{
  "case_id": "ObjectId",
  "actor": "String (User Email or System)",
  "action": "String (CONTEXT_ADDED, STATE_CHANGE, DOC_UPLOAD)",
  "content": "String",
  "source_type": "voice/text/system",
  "reliability": "high/medium/low",
  "timestamp": "ISODate"
}
```

### 4.2 Key API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/cases` | Create new disruption case |
| `POST` | `/api/voice/transcribe` | Process audio blob -> Text |
| `POST` | `/api/cases/{id}/rca` | Trigger AI Root Cause Analysis |
| `POST` | `/api/cases/{id}/responsibility/analyze` | Trigger Liability AI |
| `GET` | `/api/cases/{id}/dispute/bundle` | Download .ZIP evidence package |
| `POST` | `/api/cases/{id}/magic-link` | Generate guest access URL |
| `GET` | `/api/analytics/dashboard` | Get TTDE and Financial metrics |

---

## 5. AI & Intelligence Logic

### 5.1 RCA Prompt Engineering
**System Instruction:**
"You are an expert logistics auditor. Analyze the following unstructured timeline and voice logs. Identify the ROOT CAUSE (not just the symptom). Suggest 3 immediate actions. Output strictly in JSON."

### 5.2 Document Comparison Logic
**Workflow:**
1.  User uploads `Invoice.pdf` and `BillOfLading.pdf`.
2.  **Gemini Vision** OCRs both documents.
3.  **Comparator Agent** extracts key fields: `HS_Code`, `Consignee`, `Weight`, `Description`.
4.  **Logic:** If `Doc1.HS_Code != Doc2.HS_Code`, flag as **High Severity Discrepancy**.
5.  **Output:** "Mismatch detected: Invoice says 8517, BL says 8518. Customs hold likely."

---

## 6. User Experience & Design System

### 6.1 Design Principles
*   **"Finance Friendly":** Dark blues, Greys, Stark Whites. No playful animations. It must look like bank software.
*   **Information Density:** Ops managers scan; they don't read. Use badges, pills, and columns.
*   **Urgency:** Red/Amber/Green indicators for status and scores.

### 6.2 Key UI Components
*   **The Gauge:** SVG-based circular progress for Evidence Score. Visual anchor of the Case Detail.
*   **The Timeline:** Vertical chronological list. Distinct icons for Voice (Mic) vs System (Server).
*   **Action Center:** Tabbed interface for "Active Coordination" (Outreach) vs "Intelligence" (Analysis).

---

## 7. Commercial Strategy

### 7.1 Pricing Philosophy
**"We don't charge for software. We charge for savings."**

### 7.2 The Pilot Offer
*   **Duration:** 30 Days.
*   **Cost:** $0.
*   **Commitment:** "If we identify >$10k in recoverable demurrage, you sign the annual contract."

### 7.3 Revenue Model
*   **Platform Fee:** $499/month (Covers server costs, AI tokens).
*   **Success Fee:** 10-20% of the *value* of successfully disputed claims (verified by the Dispute Bundle).

---

## 8. Future Roadmap

### Phase 2: The "Network" (Q2 2026)
*   **Cross-Tenant Data:** "Maersk is delayed at JNPT for 5 other customers. It's not just you."
*   **Benchmarking:** "Your detention costs are 15% higher than peer average."

### Phase 3: The "Predictor" (Q4 2026)
*   **Pre-Emptive Alerts:** "Weather warning at Mundra. Reroute to Pipavav suggested."
*   **Dynamic Insurance:** One-click insurance coverage for high-risk shipments identified by Ward.

---
*Ward AI Inc. - Internal Use Only*
