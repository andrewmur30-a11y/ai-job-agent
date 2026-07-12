import os
import sqlite3

DB_PATH = os.path.join("database", "job_agent.db")

def inspect_database():
    """
    Connects to the active SQLite database, discovers all active tables,
    and prints their exact compiled columns, data types, and constraints.
    """
    if not os.path.exists(DB_PATH):
        print(f"❌ Error: Database file not found at '{DB_PATH}'")
        print("Please ensure you have created the database file and placed it in the correct directory.")
        return

    print(f"🔍 Inspecting database: {DB_PATH}")
    print("=" * 60)

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Retrieve all user tables (ignoring internal sqlite metadata tables)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = cursor.fetchall()
        
        if not tables:
            print("⚠️ The database is currently empty. No tables found!")
            print("Make sure you pasted the schema.sql into DB Browser and clicked 'Write Changes'.")
            return

        for table_tuple in tables:
            table_name = table_tuple[0]
            print(f"\n📂 Table: {table_name.upper()}")
            print("-" * 40)
            
            # Fetch column metadata
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            for col in columns:
                col_id = col[0]
                col_name = col[1]
                col_type = col[2]
                col_notnull = "NOT NULL" if col[3] else "NULL"
                col_default = f"DEFAULT '{col[4]}'" if col[4] is not None else ""
                col_pk = "[PK]" if col[5] else ""
                
                # Format a clean, visually aligned output line
                constraints = f"{col_notnull} {col_default} {col_pk}".strip()
                print(f"  👉 {col_name:<25} | {col_type:<10} | {constraints}")
                
            # Fetch active indexes for this table
            cursor.execute(f"PRAGMA index_list({table_name});")
            indexes = cursor.fetchall()
            if indexes:
                print("  Indexes:")
                for idx in indexes:
                    idx_name = idx[1]
                    idx_unique = "UNIQUE" if idx[2] else "NON-UNIQUE"
                    print(f"    - {idx_name} ({idx_unique})")
                    
        print("\n" + "=" * 60)
        print("✅ Database inspection completed successfully!")

    except Exception as e:
        print(f"❌ Database connection error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    inspect_database()