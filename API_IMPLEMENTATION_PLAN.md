# Ward API v0 Implementation Plan

**Date:** December 2024  
**Status:** Gap Analysis Complete

---

## 📊 Current State vs API v0 Spec

### ✅ Already Implemented

1. **Authentication**
   - ✅ POST `/api/auth/register`
   - ✅ POST `/api/auth/login`
   - ✅ GET `/api/auth/me`

2. **Cases (Maps to Movements in API v0)**
   - ✅ POST `/api/cases` (create)
   - ✅ GET `/api/cases` (list)
   - ✅ GET `/api/cases/{case_id}` (get)
   - ✅ POST `/api/cases/{case_id}/timeline` (add event)
   - ✅ GET `/api/cases/{case_id}/timeline` (get events)

3. **Timeline Events**
   - ✅ POST `/api/cases/{case_id}/timeline`
   - ✅ GET `/api/cases/{case_id}/timeline`

4. **Documents**
   - ✅ POST `/api/cases/{case_id}/documents/analyze`
   - ✅ GET `/api/cases/{case_id}/documents`

5. **Analytics**
   - ✅ GET `/api/analytics/dashboard`

6. **Voice/Transcription**
   - ✅ POST `/api/voice/transcribe`
   - ✅ POST `/api/voice/extract-disruption`

---

## ❌ Missing from API v0 Spec

### 1. **Movement Endpoints** (Currently using "cases" - need to align)

**API v0 Spec:**
- POST `/api/v0/movements` - Create movement
- GET `/api/v0/movements` - List movements
- GET `/api/v0/movements/{movement_id}` - Get movement
- PATCH `/api/v0/movements/{movement_id}` - Update movement
- GET `/api/v0/movements/{movement_id}/events` - Get events for movement

**Current:** Using `/api/cases` - need to either:
- Option A: Add `/api/v0/movements` endpoints that wrap cases
- Option B: Rename cases to movements (breaking change)
- Option C: Keep both for backward compatibility

**Recommendation:** Option A - Add new endpoints, keep cases for backward compatibility

### 2. **Facility Endpoints** (Not implemented)

**API v0 Spec:**
- POST `/api/v0/facilities` - Create facility
- GET `/api/v0/facilities` - List facilities
- GET `/api/v0/facilities/{facility_id}` - Get facility
- PATCH `/api/v0/facilities/{facility_id}` - Update facility
- GET `/api/v0/facilities/{facility_id}/movements` - Get movements for facility

**Status:** ❌ Not implemented

**Priority:** High (needed for web console workflow)

### 3. **Party Endpoints** (Not implemented)

**API v0 Spec:**
- POST `/api/v0/parties` - Create party
- GET `/api/v0/parties` - List parties
- GET `/api/v0/parties/{party_id}` - Get party
- PATCH `/api/v0/parties/{party_id}` - Update party
- GET `/api/v0/parties/{party_id}/movements` - Get movements for party

**Status:** ❌ Not implemented

**Priority:** High (needed for dispute attribution)

### 4. **DisputePacket Endpoints** (Not implemented)

**API v0 Spec:**
- POST `/api/v0/movements/{movement_id}/dispute-packets` - Create dispute packet
- GET `/api/v0/movements/{movement_id}/dispute-packets` - List dispute packets
- GET `/api/v0/dispute-packets/{packet_id}` - Get dispute packet
- POST `/api/v0/dispute-packets/{packet_id}/export` - Export as PDF
- PATCH `/api/v0/dispute-packets/{packet_id}` - Update dispute packet

**Status:** ❌ Not implemented (but `DisputeBundleService` exists)

**Priority:** Critical (core value proposition)

### 5. **Attachment Endpoints** (Partially implemented)

**API v0 Spec:**
- POST `/api/v0/events/{event_id}/attachments` - Upload attachment
- GET `/api/v0/events/{event_id}/attachments` - List attachments
- GET `/api/v0/attachments/{attachment_id}` - Get attachment
- DELETE `/api/v0/attachments/{attachment_id}` - Delete attachment

**Current:** Documents are stored but not as structured attachments

**Priority:** Medium (needed for mobile app)

---

## 🎯 Implementation Priority

### Phase 1: Critical (Week 1)
1. **DisputePacket Endpoints** - Core value proposition
   - POST `/api/v0/movements/{movement_id}/dispute-packets`
   - GET `/api/v0/dispute-packets/{packet_id}`
   - POST `/api/v0/dispute-packets/{packet_id}/export`

2. **Facility Endpoints** - Needed for web console
   - POST `/api/v0/facilities`
   - GET `/api/v0/facilities`
   - GET `/api/v0/facilities/{facility_id}`

### Phase 2: High Priority (Week 2)
3. **Party Endpoints** - Needed for dispute attribution
   - POST `/api/v0/parties`
   - GET `/api/v0/parties`
   - GET `/api/v0/parties/{party_id}`

4. **Movement Endpoints** - Align with API v0 spec
   - POST `/api/v0/movements`
   - GET `/api/v0/movements`
   - GET `/api/v0/movements/{movement_id}`

### Phase 3: Medium Priority (Week 3)
5. **Attachment Endpoints** - Mobile app support
   - POST `/api/v0/events/{event_id}/attachments`
   - GET `/api/v0/attachments/{attachment_id}`

6. **Enhanced Event Endpoints** - Mobile app support
   - POST `/api/v0/movements/{movement_id}/events` (with GPS, device ID, etc.)

---

## 📝 Implementation Notes

### Database Schema Updates Needed

1. **Facilities Table**
   - Already exists in `supabase/migrations/001_initial_schema.sql`?
   - Check and update if needed

2. **Parties Table**
   - Already exists in schema?
   - Check and update if needed

3. **DisputePackets Table**
   - Need to create if doesn't exist
   - Link to movements and events

4. **Attachments Table**
   - Need to create if doesn't exist
   - Link to events

### Backward Compatibility

- Keep existing `/api/cases` endpoints working
- Add new `/api/v0/*` endpoints
- Gradually migrate frontend to use v0 endpoints
- Document migration path

---

## 🚀 Next Steps

1. ✅ Review database schema for Facilities, Parties, DisputePackets, Attachments
2. ⏳ Implement DisputePacket endpoints (Phase 1)
3. ⏳ Implement Facility endpoints (Phase 1)
4. ⏳ Implement Party endpoints (Phase 2)
5. ⏳ Implement Movement endpoints (Phase 2)
6. ⏳ Implement Attachment endpoints (Phase 3)
7. ⏳ Update frontend to use new endpoints
8. ⏳ Write integration tests

---

**Last Updated:** December 2024

