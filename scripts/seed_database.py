import json
import os
import sqlite3
from scripts.database import get_connection

def recreate_and_seed_database():
    """
    Clears the existing database, creates tables with the correct up-to-date schema,
    and populates it with 8 realistic candidates and 20 diverse job postings.
    """
    conn = get_connection()
    cursor = conn.cursor()

    print("Initializing SQLite schema...")
    
    # Drop existing tables to ensure schema modifications (like adding 'skills') are fully applied
    print("Dropping old tables to enforce updated schema rules...")
    cursor.execute("DROP TABLE IF EXISTS evaluations")
    cursor.execute("DROP TABLE IF EXISTS candidates")
    cursor.execute("DROP TABLE IF EXISTS jobs")
    conn.commit()

    # Create tables with correct column configurations
    print("Creating tables with updated schemas...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            skills TEXT,
            experience TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            requirements TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL,
            candidate_id INTEGER NOT NULL,
            overall_score INTEGER,
            decision TEXT,
            strengths TEXT,
            missing_skills TEXT,
            reasoning TEXT,
            summary TEXT,
            evaluated_at TEXT,
            run_id TEXT
        )
    """)
    conn.commit()

    print("Generating seed candidate data...")
    candidates = [
        {
            "name": "Alex Carter",
            "skills": json.dumps(["Python", "PyTorch", "TensorFlow", "Scikit-Learn", "FastAPI", "SQL", "Docker"]),
            "experience": "AI & ML Engineer with 4 years of experience building predictive models, optimizing neural networks, and deploying robust NLP and computer vision pipelines using FastAPI and Docker."
        },
        {
            "name": "Sarah Jenkins",
            "skills": json.dumps(["React", "TypeScript", "Tailwind CSS", "Next.js", "Redux Toolkit", "Jest", "Git"]),
            "experience": "Senior Frontend Engineer specializing in interactive dashboard architectures, modern state-management, and high-performance Web-Core Vitals optimization using Next.js."
        },
        {
            "name": "Marcus Vance",
            "skills": json.dumps(["AWS", "Kubernetes", "Docker", "Terraform", "GitHub Actions", "Python", "Bash"]),
            "experience": "DevOps & Cloud Engineer with 6 years of experience provisioning multi-region AWS architectures via Terraform, maintaining production EKS clusters, and designing automated CI/CD pipelines."
        },
        {
            "name": "Emily Zhao",
            "skills": json.dumps(["Node.js", "Express", "Python", "PostgreSQL", "Redis", "GraphQL", "AWS"]),
            "experience": "Backend Developer with 3 years of experience writing high-throughput RESTful and GraphQL APIs, optimizing relational queries, and configuring Redis caching layer structures."
        },
        {
            "name": "David Kross",
            "skills": json.dumps(["Pentesting", "OWASP Top 10", "Python", "Wireshark", "Metasploit", "Linux", "Burp Suite"]),
            "experience": "Cybersecurity Specialist and Ethical Hacker focusing on penetration testing, threat modeling, security-focused code review, and remediation planning for enterprise web applications."
        },
        {
            "name": "Samantha Miller",
            "skills": json.dumps(["Apache Spark", "Python", "SQL", "Airflow", "Snowflake", "Databricks", "AWS"]),
            "experience": "Data Engineer with 5 years of experience building big data ETL pipelines, running distributed queries in Spark, and managing pipeline workflows using Apache Airflow."
        },
        {
            "name": "John Doe",
            "skills": json.dumps(["Python", "HTML", "CSS", "SQL", "Git", "Django"]),
            "experience": "Junior Python Developer seeking an entry-level backend position. Familiar with basic Django architectures, REST principles, and writing fundamental relational database queries."
        },
        {
            "name": "Clara Barton",
            "skills": json.dumps(["Product Strategy", "Agile Roadmap", "Jira", "User Research", "A/B Testing", "Figma"]),
            "experience": "Senior Product Manager with 8 years of experience leading cross-functional design and engineering teams to launch enterprise SaaS features, manage roadmaps, and analyze user behavior."
        }
    ]

    for c in candidates:
        cursor.execute(
            "INSERT INTO candidates (name, skills, experience) VALUES (?, ?, ?)",
            (c["name"], c["skills"], c["experience"])
        )
    conn.commit()
    print(f"Successfully seeded {len(candidates)} candidates.")

    print("Generating seed jobs listing data...")
    jobs = [
        {
            "title": "Machine Learning Engineer",
            "requirements": json.dumps(["Python", "PyTorch", "TensorFlow", "FastAPI", "Experience deploying models in production", "SQL"])
        },
        {
            "title": "Senior Frontend React Engineer",
            "requirements": json.dumps(["React", "TypeScript", "Tailwind CSS", "Next.js", "Experience optimizing frontend core web vitals"])
        },
        {
            "title": "DevOps Cloud Engineer",
            "requirements": json.dumps(["AWS", "Kubernetes", "Terraform", "Docker", "CI/CD toolchains like GitHub Actions"])
        },
        {
            "title": "Python Backend Developer",
            "requirements": json.dumps(["Python", "FastAPI", "SQL", "PostgreSQL", "Redis caching patterns", "REST API architecture"])
        },
        {
            "title": "Security Engineer",
            "requirements": json.dumps(["OWASP Top 10 knowledge", "Application penetration testing", "Python", "Burp Suite", "Security auditing"])
        },
        {
            "title": "Senior Data Engineer",
            "requirements": json.dumps(["Apache Spark", "Airflow orchestration", "Snowflake or BigQuery", "SQL", "Python ETL design"])
        },
        {
            "title": "Product Manager - SaaS Platforms",
            "requirements": json.dumps(["Agile roadmap execution", "User research methodologies", "Jira", "Product launch experience", "Data-driven decision making"])
        },
        {
            "title": "Junior Python Intern",
            "requirements": json.dumps(["Python", "Basic SQL knowledge", "Git version control", "Eagerness to learn backend architectures"])
        },
        {
            "title": "React Frontend Developer",
            "requirements": json.dumps(["React", "JavaScript", "HTML/CSS", "Git", "State management library experience like Redux or Context API"])
        },
        {
            "title": "Lead Cloud Infrastructure Architect",
            "requirements": json.dumps(["Deep AWS expertise", "Kubernetes EKS provisioning", "Terraform", "Security & Identity access management (IAM)", "Enterprise scaling"])
        },
        {
            "title": "Full Stack Engineer (Next.js & FastAPI)",
            "requirements": json.dumps(["Next.js", "FastAPI", "PostgreSQL", "Docker", "RESTful API implementation"])
        },
        {
            "title": "Data Analyst",
            "requirements": json.dumps(["SQL proficiency", "Tableau or PowerBI dashboard building", "Python", "Pandas", "Statistical modeling basics"])
        },
        {
            "title": "QA Automation Specialist",
            "requirements": json.dumps(["TypeScript", "Playwright or Cypress automation framework", "CI/CD integration", "Manual exploratory testing basics"])
        },
        {
            "title": "Database Administrator (PostgreSQL)",
            "requirements": json.dumps(["PostgreSQL replication setups", "Query optimization and indexing strategies", "Backup and disaster recovery planning", "Linux administration"])
        },
        {
            "title": "Site Reliability Engineer (SRE)",
            "requirements": json.dumps(["Python or Go scripting", "Kubernetes orchestration", "Prometheus or Grafana monitoring suites", "Linux system internals"])
        },
        {
            "title": "Golang Backend Developer",
            "requirements": json.dumps(["Go programming language", "Microservices architecture", "gRPC and Protobuf networks", "Docker", "SQL"])
        },
        {
            "title": "iOS Mobile Developer",
            "requirements": json.dumps(["Swift", "SwiftUI", "iOS Core Data frameworks", "App Store deployment pipeline cycles", "Git"])
        },
        {
            "title": "Technical Writer",
            "requirements": json.dumps(["Markdown documentation layout", "API endpoint structure writing", "Git", "Strong technical translation skills"])
        },
        {
            "title": "UI/UX Product Designer",
            "requirements": json.dumps(["Figma expert level", "User flow mapping", "Prototyping", "A/B user testing support"])
        },
        {
            "title": "Cybersecurity Risk Analyst",
            "requirements": json.dumps(["ISO 27001 or SOC2 compliance frameworks", "Security risk assessment reporting", "Vulnerability scanning management"])
        }
    ]

    for j in jobs:
        cursor.execute(
            "INSERT INTO jobs (title, requirements) VALUES (?, ?)",
            (j["title"], j["requirements"])
        )
    conn.commit()
    print(f"Successfully seeded {len(jobs)} jobs.")

    # Show database summary
    cursor.execute("SELECT COUNT(*) FROM candidates")
    total_candidates = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM jobs")
    total_jobs = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM evaluations")
    total_evals = cursor.fetchone()[0]
    
    conn.close()
    
    print("\n" + "="*40)
    print("DATABASE SEEDING COMPLETE!")
    print(f"Total Candidates: {total_candidates}")
    print(f"Total Jobs:       {total_jobs}")
    print(f"Total Evaluations: {total_evals} (Clean Wipe)")
    print("="*40)

if __name__ == "__main__":
    recreate_and_seed_database()