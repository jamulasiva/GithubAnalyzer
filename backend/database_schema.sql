-- GitHub Audit Platform Database Schema
-- Designed based on webhook_models Pydantic models
-- Optimized for Supabase PostgreSQL with performance and audit requirements

-- =============================================================================
-- CORE ENTITY TABLES (Based on common models)
-- =============================================================================

-- Organizations table (from common/organization.py)
CREATE TABLE organizations (
    id SERIAL PRIMARY KEY,
    github_id BIGINT UNIQUE NOT NULL,
    login VARCHAR(255) NOT NULL,
    node_id VARCHAR(255) NOT NULL,
    url TEXT NOT NULL,
    repos_url TEXT NOT NULL,
    events_url TEXT NOT NULL,
    hooks_url TEXT NOT NULL,
    issues_url TEXT NOT NULL,
    members_url TEXT NOT NULL,
    public_members_url TEXT NOT NULL,
    avatar_url TEXT NOT NULL,
    description TEXT,
    name VARCHAR(255),
    company VARCHAR(255),
    blog VARCHAR(255),
    location VARCHAR(255),
    email VARCHAR(255),
    twitter_username VARCHAR(255),
    is_verified BOOLEAN DEFAULT FALSE,
    has_organization_projects BOOLEAN,
    has_repository_projects BOOLEAN,
    public_repos INTEGER,
    public_gists INTEGER,
    followers INTEGER,
    following INTEGER,
    html_url TEXT,
    type VARCHAR(50) DEFAULT 'Organization',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    github_created_at TIMESTAMP WITH TIME ZONE,
    github_updated_at TIMESTAMP WITH TIME ZONE,
    
    CONSTRAINT org_github_id_check CHECK (github_id > 0)
);

-- Users table (from common/user.py)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    github_id BIGINT UNIQUE NOT NULL,
    login VARCHAR(255) NOT NULL,
    node_id VARCHAR(255) NOT NULL,
    avatar_url TEXT,
    gravatar_id VARCHAR(255),
    url TEXT NOT NULL,
    html_url TEXT NOT NULL,
    followers_url TEXT,
    following_url TEXT,
    gists_url TEXT,
    starred_url TEXT,
    subscriptions_url TEXT,
    organizations_url TEXT,
    repos_url TEXT,
    events_url TEXT,
    received_events_url TEXT,
    type VARCHAR(50) DEFAULT 'User',
    site_admin BOOLEAN DEFAULT FALSE,
    name VARCHAR(255),
    company VARCHAR(255),
    blog VARCHAR(255),
    location VARCHAR(255),
    email VARCHAR(255),
    hireable BOOLEAN,
    bio TEXT,
    twitter_username VARCHAR(255),
    public_repos INTEGER,
    public_gists INTEGER,
    followers INTEGER,
    following INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    github_created_at TIMESTAMP WITH TIME ZONE,
    github_updated_at TIMESTAMP WITH TIME ZONE,
    
    CONSTRAINT user_github_id_check CHECK (github_id > 0)
);

