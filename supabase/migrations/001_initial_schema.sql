-- Ward v0 Database Schema for Supabase PostgreSQL
-- Migration from MongoDB to PostgreSQL

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

-- Cases table (main disruptions)
CREATE TABLE cases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    operator_id UUID REFERENCES users(id) ON DELETE CASCADE,
    operator_email VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'REPORTED',
    decision_owner_id UUID REFERENCES users(id) ON DELETE SET NULL,
    decision_owner_email VARCHAR(255),
    
    -- Disruption details (stored as JSONB for flexibility)
    disruption_details JSONB NOT NULL DEFAULT '{}',
    shipment_identifiers JSONB DEFAULT '{}',
    financial_impact JSONB,
    structured_context JSONB,
    
    -- Evidence and responsibility
    evidence_score INTEGER DEFAULT 0,
    evidence_score_breakdown JSONB,
    responsibility JSONB,
    rca JSONB,
    enhanced_rca JSONB,
    rca_performed_at TIMESTAMPTZ,
    rca_performed_by VARCHAR(255),
    
    -- Coordination
    coordination_status VARCHAR(50),
    stakeholders JSONB,
    
    -- Voice and metadata
    voice_transcript TEXT,
    created_via VARCHAR(50),
    evidence_ready_at TIMESTAMPTZ,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_cases_operator_id ON cases(operator_id);
CREATE INDEX idx_cases_status ON cases(status);
CREATE INDEX idx_cases_decision_owner_email ON cases(decision_owner_email);
CREATE INDEX idx_cases_created_at ON cases(created_at);
CREATE INDEX idx_cases_updated_at ON cases(updated_at);
CREATE INDEX idx_cases_disruption_details ON cases USING GIN(disruption_details);

-- Timeline events
CREATE TABLE timeline_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID REFERENCES cases(id) ON DELETE CASCADE,
    actor VARCHAR(255) NOT NULL,
    action VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    source_type VARCHAR(50) NOT NULL,
    reliability VARCHAR(50) NOT NULL,
    metadata JSONB DEFAULT '{}',
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_timeline_events_case_id ON timeline_events(case_id);
CREATE INDEX idx_timeline_events_timestamp ON timeline_events(timestamp);
CREATE INDEX idx_timeline_events_case_timestamp ON timeline_events(case_id, timestamp);

-- Audit entries
CREATE TABLE audit_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id VARCHAR(255) NOT NULL, -- Keep as string for flexibility
    actor VARCHAR(255) NOT NULL,
    action VARCHAR(100) NOT NULL,
    payload JSONB DEFAULT '{}',
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_audit_entries_case_id ON audit_entries(case_id);
CREATE INDEX idx_audit_entries_timestamp ON audit_entries(timestamp);

-- Documents
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID REFERENCES cases(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    doc_type VARCHAR(100),
    analysis JSONB,
    uploaded_at TIMESTAMPTZ DEFAULT NOW(),
    uploaded_by VARCHAR(255) NOT NULL
);

CREATE INDEX idx_documents_case_id ON documents(case_id);
CREATE INDEX idx_documents_uploaded_at ON documents(uploaded_at);

-- Drafts (for AI decision flow)
CREATE TABLE drafts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID REFERENCES cases(id) ON DELETE CASCADE,
    decision_framing JSONB,
    known_inputs JSONB,
    declared_assumptions JSONB,
    alternatives JSONB,
    risk_and_downside JSONB,
    recommendation JSONB,
    ai_model VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_drafts_case_id ON drafts(case_id);

-- Approvals
CREATE TABLE approvals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID REFERENCES cases(id) ON DELETE CASCADE,
    section_key VARCHAR(100) NOT NULL,
    approved_by VARCHAR(255) NOT NULL,
    approved_at TIMESTAMPTZ DEFAULT NOW(),
    content_snapshot JSONB
);

CREATE INDEX idx_approvals_case_id ON approvals(case_id);
CREATE INDEX idx_approvals_case_section ON approvals(case_id, section_key);

-- Decisions
CREATE TABLE decisions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID REFERENCES cases(id) ON DELETE CASCADE,
    final_choice VARCHAR(255) NOT NULL,
    is_override BOOLEAN DEFAULT FALSE,
    override_rationale TEXT,
    recommended_choice VARCHAR(255),
    decided_by VARCHAR(255) NOT NULL,
    decided_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_decisions_case_id ON decisions(case_id);

-- Historical disruptions (read-only reference data)
CREATE TABLE historical (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    data JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_historical_created_at ON historical(created_at);

-- Master data (ports, carriers, etc.)
CREATE TABLE master_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_type VARCHAR(100) NOT NULL, -- 'port', 'carrier', 'location', etc.
    code VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(entity_type, code)
);

CREATE INDEX idx_master_data_type ON master_data(entity_type);
CREATE INDEX idx_master_data_code ON master_data(code);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_cases_updated_at BEFORE UPDATE ON cases
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_drafts_updated_at BEFORE UPDATE ON drafts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

