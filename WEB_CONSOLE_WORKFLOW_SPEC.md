# Ward Web Console Workflow Spec

## Workflow Spec (Markdown)

### Overview

The Ward web console is the ops/finance interface for converting "we'll just pay it" invoices into structured disputes, reconstructing timelines for internal escalations, and analyzing dispute patterns for monthly reviews. It transforms mobile-captured incident logs into actionable dispute packets and insights.

---

### Flow 1: Invoice Arrives → Find Movement → Export Dispute Packet

**Persona:** Finance Controller / Accounts Payable Manager

**Trigger:** D&D, detention, or waiting charge invoice arrives from port, ICD, CFS, warehouse, or logistics park.

**Inputs:**
- Invoice document (PDF/image)
- Container ID or truck number
- Port/facility name (JNPT, Mundra, Chennai, etc.)
- Invoice amount
- Invoice date
- Charge type (demurrage, detention, waiting, storage)

**Screens and Actions:**

1. **Invoice Upload Screen**
   - Upload invoice PDF/image
   - Auto-extract container ID, facility, amount, date (OCR)
   - Manual override if OCR fails
   - Select charge type from dropdown

2. **Movement Search Screen**
   - Search by container ID, truck number, or invoice reference
   - Display matching movements with:
     - Container/truck ID
     - Route (port → ICD → CFS → warehouse)
     - Date range
     - Number of incidents logged
     - Status (active, resolved, disputed)
   - Select the relevant movement

3. **Timeline Review Screen**
   - Chronological timeline of all Ward-captured incidents for this movement
   - Each event shows:
     - Timestamp ("captured at" vs "edited at" clearly marked)
     - GPS location
     - Actor (driver, yard staff, gate operator)
     - Voice/text content
     - Device ID
     - Reliability indicator
   - Filter by: date range, facility, incident type, actor
   - Highlight events that support dispute (e.g., "stuck at port gate", "CFS yard full", "dock not ready")

4. **Dispute Packet Builder**
   - Auto-generate dispute packet from timeline
   - Include/exclude specific events
   - Add supporting documents (customs clearance, e-way bills, etc.)
   - Select dispute template (JNPT format, Mundra format, generic)
   - Preview packet before export

5. **Export & Submit**
   - Export as PDF (formatted for port/facility submission)
   - Export as Excel (for internal tracking)
   - Mark invoice as "disputed" in Ward
   - Set reminder for follow-up

**Outputs:**
- Dispute packet PDF (chronological timeline, timestamps, GPS, attachments)
- Internal tracking record (invoice ID, dispute status, submission date)
- Metrics update (% invoices contested, dispute packet generated)

**Success Criteria:**
- Time from invoice upload to dispute packet export: < 10 minutes
- Packet includes all relevant Ward-captured incidents
- Packet format matches port/facility requirements

---

### Flow 2: Internal Escalation → Reconstruct Port + Warehouse Timeline

**Persona:** Ops Manager / Supply Chain Manager

**Trigger:** Internal escalation: "Who delayed whom?" Blame game between port, warehouse, transporter, or customer. Need to reconstruct what actually happened.

**Inputs:**
- Container ID or truck number
- Date range (approximate)
- Route (port → ICD → CFS → warehouse)
- Parties involved (shipper, forwarder, CHA, transporter, facility, customs)
- Escalation reason (delay, penalty, chargeback dispute)

**Screens and Actions:**

1. **Timeline Search Screen**
   - Search by container/truck ID, route, date range, or parties
   - Display matching movements
   - Filter by facility type (port, ICD, CFS, warehouse, logistics park)
   - Select movement(s) to investigate

2. **Multi-Facility Timeline View**
   - Unified chronological timeline across all facilities in the route
   - Color-coded by facility:
     - Port (blue)
     - ICD (green)
     - CFS (orange)
     - Warehouse/Logistics Park (purple)
   - Each event shows:
     - Facility name and node
     - Timestamp (with "captured at" vs "edited at")
     - Actor and role
     - Incident type (stuck, yard full, dock not ready, documents issue, etc.)
     - GPS location
     - Voice/text content
   - Time gaps highlighted (where no incidents were logged)
   - Free time windows overlaid (if configured)