-- Repositories table (from common/repository.py)
CREATE TABLE repositories (
    id SERIAL PRIMARY KEY,
    github_id BIGINT UNIQUE NOT NULL,
    node_id VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL UNIQUE,
    owner_id INTEGER REFERENCES users(id),
    organization_id INTEGER REFERENCES organizations(id),
    private BOOLEAN DEFAULT FALSE,
    html_url TEXT NOT NULL,
    description TEXT,
    fork BOOLEAN DEFAULT FALSE,
    url TEXT NOT NULL,
    archive_url TEXT,
    assignees_url TEXT,
    blobs_url TEXT,
    branches_url TEXT,
    clone_url TEXT,
    collaborators_url TEXT,
    comments_url TEXT,
    commits_url TEXT,
    compare_url TEXT,
    contents_url TEXT,
    contributors_url TEXT,
    deployments_url TEXT,
    downloads_url TEXT,
    events_url TEXT,
    forks_url TEXT,
    git_commits_url TEXT,
    git_refs_url TEXT,
    git_tags_url TEXT,
    git_url TEXT,
    hooks_url TEXT,
    issue_comment_url TEXT,
    issue_events_url TEXT,
    issues_url TEXT,
    keys_url TEXT,
    labels_url TEXT,
    languages_url TEXT,
    merges_url TEXT,
    milestones_url TEXT,
    notifications_url TEXT,
    pulls_url TEXT,
    releases_url TEXT,
    ssh_url TEXT,
    stargazers_url TEXT,
    statuses_url TEXT,
    subscribers_url TEXT,
    subscription_url TEXT,
    tags_url TEXT,
    teams_url TEXT,
    trees_url TEXT,
    homepage VARCHAR(255),
    size INTEGER,
    stargazers_count INTEGER,
    watchers_count INTEGER,
    language VARCHAR(100),
    has_issues BOOLEAN DEFAULT TRUE,
    has_projects BOOLEAN DEFAULT TRUE,
    has_wiki BOOLEAN DEFAULT TRUE,
    has_pages BOOLEAN DEFAULT FALSE,
    forks_count INTEGER,
    archived BOOLEAN DEFAULT FALSE,
    disabled BOOLEAN DEFAULT FALSE,
    open_issues_count INTEGER,
    license_key VARCHAR(50),
    allow_forking BOOLEAN DEFAULT TRUE,
    is_template BOOLEAN DEFAULT FALSE,
    topics TEXT[], -- PostgreSQL array for topics
    visibility VARCHAR(20) DEFAULT 'public',
    default_branch VARCHAR(255) DEFAULT 'main',
    temp_clone_token VARCHAR(255),
    allow_squash_merge BOOLEAN DEFAULT TRUE,
    allow_merge_commit BOOLEAN DEFAULT TRUE,
    allow_rebase_merge BOOLEAN DEFAULT TRUE,
    allow_auto_merge BOOLEAN DEFAULT FALSE,
    delete_branch_on_merge BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    github_created_at TIMESTAMP WITH TIME ZONE,
    github_updated_at TIMESTAMP WITH TIME ZONE,
    github_pushed_at TIMESTAMP WITH TIME ZONE,
    
    CONSTRAINT repo_github_id_check CHECK (github_id > 0),
    CONSTRAINT repo_visibility_check CHECK (visibility IN ('public', 'private', 'internal'))
);

-- Installations table (from common/installation.py)
CREATE TABLE installations (
    id SERIAL PRIMARY KEY,
    github_id BIGINT UNIQUE NOT NULL,
    app_id INTEGER NOT NULL,
    app_slug VARCHAR(255),
    target_id INTEGER,
    target_type VARCHAR(50),
    repository_selection VARCHAR(20),
    access_tokens_url TEXT,
    repositories_url TEXT,
    html_url TEXT,
    permissions JSONB,
    events TEXT[], -- Array of event types
    single_file_name VARCHAR(255),
    has_multiple_single_files BOOLEAN DEFAULT FALSE,
    single_file_paths TEXT[],
    suspended_by_id INTEGER REFERENCES users(id),
    suspended_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT install_github_id_check CHECK (github_id > 0),
    CONSTRAINT install_repo_selection_check CHECK (repository_selection IN ('all', 'selected'))
);

-- =============================================================================
-- AUDIT EVENT TABLES (Based on webhook events)
-- =============================================================================

-- Main webhook events table - stores all events with normalized data
CREATE TABLE webhook_events (
    id SERIAL PRIMARY KEY,
    event_id UUID DEFAULT gen_random_uuid(),
    delivery_id VARCHAR(255) UNIQUE, -- GitHub delivery ID
    event_type VARCHAR(100) NOT NULL,
    event_action VARCHAR(100),
    
    -- Foreign key references to entities
    organization_id INTEGER REFERENCES organizations(id),
    repository_id INTEGER REFERENCES repositories(id),
    sender_id INTEGER REFERENCES users(id),
    installation_id INTEGER REFERENCES installations(id),
    
    -- Event metadata
    event_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    received_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processed BOOLEAN DEFAULT FALSE,
    processed_at TIMESTAMP WITH TIME ZONE,
    processing_error TEXT,
    retry_count INTEGER DEFAULT 0,
    
    -- Store complete payload as JSONB for flexibility
    payload JSONB NOT NULL,
    headers JSONB,
    
    -- Computed fields from payload for performance
    sender_login VARCHAR(255),
    repository_name VARCHAR(255),
    organization_login VARCHAR(255),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT event_type_check CHECK (event_type IN (
        'member', 'repository', 'push', 'issues', 'pull_request', 
        'team', 'fork', 'create', 'delete', 'issue_comment',
        'pull_request_review', 'ping', 'installation', 'organization',
        'code_scanning_alert', 'dependabot_alert', 'secret_scanning_alert',
        'meta', 'personal_access_token_request'
    ))
);

-- =============================================================================
-- SPECIALIZED EVENT TABLES (For frequent queries and analytics)
-- =============================================================================

