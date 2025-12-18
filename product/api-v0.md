# Ward API v0 Specification

**Version:** 1.0  
**Date:** December 2024  
**Status:** Ready for Engineering  
**Base URL:** `https://api.ward.ai/v0` (or customer-specific subdomain)

---

## 1. Principles & Scope

### 1.1 Core Principle

**Ward is the evidence layer, not the system of record for shipments/orders.**

- Ward does NOT own: orders, shipments, inventory, bookings, routes, capacity
- Ward DOES own: events, delays, incidents, evidence, dispute packets, audit trails

### 1.2 Integration Model

**External systems push context in and pull evidence out.**

- **Push context:** TMS/WMS/PMS/marketplaces push movement context (container IDs, routes, parties, facilities) to Ward
- **Pull evidence:** External systems query Ward for timelines, events, and dispute packets when needed

### 1.3 Ward's Role

- **Captures:** Incidents and delays at the moment of friction (via mobile app)
- **Preserves:** Temporal truth with tamper-evident audit trail
- **Generates:** Dispute packets and investigation timelines
- **Exports:** Evidence in formats suitable for disputes and legal proceedings

### 1.4 What Ward Does NOT Do

- Does NOT manage orders or shipments (TMS does this)
- Does NOT manage inventory or warehouse space (WMS/PMS does this)
- Does NOT optimize routes or capacity (TMS/WMS does this)
- Does NOT predict delays or suggest actions (neutral recorder only)

---

## 2. Data Model

### 2.1 Core Entities

#### Entity: Movement

**Purpose:** Represents a container/truck move or shipment leg that may have delays/incidents.

**Fields:**
- `id` (UUID, primary key)
- `external_id` (string, optional) - Reference to TMS/WMS system (e.g., "TMS-ORDER-12345")
- `container_id` (string, optional) - Container number
- `truck_id` (string, optional) - Truck/vehicle number
- `bill_of_lading` (string, optional) - BL number
- `route` (object, optional) - Planned route
  - `origin_facility_id` (UUID, FK to Facility)
  - `destination_facility_id` (UUID, FK to Facility)
  - `intermediate_facilities` (array of UUIDs, FK to Facility)
- `lane` (string, optional) - Lane identifier (e.g., "JNPT-Delhi")
- `planned_start_date` (datetime, optional) - When movement was planned to start
- `planned_end_date` (datetime, optional) - When movement was planned to end
- `actual_start_date` (datetime, optional) - When movement actually started
- `actual_end_date` (datetime, optional) - When movement actually ended
- `parties` (object, optional) - Parties involved
  - `shipper_id` (UUID, FK to Party)
  - `forwarder_id` (UUID, FK to Party)
  - `cha_id` (UUID, FK to Party)
  - `transporter_id` (UUID, FK to Party)
  - `consignee_id` (UUID, FK to Party)
- `status` (enum) - `active`, `completed`, `disputed`, `resolved`
- `metadata` (JSON, optional) - Additional context from external systems
- `created_at` (datetime, UTC)
- `updated_at` (datetime, UTC)
- `created_by` (UUID, FK to User)

**Relationships:**
- Has many Events
- Has many DisputePackets
- Belongs to multiple Facilities (via route)
- Belongs to multiple Parties (via parties object)

**Notes:**
- Movement can be created before or after events are logged
- External systems can create Movements via API, or Movements can be auto-created when first event is logged
- Movement metadata can store TMS/WMS-specific data (not used by Ward, but preserved)

#### Entity: Facility

**Purpose:** Represents a port, ICD, CFS, logistics park, or warehouse where incidents can occur.

**Fields:**
- `id` (UUID, primary key)
- `external_id` (string, optional) - Reference to WMS/PMS system
- `name` (string, required) - Facility name (e.g., "JNPT Terminal 4")
- `type` (enum, required) - `port`, `icd`, `cfs`, `warehouse`, `logistics_park`
- `code` (string, optional) - Facility code (e.g., "JNPT", "MUNDRA")
- `address` (object, optional)
  - `street` (string)
  - `city` (string)
  - `state` (string)
  - `pincode` (string)
  - `country` (string, default: "India")
- `location` (object, optional)
  - `latitude` (float)
  - `longitude` (float)
  - `radius_meters` (integer) - Radius for GPS matching
- `contact_info` (object, optional)
  - `phone` (string)
  - `email` (string)
  - `contact_person` (string)
