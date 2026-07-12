# Changelog

All notable changes to the AI Job Agent project will be documented in this file.

---

# 2026-07-03

## ✅ Completed

- Restored n8n workflow
- Connected LM Studio
- Added candidate profile input
- Exported workflow
- Pushed project to GitHub

## 🎯 Next

- Improve structured JSON output
- Design SQLite schema

---

# 2026-07-04

## 🚧 Current State

**Under Construction**

## 🟢 Added

- FastAPI service layer for evaluation handling
- HTTP endpoint for saving evaluation results (`POST /save-evaluation`)
- SQLite integration for persistent storage of evaluations
- n8n → FastAPI integration via HTTP Request node
- End-to-end automation pipeline

  ```
  n8n → FastAPI → Python → SQLite
  ```

## 🟢 Working Features

- Candidate/job evaluation generation via AI workflow
- Structured JSON validation using Pydantic models
- Successful database writes confirmed in SQLite
- Swagger UI testing for API endpoints (`/docs`)

## 🟡 In Progress

- Evaluation deduplication logic (run_id idempotency)
- Full guardrail enforcement across workflow components
- LM Studio integration for dynamic AI-generated evaluations
- Schema hardening for production-grade stability

## 🧠 Notes

System architecture has been successfully validated end-to-end.

Current focus is incremental stabilization before introducing full LLM automation.

Core pipeline is functional and ready for the next integration phase.

---

# 2026-07-06

## 🚀 Major Milestone Achieved

### Database-Driven Evaluation Engine

## 🎯 Milestone

Successfully transitioned the evaluation pipeline from a proof-of-concept with hardcoded data into a fully database-driven workflow.

The evaluation engine now supports dynamic candidate retrieval, batch processing, and enterprise-grade duplicate protection.

## 🟢 Added

- FastAPI endpoint: `GET /candidates`
- Database-backed candidate and job retrieval endpoints
- Database helper modules for candidate queries
- Candidate and job seed scripts
- `candidate_id` tracking column added to the `evaluations` table
- Cross-node lineage tracking using `itemMatching($itemIndex)`

## 🔵 Modified & Refactored

- Updated `scripts/api.py` and Pydantic models for `candidate_id` validation
- Removed the hardcoded Set node from the n8n workflow
- Refactored workflow into:

  ```
  GET Candidates
      ↓
  GET Job
      ↓
  Multiplex Merge
      ↓
  Build Prompt
      ↓
  LM Studio
      ↓
  Save Evaluation
  ```

- Added a dedicated Build Prompt node
- Updated Merge node clash handling (`id_1` / `id_2`)
- Replaced `run_id` idempotency with `candidate_id + job_id`
- Improved prompt serialization using `JSON.stringify()`

## 🟢 Working Features

- Fully database-driven evaluation pipeline
- Dynamic candidate retrieval
- Dynamic job retrieval
- Batch evaluation
- Enterprise-grade duplicate prevention
- Dynamic prompt generation
- Successful end-to-end validation

  ```
  SQLite
      ↓
  FastAPI
      ↓
  n8n
      ↓
  LM Studio
      ↓
  SQLite
  ```

- Swagger API validation

## 🟡 Current Limitations

- Candidate records seeded manually
- Job records seeded manually
- Single selected job evaluated per workflow execution
- Automated job ingestion not yet implemented

## 🧠 Notes

This milestone transitions the project from a prototype into a reusable evaluation engine.

Architecture responsibilities are now clearly separated:

- SQLite manages persistent data.
- FastAPI exposes the data API.
- n8n orchestrates execution.
- LM Studio performs AI reasoning.

## 🎯 Next Milestone

- Build automated job ingestion
- Remove manual job seeding
- Normalize imported jobs
- Prepare unattended scheduled execution

---

# 2026-07-09

## 🚀 Major Milestone Achieved

### Batch Evaluation Engine

## 🎯 Milestone

Successfully evolved the evaluation engine from single-job processing into a true Candidate × Job batch evaluation engine.

Validated 75 evaluations (5 candidates × 15 jobs) in one execution.

## 🟢 Added

- Dynamic `GET /jobs` integration
- Candidate × Job matrix generation
- Full batch processing
- Ollama prompt generation
- Robust JSON parsing

## 🔵 Modified & Refactored

Migrated the workflow from LM Studio to Ollama.

New workflow:

```
GET Candidates
      ↓
GET Jobs
      ↓
Multiplex Merge
      ↓
Build Prompt
      ↓
Ollama
      ↓
Parse JSON
      ↓
Save Evaluation
```

Additional improvements:

- Simplified prompt generation
- Improved JSON parsing
- Preserved candidate/job lineage using `itemMatching($itemIndex)`

## 🟢 Working Features

- Dynamic candidate retrieval
- Dynamic job retrieval
- Candidate × Job matrix generation
- Local AI evaluation
- Structured JSON validation
- Duplicate prevention (`candidate_id + job_id`)
- 75 successful evaluations

## 📊 Performance Benchmark

| Metric | Result |
|---------|--------|
| Candidates | 5 |
| Jobs | 15 |
| Total Evaluations | 75 |
| Runtime | 4 minutes 5 seconds |
| Average Evaluation | ~3.27 seconds |

Performance optimization has intentionally been deferred until core functionality is complete.

## 🧠 Notes

The architecture is now LLM-provider agnostic.

Current provider:

- Ollama

Future providers could include:

- LM Studio
- OpenAI-compatible APIs

## 🎯 Next Milestone

- Candidate Profile Fingerprints
- Job Fingerprints
- Evaluation versioning

---

# 2026-07-11

## 🚀 Major Milestone Achieved

### Local Document Ingestion & Cryptographic Hashing

## 🎯 Milestone

Built a complete local ingestion pipeline supporting PDF and Word resume parsing.

Implemented identity-anchored email resolution and SHA-256 profile fingerprinting to detect meaningful profile changes while preventing unnecessary LLM evaluations.

## 🟢 Added

- `POST /candidates/import`
- Native PDF parser (`extract_text_from_pdf`)
- Native DOCX parser (`extract_text_from_docx`)
- `scripts/hashing_utils.py`
- `scripts/save_candidate.py`
- `scripts/test_resume_parser.py`
- `scripts/test_pdf_upload.py`
- `scripts/test_api_endpoints.py`

## 🔵 Modified & Refactored

- Updated `scripts/seed_database.py`
- Rebuilt `schema.sql` with WAL mode and busy timeout
- Hardened FastAPI routes
- Updated:

  - `README.md`
  - `docs/architecture.md`
  - `docs/project_todo_list.md`

## 🟢 Working Features

- Local PDF/Word extraction
- Local Qwen2.5 parsing through Ollama
- Email-based identity resolution
- SHA-256 candidate fingerprinting
- Interactive Swagger uploads
- Full regression test suite

## 🧠 Notes

This update bridges raw resume documents and persistent candidate records.

The pipeline now:

```
Resume
    ↓
Text Extraction
    ↓
Local LLM Structuring
    ↓
SHA-256 Fingerprint
    ↓
SQLite Save / Update
```

Development remains:

- 100% local
- Zero API costs
- Fully private

## 🎯 Next Milestone

- Begin Phase 2
- Playwright Job Scraper Engine
- Job normalization
- Job fingerprinting
- Manual Job Injection endpoints