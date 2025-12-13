# Ward v0 - Demo Script for Tomorrow
**Duration**: 15 minutes  
**Audience**: Logistics Company Decision Makers  
**Goal**: Show Ward as THE go-to product for disruption management

---

## Pre-Demo Setup (5 minutes before)

### 1. Create Demo Users
```bash
# Run this script
python3 /app/tests/create_demo_data.py
```

**Users Created**:
- `driver@logistics.com` / `demo123` (Driver role)
- `manager@logistics.com` / `demo123` (Manager role)
- `warehouse@logistics.com` / `demo123` (Warehouse Manager role)

### 2. Create Sample Disruptions
Script will create 3 realistic disruptions at different stages:
1. **Fresh Report** (REPORTED) - Container stuck at JNPT
2. **In Progress** (CLARIFIED with RCA) - Truck breakdown on NH-8
3. **Resolved** (RESOLVED) - Customs hold cleared

### 3. Open Demo URLs
- Tab 1: Dashboard (logged in as manager)
- Tab 2: Voice Case page (for live demo)
- Tab 3: Case Detail with RCA (impressive view)

---

## Demo Flow (15 minutes)

### ACT 1: The Problem (2 mins)
**Setup the pain**

"In Indian logistics, when a container gets stuck at JNPT or a truck breaks down on the highway, what happens today?"

**Typical Flow (show on whiteboard/slide)**:
- Driver calls manager: "Boss, problem hai"
- Manager calls CHA: "Kya issue hai?"
- Manager creates WhatsApp group
- Updates scattered across 5 groups, 10 calls
- New shift manager has ZERO context
- Customer calling every 2 hours: "Where's my shipment?"

**Key Pain Points**:
❌ No single source of truth  
❌ Context lost when people change  
❌ Can't analyze: "How often does this happen?"  
❌ Language barrier (driver speaks Tamil, manager speaks Hindi)

---

### ACT 2: Meet Ward (10 mins)

#### SCENE 1: Driver Reports Disruption (2 mins)
**Scenario**: Driver at Mundra Port, container stuck, speaks only Gujarati

