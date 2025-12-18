# Ward Web Console v0 PRD: Ops/Finance/Legal Interface

**Version:** 1.0  
**Date:** December 2024  
**Status:** Ready for Engineering & Design  
**Target Launch:** Q2 2025 (after mobile v0)

---

## 1. Context & Personas

### 1.1 Indian Freight Context

**Ports, ICDs, CFSs, and Logistics Parks:**
- Major container ports: JNPT, Mundra, Chennai (global top tier for daily D&D charges)
- ICDs (Inland Container Depots) and CFSs (Container Freight Stations) as intermediate nodes
- Large logistics parks and warehouses (IndoSpace, ESR, etc.)
- Tariffs escalate quickly after short free-time windows
- Indian courts routinely uphold port and custodian rights to levy demurrage even when customs or agencies caused delay

**D&D + Waiting Charges:**
- Demurrage: charges for containers held at port/ICD/CFS beyond free time
- Detention: charges for containers held by importer/transporter beyond free time
- Waiting charges: charges for trucks waiting at warehouses, loading docks, etc.
- Storage charges: charges for goods stored at warehouses beyond agreed time

**Current State:**
- Real "system of record" is WhatsApp, calls, and scattered PDFs
- Disputes die in internal triage because reconstructing credible packets is slow, political, and demoralizing
- Many invoices are simply paid ("we'll just pay it")
- Internal blame games: "we don't know who to blame" escalations

### 1.2 User Personas

#### Persona 1: Operations Manager (Importer/3PL)

**Profile:**
- Age: 30-45
- Role: Manages day-to-day operations, coordinates with ports, warehouses, transporters
- Tech comfort: Medium-high (uses TMS, WMS, email, Excel)
- Context: Needs to understand what happened when delays occur, coordinate responses

**Pain points:**
- Invoices arrive with D&D/waiting charges, need to understand what happened
- Internal escalations: "who delayed whom, when?"
- Need to coordinate with multiple parties (port, CHA, transporter, warehouse)
- Time-consuming to reconstruct timelines from WhatsApp/emails

**Goals:**
- Quickly find what happened for a specific container/movement
- Reconstruct timeline across multiple facilities
- Export timeline for internal investigation
- Understand delay attribution (port-side, facility-side, transport-side, customer-side)

**Usage pattern:**
- 5-10 investigations per day
- 2-5 dispute packets per week
- Needs to respond quickly (within hours of invoice arrival)

#### Persona 2: Finance Controller / Accounts Payable Manager

**Profile:**
- Age: 35-50
- Role: Manages accounts payable, disputes invoices, tracks costs
- Tech comfort: Medium (uses ERP, Excel, email)
- Context: Needs to decide which invoices to contest, track dispute outcomes

**Pain points:**
- Invoices arrive daily with D&D/waiting charges
- Need to decide: contest or pay?
- Reconstructing dispute packets is time-consuming (4-8 hours per dispute)
- No systematic way to track which disputes win/lose
- Can't see patterns (which facilities/lanes drive most disputes)

**Goals:**
- Upload invoice and quickly find related movement
- Generate dispute packet in minutes (not hours)
- Track dispute outcomes (contested, waived, paid)
- See metrics: % contested, % waivers, cost savings
- Monthly reviews: which lanes/facilities drive most costs

**Usage pattern:**
- 10-20 invoices per day
- 5-10 dispute packets per week
- Monthly review meetings (analytics, scorecards)

#### Persona 3: Legal / Compliance Manager

**Profile:**
- Age: 35-55
- Role: Handles legal disputes, compliance, contract reviews
- Tech comfort: Medium (uses email, document management, legal research tools)
- Context: Needs provable evidence for disputes, contract negotiations

**Pain points:**
- Dispute packets need to be legally sound (withstand scrutiny)
- Need to ensure evidence is tamper-evident and credible
- Review dispute packets before submission to ports/courts
- Track which dispute formats work at which ports/facilities

