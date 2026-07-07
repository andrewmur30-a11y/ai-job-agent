-- STREAMING_CHUNK:Defining the Candidates table schema with skills and preferences
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    skills TEXT,                 -- Stored as a JSON string array: ["Python", "FastAPI"]
    experience TEXT,             -- Detailed text representing profile and background
    preferred_roles TEXT,        -- Comma-separated or JSON list of target titles
    preferred_location TEXT,     -- Desired location (e.g., "Remote", "New York")
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- STREAMING_CHUNK:Defining the Jobs table schema with market metadata and requirements
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_title TEXT NOT NULL,
    company TEXT,
    location TEXT,
    employment_type TEXT,
    salary TEXT,
    job_description TEXT,        -- Raw details scraped from the web
    requirements TEXT,           -- Stored as a JSON string array of core qualifications
    job_url TEXT,
    source TEXT,
    date_found TEXT DEFAULT CURRENT_TIMESTAMP
);

-- STREAMING_CHUNK:Defining the Evaluations relational bridge table schema
CREATE TABLE IF NOT EXISTS evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    candidate_id INTEGER NOT NULL, -- Crucial: Added candidate linkage to support dynamic multi-candidate routing
    overall_score INTEGER,
    decision TEXT,                -- Strictly "Proceed", "Hold", or "Reject"
    strengths TEXT,               -- Stored as a JSON string array
    missing_skills TEXT,          -- Stored as a JSON string array
    reasoning TEXT,
    summary TEXT,
    evaluated_at TEXT,
    run_id TEXT,                  -- Removed UNIQUE! Allowing multiple evaluations per workflow run
    FOREIGN KEY(job_id) REFERENCES jobs(id),
    FOREIGN KEY(candidate_id) REFERENCES candidates(id)
);

-- STREAMING_CHUNK:Defining the Applications table schema for conversion funnel tracking
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    candidate_id INTEGER NOT NULL, -- Added candidate linkage for multi-user/multi-profile compatibility
    resume_used TEXT,
    cover_letter TEXT,
    application_status TEXT,       -- "Draft", "Submitted", "Interviewing", "Accepted", "Rejected"
    applied_at TEXT,
    FOREIGN KEY(job_id) REFERENCES jobs(id),
    FOREIGN KEY(candidate_id) REFERENCES candidates(id)
);