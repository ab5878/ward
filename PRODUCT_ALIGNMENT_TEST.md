# Product Alignment Test Plan
**Date:** December 2024  
**Purpose:** Verify all functionality aligns with Ward's problem statement and solution

---

## Problem Statement Alignment

### Core Problems Ward Solves:
1. **Information Gap:** 90% of field intelligence locked in phone calls/WhatsApp
2. **Coordination Tax:** 40% of manager time on low-value follow-ups
3. **Unorganized Barrier:** 85% of sector can't use legacy software (language/literacy)
4. **Financial Bleed:** Demurrage/detention losses accepted as "business as usual"

### Ward's One Job:
> "When something goes wrong in transit, give you proof fast enough to stop the meter and strong enough to win disputes."

---

## Test Checklist

### ✅ 1. Signin & Access (Foundation)
- [ ] User can register
- [ ] User can login
- [ ] Dashboard loads after signin
- [ ] User can see cases list
- [ ] Navigation works

### ✅ 2. Case Creation (Problem: Capture Disruption)
**Requirement:** Fast capture (≤5 seconds from incident to log)

- [ ] Can create case via form
- [ ] Case creation is fast (<5 seconds)
- [ ] Required fields are minimal
- [ ] Voice-first option available (if implemented)
- [ ] Case appears in dashboard immediately
- [ ] Case has correct status (REPORTED)

**UX Check:**
- [ ] No complex forms
- [ ] Mobile-friendly
- [ ] Clear error messages

### ✅ 3. Timeline/Event Logging (Solution: Evidence Capture)
**Requirement:** Capture 100% of field data, timestamped, geo-tagged

- [ ] Can add timeline event
- [ ] Event has timestamp
- [ ] Event has source type (voice/text/system)
- [ ] Event has reliability level
- [ ] Events appear in chronological order
- [ ] Can add multiple events quickly
- [ ] Events are immutable (audit trail)

**UX Check:**
- [ ] Quick add (one click/tap)
- [ ] No typing required for voice events
- [ ] Visual timeline is clear

### ✅ 4. Evidence Scoring (Solution: Audit-Grade Evidence)
**Requirement:** Real-time 0-100% score, turns green at 70%

- [ ] Evidence score displays on case detail
- [ ] Score updates automatically when events/documents added
- [ ] Score breakdown shows (voice +30, transcript +10, etc.)
- [ ] Missing actions are listed
- [ ] Score turns green at 70%+
- [ ] "Evidence Ready" indicator appears at 70%+

**UX Check:**
- [ ] Visual gauge is clear
- [ ] Breakdown is actionable
- [ ] Missing actions are specific

### ✅ 5. Dispute Packet Generation (Solution: Stop the Meter)
**Requirement:** One-click export, includes audio/transcript/timeline/docs

- [ ] Dispute button visible on case detail
- [ ] Can generate dispute packet
- [ ] Export includes:
  - [ ] Original audio (if available)
  - [ ] Certified transcript
  - [ ] Timeline log
  - [ ] Documents
  - [ ] Responsibility report
- [ ] Export is downloadable (ZIP/PDF)
- [ ] Export is fast (<30 seconds)

**UX Check:**
- [ ] One-click action
- [ ] Clear progress indicator
- [ ] Download works

### ✅ 6. Responsibility Attribution (Solution: Clear Attribution)
**Requirement:** AI analyzes timeline/docs to assign primary responsible party

- [ ] Responsibility card displays on case detail
- [ ] Can trigger responsibility analysis
- [ ] Analysis shows:
  - [ ] Primary responsible party
  - [ ] Confidence level
  - [ ] Reasoning (cites evidence)
- [ ] Analysis updates when new evidence added

**UX Check:**
- [ ] Clear attribution
- [ ] Reasoning is specific
- [ ] Confidence level is visible

### ✅ 7. Voice/Multilingual Features (Solution: Zero-Typing Interface)
**Requirement:** Voice-first, 10+ Indian languages, no training required

- [ ] Voice recording option available
- [ ] Can record voice note
- [ ] Voice is transcribed
- [ ] Transcript is timestamped
- [ ] Language selection available (if implemented)
- [ ] Voice events appear in timeline

**UX Check:**
- [ ] One-tap record
- [ ] Works on mobile
- [ ] Clear recording indicator