**Goals:**
- Review dispute packets for legal compliance
- Ensure evidence is credible and tamper-evident
- Export packets in formats acceptable to ports/courts
- Track dispute outcomes and learn which formats work

**Usage pattern:**
- 2-5 dispute packet reviews per week
- Monthly review of dispute outcomes
- Contract negotiation support (facility/carrier scorecards)

#### Persona 4: 3PL / Forwarder Operations Lead

**Profile:**
- Age: 30-45
- Role: Coordinates customs, ICDs, CFS, port legs for multiple customers
- Tech comfort: Medium-high (uses TMS, customs systems, email)
- Context: Stuck between custodians, customs, carriers, warehouses, and customers

**Pain points:**
- Multiple customers, multiple movements, multiple disputes
- Need to allocate delays to correct parties (port, facility, customer, carrier)
- Internal chargebacks: which customer/vendor should pay?
- Scorecards needed for facilities, carriers, customers

**Goals:**
- View all movements across customers
- Allocate delays to parties (for chargebacks)
- Generate scorecards for facilities, carriers, customers
- Export investigation packets for internal reviews

**Usage pattern:**
- 20-50 movements to review per day
- 10-20 allocation decisions per week
- Weekly scorecard reviews

---

## 2. Jobs-to-Be-Done

### Job 1: Handle D&D/Waiting Invoices with Evidence

**When:** Invoice arrives from port, ICD, CFS, warehouse, or logistics park

**Steps:**
1. Upload invoice (PDF/image) or enter invoice details
2. Search for related movement (by container ID, truck number, invoice reference)
3. Review timeline of incidents for that movement
4. Generate dispute packet (if evidence supports dispute)
5. Export and submit dispute packet
6. Track outcome (contested, waived, paid)

**Success criteria:**
- Time from invoice upload to dispute packet: < 10 minutes
- Dispute packet includes all relevant Ward-captured incidents
- Packet format matches port/facility requirements

### Job 2: Run Internal Investigations ("Who Delayed Whom, When")

**When:** Internal escalation or blame game between parties

**Steps:**
1. Search for movement(s) by container/truck ID, route, date range
2. View unified timeline across all facilities (port → ICD → CFS → warehouse)
3. Analyze delay attribution (port-side, facility-side, transport-side, customer-side)
4. Generate allocation report (who should eat which costs)
5. Export investigation packet for internal stakeholders
6. Mark escalation as resolved with conclusion

**Success criteria:**
- Time from escalation to timeline reconstruction: < 15 minutes
- Clear attribution of delays to parties
- Reduction in "we don't know who to blame" escalations

### Job 3: Produce Packets for External Disputes

**When:** Need to submit dispute to port authority, court, or facility

**Steps:**
1. Select movement(s) and incidents to include
2. Add supporting documents (customs clearance, e-way bills, etc.)
3. Select dispute template (JNPT format, Mundra format, generic)
4. Review packet (ensure legally sound, tamper-evident)
5. Export as PDF (formatted for submission)
6. Track submission and outcome

**Success criteria:**
- Packet format matches port/facility/court requirements
- All evidence is tamper-evident and credible
- Packet can withstand external scrutiny (subpoena-ready)

### Job 4: Review Lanes/Facilities/Vendors for Allocation and Performance

**When:** Monthly review, contract negotiation, vendor performance review

**Steps:**
1. View analytics dashboard (disputes by lane/facility/vendor)
2. Review scorecards (facilities, carriers, customers)
3. Analyze structural vs operational delays
4. Export reports for contract/pricing decisions
5. Create action items (contract renegotiation, facility changes, carrier reviews)

**Success criteria:**
- Clear visibility into dispute patterns and costs
- Actionable insights for operations and finance decisions
- Measurable uplift in % contested and % waivers vs baseline

---

## 3. Core Features & Screens

### 3.1 Global Search

**Purpose:** Find movements, containers, trucks, invoices quickly

**Location:** Top navigation bar (always visible)

