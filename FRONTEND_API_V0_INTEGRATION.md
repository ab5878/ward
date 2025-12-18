# Frontend API v0 Integration Guide

**Date:** December 2024  
**Status:** Ready for Integration

---

## 📦 API v0 Service Created

**File:** `frontend/src/services/apiV0.js`

This service provides a clean interface for all API v0 endpoints.

---

## 🔌 Usage Examples

### 1. Movements

```javascript
import { movementsAPI } from '../services/apiV0';

// Create a movement
const movement = await movementsAPI.create({
  container_id: "MSKU987654",
  truck_id: "MH-12-AB-1234",
  bill_of_lading: "BL-2024-001234",
  lane: "JNPT-Delhi",
  external_id: "TMS-ORDER-12345"
});

// List movements
const { items, total } = await movementsAPI.list({
  container_id: "MSKU987654",
  status: "active",
  limit: 50,
  offset: 0
});

// Get a movement
const movement = await movementsAPI.get(movementId);
```

### 2. Events (Mobile App)

```javascript
import { eventsAPI } from '../services/apiV0';

// Create an event with GPS and device ID
const event = await eventsAPI.create({
  movement_id: movementId,
  facility_id: facilityId,
  event_type: "incident",
  incident_type: "stuck_at_port_gate",
  timestamp_captured: new Date().toISOString(),
  device_id: "android-abc123def456",
  location: {
    latitude: 18.9519,
    longitude: 72.9619,
    accuracy_meters: 15.5,
    source: "gps"
  },
  content: {
    text: "Container stuck at JNPT gate 4, customs hold",
    voice_transcript: "Container stuck at JNPT gate 4, customs hold",
    language: "hi"
  },
  reliability: "high"
});
```

### 3. Attachments

```javascript
import { attachmentsAPI } from '../services/apiV0';

// Upload a photo
const attachment = await attachmentsAPI.upload(file, {
  event_id: eventId,
  movement_id: movementId,
  file_type: "photo",
  description: "Photo of port gate"
});

// List attachments for an event
const attachments = await attachmentsAPI.listForEvent(eventId);

// Get an attachment
const attachment = await attachmentsAPI.get(attachmentId);
```

### 4. DisputePackets

```javascript
import { disputePacketsAPI } from '../services/apiV0';

// Create a dispute packet
const packet = await disputePacketsAPI.create(movementId, {
  invoice_id: "INV-2024-001234",
  template_type: "jnpt_demurrage",
  selected_events: [eventId1, eventId2],
  selected_attachments: [attachmentId1],
  narrative: "Dispute for demurrage charges at JNPT"
});

// List dispute packets
const packets = await disputePacketsAPI.list(movementId);

// Export dispute packet
const zipBlob = await disputePacketsAPI.export(packetId);
// Download the blob
const url = window.URL.createObjectURL(zipBlob);
const a = document.createElement('a');
a.href = url;
a.download = `dispute-packet-${packetId}.zip`;
a.click();

// Update dispute packet
const updated = await disputePacketsAPI.update(packetId, {
  status: "submitted",
  outcome: "waived",
  outcome_amount: 50000
});
```

### 5. Facilities

```javascript
import { facilitiesAPI } from '../services/apiV0';

// Create a facility
const facility = await facilitiesAPI.create({
  name: "JNPT Terminal 4",
  type: "port",
  code: "JNPT",
  address: {
    city: "Mumbai",
    state: "Maharashtra",
    pincode: "400001"
  },
  location: {
    latitude: 18.9519,
    longitude: 72.9619
  }
});

// List facilities
const facilities = await facilitiesAPI.list({ type: "port" });

// Get a facility
const facility = await facilitiesAPI.get(facilityId);
```

### 6. Parties

```javascript
import { partiesAPI } from '../services/apiV0';

// Create a party
const party = await partiesAPI.create({
  name: "ABC Forwarders Pvt Ltd",
  type: "forwarder",
  code: "ABC-FWD",
  contact_info: {
    email: "contact@abcforwarders.com",
    phone: "+91-22-12345678"
  }
});

// List parties
const parties = await partiesAPI.list({ type: "forwarder" });

// Get a party
const party = await partiesAPI.get(partyId);
```

---

## 🔄 Migration from Old Endpoints

### Cases → Movements

**Old:**
```javascript
const response = await api.get('/cases');
const cases = response.data;
```

**New:**
```javascript
import { movementsAPI } from '../services/apiV0';
const { items: movements } = await movementsAPI.list();
```

### Timeline Events → Events

**Old:**
```javascript
await api.post(`/cases/${caseId}/timeline`, {
  content: "Event description",
  source_type: "voice",
  reliability: "high"
});
```

**New:**
```javascript
import { eventsAPI } from '../services/apiV0';
await eventsAPI.create({
  movement_id: caseId,
  event_type: "incident",
  content: { text: "Event description" },
  reliability: "high"
});
```

