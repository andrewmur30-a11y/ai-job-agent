Nexient AI Job Agent

A local-first, AI-powered recruitment automation engine. The system automatically ingests resumes, structures them into clean JSON schemas using a local Qwen2.5 model, computes profile state fingerprints, and matches candidates against target job descriptions inside a high-performance, multi-tenant SQLite database.

🚀 Quick Start Guide

1. Installation & Environment Setup

Clone the project and install all required system dependencies:

# Clone the repository (or run from your workspace directory)
cd C:\AI-Job-Agent

# Install required Python packages
pip install -r requirements.txt


2. Set Up the SQLite Database

Ensure your SQLite database is properly created, seeded, and migrated:

# Seed the initial database tables and realistic profiles
python scripts/seed_database.py

# Confirm schema integrity
python scripts/inspect_db.py


3. Run the Backend API Gateway

Start the local FastAPI instance on port 8000:

python -m uvicorn scripts.api:app --reload --host 127.0.0.1 --port 8000


Interactive API Documentation (Swagger): Visit http://127.0.0.1:8000/docs to upload resumes or trigger endpoints interactively.

4. Running Local LLM (Ollama)

Ensure your local Ollama instance is running and has the optimized model downloaded:

ollama run qwen2.5:7b


📂 Project Architecture Overview

├── database/                    # Database storage
│   └── job_agent.db             # SQLite central file (WAL Mode enabled)
├── docs/                        # Architectural specifications and guides
│   ├── architecture.md          # Visual components layout & operational flows
│   ├── project_todo_list.md     # Phase backlog tracking
│   └── ...                      # ADR documents, scaling strategies
├── resumes/                     # Local resume sandbox testing folder
├── scripts/                     # Python scripts package
│   ├── __init__.py              # Package initializer
│   ├── api.py                   # FastAPI server gateways
│   ├── hashing_utils.py         # SHA-256 state tracking fingerprint generator
│   ├── resume_parser.py         # PyPDF / DOCX layout extraction and Ollama logic
│   ├── save_candidate.py        # Database identity resolution write rules
│   ├── save_evaluation.py       # Evaluation write gates and duplicate guards
│   ├── seed_database.py         # Structural seeder script
│   └── ...                      # Endpoint and parsing test runners
├── workflows/                   # n8n workflow pipeline configurations
├── requirements.txt             # Project library requirements
└── schema.sql                   # Database table definitions


🧪 Integration Testing Suite

We maintain defensive automated tests to verify the integrity of our APIs, database operations, and LLM extractions.

Test 1: API Endpoint Coverage

Tests all GET routes and ensures the /save-evaluation idempotency duplicate lock is functional:

python scripts/test_api_endpoints.py


Test 2: Local Resume Parser Sandbox

Tests PDF/DOCX layout parsing and Qwen2.5 extraction on local disk files without involving the network:

python scripts/test_resume_parser.py


Test 3: API Ingestion Pipeline Upload

Simulates a real multi-part HTTP upload to /candidates/import to verify layout-to-database integrity:

python scripts/test_pdf_upload.py


🛠️ Core Technologies

Framework: FastAPI, Pydantic, Uvicorn

Database: SQLite3 (Write-Ahead Logging mode)

Local Inference: Ollama (Qwen2.5-7B)

Workflow Engine: n8n (Multiplex/Cross-join matching loop)

File Handling: pypdf, python-docx