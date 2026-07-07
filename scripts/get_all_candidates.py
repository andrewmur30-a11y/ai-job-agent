from scripts.database import get_connection

def get_all_candidates():
    """
    Queries the SQLite database to fetch all candidates.
    Aligned with the updated Canvas schema (using skills/experience instead of profile).
    """
    conn = get_connection()
    # Configure row_factory to return results as clean, JSON-serializable dictionaries
    conn.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
    
    cursor = conn.cursor()
    try:
        # Replaced the outdated 'profile' column with 'skills' and 'experience'
        cursor.execute("""
            SELECT id, name, skills, experience, preferred_roles, preferred_location, created_at 
            FROM candidates
        """)
        candidates = cursor.fetchall()
    except Exception as e:
        candidates = []
        print(f"Database error in get_all_candidates: {e}")
    finally:
        conn.close()
        
    return candidates