**Search Capabilities:**
- Container ID (full or partial)
- Truck number (full or partial)
- Bill of Lading (BL) number
- Invoice number/reference
- Lane (port → destination)
- Facility (port, ICD, CFS, warehouse name)
- Date range (from/to)
- Customer/vendor name

**Search Results:**
- List of matching movements with:
  - Container/truck ID
  - Route (port → ICD → CFS → warehouse)
  - Date range
  - Number of incidents logged
  - Status (active, resolved, disputed)
  - Last updated
- Click to open movement detail page

**Advanced Filters:**
- Filter by: facility type, charge type, dispute status, outcome
- Save search filters for quick access

**Requirements:**
- Search must be fast (< 2 seconds for results)
- Support partial matches and fuzzy search
- Recent searches saved (quick access)
- Search history (last 10 searches)

### 3.2 Movement Detail Page

**Purpose:** View complete timeline and details for a movement

**Layout:**
- **Header:** Container/truck ID, route, date range, status
- **Timeline View:** Chronological list of all incidents
- **Metadata Panel:** Parties, facilities, documents, dispute status
- **Actions:** Export packet, add note, link to invoice

**Timeline View:**
- **Chronological list** (newest first, or oldest first toggle)
- **Each event shows:**
  - Timestamp ("captured at" prominently displayed)
  - "Edited at" timestamp (if edited, shown separately)
  - Facility name and node (port, ICD, CFS, warehouse)
  - Actor (who logged it: driver name, yard staff, etc.)
  - Incident type (icon + text: "stuck at port gate", "CFS yard full", etc.)
  - GPS location (clickable, opens map)
  - Voice recording (play button, transcript if available)
  - Device ID (for audit trail)
  - Reliability indicator (high/medium/low based on corroboration)
  - Edit history (if edited, show original + edits)

**Visual Indicators:**
- **Color coding:**
  - Green: Captured in real-time (within 5 minutes of incident)
  - Yellow: Captured later (5-60 minutes after incident)
  - Red: Reconstructed (more than 60 minutes after incident, or edited)
- **Icons:**
  - Original event: solid circle
  - Edited event: circle with edit icon
  - Deleted event: circle with delete icon (strikethrough, but still visible)

**Filters:**
- Filter by: facility, incident type, actor, date range
- Show/hide: edits, deletions, low-reliability events

**Metadata Panel:**
- **Parties:**
  - Shipper, forwarder, CHA, transporter, facility, customs
  - Click to view all movements for that party
- **Facilities:**
  - Port, ICD, CFS, warehouse (with addresses, contact info)
- **Documents:**
  - Uploaded invoices, customs clearance, e-way bills, etc.
  - Link documents to specific events
- **Dispute Status:**
  - Not disputed, disputed, submitted, outcome (waived/paid/partial)

**Actions:**
- **Export Packet:** Generate dispute packet (see 3.3)
- **Add Note:** Add internal note (not part of dispute packet)
- **Link Invoice:** Link to invoice (if not already linked)
- **Edit Movement:** Add/edit metadata (parties, route, etc.) - creates new event, doesn't modify original

**Requirements:**
- Timeline must load quickly (< 3 seconds for 100 events)
- "Captured at" vs "edited at" must be instantly visible
- Full edit history must be accessible (click to expand)
- GPS locations must be clickable (opens map view)
- Voice recordings must be playable inline

### 3.3 Dispute Packet Builder

**Purpose:** Generate dispute packets for submission to ports/facilities/courts

**Access:** From movement detail page, click "Export Packet" or "Create Dispute Packet"

**Steps:**

**Step 1: Select Movements & Events**
- Select one or more movements (if dispute spans multiple movements)
- Select specific events to include (default: all events for selected movements)
- Exclude events (if not relevant to dispute)
- Add supporting documents (invoices, customs clearance, e-way bills, etc.)

**Step 2: Select Template**
- Choose dispute template:
  - JNPT format
  - Mundra format
  - Chennai format
  - Generic format
  - Custom format (if available)
- Preview template format

