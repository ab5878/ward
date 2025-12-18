# Ward v0 PRD: Mobile Incident Capture

## PRD Summary (Markdown)

### Problem Statement

**WhatsApp vs Ward: The Time-to-Log Problem**

In Indian freight operations, when something goes wrong—a container stuck at port gate, CFS yard full, dock not ready, documents issue, no labour, system down—the first response is a WhatsApp voice note. It's fast, familiar, and requires zero training. But WhatsApp screenshots don't hold up in disputes. Port authorities, courts, and custodians need provable, time-stamped evidence.

Ward's core challenge: **Be as fast or faster than sending a WhatsApp voice note on a low-end Android in a bad network.** If logging an incident takes longer than WhatsApp, drivers and yard staff won't use it. If they don't use it, Ward fails.

The behavioral bottleneck is clear: time-to-log vs WhatsApp is a hard metric, not a nice-to-have. Product and engineering must treat this as the primary constraint.

### Primary Success Metric

**Seconds from incident to log**

- Target: ≤ 5 seconds from "something goes wrong" to "incident logged in Ward"
- Baseline: WhatsApp voice note takes ~3-5 seconds (open app → tap mic → speak → send)
- Ward must match or beat this, including:
  - App open time
  - One-tap capture
  - Voice recording
  - Auto-attach GPS, device, actor, context
  - Offline buffering confirmation

If Ward takes > 5 seconds, drivers will default to WhatsApp. If Ward takes < 5 seconds and provides tamper-evident proof, it wins.

### Key User Stories

**1. Driver at Port Gate (Stuck Container)**
- **As a** driver waiting at JNPT gate with a container
- **I want to** log "stuck at port gate" in one tap
- **So that** my company can prove the delay wasn't our fault and dispute demurrage charges
- **Acceptance criteria:**
  - Tap → speak → done (no typing, no forms)
  - Works offline (port gate connectivity is unreliable)
  - Auto-attaches GPS, container ID, timestamp, device ID
  - Confirmation appears even if network is down

**2. Yard Staff at CFS (Yard Full)**
- **As a** yard operator at a CFS when the yard is full
- **I want to** log "CFS yard full" with my voice
- **So that** the forwarder can prove the delay was facility-side, not transport-side
- **Acceptance criteria:**
  - Single tap to start recording
  - Works on low-end Android (common device for yard staff)
  - Syncs later when connectivity improves
  - No "loading" spinners during capture

**3. Warehouse Gate Team (Dock Not Ready)**
- **As a** warehouse gate operator when a dock isn't ready
- **I want to** log "dock not ready" faster than sending a WhatsApp
- **So that** waiting time charges can be disputed with timestamped proof
- **Acceptance criteria:**
  - Faster than WhatsApp voice note
  - Auto-links to truck ID, warehouse node, shift context
  - Works in poor network conditions (warehouse gates often have weak signal)

**4. Dispatcher (Documents Issue)**
- **As a** dispatcher coordinating multiple trucks
- **I want to** see all incidents logged by drivers in real-time
- **So that** I can prioritize responses and build dispute packets
- **Acceptance criteria:**
  - View timeline of all incidents for a container/truck
  - See which events were "captured at" vs "edited at" (temporal truth)
  - Export delay log for dispute packet

**5. Finance/Ops Team (Dispute Packet)**
- **As a** finance manager disputing demurrage charges
- **I want to** export a chronological timeline of events with timestamps and GPS
- **So that** I can submit it to port authorities and courts as provable evidence
- **Acceptance criteria:**
  - Exportable delay log in dispute template format
  - Shows "captured at" vs "edited at" prominently
  - Includes GPS, device ID, actor, attachments
  - Formatted for Indian D&D/detention dispute templates

### Non-Goals

**No Dashboards**
- v0 is not a dashboard or analytics platform
- No KPIs, no charts, no "insights"
- Focus is capture and export, not visualization

**No Silent Edits**
- All edits and deletions are stored as new events
- Originals are never destroyed
- Full tamper trail is always visible
- "Logged later" vs "logged in the moment" is instantly visible

**No Prediction or Adjudication**
- Ward does not predict delays
- Ward does not score parties or assign blame
- Ward does not adjudicate disputes
- Ward is a neutral recorder of temporal truth

**No Web-First Features**
- v0 is mobile-first (Android)
- Web interface is for export/view only
- No web-based capture workflows

**No Multi-Language UI**
- UI can be in English/Hindi mix
- Voice capture supports multiple Indian languages
- But UI itself is not fully localized (v0 scope)

---

## ProductSection Component (JSX/TSX)

