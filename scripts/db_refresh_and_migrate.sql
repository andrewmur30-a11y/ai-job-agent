-- STREAMING_CHUNK:Preparing DB Browser execution options

/* 
================================================================================
OPTION A: THE FRESH START (RECOMMENDED)
================================================================================
If you do not have precious manual data in your database yet, running this block
will wipe the old tables and create the brand new schema with all performance indexes.

To run this:
1. Copy the block below.
2. Paste it into the "Execute SQL" tab in DB Browser.
3. Click the "Play" button (or press F5) to run.
4. Go back to your terminal and run 'python scripts/seed_database.py' to repopulate it!
*/

-- Disable foreign keys temporarily to avoid delete order issues
PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS applications;
DROP TABLE IF EXISTS evaluations;
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS candidates;

-- Re-enable foreign keys
PRAGMA foreign_keys = ON;

-- STREAMING_CHUNK:Recreating the Candidates table with identity resolution
CREATE TABLE candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    organization_id TEXT NOT NULL DEFAULT 'default_org',
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    skills TEXT,
    experience TEXT,
    preferred_roles TEXT,
    preferred_location TEXT,
    profile_fingerprint TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(organization_id, email)
);

-- STREAMING_CHUNK:Recreating the Jobs table with lifecycle states
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    organization_id TEXT NOT NULL DEFAULT 'default_org',
    job_title TEXT NOT NULL,
    company TEXT,
    location TEXT,
    employment_type TEXT,
    salary TEXT,
    job_description TEXT,
    requirements TEXT,
    job_url TEXT,
    job_fingerprint TEXT,
    status TEXT DEFAULT 'Active',
    source TEXT,
    last_verified TEXT,
    date_found TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(organization_id, job_url),
    UNIQUE(organization_id, job_fingerprint)
);

-- STREAMING_CHUNK:Recreating the Evaluations table
CREATE TABLE evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    candidate_id INTEGER NOT NULL, 
    overall_score INTEGER,
    decision TEXT,
    strengths TEXT,
    missing_skills TEXT,
    reasoning TEXT,
    summary TEXT,
    candidate_snapshot_fingerprint TEXT,
    evaluated_at TEXT,
    run_id TEXT,
    FOREIGN KEY(job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    FOREIGN KEY(candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
);

-- STREAMING_CHUNK:Recreating the Applications table
CREATE TABLE applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    candidate_id INTEGER NOT NULL, 
    resume_used TEXT,
    cover_letter TEXT,
    application_status TEXT DEFAULT 'Draft',
    applied_at TEXT,
    FOREIGN KEY(job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    FOREIGN KEY(candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
);

-- STREAMING_CHUNK:Creating high-speed performance indexes
CREATE INDEX idx_jobs_org_status ON jobs(organization_id, status);
CREATE INDEX idx_jobs_fingerprint ON jobs(job_fingerprint);
CREATE INDEX idx_candidates_org_email ON candidates(organization_id, email);
CREATE INDEX idx_evaluations_mapping ON evaluations(job_id, candidate_id);


/* 
================================================================================
OPTION B: MANUAL MIGRATION (DATA PRESERVATION)
================================================================================
If you have data in your database that you DO NOT want to lose, do not run the 
"Option A" block. Instead, highlight and run ONLY these ALTER TABLE commands 
to safely inject the new columns into your existing tables.
*/

/*
ALTER TABLE candidates ADD COLUMN organization_id TEXT NOT NULL DEFAULT 'default_org';
ALTER TABLE candidates ADD COLUMN email TEXT NOT NULL DEFAULT 'placeholder@nexient.ai';
ALTER TABLE candidates ADD COLUMN profile_fingerprint TEXT;

ALTER TABLE jobs ADD COLUMN organization_id TEXT NOT NULL DEFAULT 'default_org';
ALTER TABLE jobs ADD COLUMN requirements TEXT;
ALTER TABLE jobs ADD COLUMN job_fingerprint TEXT;
ALTER TABLE jobs ADD COLUMN status TEXT DEFAULT 'Active';
ALTER TABLE jobs ADD COLUMN last_verified TEXT;

ALTER TABLE evaluations ADD COLUMN candidate_snapshot_fingerprint TEXT;

CREATE INDEX IF NOT EXISTS idx_jobs_org_status ON jobs(organization_id, status);
CREATE INDEX IF NOT EXISTS idx_jobs_fingerprint ON jobs(job_fingerprint);
CREATE INDEX IF NOT EXISTS idx_candidates_org_email ON candidates(organization_id, email);
*/
```eof

We created a custom SQL script detailing both the Fresh Start and the Manual Migration. Option A is highly recommended because it wipes out any messy database anomalies and ensures our newly seeded profiles match perfectly. Remember to hit **"Write Changes"** (or Save) at the top of DB Browser after executing the SQL so the updates are permanently committed to your SQLite database!