3. **Allocation Analysis**
   - Auto-calculate delay attribution:
     - Port-side delays (customs, gate, yard)
     - Facility-side delays (CFS yard full, warehouse dock not ready)
     - Transport-side delays (driver, vehicle)
     - Customer-side delays (documents, instructions)
   - Show structural vs operational delays
   - Generate allocation report (who should eat which costs)

4. **Internal Investigation Packet**
   - Export timeline as investigation packet
   - Include allocation analysis
   - Add notes and conclusions
   - Share with internal stakeholders (ops, finance, legal)
   - Mark escalation as "resolved" with conclusion

**Outputs:**
- Multi-facility timeline (visual + exportable)
- Allocation report (delay attribution by party)
- Internal investigation packet (PDF)
- Scorecard updates (facility, carrier, customer performance)

**Success Criteria:**
- Time from escalation to timeline reconstruction: < 15 minutes
- Clear attribution of delays to parties
- Reduction in "we don't know who to blame" escalations

---

### Flow 3: Monthly Review → See Which Lanes/Facilities Drive Most Disputes and Costs

**Persona:** Finance Controller / Operations Director

**Trigger:** Monthly business review. Need to understand dispute patterns, costs, and performance across lanes, facilities, and parties.

**Inputs:**
- Date range (month, quarter, or custom)
- Filters: port, facility, lane, carrier, customer, charge type

**Screens and Actions:**

1. **Dashboard Overview**
   - Key metrics at a glance:
     - Total invoices received
     - % invoices contested (vs historical baseline)
     - % waivers/discounts (vs historical baseline)
     - Total dispute value
     - Average time per dispute
     - Dispute win rate (if outcomes tracked)

2. **Dispute Volume Analysis**
   - Bar chart: disputes by port/facility
   - Bar chart: disputes by lane (port → destination)
   - Trend line: disputes over time
   - Filter by charge type (demurrage, detention, waiting, storage)

3. **Cost Impact Analysis**
   - Total disputed amount by port/facility
   - Total waived/saved amount by port/facility
   - Cost per dispute by facility type
   - ROI calculation (Ward cost vs savings)

4. **Performance Scorecards**
   - Facility scorecards:
     - Ports, ICDs, CFSs, warehouses, logistics parks
     - Dispute frequency
     - Average delay duration
     - Structural vs operational delay ratio
   - Carrier/CHA scorecards:
     - Dispute frequency
     - Delay attribution
     - Performance rating
   - Customer scorecards:
     - Dispute frequency
     - Operational friction incidents
     - Cost impact

5. **Lane Analysis**
   - Heat map: dispute frequency by lane
   - Cost analysis: which lanes drive most dispute costs
   - Trend analysis: improving vs deteriorating lanes
   - Export lane performance report

6. **Export & Share**
   - Export monthly review report (PDF/Excel)
   - Share with stakeholders
   - Set up automated monthly reports
   - Create action items (contract renegotiation, facility changes, carrier reviews)

**Outputs:**
- Monthly review dashboard (interactive)
- Performance scorecards (facilities, carriers, customers)
- Lane analysis report
- Exportable summary report (PDF/Excel)
- Metrics for contract/pricing decisions

**Success Criteria:**
- Dashboard loads in < 3 seconds
- Clear visibility into dispute patterns and costs
- Actionable insights for operations and finance decisions
- Measurable uplift in % contested and % waivers vs baseline

---

### Common Elements Across Flows

**Navigation:**
- Top nav: Invoices, Timelines, Reviews, Settings
- Search bar (always visible): search by container, truck, invoice, facility
- Quick actions: New dispute, Upload invoice, View dashboard

**Data Display:**
- All timestamps show "captured at" vs "edited at"
- GPS locations clickable (opens map)
- Voice recordings playable inline
- Documents viewable inline (PDF viewer)

**Export Formats:**
- PDF (for submission to ports/facilities)
- Excel (for internal tracking/analysis)
- JSON (for API integration)

**Permissions:**
- Finance: Full access to invoices, disputes, reviews
- Ops: Access to timelines, escalations, scorecards
- Legal: Access to dispute packets, investigation reports
- View-only: Read access to all data

---

## FromChaosToPacketSection Component (JSX/TSX)