---

## 🎯 Integration Points

### Web Console

**Dispute Packet Generation:**
```javascript
// In CaseDetail.js or DisputePacketBuilder component
import { disputePacketsAPI } from '../services/apiV0';

const generateDisputePacket = async (caseId, selectedEvents) => {
  const packet = await disputePacketsAPI.create(caseId, {
    invoice_id: invoiceId,
    template_type: "jnpt_demurrage",
    selected_events: selectedEvents.map(e => e._id),
    narrative: narrativeText
  });
  
  // Export as ZIP
  const zipBlob = await disputePacketsAPI.export(packet._id);
  // Download...
};
```

**Facility/Party Selection:**
```javascript
// In CreateCase.js or MovementForm component
import { facilitiesAPI, partiesAPI } from '../services/apiV0';

// Load facilities for dropdown
const facilities = await facilitiesAPI.list({ type: "port" });

// Load parties for dropdown
const forwarders = await partiesAPI.list({ type: "forwarder" });
```

### Mobile App (Future)

**Incident Logging:**
```javascript
// In mobile app incident capture
import { eventsAPI, attachmentsAPI } from '../services/apiV0';

// Get GPS location
const location = await getCurrentPosition();

// Create event
const event = await eventsAPI.create({
  movement_id: movementId,
  event_type: "incident",
  incident_type: "stuck_at_port_gate",
  timestamp_captured: new Date().toISOString(),
  device_id: deviceId,
  location: {
    latitude: location.coords.latitude,
    longitude: location.coords.longitude,
    accuracy_meters: location.coords.accuracy,
    source: "gps"
  },
  content: {
    text: description,
    voice_transcript: transcript,
    language: "hi"
  },
  reliability: "high"
});

// Upload photo if available
if (photoFile) {
  await attachmentsAPI.upload(photoFile, {
    event_id: event._id,
    movement_id: movementId,
    file_type: "photo"
  });
}
```

---

## 📝 Component Examples

### DisputePacketBuilder Component

```javascript
import React, { useState, useEffect } from 'react';
import { disputePacketsAPI, eventsAPI } from '../services/apiV0';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';

export default function DisputePacketBuilder({ movementId }) {
  const [selectedEvents, setSelectedEvents] = useState([]);
  const [packets, setPackets] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadPackets();
  }, [movementId]);

  const loadPackets = async () => {
    try {
      const data = await disputePacketsAPI.list(movementId);
      setPackets(data);
    } catch (error) {
      toast.error('Failed to load dispute packets');
    }
  };

  const createPacket = async () => {
    setLoading(true);
    try {
      const packet = await disputePacketsAPI.create(movementId, {
        invoice_id: invoiceId,
        template_type: "jnpt_demurrage",
        selected_events: selectedEvents.map(e => e._id),
        narrative: narrativeText
      });
      toast.success('Dispute packet created');
      loadPackets();
    } catch (error) {
      toast.error('Failed to create dispute packet');
    } finally {
      setLoading(false);
    }
  };

  const exportPacket = async (packetId) => {
    try {
      const zipBlob = await disputePacketsAPI.export(packetId);
      const url = window.URL.createObjectURL(zipBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `dispute-packet-${packetId}.zip`;
      a.click();
      toast.success('Dispute packet exported');
    } catch (error) {
      toast.error('Failed to export dispute packet');
    }
  };

  // ... rest of component
}
```

### FacilitySelector Component

```javascript
import React, { useState, useEffect } from 'react';
import { facilitiesAPI } from '../services/apiV0';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

export default function FacilitySelector({ value, onChange, type }) {
  const [facilities, setFacilities] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadFacilities();
  }, [type]);

  const loadFacilities = async () => {
    try {
      const data = await facilitiesAPI.list({ type });
      setFacilities(data);
    } catch (error) {
      console.error('Failed to load facilities', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Select value={value} onValueChange={onChange}>
      <SelectTrigger>
        <SelectValue placeholder="Select facility" />
      </SelectTrigger>
      <SelectContent>
        {facilities.map(facility => (
          <SelectItem key={facility._id} value={facility._id}>
            {facility.name} ({facility.code})
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}
```

---

## ✅ Integration Checklist

- [ ] Import `apiV0.js` service in components
- [ ] Replace old `/api/cases` calls with `movementsAPI`
- [ ] Replace old `/api/cases/{id}/timeline` calls with `eventsAPI`
- [ ] Add facility/party selection to forms
- [ ] Integrate dispute packet generation
- [ ] Test all API v0 endpoints from frontend
- [ ] Handle errors gracefully
- [ ] Add loading states
- [ ] Add success/error toasts

---

**Last Updated:** December 2024  
**Status:** Ready for Frontend Integration

