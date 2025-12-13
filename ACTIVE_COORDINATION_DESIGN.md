# Ward v0 - Active Coordination Design
**From Passive Tracker → Active Coordinator**

---

## The Gap You Identified

**Current Workflow** (Stops Too Early):
1. ✅ Driver reports via voice: "Container stuck at JNPT"
2. ✅ Ward transcribes and creates case
3. ✅ Manager sees it on dashboard
4. ❌ **STOPS HERE** - Manager has to manually call everyone
5. ❌ RCA based only on initial report (incomplete data)
6. ❌ No automatic follow-up to reporter

**Missing**: Ward should actively coordinate the entire resolution process

---

## The Complete Active Workflow

### Phase 1: Initial Report (Current - Works)
**Driver** (08:00): Voice report in Gujarati
> "Container ABCD1234 JNPT pe stuck chhe. Gate pe customs hold bola."

**Ward** (08:00):
- Transcribes
- Creates case (REPORTED)
- Asks clarity questions via voice
- Notifies manager

### Phase 2: Active Data Collection (NEW - Need to Build) ⭐

**Ward** (08:05): Identifies stakeholders needed
```
Based on "JNPT customs hold", Ward knows to contact:
1. CHA (Customs House Agent) - has customs details
2. Port operations - has container location
3. Shipping line - has documentation status
```

**Ward** (08:06): Initiates outreach
- Sends WhatsApp to CHA: "Container ABCD1234 stuck. What's the customs status?"
- Sends SMS to port ops: "Container ABCD1234 location?"
- Calls shipping line API (if integrated)

**Ward** (08:10-08:30): Collects responses
- CHA replies (WhatsApp): "Invoice-BL mismatch. Assessment pending with Officer Sharma."
- Port ops replies (SMS): "Container at Gate 7, awaiting clearance"
- Shipping line API: "BL shows 'Electronics', invoice shows 'Computer Parts'"

**Ward** (08:31): Updates timeline automatically
- All 3 responses logged with timestamps
- Reliability tagged (CHA = high, port ops = high, API = high)
- Manager sees real-time updates

### Phase 3: Enhanced RCA (NEW - Need to Build) ⭐

**Ward** (08:35): Performs RCA with ALL data
```
Input to RCA:
- Initial report: "Customs hold at JNPT"
- CHA response: "Invoice-BL mismatch, Officer Sharma"
- Port response: "Gate 7"
- API data: "BL vs invoice discrepancy"
- Time: "30 mins since discovery"
```

**Ward AI** (08:37): Comprehensive RCA
```json
{
  "root_cause": "Invoice description 'Computer Parts' doesn't match BL 'Electronics' (HS code discrepancy)",
  "immediate_blocker": "Customs Officer Sharma awaiting corrected invoice",
  "responsible_party": "Shipper (incorrect invoice prepared)",
  "contributing_factors": [
    "CHA didn't pre-verify documents before submission",
    "No automated invoice-BL validation at origin"
  ],
  "data_sources_used": ["CHA", "Shipping Line API", "Port Ops"],
  "confidence": "high",
  "estimated_resolution_time": "4-6 hours (if corrected invoice submitted within 2 hours)",
  "similar_cases": "12 similar JNPT invoice mismatches resolved in avg 6 hours"
}
```

### Phase 4: Decision Support with Stakeholder Input (NEW) ⭐

**Ward** (08:38): Generates action plan
```
RECOMMENDED ACTIONS:

1. [URGENT] Contact shipper for corrected invoice
   - Owner: Manager
   - Deadline: Within 1 hour
   - Ward will: Prepare invoice correction template

2. [URGENT] CHA to prepare for resubmission
   - Owner: CHA (Jagdish)
   - Deadline: Within 2 hours
   - Ward will: Send checklist, notify when shipper sends invoice

3. [MEDIUM] Follow up with Customs Officer Sharma
   - Owner: CHA
   - Deadline: After invoice resubmission
   - Ward will: Track submission status

4. [LOW] Update customer on 6-hour delay
   - Owner: Customer Service
   - Deadline: Within 30 mins
   - Ward will: Draft customer message
```

