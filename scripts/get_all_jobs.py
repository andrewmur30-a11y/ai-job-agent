from scripts.database import get_connection

def get_all_jobs():
    """
    Queries the SQLite database to fetch all jobs.
    Returns a list of dictionaries containing job details.
    """
    conn = get_connection()
    # Configure row_factory to return results as dictionaries (column: value)
    conn.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
    
    cursor = conn.cursor()
    try:
        # Fetching all jobs. Depending on your business logic, this could eventually be 
        # filtered to status = 'active' or status = 'open'
        cursor.execute("SELECT * FROM jobs")
        jobs = cursor.fetchall()
    except Exception as e:
        jobs = []
        # Return structured error information if the database query fails
        print(f"Database error in get_all_jobs: {e}")
    finally:
        conn.close()
        
    return jobs