**Step 3: Review & Customize**
- Review packet contents:
  - Chronological timeline of selected events
  - Timestamps, GPS, voice recordings, attachments
  - Summary of delays and attribution
- Add cover letter/notes (optional)
- Customize formatting (if template allows)

**Step 4: Export**
- Export as PDF (formatted for submission)
- Export as Excel (for internal tracking)
- Export as JSON (for API integration)
- Email directly (if configured)

**Packet Contents:**
- **Cover page:** Movement details, parties, dispute summary
- **Timeline:** Chronological list of events with:
  - Timestamp (captured at, edited at if applicable)
  - Facility and location
  - Actor
  - Incident description
  - GPS coordinates
  - Voice recording transcript (if available)
- **Attachments:** Supporting documents, voice recordings (links)
- **Summary:** Total delay time, attribution, supporting evidence

**Requirements:**
- Packet must be tamper-evident (PDF with digital signatures, timestamps)
- All events must show "captured at" vs "edited at"
- Edit history must be visible (original + edits)
- Packet format must match port/facility requirements
- Export must be fast (< 30 seconds for 50 events)

### 3.4 Analytics View

**Purpose:** Understand dispute patterns, costs, and performance

**Access:** Top navigation → "Analytics" or "Reviews"

**Dashboard Overview:**
- **Key metrics (cards):**
  - Total invoices received (current period)
  - % invoices contested (vs historical baseline)
  - % waivers/discounts (vs historical baseline)
  - Total dispute value (₹)
  - Total waived/saved (₹)
  - Average time per dispute (hours)
  - Dispute win rate (if outcomes tracked)

**Dispute Volume Analysis:**
- **Bar chart:** Disputes by port/facility
- **Bar chart:** Disputes by lane (port → destination)
- **Line chart:** Disputes over time (trend)
- **Filters:** Date range, charge type, facility type, lane

**Cost Impact Analysis:**
- **Bar chart:** Total disputed amount by port/facility
- **Bar chart:** Total waived/saved amount by port/facility
- **Table:** Cost per dispute by facility type
- **ROI calculation:** Ward cost vs savings

**Performance Scorecards:**
- **Facility Scorecards:**
  - Ports, ICDs, CFSs, warehouses, logistics parks
  - Metrics: dispute frequency, average delay duration, structural vs operational delay ratio
  - Trend: improving vs deteriorating
- **Carrier/CHA Scorecards:**
  - Dispute frequency, delay attribution, performance rating
- **Customer Scorecards:**
  - Dispute frequency, operational friction incidents, cost impact

**Lane Analysis:**
- **Heat map:** Dispute frequency by lane
- **Table:** Cost analysis (which lanes drive most dispute costs)
- **Trend analysis:** Improving vs deteriorating lanes
- **Export:** Lane performance report

**Allocation Analysis:**
- **Structural vs Operational Delays:**
  - Structural: unavoidable physics (customs delays, port congestion)
  - Operational: controllable behaviors (driver delays, facility issues)
- **Delay Attribution:**
  - Port-side delays
  - Facility-side delays
  - Transport-side delays
  - Customer-side delays
- **Chargeback Allocation:**
  - Which vendor, lane, site, or customer should eat which share of delay-driven costs

**Export & Share:**
- Export monthly review report (PDF/Excel)
- Share with stakeholders
- Set up automated monthly reports
- Create action items (contract renegotiation, facility changes, carrier reviews)

**Requirements:**
- Dashboard must load quickly (< 3 seconds)
- Charts must be interactive (filter, drill down)
- Data must be exportable (PDF, Excel, CSV)
- Metrics must be accurate and up-to-date

### 3.5 Invoice Management

**Purpose:** Track invoices, link to movements, manage disputes

**Access:** Top navigation → "Invoices"

**Invoice List:**
- **Table view:** All invoices with:
  - Invoice number, date, amount
  - Facility, charge type
  - Status (pending, contested, paid, waived)
  - Linked movement (if linked)
  - Dispute packet (if generated)
