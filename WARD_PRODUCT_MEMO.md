# Ward v0 - Product Memo: The Demurrage Defense Platform

**Date:** December 13, 2025  
**Version:** 2.0 (Post-Pivot)  
**Status:** Live MVP  

---

## 1. The Core Thesis
**Logistics companies don't need another dashboard to *see* delays. They need a weapon to *fight* the costs caused by delays.**

Every time a shipment stops, a financial meter starts running (Demurrage/Detention). The industry loses **$184 Billion/year** to these inefficiencies. The problem isn't lack of GPS tracking; it's lack of **defensible evidence** to dispute the charges.

**Ward's One Job:**
> "When something goes wrong in transit, give you proof fast enough to stop the meter and strong enough to win disputes."

---

## 2. Product Architecture (The "Evidence Engine")

Ward operates as an intelligent evidence layer that sits on top of existing ERPs.

### **A. Voice-First Capture (The "Ground Truth")**
*   **Problem:** Drivers and field agents don't type. They call. Critical context ("Gate closed", "Official absent") is lost in the air.
*   **Solution:** Ward provides a **Voice Interface** supporting **10+ Indian languages**.
*   **Tech:** Sarvam AI (STT) + Translation Engine.
*   **Output:** Verbatim transcript + structured JSON (Time, Location, Reason).

### **B. Evidence Completeness Score (The "Audit")**
*   **Problem:** Ops managers don't know if they have enough proof to win a claim until it's too late.
*   **Solution:** A real-time **0-100% Score** on every case file.
*   **Factors:**
    *   Voice Recording (+30)
    *   Timestamped Transcript (+10)
    *   Attributed Speaker (+15)
    *   Uploaded Documents (+20)
    *   Identified Counterparty (+15)
*   **UX:** A visual gauge that turns Green only when the file is "Audit-Grade."

### **C. Responsibility Attribution (The "Judge")**
*   **Problem:** Everyone blames everyone else. "It was the CHA." "No, it was the Transporter."
*   **Solution:** AI (Gemini) analyzes the timeline, transcripts, and docs to assign a **Primary Responsible Party**.
*   **Output:** "Responsible: CHA (High Confidence). Reason: Admitted to late filing in voice note at 10:30 AM."

### **D. The Dispute Bundle (The "Weapon")**
*   **Problem:** Gathering evidence for a claim takes hours of digging through emails.
*   **Solution:** A **One-Click Export** button.
*   **Deliverable:** A ZIP file containing:
    1.  Original Audio File (The smoking gun).
    2.  Certified Transcript.
    3.  Responsibility Report.
    4.  Timeline Log.
    5.  Extracted Document Data.

---

## 3. Strategic Analytics

We don't track "Shipment Volume." We track "Defense Performance."

*   **Primary Metric:** **Average Time to Defensible Evidence (TTDE)**.
    *   *Definition:* How many minutes from the first report until the file hits 70% completeness?
    *   *Target:* < 60 Minutes.
*   **Secondary Metrics:**
    *   Total Demurrage Risk Exposure (in ₹).
    *   Resolution Rate (Win Rate).

---

## 4. Platform Strategy ("Plug & Play")

Ward is designed to be adopted without IT friction.

*   **No Login Required (Magic Links):** External vendors (CHAs) get a secure, temporary link to upload documents or give statements. They never create an account.
*   **API-First:** Everything Ward does is accessible via REST API. Large shippers can embed Ward's voice recorder directly into their own driver apps.
*   **Webhooks:** Ward pushes `evidence.ready` events back to SAP/Oracle OTM.

---

## 5. Pricing Model

**Philosophy:** "We succeed when you save money."

1.  **30-Day Pilot:** Free. We prove we can save you demurrage costs, or you walk away.
2.  **Standard:** Low monthly platform fee + **Success Share** (% of recovered/saved charges).

---

## 6. Current Status & Assets

*   **Live App:** Dashboard, Voice Recorder, Evidence Scoring, Dispute Export.
*   **Market Positioning:** Validated against "Visibility" competitors (Project44) who lack "Resolution" capabilities.
*   **Tech Stack:** Python (FastAPI), React (Shadcn), MongoDB, Gemini/Sarvam AI.

---
*Ward AI Inc. Confidential*
