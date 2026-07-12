-- STREAMING_CHUNK:Defining the Candidates table schema with identity resolution and multi-tenancy
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    organization_id TEXT NOT NULL DEFAULT 'default_org', -- Scopes candidates to recruitment firms/tenants
    name TEXT NOT NULL,
    email TEXT NOT NULL,                                  -- The structural "Identity Anchor"
    skills TEXT,                                          -- Stored as a JSON string array: ["Python", "FastAPI"]
    experience TEXT,                                      -- Detailed text representing profile and background
    preferred_roles TEXT,                                 -- Comma-separated or JSON list of target titles
    preferred_location TEXT,                              -- Desired location (e.g., "Remote", "New York")
    profile_fingerprint TEXT,                             -- Cryptographic representation of semantic qualifications state
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(organization_id, email)                        -- Blocks cross-organization identity collisions
);

-- STREAMING_CHUNK:Defining the Jobs table schema with lifecycle states and cryptographic uniqueness
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    organization_id TEXT NOT NULL DEFAULT 'default_org', -- Scopes scraped or manually injected jobs to an agency
    job_title TEXT NOT NULL,
    company TEXT,
    location TEXT,
    employment_type TEXT,
    salary TEXT,
    job_description TEXT,                                 -- Raw details scraped from the web
    requirements TEXT,                                    -- Stored as a JSON string array of core qualifications
    job_url TEXT,
    job_fingerprint TEXT,                                 -- SHA-256 hash representing unique title+company+location
    status TEXT DEFAULT 'Active',                         -- 'Active', 'Archived', 'Expired'
    source TEXT,
    last_verified TEXT,                                   -- Timestamp for link/activity validation worker
    date_found TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(organization_id, job_url),                     -- Prevents duplicate scrapers on identical links
    UNIQUE(organization_id, job_fingerprint)              -- Prevents duplicate postings under alternate URL routers
);

-- STREAMING_CHUNK:Defining the Evaluations bridge table to track static evaluations over time
CREATE TABLE IF NOT EXISTS evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    candidate_id INTEGER NOT NULL, 
    overall_score INTEGER,
    decision TEXT,                                        -- Strictly "Proceed", "Hold", or "Reject"
    strengths TEXT,                                       -- Stored as a JSON string array
    missing_skills TEXT,                                  -- Stored as a JSON string array
    reasoning TEXT,
    summary TEXT,
    candidate_snapshot_fingerprint TEXT,                  -- Tracks exactly which resume edition was scored
    evaluated_at TEXT,
    run_id TEXT,                                          -- Groups multiple evaluations under single workflow execution
    FOREIGN KEY(job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    FOREIGN KEY(candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
);

-- STREAMING_CHUNK:Defining the Applications table schema for progression mapping
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    candidate_id INTEGER NOT NULL, 
    resume_used TEXT,
    cover_letter TEXT,
    application_status TEXT DEFAULT 'Draft',              -- "Draft", "Submitted", "Interviewing", "Accepted", "Rejected"
    applied_at TEXT,
    FOREIGN KEY(job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    FOREIGN KEY(candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
);

-- STREAMING_CHUNK:Configuring performance indexes for scale and speed
CREATE INDEX IF NOT EXISTS idx_jobs_org_status ON jobs(organization_id, status);
CREATE INDEX IF NOT EXISTS idx_jobs_fingerprint ON jobs(job_fingerprint);
CREATE INDEX IF NOT EXISTS idx_candidates_org_email ON candidates(organization_id, email);
CREATE INDEX IF NOT EXISTS idx_evaluations_mapping ON evaluations(job_id, candidate_id);