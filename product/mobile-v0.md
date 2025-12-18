# Ward Mobile v0 PRD: Incident Capture for Indian Freight

**Version:** 1.0  
**Date:** December 2024  
**Status:** Ready for Engineering  
**Target Launch:** Q1 2025

---

## 1. Context & Problem

### The WhatsApp Baseline

In Indian freight operations, when something goes wrong—a container stuck at port gate, CFS yard full, dock not ready, documents issue, no labour, system down—the first response is a WhatsApp voice note. It's fast, familiar, and requires zero training. Drivers and yard staff send voice notes. Dispatchers forward screenshots. Finance teams dig through chat histories when invoices arrive.

**WhatsApp performance baseline:**
- Time to send voice note: ~3-5 seconds (open app → tap mic → speak → send)
- Works on low-end Android devices
- Works offline (queues message, sends when network available)
- Zero training required
- Familiar to all users

### The Problem

WhatsApp screenshots don't hold up in disputes. Port authorities, courts, and custodians need provable, time-stamped evidence. When money and blame are on the line, "I sent a WhatsApp" isn't enough.

**Indian freight context:**
- Major ports (JNPT, Mundra, Chennai) are in global top tier for daily D&D charges
- Tariffs escalate quickly after short free-time windows
- Indian courts routinely uphold port and custodian rights to levy demurrage even when customs or agencies caused delay
- Importers and intermediaries eat the bill unless they can show concrete, time-stamped proof

**Current state:**
- Real "system of record" is WhatsApp, calls, and scattered PDFs across port desks, CHAs, transporters, and warehouses
- Disputes die in internal triage because reconstructing credible packets is slow, political, and demoralizing
- Many invoices are simply paid
- Internal blame games: "we don't know who to blame" escalations

### The Opportunity

Ward v0 is deliberately narrow and brutal: imports, ports/ICDs/CFS/logistics parks, demurrage/detention + waiting. We make evidence exist in a provable form that survives disputes.

---

## 2. Goals & Success Metrics

### Primary Goal

Convert more "we'll just pay it" invoices (ports, ICDs, CFSs, warehouses/logistics parks) into structured disputes that sometimes win—and always stop internal blame games.

### Success Metrics

**Quantitative metrics (measured after 3-6 months):**

1. **Time-to-log vs WhatsApp**
   - Target: ≤ 5 seconds from "something goes wrong" to "incident logged in Ward"
   - Baseline: WhatsApp voice note takes ~3-5 seconds
   - Measurement: Average time from app open to incident confirmed logged
   - Hard requirement: Must match or beat WhatsApp baseline

2. **Uplift in % invoices contested**
   - Target: 3-5x increase vs historical baseline (per port/facility/lane)
   - Baseline: Typically 10-15% of invoices are contested
   - Measurement: % of invoices with Ward logs that are contested vs % without

3. **Uplift in waivers/discounts**
   - Target: 5-10x increase vs historical baseline
   - Baseline: Typically 2-5% of contested invoices result in waivers
   - Measurement: % of contested invoices that result in waiver/discount

4. **Reduction in internal time per dispute**
   - Target: 40-50% reduction in time spent by ops/finance/legal per dispute
   - Baseline: Typically 4-8 hours per dispute (gathering evidence, assembling packet)
   - Measurement: Time from invoice receipt to dispute packet ready

5. **Drop in "we don't know who to blame" escalations**
   - Target: 60-80% reduction
   - Measurement: Count of internal escalations where delay attribution is unclear

**Behavioral metrics:**

1. **Adoption rate**
   - Target: 70%+ of drivers/yard staff use Ward for incidents within 30 days
   - Measurement: % of incidents logged in Ward vs total incidents (tracked via WhatsApp/phone call volume)

2. **Offline resilience**
   - Target: 95%+ of incidents captured successfully even in poor network conditions
   - Measurement: % of incidents that sync successfully after offline capture

3. **Data quality**
   - Target: 90%+ of incidents have GPS, device ID, timestamp, and voice recording
   - Measurement: % of incidents with all required metadata

---

## 3. User Personas

### Persona 1: Driver (Port/ICD/CFS)