- `metadata` (JSON, optional) - Additional context from WMS/PMS
- `created_at` (datetime, UTC)
- `updated_at` (datetime, UTC)

**Relationships:**
- Has many Events (events that occurred at this facility)
- Has many Movements (movements that pass through this facility)

**Notes:**
- Facilities can be pre-registered by external systems (WMS/PMS) or created on-the-fly when events are logged
- GPS matching: Events with GPS coordinates can be auto-linked to facilities within radius

#### Entity: Party

**Purpose:** Represents a shipper, forwarder, CHA, transporter, facility operator, or customs agency.

**Fields:**
- `id` (UUID, primary key)
- `external_id` (string, optional) - Reference to external system
- `name` (string, required) - Party name
- `type` (enum, required) - `shipper`, `forwarder`, `cha`, `transporter`, `facility_operator`, `customs`, `consignee`
- `gstin` (string, optional) - GST identification number
- `contact_info` (object, optional)
  - `phone` (string)
  - `email` (string)
  - `address` (object)
- `metadata` (JSON, optional) - Additional context from external systems
- `created_at` (datetime, UTC)
- `updated_at` (datetime, UTC)

**Relationships:**
- Has many Movements (as shipper, forwarder, transporter, etc.)
- Has many Events (events logged by this party's employees)

**Notes:**
- Parties can be pre-registered or created on-the-fly
- Same legal entity can have multiple Party records for different roles (e.g., party can be both shipper and forwarder)

#### Entity: Event

**Purpose:** Represents an incident, delay, or milestone with full temporal truth and tamper trail.

**Fields:**
- `id` (UUID, primary key)
- `movement_id` (UUID, FK to Movement, required)
- `facility_id` (UUID, FK to Facility, optional) - Where event occurred
- `original_event_id` (UUID, FK to Event, optional) - If this is an edit, reference to original
- `version` (integer, default: 1) - Version number (1 for original, increments for edits)
- `supersedes` (UUID, FK to Event, optional) - If this event supersedes another (for deletions)
- `event_type` (enum, required) - `incident`, `milestone`, `edit`, `deletion`
- `incident_type` (enum, optional) - `stuck_at_port_gate`, `cfs_yard_full`, `dock_not_ready`, `documents_issue`, `no_labour`, `system_down`, `other`
- `timestamp_captured` (datetime, UTC, required) - System timestamp when event was captured
- `timestamp_incident` (datetime, UTC, optional) - When incident actually occurred (if different from captured)
- `timestamp_edited` (datetime, UTC, optional) - When event was edited (if edited)
- `actor_id` (UUID, FK to User, required) - Who logged the event
- `actor_role` (string, optional) - Role of actor (driver, yard_staff, gate_operator, dispatcher)
- `device_id` (string, required) - Device identifier (Android ID or device fingerprint)
- `location` (object, required)
  - `latitude` (float)
  - `longitude` (float)
  - `accuracy_meters` (float)
  - `source` (enum) - `gps`, `network`, `cached`
- `content` (object, required)
  - `voice_recording_url` (string, optional) - URL to voice recording
  - `voice_transcript` (string, optional) - Transcript of voice recording
  - `text` (string, optional) - Text description
  - `language` (string, optional) - Language of content (e.g., "hi", "en", "ta")
- `reliability` (enum, optional) - `high`, `medium`, `low` - Based on corroboration
- `metadata` (JSON, optional) - Additional context
- `created_at` (datetime, UTC)
- `updated_at` (datetime, UTC)

**Relationships:**
- Belongs to Movement
- Belongs to Facility
- Belongs to User (actor)
- Has many Attachments
- Can reference original Event (if edit)
- Can supersede another Event (if deletion)

**Immutability Rules:**
- Original events (version = 1) cannot be modified or deleted
- Edits create new events with `original_event_id` pointing to original
- Deletions create new events with `event_type = deletion` and `supersedes` pointing to deleted event
- All versions remain in database and are visible in timeline

#### Entity: Attachment

**Purpose:** Represents photos, PDFs, audio files, or other documents tied to events.

**Fields:**
- `id` (UUID, primary key)
- `event_id` (UUID, FK to Event, required)
- `type` (enum, required) - `photo`, `pdf`, `audio`, `video`, `document`
- `file_name` (string, required)
- `file_size_bytes` (integer, required)
- `mime_type` (string, required) - e.g., "image/jpeg", "application/pdf"
- `file_url` (string, required) - URL to file (S3 or storage service)
- `thumbnail_url` (string, optional) - URL to thumbnail (for images/videos)
- `description` (string, optional) - Description of attachment
- `uploaded_by` (UUID, FK to User, required)
- `created_at` (datetime, UTC)

**Relationships:**
- Belongs to Event
- Belongs to User (uploader)

**Notes:**
- Attachments are immutable (cannot be deleted, only new attachments can be added)
- File storage is handled by storage service (S3, Supabase Storage, etc.)

#### Entity: DisputePacket

**Purpose:** Represents a generated dispute packet artifact from one or more Movements + Events + Attachments.

**Fields:**
- `id` (UUID, primary key)
- `name` (string, required) - Human-readable name (e.g., "JNPT-Demurrage-Dispute-2024-12-14")
- `movement_ids` (array of UUIDs, required) - Movements included in packet
- `event_ids` (array of UUIDs, optional) - Specific events to include (if not all events)
- `attachment_ids` (array of UUIDs, optional) - Additional attachments to include
- `template_type` (enum, required) - `jnpt`, `mundra`, `chennai`, `generic`, `custom`
- `custom_template_id` (UUID, optional) - If custom template
- `filters` (object, optional) - Filters applied when generating packet
  - `date_range` (object) - `start`, `end`
  - `facility_ids` (array of UUIDs)
  - `incident_types` (array of enums)
  - `exclude_edited` (boolean) - Exclude edited events
  - `exclude_low_reliability` (boolean) - Exclude low-reliability events
- `status` (enum, required) - `draft`, `generated`, `reviewed`, `submitted`, `outcome_received`
- `outcome` (enum, optional) - `waived`, `paid`, `partial`, `pending`, `rejected`
- `outcome_amount` (decimal, optional) - Amount waived/paid (if outcome received)
- `file_url` (string, optional) - URL to generated PDF
- `file_format` (enum, optional) - `pdf`, `excel`, `json`
- `generated_by` (UUID, FK to User, required)
- `reviewed_by` (UUID, FK to User, optional)
- `submitted_by` (UUID, FK to User, optional)
- `submitted_to` (string, optional) - Who packet was submitted to (port, facility, court)
- `created_at` (datetime, UTC)
- `generated_at` (datetime, UTC, optional)
- `reviewed_at` (datetime, UTC, optional)
- `submitted_at` (datetime, UTC, optional)
- `outcome_at` (datetime, UTC, optional)

**Relationships:**
- Has many Movements
- Has many Events (via movement_ids and event_ids)
- Has many Attachments (via attachment_ids)
- Belongs to User (generated_by, reviewed_by, submitted_by)

**Notes:**
- DisputePacket is a generated artifact, not a source of truth
- Source of truth remains in Events
- Packet can be regenerated if Events are edited (new packet version)

---

## 3. REST API Surface

### 3.1 Authentication

**All endpoints require authentication via JWT token.**

**Header:**
```
Authorization: Bearer <jwt_token>
```

**Token Claims:**
- `user_id` (UUID)
- `customer_id` (UUID) - Customer/organization ID
- `role` (string) - User role
- `exp` (integer) - Expiration timestamp

### 3.2 POST /movements

**Purpose:** Create or upsert a Movement with external references.

**Request:**
```json
{
  "external_id": "TMS-ORDER-12345",
  "container_id": "MSKU987654",
  "truck_id": "MH-12-AB-1234",
  "bill_of_lading": "BL-2024-001234",
  "route": {
    "origin_facility_id": "550e8400-e29b-41d4-a716-446655440000",
    "destination_facility_id": "660e8400-e29b-41d4-a716-446655440001",
    "intermediate_facilities": ["770e8400-e29b-41d4-a716-446655440002"]
  },
  "lane": "JNPT-Delhi",
  "planned_start_date": "2024-12-15T08:00:00Z",
  "planned_end_date": "2024-12-17T18:00:00Z",
  "parties": {
    "shipper_id": "880e8400-e29b-41d4-a716-446655440003",
    "forwarder_id": "990e8400-e29b-41d4-a716-446655440004",
    "transporter_id": "aa0e8400-e29b-41d4-a716-446655440005"
  },
  "metadata": {
    "tms_order_id": "TMS-ORDER-12345",
    "wms_shipment_id": "WMS-SHIP-67890"
  }
}
```

**Response (201 Created):**
```json
{
  "id": "110e8400-e29b-41d4-a716-446655440006",
  "external_id": "TMS-ORDER-12345",
  "container_id": "MSKU987654",
  "truck_id": "MH-12-AB-1234",
  "bill_of_lading": "BL-2024-001234",
  "route": {
    "origin_facility_id": "550e8400-e29b-41d4-a716-446655440000",
    "destination_facility_id": "660e8400-e29b-41d4-a716-446655440001",
    "intermediate_facilities": ["770e8400-e29b-41d4-a716-446655440002"]
  },
  "lane": "JNPT-Delhi",
  "status": "active",
  "created_at": "2024-12-14T10:30:00Z",
  "updated_at": "2024-12-14T10:30:00Z"
}
```

**Upsert Behavior:**
- If `external_id` provided and Movement exists with same `external_id` and `customer_id`, update existing Movement
- Otherwise, create new Movement

**Validation:**
- At least one of: `container_id`, `truck_id`, `bill_of_lading`, `external_id` must be provided
- `facility_id` in route must exist (or be created if external_id provided)

### 3.3 POST /events

**Purpose:** Log an event for a Movement with timestamps, GPS, device, actor, reason, and optional attachments.

**Request:**
```json
{
  "movement_id": "110e8400-e29b-41d4-a716-446655440006",
  "facility_id": "550e8400-e29b-41d4-a716-446655440000",
  "event_type": "incident",
  "incident_type": "stuck_at_port_gate",
  "timestamp_captured": "2024-12-14T10:35:00Z",
  "timestamp_incident": "2024-12-14T10:30:00Z",
  "actor_id": "bb0e8400-e29b-41d4-a716-446655440007",
  "actor_role": "driver",
  "device_id": "android-abc123def456",
  "location": {
    "latitude": 18.9519,
    "longitude": 72.9619,
    "accuracy_meters": 15.5,
    "source": "gps"
  },
  "content": {
    "voice_recording_url": "https://storage.ward.ai/recordings/voice-123.mp3",
    "voice_transcript": "Container stuck at JNPT gate 4, customs hold",
    "text": "Stuck at port gate due to customs hold",
    "language": "hi"
  },
  "reliability": "high",
  "metadata": {
    "network_status": "offline",
    "app_version": "1.0.0"
  }
}
```

**Response (201 Created):**
```json
{
  "id": "cc0e8400-e29b-41d4-a716-446655440008",
  "movement_id": "110e8400-e29b-41d4-a716-446655440006",
  "facility_id": "550e8400-e29b-41d4-a716-446655440000",
  "original_event_id": null,
  "version": 1,
  "event_type": "incident",
  "incident_type": "stuck_at_port_gate",
  "timestamp_captured": "2024-12-14T10:35:00Z",
  "timestamp_incident": "2024-12-14T10:30:00Z",
  "timestamp_edited": null,
  "actor_id": "bb0e8400-e29b-41d4-a716-446655440007",
  "device_id": "android-abc123def456",
  "location": {
    "latitude": 18.9519,
    "longitude": 72.9619,
    "accuracy_meters": 15.5,
    "source": "gps"
  },
  "reliability": "high",
  "created_at": "2024-12-14T10:35:00Z"
}
```

**Edit Event (creates new event):**
```json
{
  "original_event_id": "cc0e8400-e29b-41d4-a716-446655440008",
  "movement_id": "110e8400-e29b-41d4-a716-446655440006",
  "event_type": "edit",
  "content": {
    "text": "Updated: Container stuck at JNPT gate 4, customs hold - cleared at 11:00 AM"
  },
  "timestamp_captured": "2024-12-14T11:05:00Z",
  "actor_id": "dd0e8400-e29b-41d4-a716-446655440009",
  "device_id": "android-xyz789",
  "location": {
    "latitude": 18.9519,
    "longitude": 72.9619,
    "accuracy_meters": 20.0,
    "source": "gps"
  }
}
```

**Response (201 Created):**
```json
{
  "id": "ee0e8400-e29b-41d4-a716-446655440010",
  "movement_id": "110e8400-e29b-41d4-a716-446655440006",
  "original_event_id": "cc0e8400-e29b-41d4-a716-446655440008",
  "version": 2,
  "event_type": "edit",
  "timestamp_captured": "2024-12-14T11:05:00Z",
  "timestamp_edited": "2024-12-14T11:05:00Z",
  "created_at": "2024-12-14T11:05:00Z"
}
```

**Validation:**
- `movement_id` must exist
- `timestamp_captured` is required (system timestamp)
- `actor_id` must exist and belong to same customer
- `device_id` is required
- `location` is required (GPS coordinates)
- If `original_event_id` provided, original event must exist and belong to same movement

### 3.4 GET /movements/{id}/timeline

**Purpose:** Return all events for a Movement in chronological order, including tamper trail (original + edits).

**Query Parameters:**
- `include_edits` (boolean, default: true) - Include edit events
- `include_deletions` (boolean, default: true) - Include deletion events
- `facility_id` (UUID, optional) - Filter by facility
- `incident_type` (enum, optional) - Filter by incident type
- `date_from` (datetime, optional) - Filter events from date
- `date_to` (datetime, optional) - Filter events to date
- `reliability` (enum, optional) - Filter by reliability (high, medium, low)

**Response (200 OK):**
```json
{
  "movement_id": "110e8400-e29b-41d4-a716-446655440006",
  "events": [
    {
      "id": "cc0e8400-e29b-41d4-a716-446655440008",
      "version": 1,
      "original_event_id": null,
      "event_type": "incident",
      "incident_type": "stuck_at_port_gate",
      "timestamp_captured": "2024-12-14T10:35:00Z",
      "timestamp_incident": "2024-12-14T10:30:00Z",
      "timestamp_edited": null,
      "facility": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "JNPT Terminal 4",
        "type": "port"
      },
      "actor": {
        "id": "bb0e8400-e29b-41d4-a716-446655440007",
        "name": "Rajesh Kumar",
        "role": "driver"
      },
      "location": {
        "latitude": 18.9519,
        "longitude": 72.9619,
        "accuracy_meters": 15.5
      },
      "content": {
        "voice_recording_url": "https://storage.ward.ai/recordings/voice-123.mp3",
        "voice_transcript": "Container stuck at JNPT gate 4, customs hold",
        "text": "Stuck at port gate due to customs hold"
      },
      "reliability": "high",
      "attachments": [
        {
          "id": "ff0e8400-e29b-41d4-a716-446655440011",
          "type": "photo",
          "file_name": "gate-photo.jpg",
          "file_url": "https://storage.ward.ai/photos/gate-photo.jpg"
        }
      ],
      "is_original": true,
      "is_edited": false,
      "is_deleted": false,
      "edit_history": [
        {
          "id": "ee0e8400-e29b-41d4-a716-446655440010",
          "version": 2,
          "timestamp_edited": "2024-12-14T11:05:00Z",
          "actor": {
            "id": "dd0e8400-e29b-41d4-a716-446655440009",
            "name": "Priya Sharma",
            "role": "dispatcher"
          },
          "content": {
            "text": "Updated: Container stuck at JNPT gate 4, customs hold - cleared at 11:00 AM"
          }
        }
      ]
    }
  ],
  "total_events": 1,
  "original_events": 1,
  "edited_events": 1,
  "deleted_events": 0
}
```

**Notes:**
- Events are returned in chronological order (by `timestamp_captured`)
- Edit history is nested under original events
- Deleted events are included but marked with `is_deleted: true`
- Timeline shows full tamper trail (original + all edits)

### 3.5 POST /attachments

**Purpose:** Upload an attachment and associate it with an Event.

**Request (multipart/form-data):**
```
file: <binary file>
event_id: "cc0e8400-e29b-41d4-a716-446655440008"
type: "photo"
description: "Photo of port gate"
```

**Response (201 Created):**
```json
{
  "id": "ff0e8400-e29b-41d4-a716-446655440011",
  "event_id": "cc0e8400-e29b-41d4-a716-446655440008",
  "type": "photo",
  "file_name": "gate-photo.jpg",
  "file_size_bytes": 245678,
  "mime_type": "image/jpeg",
  "file_url": "https://storage.ward.ai/photos/gate-photo.jpg",
  "thumbnail_url": "https://storage.ward.ai/photos/thumbs/gate-photo.jpg",
  "description": "Photo of port gate",
  "uploaded_by": "bb0e8400-e29b-41d4-a716-446655440007",
  "created_at": "2024-12-14T10:36:00Z"
}
```

**Validation:**
- `event_id` must exist and belong to same customer
- File size limit: 10MB per file
- Supported types: image/jpeg, image/png, application/pdf, audio/mpeg, video/mp4

### 3.6 POST /dispute-packets

**Purpose:** Generate a DisputePacket for one or more Movements (with filters like time window, facilities, parties).

**Request:**
```json
{
  "name": "JNPT-Demurrage-Dispute-2024-12-14",
  "movement_ids": ["110e8400-e29b-41d4-a716-446655440006"],
  "event_ids": null,
  "attachment_ids": ["ff0e8400-e29b-41d4-a716-446655440011"],
  "template_type": "jnpt",
  "filters": {
    "date_range": {
      "start": "2024-12-14T00:00:00Z",
      "end": "2024-12-14T23:59:59Z"
    },
    "facility_ids": ["550e8400-e29b-41d4-a716-446655440000"],
    "incident_types": ["stuck_at_port_gate", "cfs_yard_full"],
    "exclude_edited": false,
    "exclude_low_reliability": true
  },
  "include_cover_letter": true,
  "cover_letter_text": "We dispute the demurrage charges as the delay was caused by customs hold, not our fault."
}
```

**Response (202 Accepted):**
```json
{
  "id": "000e8400-e29b-41d4-a716-446655440012",
  "name": "JNPT-Demurrage-Dispute-2024-12-14",
  "status": "generating",
  "created_at": "2024-12-14T12:00:00Z"
}
```

**Note:** Packet generation is asynchronous. Client should poll `GET /dispute-packets/{id}` to check status.

### 3.7 GET /dispute-packets/{id}

**Purpose:** Fetch metadata + download link for the generated packet.

**Response (200 OK):**
```json
{
  "id": "000e8400-e29b-41d4-a716-446655440012",
  "name": "JNPT-Demurrage-Dispute-2024-12-14",
  "movement_ids": ["110e8400-e29b-41d4-a716-446655440006"],
  "template_type": "jnpt",
  "status": "generated",
  "file_url": "https://storage.ward.ai/packets/jnpt-dispute-2024-12-14.pdf",
  "file_format": "pdf",
  "file_size_bytes": 1234567,
  "generated_at": "2024-12-14T12:01:30Z",
  "generated_by": {
    "id": "aa0e8400-e29b-41d4-a716-446655440013",
    "name": "Finance Controller",
    "email": "finance@customer.com"
  },
  "summary": {
    "total_events": 5,
    "total_attachments": 3,
    "date_range": {
      "start": "2024-12-14T10:30:00Z",
      "end": "2024-12-14T11:00:00Z"
    },
    "facilities": ["JNPT Terminal 4"],
    "total_delay_minutes": 30
  }
}
```

**Status Values:**
- `generating` - Packet is being generated
- `generated` - Packet is ready for download
- `failed` - Generation failed (check error message)

---

## 4. Immutability & Versioning Rules

### 4.1 Original Events Are Immutable

**Rule:** Events with `version = 1` and `original_event_id = null` cannot be modified or deleted.

**Implementation:**
- Database: Original events have `version = 1`, `original_event_id = null`
- API: `PUT /events/{id}` and `DELETE /events/{id}` return 403 Forbidden for original events
- Soft delete: Even "deletions" create new events, original remains in database

### 4.2 Edits Create New Events

**Rule:** All edits create new Event records that reference the original.

**Implementation:**
- New event has:
  - `original_event_id` = ID of original event
  - `version` = original version + 1
  - `event_type` = `edit`
  - `timestamp_edited` = current timestamp
- Original event remains unchanged
- Timeline shows both original and edit (with clear visual distinction)

**Example:**
```
Original Event (version 1):
  id: event-1
  version: 1
  original_event_id: null
  content: "Stuck at port gate"

Edit Event (version 2):
  id: event-2
  version: 2
  original_event_id: event-1
  event_type: edit
  content: "Updated: Cleared at 11:00 AM"
```

### 4.3 Deletions Create New Events

**Rule:** "Deletions" create new events that mark original as deleted, but original remains in database.

**Implementation:**
- New event has:
  - `event_type` = `deletion`
  - `supersedes` = ID of deleted event
  - `timestamp_edited` = current timestamp
- Original event remains in database, marked as deleted in UI
- Timeline shows deleted event with strikethrough

**Example:**
```
Original Event (version 1):
  id: event-1
  version: 1
  content: "Stuck at port gate"

Deletion Event:
  id: event-3
  event_type: deletion
  supersedes: event-1
  content: "Event deleted - incorrect information"
```

### 4.4 Audit Trail Fields

**Fields for Audit Trail:**
- `original_event_id` - Links edit to original
- `version` - Version number (increments for edits)
- `supersedes` - Links deletion to deleted event
- `timestamp_captured` - When event was originally captured (never changes)
- `timestamp_edited` - When event was edited (only for edits)
- `timestamp_incident` - When incident actually occurred (can be different from captured)

**Client Reliance:**
- Clients can rely on `original_event_id` to trace edit history
- Clients can rely on `version` to identify original vs edited events
- Clients can rely on `timestamp_captured` vs `timestamp_edited` to identify temporal truth
- Clients can filter by `event_type` to exclude edits/deletions if needed

### 4.5 Timeline Query Behavior

**Default Behavior:**
- Timeline includes all events (original + edits + deletions)
- Events are grouped by `original_event_id` (original + its edits)
- Chronological order by `timestamp_captured`

**Filtering:**
- `include_edits=false` - Exclude edit events (show only originals)
- `include_deletions=false` - Exclude deletion events
- `version=1` - Show only original events

**Visual Indicators:**
- Original events: `is_original: true`, `is_edited: false`
- Edited events: `is_original: false`, `is_edited: true`, `original_event_id` present
- Deleted events: `is_deleted: true`, `supersedes` present

---

## 5. Integration Patterns

### 5.1 TMS Integration: Push Planned Movements, Query Timelines

**Flow:**
1. TMS creates shipment/order → calls `POST /movements` with external_id, container_id, route, parties
2. Movement created in Ward (or updated if external_id exists)
3. Drivers/yard staff log events via mobile app (events linked to Movement)
4. When dispute arises, TMS calls `GET /movements/{id}/timeline` to get all events
5. TMS displays timeline in its UI or generates dispute packet via `POST /dispute-packets`

**Example TMS Code (pseudo-code):**
```javascript
// TMS creates movement
const movement = await wardAPI.post('/movements', {
  external_id: `TMS-${order.id}`,
  container_id: order.containerNumber,
  route: {
    origin_facility_id: jnptFacilityId,
    destination_facility_id: delhiFacilityId
  },
  parties: {
    shipper_id: shipperPartyId,
    forwarder_id: forwarderPartyId
  }
});

// Later, when dispute arises
const timeline = await wardAPI.get(`/movements/${movement.id}/timeline`);

// Generate dispute packet
const packet = await wardAPI.post('/dispute-packets', {
  movement_ids: [movement.id],
  template_type: 'jnpt'
});
```

### 5.2 WMS/PMS Integration: Push Facility Context, Query Facility Events

**Flow:**
1. WMS/PMS registers facilities → calls `POST /facilities` (or Ward auto-creates from events)
2. Events logged at facilities are auto-linked via GPS matching
3. WMS/PMS queries `GET /facilities/{id}/events` to see all incidents at their facility
4. WMS/PMS can generate scorecards or dispute packets for facility-side delays

**Example WMS Code (pseudo-code):**
```javascript
// WMS registers facility
const facility = await wardAPI.post('/facilities', {
  external_id: `WMS-${warehouse.id}`,
  name: warehouse.name,
  type: 'warehouse',
  location: {
    latitude: warehouse.lat,
    longitude: warehouse.lng,
    radius_meters: 100
  }
});

// Query events at facility
const events = await wardAPI.get(`/facilities/${facility.id}/events`, {
  date_from: '2024-12-01',
  date_to: '2024-12-31'
});
```

### 5.3 Finance System Integration: Pull Dispute Packets for Invoices

**Flow:**
1. Invoice arrives → Finance system uploads invoice via `POST /invoices` (if invoice API exists) or links to Movement
2. Finance system searches for Movement by container_id or invoice reference
3. Finance system generates dispute packet via `POST /dispute-packets`
4. Finance system polls `GET /dispute-packets/{id}` until status is "generated"
5. Finance system downloads packet PDF and submits to port/facility
6. Finance system updates packet status via `PUT /dispute-packets/{id}/status` when outcome received

**Example Finance Code (pseudo-code):**
```javascript
// Search for movement by container
const movements = await wardAPI.get('/movements', {
  container_id: invoice.containerNumber
});

// Generate dispute packet
const packet = await wardAPI.post('/dispute-packets', {
  movement_ids: [movements[0].id],
  template_type: 'jnpt',
  filters: {
    date_range: {
      start: invoice.chargeStartDate,
      end: invoice.chargeEndDate
    }
  }
});

// Poll until ready
let packetStatus = 'generating';
while (packetStatus === 'generating') {
  await sleep(2000);
  const packetData = await wardAPI.get(`/dispute-packets/${packet.id}`);
  packetStatus = packetData.status;
}

// Download packet
const pdfUrl = packetData.file_url;
// Submit to port/facility...

// Update outcome
await wardAPI.put(`/dispute-packets/${packet.id}/status`, {
  status: 'outcome_received',
  outcome: 'waived',
  outcome_amount: invoice.amount
});
```

### 5.4 Marketplace Integration: Query Events for Vendor Scorecards

**Flow:**
1. Marketplace (e.g., warehouse marketplace) queries `GET /parties/{id}/events` to see all events for a vendor
2. Marketplace generates scorecard based on event frequency, delay attribution, reliability
3. Marketplace uses scorecard for vendor performance reviews and contract negotiations

**Example Marketplace Code (pseudo-code):**
```javascript
// Query events for transporter
const events = await wardAPI.get(`/parties/${transporterId}/events`, {
  date_from: '2024-12-01',
  date_to: '2024-12-31',
  incident_types: ['stuck_at_port_gate', 'dock_not_ready']
});

// Generate scorecard
const scorecard = {
  total_incidents: events.length,
  delay_attribution: {
    transport_side: events.filter(e => e.incident_type === 'dock_not_ready').length,
    facility_side: events.filter(e => e.incident_type === 'cfs_yard_full').length
  },
  reliability_score: calculateReliability(events)
};
```

---

## 6. Additional Endpoints (Supporting)

### 6.1 GET /movements

**Purpose:** List movements with filters.

**Query Parameters:**
- `container_id` (string, optional)
- `truck_id` (string, optional)
- `external_id` (string, optional)
- `facility_id` (UUID, optional)
- `party_id` (UUID, optional)
- `status` (enum, optional)
- `date_from` (datetime, optional)
- `date_to` (datetime, optional)
- `limit` (integer, default: 50, max: 100)
- `offset` (integer, default: 0)

**Response:** Array of Movement objects with pagination metadata.

### 6.2 GET /facilities

**Purpose:** List facilities with filters.

**Query Parameters:**
- `type` (enum, optional)
- `code` (string, optional)
- `near` (object, optional) - `latitude`, `longitude`, `radius_meters`

**Response:** Array of Facility objects.

### 6.3 POST /facilities

**Purpose:** Create or upsert a Facility.

**Request/Response:** Similar to POST /movements, but for Facility entity.

### 6.4 GET /parties

**Purpose:** List parties with filters.

**Query Parameters:**
- `type` (enum, optional)
- `name` (string, optional, fuzzy search)
- `gstin` (string, optional)

**Response:** Array of Party objects.

### 6.5 POST /parties

**Purpose:** Create or upsert a Party.

**Request/Response:** Similar to POST /movements, but for Party entity.

---

## 7. Error Handling

### 7.1 Standard Error Response

**Format:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "movement_id is required",
    "details": {
      "field": "movement_id",
      "reason": "required"
    }
  }
}
```

### 7.2 Error Codes

- `VALIDATION_ERROR` (400) - Request validation failed
- `UNAUTHORIZED` (401) - Authentication required
- `FORBIDDEN` (403) - Not authorized (e.g., trying to delete original event)
- `NOT_FOUND` (404) - Resource not found
- `CONFLICT` (409) - Resource conflict (e.g., duplicate external_id)
- `INTERNAL_ERROR` (500) - Server error

---

## 8. Rate Limiting

**Limits:**
- 100 requests per minute per API key
- 1000 requests per hour per API key
- Burst: 20 requests per second

**Headers:**
- `X-RateLimit-Limit` - Request limit
- `X-RateLimit-Remaining` - Remaining requests
- `X-RateLimit-Reset` - Reset timestamp

---

## 9. Versioning

**API Version:**
- Current version: `v0`
- Version in URL: `/v0/movements`
- Version in header: `X-API-Version: v0`

**Backward Compatibility:**
- v0 is initial version, no backward compatibility concerns
- Future versions (v1, v2) will maintain backward compatibility for at least 12 months

---

**Document Status:** Ready for Engineering Implementation  
**Next Steps:** API design review, OpenAPI/Swagger spec generation, implementation planning

