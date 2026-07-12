import hashlib
import json

def generate_profile_fingerprint(skills: list, experience: str, roles: list) -> str:
    """
    Creates a deterministic SHA-256 fingerprint of the semantic profile data.
    Ensures that minor formatting changes don't trigger re-evaluations.
    """
    normalized_skills = sorted([s.strip().lower() for s in skills])
    normalized_roles = sorted([r.strip().lower() for r in roles])
    normalized_exp = experience.strip().lower()
    
    payload = f"{normalized_skills}|{normalized_exp}|{normalized_roles}"
    
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()