**Profile:**
- Age: 25-45
- Device: Low-end Android (₹8,000-15,000 range)
- Network: Intermittent 3G/4G, often poor at port gates and yards
- Language: Hindi/regional language primary, basic English
- Tech comfort: Low-medium (uses WhatsApp, phone calls, basic apps)
- Context: On the move, often stressed, needs to log quickly and get back to work

**Pain points:**
- Stuck at port gate, CFS yard full, waiting for documents
- Needs to report quickly but network is poor
- Can't type well, prefers voice
- Worried about being blamed for delays

**Goals:**
- Log incident in one tap
- Know it was recorded even if network is down
- See confirmation immediately

**Usage pattern:**
- 2-5 incidents per day
- Usually in vehicle or at gate/yard
- Needs to log and move on quickly

### Persona 2: Yard Staff / Gate Guard (CFS/Warehouse)

**Profile:**
- Age: 30-50
- Device: Low-end Android (shared or personal)
- Network: Variable (better than drivers, but still poor in yards)
- Language: Hindi/regional language primary, some English
- Tech comfort: Low-medium
- Context: Stationary but busy, managing multiple trucks/containers

**Pain points:**
- Yard full, dock not ready, no labour available
- Multiple incidents happening simultaneously
- Needs to log quickly without disrupting operations
- Often coordinating via phone while logging

**Goals:**
- Log incident without stopping work
- Link to specific container/truck quickly
- See what's been logged today

**Usage pattern:**
- 5-15 incidents per day
- Usually at fixed location (gate, yard office)
- May need to log multiple incidents in sequence

### Persona 3: Yard Supervisor / Dispatcher

**Profile:**
- Age: 30-45
- Device: Mid-range Android (₹15,000-25,000)
- Network: Better connectivity (office/yard office)
- Language: Hindi + English
- Tech comfort: Medium-high
- Context: Coordinating multiple drivers/vehicles, needs visibility

**Pain points:**
- Needs to see what drivers/yard staff have logged
- May need to add context or link incidents
- Coordinating with multiple parties (port, CHA, warehouse)
- Needs to export timeline for disputes

**Goals:**
- View timeline of incidents for a movement
- Add context or link incidents
- Export dispute packet
- See which incidents were logged in real-time vs reconstructed

**Usage pattern:**
- 10-30 incidents to review per day
- Mix of viewing and adding context
- May need to export 2-5 dispute packets per day

### Persona 4: Warehouse Gate Operator

**Profile:**
- Age: 25-40
- Device: Low-end Android (shared device common)
- Network: Variable (warehouse gates often have weak signal)
- Language: Hindi/regional language
- Tech comfort: Low
- Context: Managing truck entry/exit, loading/unloading

**Pain points:**
- Dock not ready, loading delays, documents issue
- Needs to log quickly while managing gate operations
- Often using shared device
- Network poor at gate location

**Goals:**
- Log incident in one tap
- Works on shared device
- See confirmation even offline

**Usage pattern:**
- 3-10 incidents per day
- Usually at gate or dock
- Needs to log and continue operations

---

## 4. Detailed Feature Requirements

### 4.1 Incident Capture Flow

#### 4.1.1 Primary Capture Flow (Driver/Yard Staff/Gate Operator)

**Trigger:** User opens Ward app and taps "Log Incident" button (or shortcut from home screen)

**Step 1: App Launch & Quick Capture**
- **Requirement:** App must open in < 2 seconds on low-end Android
- **Requirement:** "Log Incident" button must be visible immediately (no loading screen)
- **Requirement:** Button must be large enough for easy tap (minimum 48x48dp)
- **Requirement:** Button must work even if network is unavailable

**Step 2: Voice Recording**
- **Action:** User taps "Log Incident" → immediately starts voice recording
- **Requirement:** No confirmation dialog, no permission request (permissions granted on first app launch)
- **Requirement:** Visual feedback: large red recording button, timer showing duration
- **Requirement:** User can stop recording by tapping again (minimum 1 second, maximum 60 seconds)
- **Requirement:** Recording must work offline (saved locally first)

**Step 3: Auto-Attach Metadata**
- **Requirement:** Automatically attach (no user input required):
  - GPS location (lat/long, accuracy)
  - Device ID (Android ID or device fingerprint)
  - Timestamp (system time at moment of capture, UTC)
  - Actor (user account/phone number)
  - Network status (online/offline at time of capture)