- **Filters:** Date range, facility, charge type, status
- **Search:** By invoice number, container ID, facility

**Invoice Detail:**
- **Invoice information:** Number, date, amount, facility, charge type
- **Linked movement:** Container/truck ID, route, timeline
- **Dispute status:** Contested, submitted, outcome
- **Actions:** Link to movement, generate dispute packet, mark as paid/waived

**Upload Invoice:**
- **Upload PDF/image:** Drag and drop or file picker
- **OCR extraction:** Auto-extract container ID, facility, amount, date
- **Manual entry:** If OCR fails, manual entry form
- **Link to movement:** Search and link to existing movement, or create new

**Requirements:**
- OCR must be accurate (90%+ for common invoice formats)
- Invoice must link to movement automatically (if container ID matches)
- Invoice status must be trackable (pending → contested → outcome)

---

## 4. Permissions & Auditability

### 4.1 User Roles

#### Role 1: Viewer (Read-Only)

**Permissions:**
- View all movements, timelines, invoices
- View analytics and scorecards
- Export dispute packets (read-only)
- Cannot edit, delete, or modify any data

**Use case:** Executives, auditors, external stakeholders who need visibility but shouldn't modify data

#### Role 2: Operations

**Permissions:**
- All Viewer permissions
- Add notes to movements
- Link invoices to movements
- Export dispute packets
- View and edit movement metadata (creates new event, doesn't modify original)
- Cannot delete or modify original events

**Use case:** Operations managers, 3PL ops leads who need to investigate and coordinate

#### Role 3: Finance

**Permissions:**
- All Operations permissions
- Upload invoices
- Generate dispute packets
- Mark invoices as contested/paid/waived
- View and export analytics
- Cannot delete or modify original events

**Use case:** Finance controllers, accounts payable managers who handle invoices and disputes

#### Role 4: Legal

**Permissions:**
- All Finance permissions
- Review and approve dispute packets (before submission)
- Export packets in legal formats
- View audit logs
- Cannot delete or modify original events

**Use case:** Legal/compliance managers who review dispute packets for legal compliance

#### Role 5: Admin

**Permissions:**
- All permissions
- Manage users and roles
- Configure dispute templates
- View full audit logs
- System configuration
- Cannot delete or modify original events (even admins cannot)

**Use case:** System administrators, customer success managers

### 4.2 Audit Log Rules

**Requirement:** Every action in the console must be logged

**Audit Log Fields:**
- Timestamp (UTC)
- User (who performed action)
- Action type (view, export, edit, delete, etc.)
- Resource (movement ID, invoice ID, etc.)
- Details (what changed, before/after values)
- IP address
- Device/browser info

**Audit Log Actions:**
- View movement/invoice (logged, but not detailed)
- Export dispute packet (logged with packet contents summary)
- Add note (logged with note content)
- Link invoice (logged with invoice and movement IDs)
- Edit movement metadata (logged with before/after values)
- Upload document (logged with document name and type)
- Mark invoice as contested/paid/waived (logged with status change)

**Audit Log Access:**
- Admins: Full access to all audit logs
- Legal: Access to audit logs for dispute packets they review
- Others: Access to their own audit logs only

**Audit Log Export:**
- Export audit logs (for compliance, legal purposes)
- Format: CSV, JSON
- Include: all fields, filterable by user, date range, action type

**Requirements:**
- Audit logs must be immutable (cannot be deleted or modified)
- Audit logs must be retained for minimum 7 years (legal requirement)
- Audit logs must be searchable and filterable

### 4.3 Data Modification Rules

**Original Events:**
- **Cannot be deleted** (by anyone, including admins)
- **Cannot be modified** (by anyone, including admins)
- **Can be viewed** by all authorized users
- **Can be linked** to invoices, documents, notes

**Movement Metadata:**
- **Can be edited** (parties, route, etc.) - but creates new event, doesn't modify original
- **Edit history** must be visible (who edited, when, what changed)
- **Original metadata** must be preserved

**Notes:**
- **Can be added** by authorized users
- **Can be edited/deleted** by author or admin
- **Notes are not part of dispute packets** (internal only)
- **Note history** must be visible (if edited)

**Documents:**
- **Can be uploaded** by authorized users
- **Can be deleted** by uploader or admin (but deletion is logged)
- **Documents linked to events** cannot be deleted if event is part of dispute packet

---

## 5. Data & Integrity Rules

### 5.1 No Deletion of Original Events

**Requirement:** Original incident events cannot be deleted by anyone

**Implementation:**
- Database: Soft delete only (mark as deleted, but don't remove from database)
- UI: Deleted events shown with strikethrough, but still visible
- Dispute packets: Include deleted events (marked as deleted, with deletion timestamp and reason)

**Rationale:** Tamper-evident integrity is core to Ward's value proposition. If users can delete originals, we become "WhatsApp with a UI."

### 5.2 All Edits Additive and Visible

**Requirement:** All edits create new events, original events never modified

**Implementation:**
- Edit creates new event with:
  - Link to original event
  - "Edited at" timestamp
  - New content (if content changed)
  - Reason for edit (optional, but recommended)
- Original event remains visible in timeline
- UI shows both original and edit (with clear visual distinction)

**Display Rules:**
- Timeline shows: Original event → Edit event (indented or grouped)
- Dispute packets show: Full history (original + edits)
- "Captured at" vs "edited at" must be prominently displayed

### 5.3 Clear Display of Temporal Truth

**Requirement:** "Captured at" vs "edited at" must be instantly visible

**Implementation:**
- **Timeline view:**
  - "Captured at" timestamp: Large, prominent
  - "Edited at" timestamp: Smaller, below "captured at" (if edited)
  - Color coding: Green (real-time), Yellow (later), Red (reconstructed/edited)
- **Dispute packets:**
  - Both timestamps shown for each event
  - Edit history included (if edited)
  - Clear indication of which events were reconstructed later

**Validation:**
- If user cannot instantly see which events were reconstructed later, Ward hasn't earned its job
- User testing: Can users identify "captured at" vs "edited at" in < 2 seconds?

### 5.4 Subpoena-Ready Data

**Requirement:** All data must be exportable in format that can withstand legal scrutiny

**Implementation:**
- Export formats: PDF (with digital signatures), JSON (with checksums), Excel (with metadata)
- Export includes:
  - Original events (with all metadata)
  - Edit history (all edits, with timestamps and reasons)
  - Deletion history (all deletions, with timestamps and reasons)
  - Audit logs (who accessed, when, what they did)
  - GPS coordinates, device IDs, timestamps (all original values preserved)

**Legal Compliance:**
- Data retention: Minimum 7 years (as per Indian legal requirements)
- Data export: Must be complete and verifiable
- Digital signatures: PDF exports must be digitally signed (for authenticity)

---

## 6. Non-Goals

### 6.1 No Planning/Optimization Features

**Requirement:** Web console does NOT include TMS/WMS features

**Excluded:**
- Route optimization
- Load planning
- Inventory management
- Booking management
- Capacity planning
- Predictive analytics (predict delays, optimize routes)

**Rationale:** Ward is the evidence layer, not the planning layer. We sit above TMS/WMS systems, not replace them.

**Exception:** Basic timeline view and analytics are allowed (for dispute/investigation purposes).

### 6.2 No Features That Allow Silent History Edits

**Requirement:** No features that allow hiding or suppressing original events

**Excluded:**
- "Hide original event" option
- "Suppress edit history" option
- "Clean up timeline" feature (that removes events)
- Any feature that makes original events invisible or hard to find

**Rationale:** If we allow silent edits, we become "WhatsApp with a UI." This is the red line.

**Validation:**
- Every feature must pass: "Would this withstand external scrutiny if subpoenaed?"
- If answer is no, feature does not ship—even if large customer asks, even if ARR is on the line

### 6.3 No Prediction or Adjudication

**Requirement:** Web console does NOT predict or adjudicate

**Excluded:**
- Predicting which disputes will win/lose
- Scoring parties or assigning blame
- Suggesting which invoices to contest
- AI-generated dispute arguments
- Automated dispute submission

**Rationale:** Ward is a neutral recorder. We preserve what was logged, not what should have happened or what will happen.

**Exception:** Analytics can show historical patterns (which dispute formats worked at which ports), but cannot predict future outcomes.

### 6.4 No Mobile-First Features

**Requirement:** Web console is desktop-first (mobile is separate app)

**Excluded:**
- Mobile-optimized capture workflows
- Mobile-specific features
- Responsive design for mobile (basic responsive is OK, but not optimized)

**Rationale:** Web console is for ops/finance/legal (desktop users). Mobile capture is separate app (mobile v0).

**Exception:** Basic responsive design (so console works on tablets for viewing).

### 6.5 No Real-Time Collaboration

**Requirement:** Web console does NOT include real-time collaboration features

**Excluded:**
- Live chat or comments
- Real-time notifications
- Collaborative editing
- Presence indicators

**Rationale:** v0 scope is deliberately narrow. Collaboration features are v1+.

**Exception:** Notes and comments (async, not real-time) are allowed.

---

## 7. Technical Architecture (High-Level)

### 7.1 Tech Stack

**Frontend:**
- Framework: React (or Next.js for SSR if needed)
- UI Library: Tailwind CSS + shadcn/ui components
- State Management: React Query (for server state), Zustand (for client state)
- Charts: Recharts or Chart.js

**Backend:**
- API: REST API (FastAPI, same as mobile)
- Database: PostgreSQL (Supabase)
- File Storage: S3 or Supabase Storage (for invoices, documents, voice recordings)
- Search: PostgreSQL full-text search (or Elasticsearch if needed)

**Authentication:**
- JWT tokens (same as mobile)
- Role-based access control (RBAC)

### 7.2 Data Model

**Movements:**
- id (UUID)
- container_id, truck_id
- route (port → ICD → CFS → warehouse)
- date_range (start, end)
- parties (shipper, forwarder, CHA, transporter, facility, customs)
- status (active, resolved, disputed)
- created_at, updated_at

**Incident Events:**
- id (UUID)
- movement_id (FK)
- user_id (who logged it)
- device_id (Android ID)
- timestamp_captured (UTC, system time)
- timestamp_edited (UTC, if edited)
- gps_lat, gps_lon, gps_accuracy
- facility_id (FK)
- incident_type (enum)
- voice_recording_url
- metadata (JSON)
- linked_to_event_id (if edit/deletion, link to original)
- created_at, updated_at

**Invoices:**
- id (UUID)
- invoice_number
- invoice_date
- amount
- facility_id (FK)
- charge_type (demurrage, detention, waiting, storage)
- status (pending, contested, paid, waived)
- movement_id (FK, if linked)
- dispute_packet_id (FK, if generated)
- ocr_data (JSON, extracted data)
- file_url (PDF/image)
- created_at, updated_at

**Dispute Packets:**
- id (UUID)
- movement_ids (array of UUIDs)
- event_ids (array of UUIDs, selected events)
- template_type (JNPT, Mundra, Chennai, generic)
- status (draft, reviewed, submitted, outcome)
- outcome (waived, paid, partial, pending)
- file_url (PDF)
- created_by, reviewed_by, submitted_by
- created_at, reviewed_at, submitted_at, outcome_at

**Audit Logs:**
- id (UUID)
- user_id (FK)
- action_type (enum)
- resource_type (movement, invoice, packet, etc.)
- resource_id (UUID)
- details (JSON, before/after values)
- ip_address
- device_info (JSON)
- created_at

### 7.3 API Endpoints (Web Console)

**Movements:**
- GET /api/web/movements (list, with filters)
- GET /api/web/movements/{id} (detail)
- POST /api/web/movements/{id}/notes (add note)
- PUT /api/web/movements/{id}/metadata (edit metadata, creates new event)

**Incidents:**
- GET /api/web/incidents (list, with filters)
- GET /api/web/incidents/{id} (detail)
- POST /api/web/incidents/{id}/edit (create edit event)

**Invoices:**
- GET /api/web/invoices (list, with filters)
- POST /api/web/invoices (upload)
- GET /api/web/invoices/{id} (detail)
- PUT /api/web/invoices/{id}/link (link to movement)
- PUT /api/web/invoices/{id}/status (mark as contested/paid/waived)

**Dispute Packets:**
- POST /api/web/packets (create)
- GET /api/web/packets/{id} (detail)
- POST /api/web/packets/{id}/export (export as PDF/Excel)
- PUT /api/web/packets/{id}/status (mark as reviewed/submitted)

**Analytics:**
- GET /api/web/analytics/dashboard (key metrics)
- GET /api/web/analytics/disputes (dispute volume analysis)
- GET /api/web/analytics/costs (cost impact analysis)
- GET /api/web/analytics/scorecards (facility/carrier/customer scorecards)
- GET /api/web/analytics/lanes (lane analysis)

**Search:**
- GET /api/web/search (global search, by container, truck, BL, etc.)

**Audit:**
- GET /api/web/audit (audit logs, with filters)

---

## 8. Success Criteria for v0 Launch

### Must-Have (Blocking Launch)

1. ✅ Global search works (< 2 seconds for results)
2. ✅ Movement detail page loads quickly (< 3 seconds for 100 events)
3. ✅ Timeline shows "captured at" vs "edited at" prominently
4. ✅ Dispute packet builder generates packets in < 30 seconds
5. ✅ Dispute packets are tamper-evident (PDF with signatures)
6. ✅ Analytics dashboard loads quickly (< 3 seconds)
7. ✅ Invoice upload with OCR (90%+ accuracy)
8. ✅ Role-based permissions work correctly
9. ✅ Audit logs capture all actions
10. ✅ No deletion of original events (even by admins)

### Nice-to-Have (Post-Launch)

1. Advanced search filters
2. Custom dispute templates
3. Automated monthly reports
4. Email notifications
5. Mobile-responsive design (basic)

---

## 9. Open Questions & Risks

### Open Questions

1. **OCR accuracy:** How accurate is OCR for Indian invoice formats (Hindi/English mix)?
   - **Mitigation:** Test on real invoices, fallback to manual entry

2. **Dispute template formats:** What formats do JNPT, Mundra, Chennai actually accept?
   - **Mitigation:** Research port requirements, start with generic format, iterate based on feedback

3. **Performance at scale:** Can timeline handle 1000+ events per movement?
   - **Mitigation:** Pagination, lazy loading, virtual scrolling

### Risks

1. **Adoption risk:** Finance/ops teams may not adopt if it's slower than current process
   - **Mitigation:** Time-to-packet is key metric, must be < 10 minutes

2. **Data integrity risk:** Users may try to game the system (fake events, wrong timestamps)
   - **Mitigation:** Server-side validation, audit logs, device binding

3. **Legal risk:** Dispute packets may not be accepted by ports/courts
   - **Mitigation:** Start with generic format, iterate based on outcomes, learn which formats work

---

## 10. Appendix

### A. Dispute Templates (v0)

1. **JNPT Format:** (to be researched)
2. **Mundra Format:** (to be researched)
3. **Chennai Format:** (to be researched)
4. **Generic Format:** Chronological timeline with timestamps, GPS, attachments

### B. Charge Types

1. Demurrage
2. Detention
3. Waiting charges
4. Storage charges

### C. Incident Types (from mobile v0)

1. Stuck at port gate
2. CFS yard full
3. Dock not ready
4. Documents issue
5. No labour
6. System down
7. Other

### D. Facility Types

1. Port
2. ICD (Inland Container Depot)
3. CFS (Container Freight Station)
4. Warehouse
5. Logistics Park

---

**Document Status:** Ready for Engineering & Design Review  
**Next Steps:** Design wireframes, technical design doc, sprint planning

