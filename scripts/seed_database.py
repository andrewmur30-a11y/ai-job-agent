import os
import json
import sqlite3
import hashlib
from datetime import datetime

# Resolve the database path
DB_PATH = os.path.join("database", "job_agent.db")

def calculate_local_profile_fingerprint(skills: list, experience: str, roles: list) -> str:
    """
    Computes a deterministic SHA-256 fingerprint representing candidate state.
    Used as a fallback in case the scripts.hashing_utils import fails.
    """
    normalized_skills = sorted([s.strip().lower() for s in skills])
    normalized_roles = sorted([r.strip().lower() for r in roles])
    normalized_exp = experience.strip().lower()
    payload = f"{normalized_skills}|{normalized_exp}|{normalized_roles}"
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()

def calculate_job_fingerprint(title: str, company: str, location: str) -> str:
    """
    Computes a SHA-256 fingerprint representing unique job parameters
    to prevent duplication across scraper ingestion engines.
    """
    normalized_title = title.strip().lower()
    normalized_company = company.strip().lower() if company else ""
    normalized_location = location.strip().lower() if location else ""
    payload = f"{normalized_title}|{normalized_company}|{normalized_location}"
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()

try:
    from scripts.hashing_utils import generate_profile_fingerprint
except ImportError:
    # Use our bulletproof local fallback function
    generate_profile_fingerprint = calculate_local_profile_fingerprint

