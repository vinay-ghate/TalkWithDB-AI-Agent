import sqlite3
import json

def list_tables(db_path: str) -> list[str]:
    """Lists all tables in the specified database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

def get_table_schema(db_path: str, table_name: str) -> str:
    """Returns the schema of a specific table from the specified database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info('{table_name}');")
    schema = cursor.fetchall()
    conn.close()
    
    columns = [f"{col[1]} ({col[2]})" for col in schema]
    return f"Schema for {table_name}: " + ", ".join(columns)

def run_sql_query(db_path: str, query: str) -> str:
    """
    Executes a read-only SQL query (SELECT only) on the specified database.
    Returns the result as a JSON string.
    """
    if not query.strip().lower().startswith("select"):
        return "Error: Only SELECT queries are allowed."

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()

        if not result:
            return "Query returned no results."
        
        return json.dumps([dict(row) for row in result])
    except sqlite3.Error as e:
        return f"Database Error: {e}"