### ✅ 8. Mobile-First UX (Solution: Unorganized Barrier)
**Requirement:** Works for 85% of sector (low literacy, mobile-only)

- [ ] Dashboard is mobile-responsive
- [ ] Forms are mobile-friendly
- [ ] Buttons are large enough for touch
- [ ] Text is readable on small screens
- [ ] Navigation works on mobile
- [ ] No complex interactions

**UX Check:**
- [ ] Test on mobile viewport (375px)
- [ ] Touch targets ≥44px
- [ ] No horizontal scroll

### ✅ 9. Speed & Performance (Solution: Fast Enough to Stop Meter)
**Requirement:** ≤5 seconds from incident to log

- [ ] Page loads <2 seconds
- [ ] Case creation <5 seconds
- [ ] Event addition <3 seconds
- [ ] Dashboard loads <2 seconds
- [ ] No laggy interactions

**Performance Check:**
- [ ] Network throttling test (3G)
- [ ] Large dataset test (100+ cases)

### ✅ 10. Financial Impact Visibility (Solution: Stop Financial Bleed)
**Requirement:** Show demurrage risk, financial impact

- [ ] Financial impact card displays
- [ ] Shows currency and amount
- [ ] Risk level is visible
- [ ] Links to dispute packet

**UX Check:**
- [ ] Financial data is prominent
- [ ] Clear call-to-action

---

## Test Execution

### Manual Test Script

1. **Signin Test**
   ```bash
   # Register new user
   curl -X POST http://localhost:8001/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email": "test@ward.com", "password": "Test123!"}'
   
   # Login
   curl -X POST http://localhost:8001/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "test@ward.com", "password": "Test123!"}'
   ```

2. **Case Creation Test**
   ```bash
   # Create case (should be fast)
   time curl -X POST http://localhost:8001/api/cases \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "description": "Container stuck at JNPT gate",
       "disruption_details": {
         "disruption_type": "customs_hold",
         "identifier": "JNPT-GATE-4"
       }
     }'
   ```

3. **Evidence Scoring Test**
   ```bash
   # Add voice event (should auto-calculate score)
   curl -X POST http://localhost:8001/api/cases/{case_id}/timeline \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "content": "Driver called: stuck at gate",
       "source_type": "voice",
       "reliability": "high"
     }'
   
   # Check evidence score
   curl http://localhost:8001/api/cases/{case_id}/evidence \
     -H "Authorization: Bearer $TOKEN"
   ```

4. **Responsibility Attribution Test**
   ```bash
   # Analyze responsibility
   curl -X POST http://localhost:8001/api/cases/{case_id}/responsibility/analyze \
     -H "Authorization: Bearer $TOKEN"
   ```

5. **Dispute Packet Test**
   ```bash
   # Generate dispute packet
   curl -X POST http://localhost:8001/api/cases/{case_id}/dispute/export \
     -H "Authorization: Bearer $TOKEN" \
     -o dispute_packet.zip
   ```

---

## Expected Results

### ✅ Alignment with Problem Statement

1. **Information Gap:** ✅ Solved
   - Voice capture captures 100% of field data
   - Timeline logs all events
   - No data lost in phone calls

2. **Coordination Tax:** ⚠️ Partially Solved
   - Timeline reduces follow-ups
   - Active coordination (if implemented) would fully solve

3. **Unorganized Barrier:** ✅ Solved
   - Voice-first = no typing
   - Mobile-friendly
   - Simple interface

4. **Financial Bleed:** ✅ Solved
   - Evidence score = defensible proof
   - Dispute packet = ready to fight
   - Financial impact visible

### ✅ Alignment with Solution

1. **Fast Enough:** ✅
   - Case creation <5 seconds
   - Event addition <3 seconds

2. **Strong Enough:** ✅
   - Evidence score = audit-grade
   - Dispute packet = complete
   - Responsibility attribution = clear

---

## Gaps & Recommendations

### Critical Gaps
1. **Voice Recording:** Not fully implemented in frontend
2. **Mobile PWA:** Not implemented
3. **Offline Support:** Not implemented
4. **Active Coordination:** Not fully implemented

### Recommendations
1. Implement voice recording UI component
2. Add PWA support for offline use
3. Implement active coordination agents
4. Add mobile-specific navigation (bottom nav)
5. Add onboarding flow for new users

---

**Last Updated:** December 2024