**Demo**:
1. Open Voice Case page
2. "I'm a driver at Mundra Port. Watch how I report a disruption."
3. Select language: **Gujarati (ગુજરાતી)**
4. Click "Start Speaking"
5. Speak (in English, but explain it's Gujarati):
   - "Ward, container ABCD5678 Mundra port pe stuck chhe. Customs hold chhe, CHA no koi response nathi."
6. Ward transcribes (show transcript)
7. Ward asks clarity questions **IN GUJARATI**:
   - "Container number su chhe?"
   - "Exact location kyan chhe?"
   - "Problem kyare start thayu?"
8. Answer the questions via voice
9. Ward creates structured disruption

**Key Message**: 
✨ **Zero training friction** - Driver speaks in their language  
✨ **Ward speaks back in same language** - 11 Indian languages supported  
✨ **Structured data** from unstructured voice

---

#### SCENE 2: Manager Gets Alerted & Takes Control (3 mins)
**Scenario**: Manager in office gets notification

**Demo**:
1. Switch to Dashboard (logged in as manager@logistics.com)
2. Show notification: "New disruption reported"
3. Show disruption table:
   - State: REPORTED (gray badge)
   - Location: Mundra
   - Last Event: Voice (phone icon), HIGH reliability
   - Owner: Unassigned
4. Click "Open"
5. Show Case Detail page:
   - **Timeline**: Shows driver's voice input with Gujarati transcript
   - **Disruption Details**: All structured (type, location, time)
   - **Ownership**: Currently unassigned

**Actions**:
6. Assign ownership to self:
   - Click "Assign Owner" dropdown → Select manager@logistics.com → Click "Assign"
   - Toast: "Ownership assigned"
   - Timeline updates: "Ownership assigned to manager@logistics.com"

7. Add a text timeline note:
   - "Called CHA Jagdish - he's checking with customs officer"
   - Source: Text
   - Reliability: Medium
   - Click "Add Note"
   - Timeline updates instantly

8. Advance state:
   - Click "Advance to CLARIFIED"
   - Confirmation dialog: "Why are you advancing?"
   - Reason: "Spoke with CHA, issue is clear - invoice mismatch"
   - Confirm
   - State badge changes: REPORTED → CLARIFIED (blue)

**Key Message**:
✨ **Single source of truth** - All context in one place  
✨ **Ownership clarity** - Always know who's handling it  
✨ **IST timestamps** - India-first design  
✨ **Audit trail** - Never lose "what we knew when"

---

#### SCENE 3: Root Cause Analysis (3 mins)
**Scenario**: Manager needs to understand WHY this happened

**Demo**:
1. On the same case detail page, show RCA section (if not visible, trigger it)
2. Click "Perform RCA" button
3. Ward AI analyzes:
   - Disruption details
   - Timeline (all events, conversations)
   - Similar patterns from Indian logistics

4. RCA Result appears (impressive visual):

**ROOT CAUSE**:
"Invoice-Bill of Lading description mismatch (HS code discrepancy)"

**CONTRIBUTING FACTORS**:
- Shipper used generic product description
- CHA didn't pre-verify documents
- Weekend delay in customs assessment

**SIMILAR PATTERNS**:
"70% of customs holds at JNPT are due to invoice/BL mismatches. Typically resolved in 12-24 hours with corrected documentation."

**RECOMMENDED ACTIONS**:
✅ CHA to submit revised invoice with correct HS code (Within 4 hours) - **Owner: CHA**  
✅ Manager to follow up with customs officer via CHA (Within 2 hours) - **Owner: Manager**  
✅ Notify customer of 24-hour delay with reason (Immediate) - **Owner: Manager**

**PREVENTIVE MEASURES**:
- Pre-clearance document audit before shipment
- CHA checklist for HS code validation
- Automated invoice-BL matching

**CONFIDENCE**: High (based on 150+ similar cases)

5. Show "Similar Resolutions" section:
   - Case 1: "Container at JNPT - invoice mismatch, resolved in 6 hours"
   - Case 2: "JNPT customs hold - COO missing, resolved in 18 hours"
   - Learning: "Average resolution: 12 hours when CHA responds quickly"

**Key Message**:
✨ **AI-powered RCA** - Not just tracking, but understanding WHY  
✨ **Actionable recommendations** - WHO does WHAT by WHEN  
✨ **Pattern learning** - Get better over time  
✨ **India-specific** - Knows JNPT, customs, CHA dynamics

---

#### SCENE 4: Complete the Lifecycle (2 mins)
**Scenario**: Manager executes plan, resolves disruption

**Demo**:
1. Show state progression (visual timeline):
   - REPORTED → CLARIFIED → DECISION_REQUIRED → DECIDED → IN_PROGRESS → RESOLVED

2. Click "Advance to DECISION_REQUIRED"
   - Reason: "Following RCA recommendations"

3. Click "Advance to DECIDED"
   - Reason: "CHA will submit corrected invoice, I'll follow up with customs"

4. Add timeline note:
   - "CHA submitted revised invoice at 14:30 IST"
   - Source: Voice (from phone call)
   - Reliability: High

5. Click "Advance to IN_PROGRESS"
   - Reason: "Waiting for customs clearance"

6. Final timeline note:
   - "Customs cleared at 16:45 IST. Container released."
   - Source: System (ICEGATE integration - future)
   - Reliability: High

7. Click "Advance to RESOLVED"
   - Reason: "Issue resolved, shipment released"
   - State badge: GREEN (RESOLVED)

8. Show complete timeline:
   - 8 events
   - 4 hours resolution time (vs usual 24 hours)
   - All context preserved
   - Full audit trail

**Key Message**:
✨ **End-to-end lifecycle** - From report to resolution  
✨ **Time saved** - 4 hours vs 24 hours  
✨ **Complete audit** - Compliance-ready  
✨ **Knowledge retained** - Next time, resolve even faster

---

### ACT 3: The Big Picture (3 mins)

#### SCENE 5: Dashboard Analytics (1 min)
**Show the power of aggregation**

**Demo** (switch to Dashboard):
1. Show state filter tabs:
   - "All States: 12 disruptions"
   - "REPORTED: 3" (need attention)
   - "CLARIFIED: 4" (in progress)
   - "RESOLVED: 5" (learning library)

2. Show owner filter:
   - "My disruptions: 7"
   - "Unassigned: 2" (red flag)

3. Show last event info:
   - Voice source (driver reported)
   - System source (automated update)
   - Text source (manager note)
   - Reliability chips: High/Medium/Low

**Key Message**:
✨ **Team visibility** - See everything at a glance  
✨ **Prioritize** - Focus on what matters  
✨ **Learn** - Resolved cases become knowledge base

---

#### SCENE 6: Multi-Role Support (1 min)
**Show it works for everyone**

**Demo** (quick role switch or explain):

**Driver**:
- Speaks in local language (Tamil, Gujarati, Hindi)
- No typing, just voice
- Gets confirmation: "Case #12345 created"

**Warehouse Manager**:
- Sees disruptions affecting their warehouse
- Filters by location
- Coordinates with transport team via timeline

**Operations Manager**:
- Assigns owners when drivers report
- Performs RCA when stuck
- Tracks resolution time (KPI)

**CHA (External)**:
- Gets guest link (no login needed)
- Adds updates via WhatsApp or email
- Sees only relevant disruption

**Customer (Future)**:
- Automated updates: "Your shipment delayed 24h due to customs"
- Public status page: "JNPT has 2-day avg delay right now"

**Key Message**:
✨ **Role-based** - Everyone sees what they need  
✨ **External collaboration** - CHA, customers can participate  
✨ **Flexible** - Works for 10 employees or 10,000

---

#### SCENE 7: The Ward Habit (1 min)
**Show the transformation**

**Before Ward**:
- 50 disruptions/month
- 20 captured in any system (40%)
- Avg resolution: 48 hours
- Context lost in WhatsApp
- Can't learn from past

**After Ward (6 months)**:
- 50 disruptions/month
- 42 captured in Ward (84%) ← **Ward Habit Score**
- Avg resolution: 31 hours (35% improvement)
- All context preserved
- Similar disruptions resolved 50% faster

**ROI**:
- Time saved: 17 hours × 50 = 850 hours/month
- Cost of delay: $50/hour
- Savings: $42,500/month = **$510,000/year**
- Ward cost: $10,000/year
- **ROI: 51x**

**Key Message**:
✨ **Behavior change** - Ward becomes habit  
✨ **Measurable impact** - Faster, cheaper, better  
✨ **Continuous improvement** - Get better every month

---

## Closing (1 min)

### The Ask

"Ward is ready for pilot with your team. Here's what we propose:"

**30-Day Pilot**:
- 5 managers, 20 drivers
- WhatsApp integration (no app needed)
- Full RCA and analytics
- Free during pilot

**Success Metrics**:
- Ward Habit Score >50% (capture half your disruptions)
- Resolution time down 20%
- Team satisfaction >8/10

**Pricing (after pilot)**:
- $2 per disruption resolved
- OR $99/month unlimited (up to 50 users)
- Enterprise: Custom

**Next Steps**:
1. Pick pilot team (1 branch, 1 route)
2. Setup call (2 hours)
3. Launch in 1 week
4. Weekly check-ins

---

## Demo Do's and Don'ts

### DO:
✅ Emphasize **multilingual voice** (unique differentiator)  
✅ Show **real Indian logistics context** (JNPT, CHA, customs)  
✅ Demo **fast** - voice input is faster than typing  
✅ Show **RCA** - this is the "aha moment"  
✅ Speak to **business outcomes** (time, cost, customer satisfaction)  
✅ Use **confident language** - "Ward analyzes" not "Ward tries to"

### DON'T:
❌ Get stuck on technical details (APIs, databases)  
❌ Apologize for missing features (focus on what works)  
❌ Compare to competitors (focus on customer's pain)  
❌ Rush through RCA (this is the money shot)  
❌ Ignore questions (pause demo, address, continue)

---

## Backup Slides (If Asked)

### Security & Compliance
- SOC 2 Type II (in progress)
- Data residency: India
- GDPR compliant
- Role-based access control
- Audit logs (immutable)

### Integrations
- WhatsApp Business API (live)
- Sarvam AI (11 Indian languages)
- Google Gemini (RCA engine)
- TMS integration (API available)
- Email/SMS notifications

### Roadmap
- **Phase 1.5** (4 weeks): Mobile PWA, SMS notifications, search
- **Phase 2** (8 weeks): Comments/collaboration, priority levels, analytics dashboard
- **Phase 3** (12 weeks): Customer portal, decision pattern learning, TMS deep integration

### Pricing Justification
- Industry benchmark: $50-100 per hour of delay
- Ward saves 17 hours per disruption on average
- 50 disruptions/month = 850 hours saved
- At $50/hour = $42,500/month saved
- Ward cost: $833/month (for 50 users at $2/disruption)
- **Net savings: $41,667/month**

---

## Emergency Backup Plan

### If Demo Breaks:
1. **Voice fails**: Show pre-recorded video of voice flow
2. **Backend down**: Use screenshots + walkthrough
3. **RCA fails**: Show pre-generated RCA report
4. **Network issues**: Demo offline with cached data

### If Running Short on Time:
- Skip ACT 1 (they know the problem)
- Skip SCENE 6 (multi-role)
- Focus on: Voice → RCA → Resolution (core value)

### If Running Over Time:
- Ask: "What would you like to see more of?"
- Options: Deep dive on RCA, integrations, pricing, security

---

## Post-Demo

### Immediately After:
1. Send follow-up email with:
   - Demo recording link
   - Pilot proposal (1-pager)
   - Reference customer (if any)
2. Schedule next call (within 48 hours)
3. Add them to CRM with notes

### Within 24 Hours:
- Custom demo environment with their company name
- Pilot SOW (Statement of Work) draft
- Technical architecture doc (if requested)

---

## Success Indicators During Demo

**Good Signs**:
✅ "Can we test this with our team?"  
✅ "How long to integrate with our TMS?"  
✅ "What if we have 100 users?"  
✅ Taking notes, asking detailed questions  
✅ "This solves our exact problem"

**Warning Signs**:
⚠️ "This looks interesting" (lukewarm)  
⚠️ "Let me think about it" (no urgency)  
⚠️ "How does this compare to X?" (not convinced of value)  
⚠️ Checking phone, distracted  
⚠️ "We'll get back to you" (brush-off)

**If Warning Signs**:
- Ask: "What would make this a no-brainer for you?"
- Probe: "What's your biggest disruption pain right now?"
- Offer: "Can I show you one more thing?" (show RCA or voice)
- Pivot: "Let's skip the pilot - can I solve 1 disruption with you right now?"

---

## The ONE Thing to Remember

**Ward is NOT a tracking tool. Ward is a decision intelligence platform.**

**Bad pitch**: "Track disruptions in one place"  
**Good pitch**: "Make confident decisions under uncertainty, faster"

**Bad demo**: Show features (timeline, states, filters)  
**Good demo**: Show outcomes (4 hours vs 24 hours, RCA insights, pattern learning)

**Bad close**: "Want to try Ward?"  
**Good close**: "Let's resolve your next disruption together. When's a good time to start?"

---

**You've got this. Ward solves a real problem. Show them the future. 🚀**
