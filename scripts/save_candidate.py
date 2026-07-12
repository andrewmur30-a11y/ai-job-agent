import json
from datetime import datetime
from scripts.database import get_connection
from scripts.hashing_utils import generate_profile_fingerprint

def save_candidate(name: str, email: str, skills: list, experience: str, preferred_roles: list, preferred_location: str, organization_id: str = "default_org") -> dict:
    """
    Validates, fingerprints, and inserts/updates a parsed candidate in the SQLite database.
    Implements identity resolution based on email and profile state fingerprinting.
    """
    # 1. Generate the Candidate Profile Fingerprint representing semantic state
    fingerprint = generate_profile_fingerprint(
        skills=skills,
        experience=experience,
        roles=preferred_roles
    )
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # 2. Resolve identity using Email and Organization ID
        cursor.execute("""
            SELECT id, name, profile_fingerprint 
            FROM candidates 
            WHERE email = ? AND organization_id = ?
        """, (email, organization_id))
        existing = cursor.fetchone()
        
        if existing:
            existing_id, existing_name, existing_fingerprint = existing
            
            # Case A: Profile fingerprint matches exactly (redundant upload, skip evaluation)
            if existing_fingerprint == fingerprint:
                return {
                    "status": "skipped",
                    "message": f"Candidate '{existing_name}' with email '{email}' is already up-to-date.",
                    "candidate_id": existing_id,
                    "fingerprint": fingerprint
                }
            
            # Case B: Email exists but fingerprint differs (semantic update, run re-evaluation)
            skills_str = json.dumps(skills)
            roles_str = json.dumps(preferred_roles)
            updated_at = datetime.now().isoformat()
            
            cursor.execute("""
                UPDATE candidates 
                SET name = ?, skills = ?, experience = ?, preferred_roles = ?, preferred_location = ?, profile_fingerprint = ?
                WHERE id = ?
            """, (name, skills_str, experience, roles_str, preferred_location, fingerprint, existing_id))
            
            conn.commit()
            return {
                "status": "updated",
                "message": f"Candidate '{name}' profile updated with new qualifications.",
                "candidate_id": existing_id,
                "fingerprint": fingerprint
            }
            
        # Case C: Completely new email anchor, perform insertion
        skills_str = json.dumps(skills)
        roles_str = json.dumps(preferred_roles)
        created_at = datetime.now().isoformat()
        
        cursor.execute("""
            INSERT INTO candidates (organization_id, name, email, skills, experience, preferred_roles, preferred_location, created_at, profile_fingerprint)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (organization_id, name, email, skills_str, experience, roles_str, preferred_location, created_at, fingerprint))
        
        candidate_id = cursor.lastrowid
        conn.commit()
        
        return {
            "status": "success",
            "message": f"Candidate '{name}' successfully imported.",
            "candidate_id": candidate_id,
            "fingerprint": fingerprint
        }
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()