-- Repository events (create, delete, visibility changes, etc.)
CREATE TABLE repository_events (
    id SERIAL PRIMARY KEY,
    webhook_event_id INTEGER REFERENCES webhook_events(id),
    repository_id INTEGER REFERENCES repositories(id),
    action VARCHAR(100) NOT NULL,
    changes JSONB, -- Store what changed (for edited events)
    event_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT repo_event_action_check CHECK (action IN (
        'created', 'deleted', 'archived', 'unarchived', 'edited', 
        'publicized', 'privatized', 'transferred'
    ))
);

-- Member/collaboration events
CREATE TABLE member_events (
    id SERIAL PRIMARY KEY,
    webhook_event_id INTEGER REFERENCES webhook_events(id),
    repository_id INTEGER REFERENCES repositories(id),
    organization_id INTEGER REFERENCES organizations(id),
    member_id INTEGER REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    permission_level VARCHAR(50),
    changes JSONB, -- Store permission changes
    event_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT member_event_action_check CHECK (action IN (
        'added', 'removed', 'edited', 'invited', 'member_invited', 
        'member_added', 'member_removed'
    ))
);

-- Security events (alerts, scanning, etc.)
CREATE TABLE security_events (
    id SERIAL PRIMARY KEY,
    webhook_event_id INTEGER REFERENCES webhook_events(id),
    repository_id INTEGER REFERENCES repositories(id),
    alert_type VARCHAR(100) NOT NULL,
    alert_number INTEGER,
    action VARCHAR(100) NOT NULL,
    state VARCHAR(50),
    severity VARCHAR(50),
    rule_id VARCHAR(255),
    tool_name VARCHAR(100),
    secret_type VARCHAR(100),
    event_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT security_alert_type_check CHECK (alert_type IN (
        'code_scanning_alert', 'dependabot_alert', 'secret_scanning_alert'
    )),
    CONSTRAINT security_action_check CHECK (action IN (
        'created', 'fixed', 'dismissed', 'reopened', 'resolved', 'revoked'
    ))
);

-- Code activity events (push, commits, branches, tags)
CREATE TABLE code_events (
    id SERIAL PRIMARY KEY,
    webhook_event_id INTEGER REFERENCES webhook_events(id),
    repository_id INTEGER REFERENCES repositories(id),
    event_type VARCHAR(100) NOT NULL,
    ref_name VARCHAR(255), -- branch/tag name
    ref_type VARCHAR(20), -- 'branch' or 'tag'
    before_sha VARCHAR(255),
    after_sha VARCHAR(255),
    commits_count INTEGER DEFAULT 0,
    distinct_commits_count INTEGER DEFAULT 0,
    forced BOOLEAN DEFAULT FALSE,
    event_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT code_event_type_check CHECK (event_type IN (
        'push', 'create', 'delete', 'fork'
    )),
    CONSTRAINT code_ref_type_check CHECK (ref_type IN ('branch', 'tag') OR ref_type IS NULL)
);

-- =============================================================================
-- RELATIONSHIP TABLES
-- =============================================================================

-- Organization memberships
CREATE TABLE organization_memberships (
    id SERIAL PRIMARY KEY,
    organization_id INTEGER REFERENCES organizations(id),
    user_id INTEGER REFERENCES users(id),
    role VARCHAR(50) NOT NULL DEFAULT 'member',
    state VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(organization_id, user_id),
    CONSTRAINT membership_role_check CHECK (role IN ('member', 'admin', 'billing_manager')),
    CONSTRAINT membership_state_check CHECK (state IN ('active', 'pending'))
);

-- Repository collaborators
CREATE TABLE repository_collaborators (
    id SERIAL PRIMARY KEY,
    repository_id INTEGER REFERENCES repositories(id),
    user_id INTEGER REFERENCES users(id),
    permission VARCHAR(50) NOT NULL DEFAULT 'read',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(repository_id, user_id),
    CONSTRAINT collaborator_permission_check CHECK (permission IN ('read', 'write', 'admin', 'maintain', 'triage'))
);

-- =============================================================================
-- PERFORMANCE INDEXES
-- =============================================================================

-- Webhook events indexes
CREATE INDEX idx_webhook_events_timestamp ON webhook_events(event_timestamp DESC);
CREATE INDEX idx_webhook_events_type_timestamp ON webhook_events(event_type, event_timestamp DESC);
CREATE INDEX idx_webhook_events_repo_timestamp ON webhook_events(repository_id, event_timestamp DESC) WHERE repository_id IS NOT NULL;
CREATE INDEX idx_webhook_events_org_timestamp ON webhook_events(organization_id, event_timestamp DESC) WHERE organization_id IS NOT NULL;
CREATE INDEX idx_webhook_events_sender ON webhook_events(sender_id) WHERE sender_id IS NOT NULL;
CREATE INDEX idx_webhook_events_processed ON webhook_events(processed, received_at) WHERE NOT processed;
CREATE INDEX idx_webhook_events_delivery ON webhook_events(delivery_id);

