from scripts.database import get_connection

def get_candidate(candidate_id: int):
    """
    Queries the SQLite database to fetch a single candidate by ID.
    Uses defensive schema inspection to dynamically select only existing columns,
    preventing crashes due to schema drift, local database mismatches, or older seed data.
    Highly resilient: supports both legacy 'profile' schemas and updated 'skills'/'experience' schemas.
    """
    conn = get_connection()
    # Configure row_factory to return results as clean dictionaries
    conn.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
    
    cursor = conn.cursor()
    try:
        # 1. Inspect the 'candidates' table to see what columns actually exist in the database right now
        cursor.execute("PRAGMA table_info(candidates)")
        columns_in_db = [row['name'] for row in cursor.fetchall()]
        
        # 2. Define the complete list of columns we would ideally want to select
        # Included 'profile' to natively support databases seeded with single-block text
        ideal_columns = ['id', 'name', 'profile', 'skills', 'experience', 'preferred_roles', 'preferred_location', 'created_at']
        
        # 3. Filter our selection to ONLY include columns that physically exist in the table
        safe_columns = [col for col in ideal_columns if col in columns_in_db]
        
        # Fallback safeguard in case table_info somehow comes back empty
        if not safe_columns:
            safe_columns = ['id', 'name']
            
        # 4. Construct and execute the dynamic select query
        query = f"SELECT {', '.join(safe_columns)} FROM candidates WHERE id = ?"
        cursor.execute(query, (candidate_id,))
        candidate = cursor.fetchone()
        
        # 5. For any missing expected schema columns, pad the returned dictionary with None values
        # This keeps the API response structure consistent for n8n even if columns are missing
        if candidate:
            for col in ideal_columns:
                if col not in candidate:
                    candidate[col] = None
                    
    except Exception as e:
        candidate = None
        print(f"Database error in get_candidate for ID {candidate_id}: {e}")
    finally:
        conn.close()
        
    return candidate