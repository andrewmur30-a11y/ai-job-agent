# ARCHITECTURE.md

# System Architecture

## Overview

**Nexient (under review)** is a local-first AI recruitment platform designed around modular, loosely coupled components.

The platform evaluates candidates against job opportunities using a local Large Language Model (LLM), stores structured evaluation results, and has been intentionally designed to evolve into a fully autonomous AI recruitment platform.

The architecture emphasizes maintainability, modularity, and replaceable components over tightly coupled implementations.

---

# Design Philosophy

The project follows several core engineering principles.

## Local-First

All core services can run locally without requiring cloud infrastructure.

Benefits:

* Lower operating costs
* Faster experimentation
* Complete data ownership
* Offline development

---

## API-First

Every major component communicates through APIs instead of direct database access whenever practical.

This creates clear boundaries between:

* Data storage
* Business logic
* Workflow orchestration
* AI reasoning

---

## Database-Driven

Business data is never hardcoded inside workflows.

Candidates, jobs, and evaluations are stored within SQLite and retrieved dynamically through FastAPI endpoints.

This allows workflows to scale without modification.

---

## LLM Provider Agnostic

The architecture is intentionally independent of any single AI provider.

Current provider:

* Ollama

Compatible providers include:

* LM Studio
* Ollama
* OpenAI-compatible APIs

Changing inference providers should not require architectural changes.

---

## Modular Components

Every subsystem has a single responsibility.

| Component | Responsibility                  |
| --------- | ------------------------------- |
| SQLite    | Persistent storage              |
| FastAPI   | Data access and persistence API |
| n8n       | Workflow orchestration          |
| Local LLM | Candidate reasoning and scoring |

---

# High-Level Architecture

```text
                    Candidates
                         │
                    Jobs Database
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
               Local LLM (Inference)
                         │
                Structured JSON Output
                         │
                         ▼
                  FastAPI Persistence
                         │
                         ▼
                  SQLite Evaluations
```

Each layer performs one responsibility before handing work to the next.

---

# Component Responsibilities

## SQLite

Stores persistent project data.

Current tables include:

* candidates
* jobs
* evaluations

SQLite acts as the system of record.

---

## FastAPI

FastAPI provides a stable interface between workflows and the database.

Current responsibilities include:

* Retrieve candidate records
* Retrieve job records
* Save evaluation results
* Validate incoming data with Pydantic
* Expose Swagger documentation

FastAPI prevents workflow logic from interacting directly with SQLite.

---

## n8n

n8n acts as the orchestration layer.

Responsibilities include:

* Retrieve candidates
* Retrieve jobs
* Generate evaluation combinations
* Build prompts
* Call the inference provider
* Parse structured responses
* Persist evaluation results

Business logic is intentionally kept outside the workflow whenever possible.

---

## Local LLM

The LLM performs reasoning only.

Responsibilities:

* Compare candidate profiles
* Compare job requirements
* Produce structured JSON
* Generate objective evaluation summaries

The model does not perform persistence or workflow control.

---

# Evaluation Engine

The Evaluation Engine is the core subsystem of the platform.

Its purpose is to evaluate every selected candidate against every selected job.

Workflow:

```text
Retrieve Candidates
        │
Retrieve Jobs
        │
Multiplex Merge
        │
Build Prompt
        │
LLM Evaluation
        │
Parse JSON
        │
Save Evaluation
```

The workflow remains entirely data-driven.

No candidate or job information is hardcoded inside the evaluation process.

---

# Evaluation Matrix

The platform supports evaluating multiple candidates against multiple jobs within a single execution.

Example:

```text
Candidates

Andrew
Jane
John

        ×

Jobs

Operations Analyst
Project Manager
Customer Success Manager

        =

Andrew → Operations Analyst
Andrew → Project Manager
Andrew → Customer Success Manager

Jane → Operations Analyst
Jane → Project Manager
Jane → Customer Success Manager

John → Operations Analyst
John → Project Manager
John → Customer Success Manager
```

This architecture allows the evaluation engine to scale naturally as additional candidates and jobs are introduced.

---

# Current Data Flow

```text
SQLite
      │
      ▼
FastAPI
      │
      ▼
Retrieve Candidates
      │
Retrieve Jobs
      │
      ▼
Multiplex Merge
      │
      ▼
Prompt Builder
      │
      ▼
Local LLM
      │
      ▼
Structured JSON
      │
      ▼
FastAPI
      │
      ▼
SQLite Evaluations
```

Every component performs one clearly defined task before passing data to the next stage.

---

# Duplicate Protection

Evaluation records are uniquely identified by:

* candidate_id
* job_id

Before creating a new evaluation, the persistence layer checks whether the candidate has already been evaluated against the same job.

This prevents unnecessary inference requests while maintaining evaluation history integrity.

---

# Current Capabilities

The platform currently supports:

* Candidate storage
* Job storage
* Database-backed retrieval
* Dynamic prompt generation
* Batch evaluation
* Structured JSON parsing
* Evaluation persistence
* Duplicate detection
* Swagger API documentation

---

# Performance

Current benchmark:

| Metric             | Result              |
| ------------------ | ------------------- |
| Candidates         | 5                   |
| Jobs               | 15                  |
| Evaluations        | 75                  |
| Runtime            | 4 minutes 5 seconds |
| Average Evaluation | ~3.27 seconds       |

This benchmark was achieved using Ollama running locally on consumer hardware.

Performance optimization has intentionally been deferred until core functionality is complete.

---

# Future Architecture

The Evaluation Engine is the first major subsystem.

Future modules will extend the platform without requiring architectural redesign.

Planned additions include:

```text
Job Discovery
        │
Resume Parsing
        │
Resume Ranking
        │
Evaluation Engine
        │
Resume Selection
        │
Cover Letter Generation
        │
Human Approval
        │
Application Automation
        │
Application Tracking
        │
Learning & Feedback
```

Each module will communicate through existing interfaces, allowing the platform to evolve incrementally.

---

# Architectural Decisions

Several key decisions have shaped the project:

* Local-first development
* SQLite for rapid iteration
* FastAPI as the application interface
* n8n for orchestration
* Replaceable inference providers
* Database-driven workflows
* Modular system boundaries
* Human approval before automation

These decisions prioritize maintainability, flexibility, and long-term scalability.

---

# Guiding Philosophy

The objective of this project is not simply to automate job applications.

The objective is to build a modular AI recruitment platform capable of evolving through independent, replaceable components.

Each subsystem is designed to perform one responsibility well, communicate through stable interfaces, and remain adaptable as the platform grows.

This philosophy allows the project to evolve from an evaluation engine into a fully autonomous AI recruitment platform without requiring fundamental architectural redesign.