**Ward** (08:39): Seeks approval from decision owner
**WhatsApp to Manager**:
> "Container ABCD1234 RCA complete.
> 
> Root Cause: Invoice-BL mismatch (Computer Parts vs Electronics)
> Resolution: Corrected invoice needed
> Time: 4-6 hours if we act now
> 
> I've prepared 4 actions. Approve to execute?
> 
> [Approve] [Modify] [View Details]"

### Phase 5: Active Execution (NEW - Need to Build) ⭐

**Manager** (08:42): Clicks "Approve"

**Ward** (08:43): Executes action plan

**Action 1: Contact Shipper**
- Ward sends WhatsApp to shipper contact:
  > "Urgent: Container ABCD1234 held at JNPT customs.
  > Issue: Invoice shows 'Computer Parts', BL shows 'Electronics'
  > 
  > Please send corrected invoice with 'Electronics' within 1 hour.
  > 
  > Template attached. Reply here when sent."

**Action 2: Prepare CHA**
- Ward sends WhatsApp to CHA Jagdish:
  > "Corrected invoice coming from shipper within 1 hour.
  > 
  > Next steps:
  > ✓ Verify invoice matches BL exactly
  > ✓ Submit to Officer Sharma
  > ✓ Get OOC (Out of Charge)
  > 
  > I'll notify you when shipper sends invoice.
  > Checklist: [link]"

**Action 3: Queue Follow-up**
- Ward sets reminder: "Check with CHA in 2 hours"

**Action 4: Draft Customer Message**
- Ward prepares draft for customer service:
  > "Your shipment ABCD1234 delayed 4-6 hours due to customs document correction. 
  > We're actively resolving. Updated ETA: [original + 6 hours]."

### Phase 6: Active Monitoring (NEW) ⭐

**Ward** (09:00-11:00): Monitors progress

**09:15** - Shipper replies on WhatsApp:
> "Invoice sent. Attached."

**Ward** (09:16): 
- Downloads invoice
- Verifies: "Electronics" matches BL ✓
- Forwards to CHA Jagdish:
  > "Corrected invoice received from shipper. Verified correct.
  > Please submit to Officer Sharma now."
- Updates timeline with "Invoice corrected" event

**10:30** - CHA replies:
> "Submitted to Officer Sharma. Waiting for assessment."

**Ward** (10:31):
- Updates timeline: "Assessment in progress"
- Sends reminder to manager:
  > "Update: CHA submitted corrected invoice. Assessment pending. ETA: 1-2 hours."

**11:45** - CHA replies:
> "OOC received. Cleared."

**Ward** (11:46):
- Updates timeline: "Customs cleared"
- Transitions case: DECIDED → IN_PROGRESS → RESOLVED
- **Calculates**: Total time 3h 46m (vs usual 24h)

### Phase 7: Close the Loop (NEW - Need to Build) ⭐

**Ward** (11:47): Notifies EVERYONE involved

**To Driver** (Original Reporter) via WhatsApp:
> "✅ Container ABCD1234 cleared!
> 
> Issue: Invoice mismatch (you reported it at 08:00)
> Resolution: Corrected invoice submitted, customs cleared
> Total time: 3h 46m
> 
> Thanks for quick reporting. Container ready for delivery.
> 
> [View Full Timeline]"

**To Manager** via WhatsApp:
> "✅ Case ABCD1234 RESOLVED
> 
> Resolution time: 3h 46m (84% faster than avg 24h)
> 
> What worked:
> - Quick stakeholder coordination (CHA + shipper)
> - Corrected invoice submitted in 1h 15m
> 
> Post-Resolution Survey: How did Ward help? [Link]"

**To CHA** via WhatsApp:
> "✅ Container ABCD1234 cleared. Thanks for quick turnaround!
> 
> Timeline for your records: [PDF attached]"