def seed_database():
    print(f"Connecting to database at: {DB_PATH}")
    
    # Ensure database directory exists
    db_dir = os.path.dirname(DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Enable foreign key support
        cursor.execute("PRAGMA foreign_keys = ON;")

        print("Clearing historical seed data from tables...")
        cursor.execute("DELETE FROM applications;")
        cursor.execute("DELETE FROM evaluations;")
        cursor.execute("DELETE FROM candidates;")
        cursor.execute("DELETE FROM jobs;")
        
        # Reset autoincrement keys so testing IDs always start cleanly at 1
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='candidates';")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='jobs';")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='evaluations';")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='applications';")

        print("Seeding candidates table with realistic profiles...")
        
        candidates_raw = [
            {
                "org_id": "default_org",
                "name": "Andrew Murray",
                "email": "andrew.murray@nexient.ai",
                "skills": ["Python", "FastAPI", "SQLite", "n8n", "Docker", "Machine Learning", "LLMs", "Git"],
                "experience": "Senior Backend Engineer with 5 years of experience building integration pipelines, automating workflows with n8n, and deploying FastAPI web services.",
                "preferred_roles": ["Backend Engineer", "Integration Specialist", "AI Automation Engineer"],
                "preferred_location": "Remote, Hybrid"
            },
            {
                "org_id": "default_org",
                "name": "Jane Doe",
                "email": "jane.doe@pixelcraft.io",
                "skills": ["React", "TypeScript", "Tailwind CSS", "Next.js", "Redux", "Jest", "Vercel"],
                "experience": "Frontend developer specialized in creating accessible, responsive UI/UX experiences. Proven experience in single-file React configurations and Tailwind animations.",
                "preferred_roles": ["Frontend Engineer", "UI/UX Engineer", "React Developer"],
                "preferred_location": "Remote"
            },
            {
                "org_id": "default_org",
                "name": "Marcus Vance",
                "email": "marcus.vance@coreai.tech",
                "skills": ["Python", "PyTorch", "Hugging Face", "LangChain", "Vector Databases", "FastAPI", "SQL"],
                "experience": "AI Core Engineer focused on fine-tuning open-source models (Llama, Qwen) and optimizing retrieval-augmented generation (RAG) loops for enterprise document search.",
                "preferred_roles": ["AI Engineer", "LLM Solutions Architect", "ML Engineer"],
                "preferred_location": "Remote, Onsite"
            },
            {
                "org_id": "default_org",
                "name": "Sarah Connor",
                "email": "sconnor@cyberdyne.org",
                "skills": ["AWS", "Kubernetes", "Docker", "Terraform", "CI/CD", "Linux", "Bash", "Prometheus"],
                "experience": "DevOps and Infrastructure Engineer specialized in orchestrating scalable microservice runtimes and setting up automated CI/CD monitoring dashboards.",
                "preferred_roles": ["DevOps Engineer", "SRE", "Cloud Infrastructure Specialist"],
                "preferred_location": "Remote, Hybrid"
            },
            {
                "org_id": "default_org",
                "name": "Elena Rostova",
                "email": "elena.rostova@productlabs.co",
                "skills": ["Product Management", "Agile", "Scrum", "Jira", "User Research", "A/B Testing", "Figma"],
                "experience": "Technical Product Manager with a background in software engineering. Skilled at translating LLM capabilities into concrete, high-conversion product features.",
                "preferred_roles": ["Technical Product Manager", "Product Owner"],
                "preferred_location": "Remote"
            }
        ]

        for cand in candidates_raw:
            # Dynamically calculate the cryptographic state fingerprint
            fingerprint = generate_profile_fingerprint(
                skills=cand["skills"],
                experience=cand["experience"],
                roles=cand["preferred_roles"]
            )
            
            cursor.execute("""
                INSERT INTO candidates (
                    organization_id, name, email, skills, experience, 
                    preferred_roles, preferred_location, profile_fingerprint, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                cand["org_id"],
                cand["name"],
                cand["email"],
                json.dumps(cand["skills"]),
                cand["experience"],
                json.dumps(cand["preferred_roles"]),
                cand["preferred_location"],
                fingerprint,
                datetime.now().isoformat()
            ))

        print("Seeding jobs table with realistic market descriptions...")
        
        jobs_raw = [
            {
                "org_id": "default_org",
                "title": "AI Automation Engineer",
                "company": "Agents & Co.",
                "location": "San Francisco, CA",
                "type": "Full-time",
                "salary": "$130k - $160k",
                "desc": "Looking for an engineer to build production integrations using self-hosted automation workflows (n8n), Python gateways, and local LLMs (Qwen, Llama). Strong experience in SQL mapping and microservice structures required.",
                "reqs": ["Python", "FastAPI", "n8n", "SQL", "LLMs"],
                "url": "https://agentsandco.jobs/ai-auto-eng",
                "source": "LinkedIn"
            },
            {
                "org_id": "default_org",
                "title": "Senior React Architect",
                "company": "PixelCraft Studios",
                "location": "New York, NY",
                "type": "Full-time",
                "salary": "$140k - $170k",
                "desc": "We are seeking a React specialist to overhaul our client dashboard interfaces. Must be highly expert in modern Tailwind styling, React hooks, custom state machinery, and optimizing single-page application performance.",
                "reqs": ["React", "TypeScript", "Tailwind CSS", "Next.js"],
                "url": "https://pixelcraft.jobs/react-arch",
                "source": "Indeed"
            },
            {
                "org_id": "default_org",
                "title": "DevOps & Infrastructure Specialist",
                "company": "CloudScale Inc.",
                "location": "Austin, TX",
                "type": "Contract",
                "salary": "$90 - $110 / hr",
                "desc": "Urgently seeking a contractor to configure high-availability Kubernetes environments on AWS. Requires deep Terraform experience and solid scripting abilities in Python and Bash.",
                "reqs": ["AWS", "Kubernetes", "Terraform", "Docker", "Python"],
                "url": "https://cloudscale.jobs/devops-contract",
                "source": "Direct"
            },
            {
                "org_id": "default_org",
                "title": "Data Pipeline Engineer",
                "company": "Insight Analytics",
                "location": "Chicago, IL",
                "type": "Full-time",
                "salary": "$115k - $135k",
                "desc": "Help design our next-generation ETL architectures. Experience with Python, SQL databases (PostgreSQL/SQLite), and analytics warehouses (Snowflake, BigQuery) is highly critical.",
                "reqs": ["Python", "SQL", "PostgreSQL", "Snowflake", "ETL"],
                "url": "https://insightanalytics.jobs/data-eng",
                "source": "LinkedIn"
            },
            {
                "org_id": "default_org",
                "title": "Technical Product Manager (AI Services)",
                "company": "Nexus Systems",
                "location": "Seattle, WA",
                "type": "Full-time",
                "salary": "$150k - $180k",
                "desc": "Lead the discovery and development roadmap of our Generative AI integrations. Work closely with AI researchers and backend developers to deploy reliable NLP features for our global SaaS platform.",
                "reqs": ["Product Management", "Agile", "Scrum", "Jira", "AI"],
                "url": "https://nexussystems.jobs/tpm-ai",
                "source": "Glassdoor"
            }
        ]

        for job in jobs_raw:
            # Calculate unique SHA-256 job fingerprint
            j_fingerprint = calculate_job_fingerprint(
                title=job["title"],
                company=job["company"],
                location=job["location"]
            )
            
            cursor.execute("""
                INSERT INTO jobs (
                    organization_id, job_title, company, location, employment_type, 
                    salary, job_description, requirements, job_url, job_fingerprint, 
                    status, source, last_verified, date_found
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                job["org_id"],
                job["title"],
                job["company"],
                job["location"],
                job["type"],
                job["salary"],
                job["desc"],
                json.dumps(job["reqs"]),
                job["url"],
                j_fingerprint,
                "Active",
                job["source"],
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))

        conn.commit()
        print("✅ Database tables successfully populated with fingerprint-backed test data!")

    except Exception as e:
        conn.rollback()
        print(f"❌ Transaction rolled back due to error: {e}")
        raise e
    finally:
        conn.close()

if __name__ == "__main__":
    seed_database()