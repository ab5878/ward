-- Ward API v0 Additional Tables
-- Migration to add Facilities, Parties, DisputePackets, and Attachments

-- Facilities table (ports, ICDs, CFSs, warehouses, logistics parks)
CREATE TABLE facilities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    external_id VARCHAR(255), -- Reference to WMS/PMS system
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL, -- 'port', 'icd', 'cfs', 'warehouse', 'logistics_park'
    code VARCHAR(100), -- Facility code (e.g., 'JNPT', 'MUNDRA')
    address JSONB, -- {street, city, state, pincode, country}
    location JSONB, -- {latitude, longitude}
    metadata JSONB DEFAULT '{}', -- Additional context from external systems
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX idx_facilities_type ON facilities(type);
CREATE INDEX idx_facilities_code ON facilities(code);
CREATE INDEX idx_facilities_external_id ON facilities(external_id);
CREATE INDEX idx_facilities_name ON facilities(name);

-- Parties table (shippers, forwarders, CHAs, transporters, consignees, etc.)
CREATE TABLE parties (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    external_id VARCHAR(255), -- Reference to TMS/WMS system
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL, -- 'shipper', 'forwarder', 'cha', 'transporter', 'consignee', 'carrier', 'warehouse_operator'
    code VARCHAR(100), -- Party code
    contact_info JSONB, -- {email, phone, address}
    metadata JSONB DEFAULT '{}', -- Additional context from external systems
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX idx_parties_type ON parties(type);
CREATE INDEX idx_parties_code ON parties(code);
CREATE INDEX idx_parties_external_id ON parties(external_id);
CREATE INDEX idx_parties_name ON parties(name);

-- DisputePackets table
CREATE TABLE dispute_packets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    movement_id UUID REFERENCES cases(id) ON DELETE CASCADE, -- Using cases as movements for now
    external_id VARCHAR(255), -- Reference to external dispute system
    invoice_id VARCHAR(255), -- Invoice that triggered this dispute
    template_type VARCHAR(100), -- 'jnpt_demurrage', 'warehouse_waiting_charge', etc.
    status VARCHAR(50) NOT NULL DEFAULT 'draft', -- 'draft', 'generated', 'submitted', 'resolved'
    selected_events UUID[], -- Array of timeline_event IDs included in packet
    selected_attachments UUID[], -- Array of attachment IDs included in packet
    narrative TEXT, -- Summary narrative or legal arguments
    generated_at TIMESTAMPTZ,
    submitted_at TIMESTAMPTZ,
    resolved_at TIMESTAMPTZ,
    outcome VARCHAR(100), -- 'waived', 'discounted', 'paid', 'pending'
    outcome_amount DECIMAL(12, 2), -- Amount waived/discounted/paid
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX idx_dispute_packets_movement_id ON dispute_packets(movement_id);
CREATE INDEX idx_dispute_packets_status ON dispute_packets(status);
CREATE INDEX idx_dispute_packets_invoice_id ON dispute_packets(invoice_id);
CREATE INDEX idx_dispute_packets_created_at ON dispute_packets(created_at);

-- Attachments table (photos, videos, audio files linked to events)
CREATE TABLE attachments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_id UUID REFERENCES timeline_events(id) ON DELETE CASCADE,
    movement_id UUID REFERENCES cases(id) ON DELETE CASCADE, -- Denormalized for easier querying
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL, -- 'photo', 'video', 'audio', 'document'
    mime_type VARCHAR(100),
    file_size BIGINT, -- Size in bytes
    storage_url TEXT, -- URL to file in storage (S3, Supabase Storage, etc.)
    storage_key TEXT, -- Key/path in storage system
    metadata JSONB DEFAULT '{}', -- {gps: {lat, lng}, device_id, etc.}
    created_at TIMESTAMPTZ DEFAULT NOW(),
    uploaded_by UUID REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX idx_attachments_event_id ON attachments(event_id);
CREATE INDEX idx_attachments_movement_id ON attachments(movement_id);
CREATE INDEX idx_attachments_file_type ON attachments(file_type);
CREATE INDEX idx_attachments_created_at ON attachments(created_at);

-- Movement-Party relationships (many-to-many)
CREATE TABLE movement_parties (
    movement_id UUID REFERENCES cases(id) ON DELETE CASCADE,
    party_id UUID REFERENCES parties(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL, -- 'shipper', 'forwarder', 'cha', 'transporter', 'consignee'
    PRIMARY KEY (movement_id, party_id, role)
);

CREATE INDEX idx_movement_parties_movement_id ON movement_parties(movement_id);
CREATE INDEX idx_movement_parties_party_id ON movement_parties(party_id);

-- Movement-Facility relationships (many-to-many for route)
CREATE TABLE movement_facilities (
    movement_id UUID REFERENCES cases(id) ON DELETE CASCADE,
    facility_id UUID REFERENCES facilities(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL, -- 'origin', 'destination', 'intermediate'
    sequence_order INTEGER, -- Order in route (for intermediate facilities)
    PRIMARY KEY (movement_id, facility_id, role)
);

CREATE INDEX idx_movement_facilities_movement_id ON movement_facilities(movement_id);
CREATE INDEX idx_movement_facilities_facility_id ON movement_facilities(facility_id);

-- Triggers for updated_at
CREATE TRIGGER update_facilities_updated_at BEFORE UPDATE ON facilities
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_parties_updated_at BEFORE UPDATE ON parties
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_dispute_packets_updated_at BEFORE UPDATE ON dispute_packets
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Add columns to timeline_events for API v0 compatibility
ALTER TABLE timeline_events 
    ADD COLUMN IF NOT EXISTS gps JSONB, -- {latitude, longitude, accuracy}
    ADD COLUMN IF NOT EXISTS device_id VARCHAR(255),
    ADD COLUMN IF NOT EXISTS captured_at TIMESTAMPTZ, -- Original capture time (immutable)
    ADD COLUMN IF NOT EXISTS edited_at TIMESTAMPTZ; -- When event was edited (if applicable)

CREATE INDEX idx_timeline_events_captured_at ON timeline_events(captured_at);
CREATE INDEX idx_timeline_events_device_id ON timeline_events(device_id);

-- Add columns to cases for API v0 Movement compatibility
ALTER TABLE cases
    ADD COLUMN IF NOT EXISTS external_id VARCHAR(255), -- Reference to TMS/WMS system
    ADD COLUMN IF NOT EXISTS container_id VARCHAR(255),
    ADD COLUMN IF NOT EXISTS truck_id VARCHAR(255),
    ADD COLUMN IF NOT EXISTS bill_of_lading VARCHAR(255),
    ADD COLUMN IF NOT EXISTS lane VARCHAR(255), -- e.g., 'JNPT-Delhi'
    ADD COLUMN IF NOT EXISTS planned_start_date TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS planned_end_date TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS actual_start_date TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS actual_end_date TIMESTAMPTZ;

CREATE INDEX idx_cases_external_id ON cases(external_id);
CREATE INDEX idx_cases_container_id ON cases(container_id);
CREATE INDEX idx_cases_truck_id ON cases(truck_id);
CREATE INDEX idx_cases_bill_of_lading ON cases(bill_of_lading);
CREATE INDEX idx_cases_lane ON cases(lane);

