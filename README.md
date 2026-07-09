# AI Job Agent

> **A local-first AI recruitment platform that evaluates candidates against job opportunities using a modular, database-driven architecture.**

---

## 🚀 Project Status

**Current Milestone:** Evaluation Engine MVP Complete

AI Job Agent has successfully evolved from a proof of concept into a fully database-driven candidate evaluation engine.

Current capabilities include:

* Dynamic candidate retrieval from SQLite
* Dynamic job retrieval from SQLite
* Batch candidate × job evaluation
* AI-powered candidate scoring using a local Large Language Model (LLM)
* Structured evaluation persistence
* Duplicate evaluation prevention
* Modular architecture designed for future autonomous job applications

---

# ✨ Features

## Current Features

* ✅ SQLite-backed candidate and job database
* ✅ FastAPI REST API
* ✅ n8n workflow orchestration
* ✅ Local LLM integration (currently Ollama)
* ✅ OpenAI-compatible inference architecture
* ✅ Structured JSON evaluation output
* ✅ Batch processing
* ✅ Duplicate protection
* ✅ Evaluation history persistence
* ✅ Swagger API documentation

---

# 🏗 High-Level Architecture

```text
                    Candidates
                         │
                         ▼
                   SQLite Database
                         │
                         ▼
                     FastAPI API
                         │
                         ▼
                n8n Evaluation Engine
                         │
                Build Evaluation Prompt
                         │
                         ▼
              Local LLM (Ollama / Compatible)
                         │
               Structured JSON Evaluation
                         │
                         ▼
                  FastAPI Persistence
                         │
                         ▼
                   SQLite Evaluations
```

The architecture is intentionally modular. Every component has a single responsibility, making it easy to replace or extend individual services without redesigning the system.

---

# ⚙ Technology Stack

| Layer                          | Technology                                |
| ------------------------------ | ----------------------------------------- |
| Language                       | Python                                    |
| Database                       | SQLite                                    |
| API                            | FastAPI                                   |
| Workflow Orchestration         | n8n                                       |
| AI Inference                   | Ollama                                    |
| Compatible Inference Providers | LM Studio, Ollama, OpenAI-compatible APIs |
| Validation                     | Pydantic                                  |
| Version Control                | Git & GitHub                              |

---

# 📂 Repository Structure

```text
AI-Job-Agent/

├── database/          SQLite databases
├── docker/            Docker Compose & n8n configuration
├── docs/              Project documentation
├── logs/              Runtime logs
├── output/            Generated outputs
├── prompts/           Prompt templates
├── resumes/           Candidate resumes
├── scripts/           FastAPI, database helpers, seed scripts
├── tests/             Test suite
├── workflows/         n8n workflow exports

README.md
ARCHITECTURE.md
CHANGELOG.md
COMMANDS.md
schema.sql
requirements.txt
```

---

# 🔄 Evaluation Engine

The Evaluation Engine compares every candidate against every selected job.

Current workflow:

```text
SQLite
    │
    ▼
Retrieve Candidates
    │
Retrieve Jobs
    │
Multiplex Merge
    │
Build Prompt
    │
Local LLM
    │
Parse JSON
    │
Save Evaluation
    │
SQLite
```

This design allows the platform to evaluate multiple candidates against multiple jobs in a single workflow execution.

---

# 📊 Performance

Current benchmark:

| Metric             | Value         |
| ------------------ | ------------- |
| Candidates         | 5             |
| Jobs               | 15            |
| Evaluations        | 75            |
| Runtime            | 4 min 5 sec   |
| Average Evaluation | ~3.27 seconds |

These figures represent local execution using Ollama on consumer hardware. 

---

# 🎯 Design Principles

AI Job Agent follows several core architectural principles:

* Local-first development
* API-first communication
* Database-driven workflows
* Modular services
* LLM provider agnostic
* Human approval before automation
* Replaceable components
* Incremental evolution

These principles allow the platform to grow without major architectural redesign.

---

# 🛣 Roadmap

## Phase 1 — Evaluation Engine ✅

* Candidate database
* Job database
* AI evaluation
* Evaluation persistence
* Batch processing

---

## Phase 2 — Job Discovery

* Automated job ingestion
* Job normalization
* Scheduled imports
* Duplicate job detection

---

## Phase 3 — Candidate Intelligence

* Resume parsing
* Resume ranking
* Resume selection
* Candidate matching improvements

---

## Phase 4 — Autonomous Applications

* Tailored resume generation
* Cover letter generation
* Human approval workflow
* Automated application submission

---

## Phase 5 — Learning System

* Application tracking
* Interview tracking
* Outcome analysis
* Feedback-driven ranking improvements

---

# 🌍 Long-Term Vision

The current platform evaluates candidates against job opportunities.

The long-term objective is an autonomous AI recruitment platform capable of:

* Discovering opportunities
* Ranking jobs by candidate fit
* Selecting the best resume
* Generating tailored cover letters
* Applying automatically
* Tracking application progress
* Learning from historical outcomes

The architecture has been intentionally designed to support this evolution through modular components, allowing additional capabilities to be introduced without major structural changes.

---

# 🚀 Getting Started

1. Start Docker Desktop.
2. Launch the FastAPI server.
3. Start the local LLM provider (currently Ollama).
4. Start n8n.
5. Execute the evaluation workflow.

Detailed startup commands are documented in **COMMANDS.md**.

---

# 📄 Documentation

* **ARCHITECTURE.md** — System architecture and design decisions
* **COMMANDS.md** — Daily development commands and operational guide
* **CHANGELOG.md** — Project history and milestones

---

# 🤝 Project Philosophy

AI Job Agent is intentionally designed as a collection of loosely coupled services.

Each subsystem communicates through well-defined interfaces, allowing workflow orchestration, AI inference, storage, and future automation modules to evolve independently while maintaining a stable overall architecture.

This approach prioritizes maintainability, flexibility, and long-term scalability over tightly coupled implementations.