**To Customer Service**:
> "✅ ABCD1234 cleared. Customer update:
> 'Your shipment cleared customs. New ETA: [time]. Delay was 4 hours (not 6 hours as estimated).'"

---

## The New Enhanced Workflow (Summary)

```
08:00 | Driver reports via voice
      ↓
08:05 | Ward identifies stakeholders (CHA, port, shipper)
      ↓
08:06 | Ward reaches out (WhatsApp, SMS, API)
      ↓
08:30 | Ward collects all responses
      ↓
08:35 | Ward performs RCA with complete data
      ↓
08:38 | Ward generates action plan
      ↓
08:39 | Ward asks manager for approval
      ↓
08:43 | Ward executes (sends messages, sets reminders)
      ↓
09:00-11:00 | Ward monitors and coordinates
      ↓
11:45 | Issue resolved
      ↓
11:47 | Ward notifies everyone (close the loop)
```

**Key Difference**: Ward is ACTIVE, not passive

---

## Technical Implementation Plan

### New Backend Components Needed

#### 1. Stakeholder Identifier Service
```python
class StakeholderIdentifier:
    def identify_stakeholders(self, disruption_type, location):
        """
        Based on disruption type and location, identify who to contact
        """
        stakeholders = {
            "customs_hold": {
                "required": ["CHA", "shipping_line"],
                "optional": ["customs_officer", "port_ops"]
            },
            "truck_breakdown": {
                "required": ["driver", "mechanic"],
                "optional": ["depot_manager", "alternate_truck"]
            },
            "port_congestion": {
                "required": ["port_ops", "shipping_line"],
                "optional": ["alternate_port"]
            }
        }
        return stakeholders.get(disruption_type, [])
```

#### 2. Outreach Orchestrator
```python
class OutreachOrchestrator:
    async def initiate_outreach(self, case_id, stakeholders):
        """
        Send messages to all stakeholders
        Returns: tracking_ids for responses
        """
        tasks = []
        for stakeholder in stakeholders:
            if stakeholder.channel == "whatsapp":
                task = self.send_whatsapp(stakeholder, message)
            elif stakeholder.channel == "sms":
                task = self.send_sms(stakeholder, message)
            elif stakeholder.channel == "email":
                task = self.send_email(stakeholder, message)
            tasks.append(task)
        
        return await asyncio.gather(*tasks)
```

#### 3. Response Collector
```python
class ResponseCollector:
    async def collect_responses(self, case_id, timeout_minutes=30):
        """
        Listen for responses from stakeholders
        Update timeline as responses come in
        """
        responses = []
        deadline = datetime.now() + timedelta(minutes=timeout_minutes)
        
        while datetime.now() < deadline:
            # Check WhatsApp webhook for replies
            # Check SMS webhook for replies
            # Check email inbox for replies
            
            if new_response:
                responses.append(new_response)
                await self.update_timeline(case_id, new_response)
        
        return responses
```

#### 4. Enhanced RCA Engine (Upgrade Current)
```python
class EnhancedRCAEngine:
    async def analyze_with_stakeholder_data(
        self,
        disruption_data,
        initial_timeline,
        stakeholder_responses  # NEW
    ):
        """
        RCA with all collected data, not just initial report
        """
        context = self._build_rich_context(
            disruption_data,
            initial_timeline,
            stakeholder_responses
        )
        
        # Enhanced prompt includes stakeholder insights
        prompt = f"""
        Analyze this disruption with data from multiple sources:
        
        INITIAL REPORT: {disruption_data}
        
        STAKEHOLDER RESPONSES:
        {stakeholder_responses}
        
        Perform RCA considering all sources. Identify:
        1. Root cause (with evidence from stakeholders)
        2. Immediate blocker
        3. Responsible party
        4. Action plan with specific owners
        5. Estimated resolution time
        """
```