- **Requirement:** If GPS unavailable, use last known location (cached)
- **Requirement:** If GPS accuracy > 100m, show warning but still save

**Step 4: Basic Context Selection (Minimal Taps)**
- **Requirement:** After recording stops, show context selection screen
- **Requirement:** Maximum 2-3 taps to complete context
- **Options (single selection, large buttons):**
  - Incident type (pre-filled based on location if possible):
    - "Stuck at port gate"
    - "CFS yard full"
    - "Dock not ready"
    - "Documents issue"
    - "No labour"
    - "System down"
    - "Other" (voice note explains)
  - Container/Truck ID (optional, can skip):
    - Voice input for container/truck number
    - Or skip (can link later)
  - Facility (auto-detected from GPS if possible, else manual):
    - Port/ICD/CFS/Warehouse name
    - Large buttons, pre-populated if GPS matches known facility

**Step 5: Confirmation & Save**
- **Requirement:** Show confirmation immediately (even if offline)
- **Requirement:** Confirmation shows:
  - "Incident logged" message
  - Timestamp
  - Location (facility name)
  - Sync status (synced / will sync when online)
- **Requirement:** User can tap "Done" and return to home screen
- **Requirement:** No "loading" spinner during save (happens in background)

**Total time target:** ≤ 5 seconds from app open to confirmation

#### 4.1.2 Offline Behavior

**Requirement:** All incident capture must work completely offline

**Local Storage:**
- **Requirement:** Incidents saved to local SQLite database immediately
- **Requirement:** Voice recordings saved to local storage (compressed format)
- **Requirement:** GPS, timestamps, metadata all stored locally
- **Requirement:** No network call required for capture

**Sync Behavior:**
- **Requirement:** Background sync when network available
- **Requirement:** Sync happens automatically (no user action required)
- **Requirement:** Sync status visible in app (number of pending incidents)
- **Requirement:** Failed syncs retry automatically (exponential backoff)
- **Requirement:** User can manually trigger sync (pull to refresh)

**Conflict Resolution:**
- **Requirement:** If same incident logged multiple times (network issue), merge on server
- **Requirement:** Server assigns unique ID, client updates local record
- **Requirement:** No data loss if sync fails (retry until success)

#### 4.1.3 Minimal Tagging & Selection Patterns

**Principle:** Everything else (structure, tagging, linkage) is invisible. Only capture is visible.

**Container/Truck ID Linking:**
- **Requirement:** Optional during capture (can skip)
- **Requirement:** Can link later via timeline view
- **Requirement:** Voice input for ID (speech-to-text)
- **Requirement:** Or manual entry (but voice preferred)

**Facility Selection:**
- **Requirement:** Auto-detect from GPS if possible (match against known facilities)
- **Requirement:** If match found, pre-select (user can change)
- **Requirement:** If no match, show list of nearby facilities (sorted by distance)
- **Requirement:** Large buttons, facility names in local language + English

**Incident Type:**
- **Requirement:** Pre-populated list (7 common types + "Other")
- **Requirement:** Large buttons, icons + text
- **Requirement:** Can skip (defaults to "Other" if voice note explains)

**Parties (Shipper, Forwarder, CHA, etc.):**
- **Requirement:** NOT required during capture (too many taps)
- **Requirement:** Auto-linked based on user account/context
- **Requirement:** Can be added later by supervisor/dispatcher

#### 4.1.4 Local Timeline View

**Requirement:** Front-line users can see incidents they've logged today

**Timeline Screen:**
- **Requirement:** Simple list view (chronological, newest first)
- **Requirement:** Each incident shows:
  - Time (local time, "2 hours ago" format)
  - Facility name
  - Incident type (icon + text)
  - Status (synced / pending sync)
