# Ward v0 - The AI Disruption Layer

Ward is an API-first platform that transforms how logistics companies handle disruptions. It acts as an intelligent layer between the chaotic real world (voice calls, documents, messages) and your system of record (TMS/ERP).

## 🚀 Key Features

### 1. Voice-First Ingestion
- **Multilingual Support:** Drivers speak naturally in 10+ Indian languages (Hindi, Tamil, Gujarati, etc.).
- **AI Transcription:** Powered by Sarvam AI for high-accuracy local language processing.
- **Structured Data Extraction:** Converts "container stuck at JNPT" voice notes into structured JSON.

### 2. Active Coordination
- **Autonomous Agents:** Ward identifies stakeholders (CHA, Transporter) and reaches out via WhatsApp/SMS.
- **RCA Engine:** Analyzes data from multiple sources to determine Root Cause.
- **Action Execution:** Automates follow-ups and notifications.

### 3. Document Intelligence
- **Vision AI:** Upload Invoices/Bills of Lading.
- **Discrepancy Detection:** Automatically flags mismatches (e.g., HS Code errors).

### 4. Enterprise Grade
- **Master Data:** Built-in standard codes for Indian ports (INNSA, INMUN) and carriers.
- **Financial Risk:** Tracks Detention/Demurrage costs in real-time.
- **Institutional Memory:** Suggests resolutions based on historical patterns.

## 🛠️ Developer Platform

Ward is designed to be embedded.

### Magic Links
Generate secure, temporary links for external vendors (CHAs, Truckers) to view/update cases without a login.
`POST /api/cases/{id}/magic-link`

### Webhooks
Subscribe to real-time events (`case.created`, `status.changed`) to sync data back to SAP/Oracle OTM.

## 🏗️ Architecture

- **Backend:** Python FastAPI (Async)
- **Database:** MongoDB (Motor)
- **Frontend:** React + Tailwind + Shadcn/UI
- **AI Layer:** Google Gemini (Reasoning), Sarvam AI (Voice)

## 🚦 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB

### Installation

1. **Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn server:app --reload
   ```

2. **Frontend**
   ```bash
   cd frontend
   yarn install
   yarn start
   ```

3. **Seed Data**
   ```bash
   # Generate realistic Indian logistics data
   python tests/generate_enterprise_data.py
   ```

## 📝 License
Proprietary software. Copyright 2025 Ward AI Inc.
