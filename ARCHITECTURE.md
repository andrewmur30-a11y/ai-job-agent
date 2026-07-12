# AI Job Agent - System Architecture

## Overview

AI Job Agent is a local-first, AI-powered recruitment automation platform designed to operate with complete data privacy, high cost-efficiency, and transactional reliability.

The platform executes a multi-step pipeline: it ingests unstructured candidate resumes (PDF or Word), parses them into structured profile models using a local LLM, dynamically cross-evaluates candidates against available job requirements, and writes normalized matching metrics to an index-optimized SQLite database.

---

# Architectural Diagram


+---------------------------------------------------------------------------------+
|                                 USER GATEWAY                                    |
|         Interactive API Docs (Swagger)  <--->  Local CLI Sandbox Tools          |
+---------------------------------------+-----------------------------------------+
                                        |
                                        v (File Upload / JSON POST)
+---------------------------------------------------------------------------------+
|                                 FASTAPI SERVER                                  |
|                                  (Port 8000)                                    |
|                                                                                 |
|  [Ingestion / Route Parsing] --> [Ollama/LLM Parser] --> [State Hashing]        |
|   - PDF Layout Extraction        - qwen2.5:7b           - SHA-256 Profile       |
|   - DOCX Paragraph Parser        - Strict JSON Schema     Fingerprint           |
+---------------------------------------+-----------------------------------------+
                                        |
                                        v (Identity & Deduplication Gates)
+---------------------------------------------------------------------------------+
|                                SQLITE DATABASE                                  |
|                          (database/job_agent.db | WAL Mode)                     |
|                                                                                 |
|   Candidates Table <---> Jobs Table <---> Evaluations Table                     |
|   (Identity Anchored)                  (Duplicate/Fingerprint Guard)            |
+---------------------------------------+-----------------------------------------+
                                        ^
                                        | (Dynamic Hydration & Processing)
+---------------------------------------------------------------------------------+
|                                  n8n WORKFLOW                                   |
|                                  (Port 5678)                                    |
|                                                                                 |
|  [GET Candidates] + [GET Jobs] --> [Multiplex Cross-Join] --> [Ollama Call]     |
+---------------------------------------------------------------------------------+



# Technical Specifications

## 1. FastAPI Gateway & Verification Routes

Our FastAPI backend serves as the sole write interface and central schema-enforcement layer to the SQLite database. It manages six highly specialized endpoints.

### POST /candidates/import

Expects a multipart file upload (`.pdf` or `.docx`). Extracts raw layout text, prompts Ollama, hashes the result, resolves the candidate's identity using their email anchor, and saves or updates the profile in SQLite.

### POST /save-evaluation

Receives structural match assessments, implements an idempotency guard to block redundant database writes, and stores clean matching metrics.

### GET /candidates

Fetches all registered candidate records.

### GET /candidate/{candidate_id}

Dynamic, resilient fetch for individual candidate profiles. Inspects table schemas using `PRAGMA` to prevent crashes during database schema migrations.

### GET /jobs

Retrieves all target job descriptions.

### GET /job/{job_id}

Retrieves a single job posting by primary key.

---

## 2. Cryptographic Profile State Tracking (Fingerprinting)

To ensure the pipeline is cost-effective and resilient against duplicate executions, we implement a **Candidate Profile Fingerprint Strategy**.


Candidate Profile Fingerprint = SHA-256(
    Sorted Skills
    + Cleaned Experience
    + Sorted Preferred Roles


### Purpose

A deterministic signature representing the exact semantic qualifications of a candidate.

### Behavior

If a candidate uploads an identical resume, or makes an update that doesn't affect their professional profile (for example, correcting an address typo), the fingerprint remains identical.

The database skips re-evaluation, saving significant GPU cycles.

If their skills or experience change, a fingerprint mismatch is detected and a fresh evaluation is safely authorized.

---

## 3. Local LLM Parsing Pipeline (Ollama)

Instead of relying on fragile regex parsers or expensive cloud APIs, resume processing is performed by a local Qwen2.5-7B model managed by Ollama.

### JSON Constraints

The prompt uses native structural requirements to force Qwen into outputting a raw JSON object containing:

- name
- email
- skills
- experience
- preferred_roles
- preferred_location

### Sanitization

The backend Python parser removes Markdown code fences (for example, JSON wrapped in triple backticks) to guarantee valid JSON deserialization.

---

## 4. Database Transaction Safeguards

SQLite is configured with production-grade settings to prevent lockouts during high-concurrency loops.

### Write-Ahead Logging (WAL)

Enabled using:

PRAGMA journal_mode = WAL;

This allows concurrent reads while write transactions are executing.

### Busy Connection Timeout

Database connections are configured with a **10-second busy timeout**, allowing rapid write operations to queue safely instead of immediately failing due to database locks.

---

# Current Status & Capabilities

- ✅ Validated ingestion of both Word and PDF resume formats.
- ✅ Validated candidate identity resolution using email anchoring.
- ✅ Fully tested integration across all internal API endpoints.
- ✅ 100% success rate across automated endpoint validation tests.