- **Requirement:** Tap to view details:
  - Full timestamp (captured at)
  - GPS location (map view)
  - Voice recording (play button)
  - Container/truck ID (if linked)
  - Edit option (adds new event, doesn't delete original)

**Filtering:**
- **Requirement:** Filter by facility (if logged multiple facilities)
- **Requirement:** Filter by sync status (synced / pending)
- **Requirement:** Search by container/truck ID (if linked)

**Export (Supervisor/Dispatcher only):**
- **Requirement:** Export timeline for a movement (all incidents linked to container/truck)
- **Requirement:** Export as PDF (formatted for dispute packet)
- **Requirement:** Export includes: timeline, GPS, timestamps, voice recordings (links)

---

## 5. UX & Technical Constraints

### 5.1 Device & Platform Constraints

**Android-First:**
- **Requirement:** Android only for v0 (iOS later)
- **Requirement:** Minimum Android version: 7.0 (API 24)
- **Requirement:** Target: Android 8.0+ (API 26+) for best experience
- **Requirement:** Test on low-end devices (2GB RAM, quad-core processor)

**Low-End Device Optimization:**
- **Requirement:** App size < 50MB (download)
- **Requirement:** RAM usage < 150MB
- **Requirement:** Battery efficient (background sync only when charging or WiFi)
- **Requirement:** No heavy animations or transitions
- **Requirement:** Offline-first architecture (minimal network calls)

### 5.2 Network Constraints

**Intermittent 3G/4G:**
- **Requirement:** All core features work offline
- **Requirement:** Graceful degradation when network unavailable
- **Requirement:** No "loading" spinners during capture
- **Requirement:** Background sync with retry logic
- **Requirement:** Show sync status clearly (don't hide failures)

**Poor Connectivity Handling:**
- **Requirement:** Aggressive local caching
- **Requirement:** Compress voice recordings before upload
- **Requirement:** Batch sync (multiple incidents in one request)
- **Requirement:** Resume interrupted uploads

### 5.3 Language Considerations

**Voice Input:**
- **Requirement:** Support Hindi and major regional languages (Tamil, Telugu, Marathi, Gujarati, Bengali)
- **Requirement:** Speech-to-text for container/truck IDs (even if in English)
- **Requirement:** Voice recordings preserved as-is (no translation required)

**UI Language:**
- **Requirement:** English + Hindi UI (user can switch)
- **Requirement:** Facility names in local language + English
- **Requirement:** Incident types in local language + English
- **Requirement:** Error messages in local language

**Text Input:**
- **Requirement:** Zero mandatory text input
- **Requirement:** Optional text input supports local language keyboards
- **Requirement:** Voice input preferred over typing

### 5.4 UX Principles

**Voice-First & Tap-First:**
- **Requirement:** Zero mandatory typing
- **Requirement:** All actions via tap or voice
- **Requirement:** Large touch targets (minimum 48x48dp)
- **Requirement:** Clear visual feedback for all actions

**Habit Formation:**
- **Requirement:** Less annoying than WhatsApp
- **Requirement:** More protective than WhatsApp (tamper-evident proof)
- **Requirement:** Familiar patterns (similar to WhatsApp voice note)
- **Requirement:** Immediate confirmation (no waiting)

**No Loading Spinners:**
- **Requirement:** All capture happens instantly (saved locally)
- **Requirement:** Sync happens in background (no blocking UI)
- **Requirement:** Show sync status, but don't block user

---

## 6. Data & Integrity Rules

### 6.1 Time-Stamping

**System Time-Stamp:**
- **Requirement:** Every incident must have system timestamp (UTC) at moment of capture
- **Requirement:** Timestamp cannot be modified by user
- **Requirement:** Timestamp stored with millisecond precision
- **Requirement:** Display in local timezone, but store in UTC

**"Captured At" vs "Edited At":**
- **Requirement:** Original capture timestamp always preserved
- **Requirement:** If incident edited, new event created with "edited at" timestamp
- **Requirement:** Original event never deleted or modified
- **Requirement:** UI shows both timestamps prominently

**Time Validation:**
- **Requirement:** Validate system time (detect if device time is wrong)
- **Requirement:** If device time off by > 5 minutes, show warning but still save
- **Requirement:** Server can correct timestamp based on server time (but preserve original)

### 6.2 Device Binding

**Device ID:**
- **Requirement:** Every incident bound to device ID (Android ID or device fingerprint)
- **Requirement:** Device ID cannot be spoofed or modified
- **Requirement:** Device ID stored with incident (for audit trail)

**User Account:**
- **Requirement:** Every incident bound to user account (phone number or email)
- **Requirement:** User account verified (SMS OTP or email verification)
- **Requirement:** User account linked to customer (shipper, forwarder, 3PL, etc.)

**Actor Attribution:**
- **Requirement:** Every incident has actor (who logged it)
- **Requirement:** Actor cannot be changed after capture
- **Requirement:** Actor visible in dispute packets

### 6.3 GPS Binding

**Location Capture:**
- **Requirement:** GPS location captured at moment of incident logging
- **Requirement:** Store: latitude, longitude, accuracy (meters), altitude (if available)
- **Requirement:** If GPS unavailable, use last known location (cached, marked as "approximate")
- **Requirement:** If GPS accuracy > 100m, mark as "low accuracy" but still save

**Location Validation:**
- **Requirement:** Validate GPS is reasonable (not 0,0 or clearly wrong)
- **Requirement:** Match GPS to known facilities (ports, ICDs, CFSs, warehouses)
- **Requirement:** If GPS matches facility, auto-link facility

**Location Privacy:**
- **Requirement:** GPS only used for incident context (not tracking)
- **Requirement:** GPS visible in dispute packets (for evidence)
- **Requirement:** User can see their own GPS history

### 6.4 No Deletion of Originals

**Immutable Events:**
- **Requirement:** Original incident events cannot be deleted
- **Requirement:** Original events cannot be modified
- **Requirement:** All edits create new events (additive only)

**Edit Behavior:**
- **Requirement:** If user wants to "edit" incident, create new event with:
  - Link to original event
  - "Edited at" timestamp
  - New content (voice, text, context)
  - Reason for edit (optional)
- **Requirement:** Original event remains visible in timeline
- **Requirement:** Dispute packets show full history (original + edits)

**Deletion Behavior:**
- **Requirement:** If user wants to "delete" incident, create deletion event:
  - Link to original event
  - "Deleted at" timestamp
  - Reason for deletion (optional)
- **Requirement:** Original event marked as "deleted" but not removed
- **Requirement:** Deleted events still visible in audit trail (for legal/dispute purposes)

### 6.5 Tamper Trail

**Full History:**
- **Requirement:** Every incident has complete history (capture, edits, deletions)
- **Requirement:** History cannot be hidden or suppressed
- **Requirement:** History visible in dispute packets

**Audit Log:**
- **Requirement:** Server maintains audit log of all changes
- **Requirement:** Audit log includes: who, what, when, why (if provided)
- **Requirement:** Audit log cannot be modified or deleted

**Subpoena-Ready:**
- **Requirement:** All data stored in format that can be exported for legal/dispute purposes
- **Requirement:** Export includes: original events, edits, deletions, timestamps, GPS, device IDs
- **Requirement:** Export format: JSON + PDF (human-readable)

---

## 7. Non-Goals

### 7.1 No Analytics or Dashboards on Mobile

**Requirement:** Mobile app does NOT include:
- Analytics dashboards
- Charts or graphs
- KPIs or metrics
- Reports or summaries

**Rationale:** Mobile v0 is for capture only. Analytics and dashboards are web console features.

**Exception:** Basic timeline view (user's own incidents) is allowed, but no aggregation or analysis.

### 7.2 No UI for Editing History in Way That Hides Originals

**Requirement:** Mobile app does NOT allow:
- Deleting original events
- Modifying original events
- Hiding original events
- Suppressing edit history

**Requirement:** All edits must be visible and traceable.

**Rationale:** Tamper-evident integrity is core to Ward's value proposition. If users can hide originals, we become "WhatsApp with a UI."

### 7.3 No Prediction or Adjudication

**Requirement:** Mobile app does NOT:
- Predict delays
- Score parties or assign blame
- Adjudicate disputes
- Suggest actions

**Rationale:** Ward is a neutral recorder. We preserve what was logged, not what should have happened.

### 7.4 No Web-First Features

**Requirement:** Mobile app does NOT include:
- Web-based workflows
- Browser-based features
- Features that require desktop/laptop

**Rationale:** Mobile v0 is Android-first, designed for field use.

### 7.5 No Multi-Language UI (v0 Scope)

**Requirement:** UI is English + Hindi only (not fully localized).

**Rationale:** v0 scope is deliberately narrow. Full localization is v1+.

**Exception:** Voice input supports multiple languages (Hindi, regional languages).

---

## 8. Technical Architecture (High-Level)

### 8.1 Mobile App Stack

**Framework:** React Native (or native Android if performance requires)

**Database:** SQLite (local storage)

**Sync:** REST API with background sync service

**Voice:** Android MediaRecorder API

**GPS:** Android Location Services

**Offline:** Service Worker / Background Service for sync

### 8.2 Data Model

**Incident Event:**
- id (UUID, client-generated)
- user_id (phone/email)
- device_id (Android ID)
- timestamp_captured (UTC, system time)
- timestamp_edited (UTC, if edited)
- gps_lat, gps_lon, gps_accuracy
- facility_id (port/ICD/CFS/warehouse)
- incident_type (enum)
- container_id (optional)
- truck_id (optional)
- voice_recording_url (local path, then server URL after sync)
- metadata (JSON: network status, app version, etc.)
- linked_to_event_id (if edit/deletion, link to original)

**Sync Status:**
- incident_id
- sync_status (pending, syncing, synced, failed)
- sync_attempts
- last_sync_attempt
- server_id (after successful sync)

### 8.3 API Endpoints (Mobile)

**POST /api/mobile/incidents**
- Create new incident
- Accept: voice recording, GPS, metadata
- Return: server_id, sync confirmation

**GET /api/mobile/incidents**
- Get user's incidents (for timeline view)
- Filter: date range, facility, sync status

**POST /api/mobile/incidents/{id}/edit**
- Create edit event (new event, links to original)
- Accept: new content, reason

**POST /api/mobile/sync**
- Batch sync (multiple incidents)
- Return: sync status for each

**GET /api/mobile/facilities**
- Get facilities (for selection)
- Filter: nearby (GPS-based)

---

## 9. Success Criteria for v0 Launch

### Must-Have (Blocking Launch)

1. ✅ Time-to-log ≤ 5 seconds (matches WhatsApp baseline)
2. ✅ 100% offline capture (no network required)
3. ✅ 95%+ successful sync rate (offline → online)
4. ✅ All incidents have GPS, device ID, timestamp, voice recording
5. ✅ No deletion of original events (only additive edits)
6. ✅ Works on low-end Android (2GB RAM, Android 7.0+)
7. ✅ Voice input in Hindi + English
8. ✅ Basic timeline view (user's incidents)

### Nice-to-Have (Post-Launch)

1. Voice input in regional languages
2. Auto-detect facility from GPS
3. Batch sync optimization
4. Offline map view (for GPS validation)

---

## 10. Open Questions & Risks

### Open Questions

1. **Speech-to-text accuracy:** How accurate is Hindi/regional language speech-to-text on low-end devices?
   - **Mitigation:** Test on target devices, fallback to manual entry if needed

2. **GPS accuracy in ports/yards:** How accurate is GPS in port gates and warehouse yards (often poor due to structures)?
   - **Mitigation:** Accept lower accuracy, mark as "approximate," use facility matching

3. **Battery drain:** Will background sync drain battery on low-end devices?
   - **Mitigation:** Sync only when charging or WiFi, optimize sync frequency

### Risks

1. **Adoption risk:** Drivers/yard staff may not adopt if it's slower than WhatsApp
   - **Mitigation:** Time-to-log is hard metric, must match WhatsApp baseline

2. **Network risk:** Poor connectivity may prevent sync, causing data loss
   - **Mitigation:** Aggressive local storage, retry logic, manual sync option

3. **Data integrity risk:** Users may try to game the system (fake GPS, wrong timestamps)
   - **Mitigation:** Server-side validation, audit logs, device binding

---

## 11. Appendix

### A. Incident Types (v0)

1. Stuck at port gate
2. CFS yard full
3. Dock not ready
4. Documents issue
5. No labour
6. System down
7. Other (voice note explains)

### B. Facility Types

1. Port (JNPT, Mundra, Chennai, etc.)
2. ICD (Inland Container Depot)
3. CFS (Container Freight Station)
4. Warehouse
5. Logistics Park

### C. User Roles (v0)

1. Driver
2. Yard Staff
3. Gate Operator
4. Supervisor/Dispatcher (can view timeline, export)

---

**Document Status:** Ready for Engineering Review  
**Next Steps:** Engineering team review, technical design doc, sprint planning