#### 5. Action Executor
```python
class ActionExecutor:
    async def execute_action_plan(self, case_id, actions, approval):
        """
        Execute approved actions
        """
        if not approval:
            return
        
        for action in actions:
            if action.type == "notify_stakeholder":
                await self.send_notification(action.owner, action.message)
            elif action.type == "set_reminder":
                await self.schedule_reminder(action.deadline, action.callback)
            elif action.type == "update_external_system":
                await self.call_external_api(action.system, action.data)
            
            # Log execution
            await self.log_action_execution(case_id, action)
```

#### 6. Loop Closer
```python
class LoopCloser:
    async def notify_all_parties(self, case_id, resolution_summary):
        """
        Close the loop with everyone involved
        """
        case = await self.get_case(case_id)
        
        # Notify reporter
        await self.notify_reporter(
            case.reporter,
            "✅ Issue you reported is resolved",
            resolution_summary
        )
        
        # Notify decision owner
        await self.notify_decision_owner(
            case.decision_owner,
            "✅ Case resolved",
            performance_metrics
        )
        
        # Notify all stakeholders who contributed
        for stakeholder in case.contributors:
            await self.notify_contributor(
                stakeholder,
                "✅ Issue resolved, thanks for help"
            )
```

---

## New API Endpoints Needed

### 1. Stakeholder Management
```
POST /api/cases/{case_id}/identify-stakeholders
- Identifies who to contact based on disruption type

POST /api/cases/{case_id}/initiate-outreach
- Sends messages to identified stakeholders
- Returns tracking IDs

GET /api/cases/{case_id}/stakeholder-responses
- Get all responses collected
```

### 2. Enhanced RCA
```
POST /api/cases/{case_id}/rca-with-stakeholders
- Performs RCA with complete data (not just initial report)
- Includes stakeholder responses in analysis
```

### 3. Action Planning
```
POST /api/cases/{case_id}/generate-action-plan
- Creates action plan with specific owners and deadlines

POST /api/cases/{case_id}/execute-actions
- Executes approved action plan
- Sends notifications, sets reminders
```

### 4. Loop Closure
```
POST /api/cases/{case_id}/close-loop
- Notifies all parties involved
- Sends resolution summary
- Collects feedback
```

---

## WhatsApp Integration (Critical)

### Inbound Handling
```python
@app.post("/api/webhooks/whatsapp/message")
async def handle_whatsapp_message(webhook_data):
    """
    Handle incoming WhatsApp messages
    """
    from_number = webhook_data["from"]
    message = webhook_data["message"]
    
    # Identify: Is this a new disruption or response to existing case?
    if is_new_disruption(message):
        # Create case
        case_id = await create_case_from_whatsapp(message, from_number)
        await send_whatsapp_confirmation(from_number, case_id)
    else:
        # Response to existing outreach
        case_id = identify_case_from_context(from_number, message)
        await add_stakeholder_response(case_id, from_number, message)
        await trigger_rca_if_all_responses_collected(case_id)
```

### Outbound Sending
```python
async def send_whatsapp_to_stakeholder(phone_number, message, case_id):
    """
    Send WhatsApp message to stakeholder
    Track in timeline
    """
    # WhatsApp Business API call
    response = await whatsapp_api.send_message(
        to=phone_number,
        body=message,
        context_id=case_id  # For threading
    )
    
    # Log in timeline
    await db.timeline_events.insert_one({
        "case_id": case_id,
        "actor": "Ward AI",
        "action": "STAKEHOLDER_CONTACTED",
        "content": f"Sent WhatsApp to {phone_number}: {message}",
        "source_type": "system",
        "reliability": "high",
        "timestamp": datetime.now(timezone.utc),
        "metadata": {"message_id": response.id}
    })
```

---

## UI Changes Needed

### 1. Case Detail Page - Add "Active Coordination" Section
```
Current:
├─ Timeline
├─ State Transition
├─ RCA
└─ Add Note

New:
├─ Timeline
├─ Active Coordination (NEW) ⭐
│  ├─ Stakeholders Contacted (3)
│  │  ├─ CHA Jagdish: Responded 10 mins ago ✓
│  │  ├─ Port Ops: Responded 5 mins ago ✓
│  │  └─ Shipper: Waiting... (sent 15 mins ago)
│  ├─ Action Plan Status
│  │  ├─ Action 1: In progress (Owner: Manager)
│  │  ├─ Action 2: Completed ✓ (Owner: CHA)
│  │  └─ Action 3: Pending (Owner: CS)
│  └─ [Initiate Coordination] button
├─ State Transition
├─ RCA (Enhanced)
└─ Add Note
```

