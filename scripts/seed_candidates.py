import os
import sqlite3
import json
from datetime import datetime

# Define the database path
DB_PATH = os.path.join("database", "job_agent.db")

def get_connection():
    # Connect with a timeout to handle any local locks gracefully
    return sqlite3.connect(DB_PATH, timeout=10.0)

def seed_custom_candidates():
    print(f"Connecting to database at: {DB_PATH}")
    if not os.path.exists(os.path.dirname(DB_PATH)):
        os.makedirs(os.path.dirname(DB_PATH))
        
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Enable foreign key support
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        # 1. Clear existing candidates and evaluations/applications to maintain integrity
        print("Clearing existing candidates, evaluations, and applications to prevent structural conflicts...")
        cursor.execute("DELETE FROM evaluations")
        cursor.execute("DELETE FROM applications")
        cursor.execute("DELETE FROM candidates")
        
        # Reset the autoincrement sequence for candidates so IDs start fresh at 1
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='candidates'")
        
        # 2. Define the new candidate dataset
        # We parse the JSON lists from your raw insert query to store them cleanly as strings in SQLite
        candidates = [
            (
                'Emily Carter',
                json.dumps(["Python", "FastAPI", "SQL", "Docker", "Git", "REST APIs"]),
                'Software engineer with 5 years of experience building backend web applications using Python and FastAPI. Experienced with Docker deployments, PostgreSQL, API integrations, and Agile development. Enjoys building scalable cloud-native services.',
                json.dumps(["Backend Developer", "Python Developer", "Software Engineer"]),
                'Remote',
                datetime.now().isoformat()
            ),
            (
                'Michael Chen',
                json.dumps(["Java", "Spring Boot", "Kafka", "AWS", "Docker", "Kubernetes"]),
                'Senior backend engineer with over 9 years of experience designing distributed microservices in financial technology environments. Strong background in AWS infrastructure, Kubernetes, and event-driven architectures.',
                json.dumps(["Senior Software Engineer", "Backend Engineer", "Solutions Architect"]),
                'Toronto, Canada',
                datetime.now().isoformat()
            ),
            (
                'Sarah Williams',
                json.dumps(["Project Management", "Jira", "Asana", "Stakeholder Management", "Agile", "Scrum"]),
                'Project manager with 8 years leading SaaS implementation projects across healthcare and hospitality sectors. Experienced managing cross-functional teams, customer onboarding, and process improvement initiatives.',
                json.dumps(["Project Manager", "Implementation Manager", "Customer Success Manager"]),
                'Remote',
                datetime.now().isoformat()
            ),
            (
                'David Rodriguez',
                json.dumps(["React", "TypeScript", "JavaScript", "HTML", "CSS", "Next.js"]),
                'Frontend developer with 4 years of experience building responsive web applications. Passionate about UI/UX, accessibility, and performance optimization. Works closely with design teams to deliver modern user experiences.',
                json.dumps(["Frontend Developer", "React Developer", "Full Stack Developer"]),
                'Mexico City, Mexico',
                datetime.now().isoformat()
            ),
            (
                'Priya Nair',
                json.dumps(["SQL", "Power BI", "Excel", "Python", "Tableau", "Data Analysis"]),
                'Data analyst with 6 years of experience transforming business data into actionable insights. Skilled in dashboard development, reporting automation, SQL optimization, and executive presentations.',
                json.dumps(["Data Analyst", "Business Intelligence Analyst", "Operations Analyst"]),
                'Remote',
                datetime.now().isoformat()
            ),
            (
                'James Thompson',
                json.dumps(["Azure", "Terraform", "Docker", "Linux", "CI/CD", "PowerShell"]),
                'DevOps engineer with 7 years of experience automating infrastructure and deployment pipelines. Strong expertise in Azure cloud services, Infrastructure as Code, monitoring, and production support.',
                json.dumps(["DevOps Engineer", "Cloud Engineer", "Site Reliability Engineer"]),
                'Austin, Texas',
                datetime.now().isoformat()
            ),
            (
                'Sofia Martinez',
                json.dumps(["Salesforce", "HubSpot", "Zendesk", "Customer Success", "API Integrations", "Training"]),
                'Customer success professional with 6 years helping enterprise SaaS customers implement software, improve adoption, and optimize business processes. Experienced with CRM administration and customer onboarding.',
                json.dumps(["Customer Success Manager", "Implementation Consultant", "Technical Account Manager"]),
                'Remote',
                datetime.now().isoformat()
            ),
            (
                'Andrew Murray',
                json.dumps(["Project Management", "SQL", "Power BI", "Salesforce", "HubSpot", "Jira", "Asana", "Zendesk", "FastAPI", "API Integrations", "Stakeholder Management", "Process Improvement"]),
                'Technical implementation and operations leader with over 8 years of experience delivering SaaS implementations, system integrations, and customer success initiatives. Managed large-scale migrations involving thousands of customer accounts, coordinated cross-functional teams, and improved operational processes through automation and data analysis. Experienced working remotely with international clients and leading complex implementation projects.',
                json.dumps(["Implementation Manager", "Technical Project Manager", "Operations Analyst", "Customer Success Manager", "Integration Manager"]),
                'Remote',
                datetime.now().isoformat()
            )
        ]
        
        # 3. Execute bulk inserts
        print(f"Inserting {len(candidates)} candidates into 'candidates' table...")
        cursor.executemany("""
            INSERT INTO candidates (name, skills, experience, preferred_roles, preferred_location, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, candidates)
        
        conn.commit()
        print("✅ Database successfully seeded with custom candidates!")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error occurred during seeding: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    seed_custom_candidates()