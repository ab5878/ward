-- Ward Operator & Fleet Management Tables
-- This migration adds tables for transport operator accounts, fleet management, and driver onboarding

-- Operators table (transport companies)
CREATE TABLE operators (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50),
    fleet_size INTEGER DEFAULT 0,
    account_type VARCHAR(50) DEFAULT 'pilot', -- 'pilot', 'standard', 'enterprise'
    settings JSONB DEFAULT '{}', -- notifications, webhooks, branding
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES users(id) ON DELETE SET NULL
);
CREATE INDEX idx_operators_email ON operators(email);
CREATE INDEX idx_operators_account_type ON operators(account_type);

-- Fleet Vehicles table
CREATE TABLE fleet_vehicles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    operator_id UUID REFERENCES operators(id) ON DELETE CASCADE,
    vehicle_number VARCHAR(100) NOT NULL,
    vehicle_type VARCHAR(50) DEFAULT 'truck', -- 'truck', 'container', 'trailer'
    driver_name VARCHAR(255),
    driver_phone VARCHAR(50),
    route VARCHAR(255), -- e.g., "JNPT-Delhi"
    status VARCHAR(50) DEFAULT 'active', -- 'active', 'inactive', 'maintenance'
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(operator_id, vehicle_number)
);
CREATE INDEX idx_fleet_vehicles_operator_id ON fleet_vehicles(operator_id);
CREATE INDEX idx_fleet_vehicles_vehicle_number ON fleet_vehicles(vehicle_number);
CREATE INDEX idx_fleet_vehicles_status ON fleet_vehicles(status);

-- Magic Links table (for driver onboarding - no login required)
CREATE TABLE magic_links (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    operator_id UUID REFERENCES operators(id) ON DELETE CASCADE,
    vehicle_id UUID REFERENCES fleet_vehicles(id) ON DELETE CASCADE,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    used_count INTEGER DEFAULT 0,
    max_uses INTEGER DEFAULT NULL, -- NULL = unlimited
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_used_at TIMESTAMPTZ
);
CREATE INDEX idx_magic_links_token ON magic_links(token);
CREATE INDEX idx_magic_links_operator_id ON magic_links(operator_id);
CREATE INDEX idx_magic_links_expires_at ON magic_links(expires_at);

-- Webhooks table (for operator integrations)
CREATE TABLE webhooks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    operator_id UUID REFERENCES operators(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    events TEXT[] NOT NULL, -- ['disruption_reported', 'evidence_ready', 'dispute_generated']
    secret VARCHAR(255), -- For webhook signature verification
    active BOOLEAN DEFAULT true,
    last_triggered_at TIMESTAMPTZ,
    failure_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_webhooks_operator_id ON webhooks(operator_id);
CREATE INDEX idx_webhooks_active ON webhooks(active);

-- Link cases to vehicles (for operator tracking)
ALTER TABLE cases
    ADD COLUMN vehicle_id UUID REFERENCES fleet_vehicles(id) ON DELETE SET NULL;

CREATE INDEX idx_cases_vehicle_id ON cases(vehicle_id);

-- Add triggers for updated_at
CREATE TRIGGER update_operators_updated_at BEFORE UPDATE ON operators
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_fleet_vehicles_updated_at BEFORE UPDATE ON fleet_vehicles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_webhooks_updated_at BEFORE UPDATE ON webhooks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