### 2. Dashboard - Add "Awaiting Response" Filter
```
Current tabs:
├─ All States
├─ REPORTED
├─ CLARIFIED
└─ ...

New tabs:
├─ All States
├─ REPORTED
├─ CLARIFIED
├─ Awaiting Stakeholder Response (NEW) ⭐
└─ ...
```

---

## Demo Script Updates (For Tomorrow)

### New Flow to Demo:

**After showing voice capture and initial RCA:**

> "Now watch what Ward does next - this is where it gets powerful.
> 
> Based on 'customs hold at JNPT', Ward knows it needs input from:
> - CHA (has customs details)
> - Shipping line (has documentation)
> 
> So Ward automatically reaches out..."

**[Show UI: Stakeholder Outreach Section]**

> "WhatsApp sent to CHA: 'What's the customs status?'
> WhatsApp sent to shipper: 'Need your documentation details'
> 
> [Simulate responses coming in]
> 
> CHA replies: 'Invoice-BL mismatch, Officer Sharma handling'
> Shipper replies: 'BL shows Electronics, invoice says Computer Parts'
> 
> Now Ward has complete data - not just driver's initial report.
> 
> Ward performs enhanced RCA..."

**[Show: Enhanced RCA with stakeholder data]**

> "Root Cause: HS code mismatch
> Immediate Blocker: Officer Sharma awaiting corrected invoice
> Responsible: Shipper (incorrect invoice)
> 
> Action Plan generated:
> 1. Contact shipper for corrected invoice (Manager, 1 hour)
> 2. CHA prepares for resubmission (CHA, 2 hours)
> 3. Follow up with Officer Sharma (CHA, after submission)
> 
> Manager approves action plan with one click.
> 
> Ward executes:
> - Sends WhatsApp to shipper with invoice template
> - Sends WhatsApp to CHA with checklist
> - Sets reminder to follow up
> 
> [Fast forward]
> 
> Shipper sends corrected invoice → Ward forwards to CHA
> CHA submits → Ward tracks status
> Cleared → Ward notifies EVERYONE
> 
> Most importantly: Ward notifies the DRIVER who first reported it:
> '✅ Container cleared! Issue you reported at 08:00 is resolved. Total time: 3h 46m'"

**Impact**:
> "This is the difference:
> - **Without Ward**: Manager makes 12 calls, 3 WhatsApp groups, 24 hours
> - **With Ward**: Ward coordinates everyone, manager approves plan, 4 hours
> 
> Ward doesn't just track. Ward actively coordinates."

---

## Implementation Priority

### Phase 1 (Next 2 Weeks) - Critical for Demo
1. ✅ WhatsApp Business API integration
2. ✅ Stakeholder identification logic
3. ✅ Outreach orchestrator (send messages)
4. ✅ Response collector (receive & log)
5. ✅ Enhanced RCA (with stakeholder data)

### Phase 2 (Weeks 3-4) - Full Coordination
6. ✅ Action plan generator
7. ✅ Action executor
8. ✅ Reminder system
9. ✅ Loop closer (notify all parties)

### Phase 3 (Month 2) - Intelligence Layer
10. ✅ Learn optimal stakeholders per disruption type
11. ✅ Predict resolution time based on stakeholder response speed
12. ✅ Auto-escalate if stakeholders don't respond

---

## Bottom Line

**Current Ward**: Driver reports → RCA → Manager acts manually  
**New Ward**: Driver reports → Ward coordinates ALL stakeholders → RCA with complete data → Action plan executed → Everyone notified

**The shift**: From **passive tracker** to **active coordinator**

This is the missing piece that makes Ward 10x more valuable.
