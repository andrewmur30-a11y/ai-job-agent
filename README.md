# AI Job Agent

An autonomous AI-powered recruitment assistant built with
LM Studio, n8n, FastAPI, SQLite and Playwright.

## Project Status

**Version:** 0.4 (In Development)

### Completed

- SQLite database
- Candidate persistence
- Job persistence
- Evaluation persistence
- FastAPI service layer
- n8n workflow
- LM Studio integration
- JSON parsing
- Duplicate prevention (run_id guardrails)

### Under Construction

- Live AI evaluation pipeline
- Database-driven candidate profile
- Automated job ingestion
- Multi-job evaluation
- Application generation

---

## Tech Stack

- Python 3.14
- SQLite
- FastAPI
- n8n
- LM Studio
- Qwen2.5-14B-Instruct-1M

---

## Project Structure

```
AI-Job-Agent/
│
├── database/
│   ├── schema.sql
│   └── job_agent.db
│
├── scripts/
│   ├── api.py
│   ├── database.py
│   ├── save_candidate.py
│   ├── save_evaluation.py
│
├── README.md
├── requirements.txt
└── CHANGELOG.md
```

---

## Database

### Candidates

Stores candidate profile information.

### Jobs

Stores discovered job postings.

### Evaluations

Stores AI evaluation results.

### Applications

Reserved for future automated applications.

---

## Current Workflow

```
Manual Trigger
        │
        ▼
Set Node
        │
        ▼
LM Studio
        │
        ▼
Code Node
(JSON Parsing)
        │
        ▼
FastAPI
        │
        ▼
SQLite
```

---

## Roadmap

### Version 0.5

- Complete AI evaluation pipeline
- Read candidate from database
- Save evaluations automatically

### Version 0.6

- Automated job ingestion
- Multi-job processing

### Version 0.7

- Resume selection
- Cover letter generation

### Version 1.0

- Fully autonomous AI Job Agent