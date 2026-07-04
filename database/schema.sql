CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    title TEXT NOT NULL,
    location TEXT,
    remote_type TEXT,
    employment_type TEXT,
    salary_min REAL,
    salary_max REAL,
    salary_currency TEXT,
    description TEXT NOT NULL,
    source TEXT,
    url TEXT,
    job_hash TEXT,
    date_found TEXT
);

CREATE TABLE evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    overall_score INTEGER,
    decision TEXT,
    strengths TEXT,
    missing_skills TEXT,
    reasoning TEXT,
    summary TEXT,
    evaluated_at TEXT,
    FOREIGN KEY (job_id) REFERENCES jobs(id)
);

CREATE TABLE applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    resume_path TEXT,
    cover_letter_path TEXT,
    status TEXT,
    applied_at TEXT,
    FOREIGN KEY (job_id) REFERENCES jobs(id)
);