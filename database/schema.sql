CREATE TABLE candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    profile TEXT,
    preferred_roles TEXT,
    preferred_location TEXT,
    created_at TEXT
);

CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_title TEXT NOT NULL,
    company TEXT,
    location TEXT,
    employment_type TEXT,
    salary TEXT,
    job_description TEXT,
    job_url TEXT,
    source TEXT,
    date_found TEXT
);

CREATE TABLE evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER,
    overall_score INTEGER,
    decision TEXT,
    strengths TEXT,
    missing_skills TEXT,
    reasoning TEXT,
    summary TEXT,
    evaluated_at TEXT,
    run_id TEXT UNIQUE,
    FOREIGN KEY(job_id) REFERENCES jobs(id)
);

CREATE TABLE applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER,
    resume_used TEXT,
    cover_letter TEXT,
    application_status TEXT,
    applied_at TEXT,
    FOREIGN KEY(job_id) REFERENCES jobs(id)
);