-- JSONB payload indexes for fast queries
CREATE INDEX idx_webhook_events_payload_gin ON webhook_events USING GIN(payload);
CREATE INDEX idx_webhook_events_action ON webhook_events((payload->>'action'));

-- Entity indexes
CREATE INDEX idx_organizations_login ON organizations(login);
CREATE INDEX idx_users_login ON users(login);
CREATE INDEX idx_repositories_full_name ON repositories(full_name);
CREATE INDEX idx_repositories_owner ON repositories(owner_id);
CREATE INDEX idx_repositories_org ON repositories(organization_id);

-- Event-specific indexes
CREATE INDEX idx_repository_events_timestamp ON repository_events(event_timestamp DESC);
CREATE INDEX idx_member_events_timestamp ON member_events(event_timestamp DESC);
CREATE INDEX idx_security_events_timestamp ON security_events(event_timestamp DESC);
CREATE INDEX idx_code_events_timestamp ON code_events(event_timestamp DESC);

-- =============================================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- =============================================================================

-- Enable RLS on all tables
ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE repositories ENABLE ROW LEVEL SECURITY;
ALTER TABLE installations ENABLE ROW LEVEL SECURITY;
ALTER TABLE webhook_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE repository_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE member_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE security_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE code_events ENABLE ROW LEVEL SECURITY;

-- Basic RLS policies (will be refined based on auth requirements)
CREATE POLICY "Users can read all data" ON webhook_events FOR SELECT TO authenticated USING (true);
CREATE POLICY "Service role can manage all data" ON webhook_events FOR ALL TO service_role USING (true);

-- =============================================================================
-- FUNCTIONS AND TRIGGERS
-- =============================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply updated_at triggers to relevant tables
CREATE TRIGGER tr_organizations_updated_at BEFORE UPDATE ON organizations FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_repositories_updated_at BEFORE UPDATE ON repositories FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_memberships_updated_at BEFORE UPDATE ON organization_memberships FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_collaborators_updated_at BEFORE UPDATE ON repository_collaborators FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Function to extract and update computed fields from webhook payload
CREATE OR REPLACE FUNCTION update_webhook_computed_fields()
RETURNS TRIGGER AS $$
BEGIN
    -- Extract sender login
    NEW.sender_login = NEW.payload->'sender'->>'login';
    
    -- Extract repository name
    IF NEW.payload->'repository' IS NOT NULL THEN
        NEW.repository_name = NEW.payload->'repository'->>'full_name';
    END IF;
    
    -- Extract organization login
    IF NEW.payload->'organization' IS NOT NULL THEN
        NEW.organization_login = NEW.payload->'organization'->>'login';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_webhook_computed_fields 
BEFORE INSERT OR UPDATE ON webhook_events 
FOR EACH ROW EXECUTE FUNCTION update_webhook_computed_fields();

-- =============================================================================
-- VIEWS FOR COMMON QUERIES
-- =============================================================================

-- Recent events view with entity details
CREATE VIEW recent_events AS
SELECT 
    we.id,
    we.event_type,
    we.event_action,
    we.event_timestamp,
    we.sender_login,
    r.full_name as repository_name,
    o.login as organization_name,
    we.payload
FROM webhook_events we
LEFT JOIN repositories r ON we.repository_id = r.id
LEFT JOIN organizations o ON we.organization_id = o.id
ORDER BY we.event_timestamp DESC;

-- Security events summary view
CREATE VIEW security_events_summary AS
SELECT 
    se.alert_type,
    se.severity,
    se.state,
    COUNT(*) as count,
    r.full_name as repository_name,
    DATE_TRUNC('day', se.event_timestamp) as event_date
FROM security_events se
JOIN repositories r ON se.repository_id = r.id
GROUP BY se.alert_type, se.severity, se.state, r.full_name, DATE_TRUNC('day', se.event_timestamp);

-- Repository activity summary
CREATE VIEW repository_activity_summary AS
SELECT 
    r.full_name,
    COUNT(we.id) as total_events,
    COUNT(CASE WHEN we.event_type = 'push' THEN 1 END) as push_events,
    COUNT(CASE WHEN we.event_type = 'issues' THEN 1 END) as issue_events,
    COUNT(CASE WHEN we.event_type = 'pull_request' THEN 1 END) as pr_events,
    MAX(we.event_timestamp) as last_activity
FROM repositories r
LEFT JOIN webhook_events we ON r.id = we.repository_id
WHERE we.event_timestamp >= NOW() - INTERVAL '30 days'
GROUP BY r.id, r.full_name;