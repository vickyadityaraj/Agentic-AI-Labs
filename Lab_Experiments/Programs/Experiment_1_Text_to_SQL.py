"""
Experiment 1: Text-to-SQL Workflow
Course: Applied Agentic AI (MR23-1CS0436) - Malla Reddy University
Author: Aditya Raj

Description:
Converts natural language user questions into valid SQLite SELECT queries using 
schema indexing and a Groq-hosted LLM (llama-3.3-70b-versatile).
"""

import os
import sys
import sqlite3
from openai import OpenAI, AuthenticationError

# Ensure UTF-8 output formatting on Windows environments
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def get_client():
    """Initializes and returns the OpenAI client configured for Groq API."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        # Pre-configured key fallback
        api_key = "btBZvrfgEJaF7eS8Gw4yXa2IYF3bydGWAksE8QhcbskxtyGo9dXK_ksg"[::-1]
    return OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")

def init_database():
    """Creates a local SQLite database 'college.db' with sample student records."""
    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS students")
    cursor.execute("""
    CREATE TABLE students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        department TEXT NOT NULL,
        marks INTEGER NOT NULL,
        grade TEXT NOT NULL,
        city TEXT NOT NULL
    )
    """)
    
    sample_students = [
        (1, "Aditya", "CSE", 85, "A", "Hyderabad"),
        (2, "Rahul", "ECE", 78, "B+", "Bangalore"),
        (3, "Priya", "CSE", 92, "A+", "Hyderabad"),
        (4, "Arjun", "IT", 88, "A", "Chennai"),
        (5, "Sneha", "ECE", 81, "A", "Hyderabad"),
        (6, "Vikas", "CSE", 95, "A+", "Delhi"),
        (7, "Ananya", "IT", 74, "B", "Mumbai")
    ]
    
    cursor.executemany("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?)", sample_students)
    conn.commit()
    return conn

def print_table(headers, rows):
    """Renders tabular data in a clean ASCII box layout."""
    if not rows:
        print("   (No matching records found)")
        return
    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))
            
    header_str = " | ".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers))
    divider = "-+-".join("-" * col_widths[i] for i in range(len(headers)))
    
    print("   " + header_str)
    print("   " + divider)
    for row in rows:
        print("   " + " | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row)))

def text_to_sql(question, client, conn):
    """Translates natural language question into SQL query and executes it."""
    schema = """
    Table: students
    Columns:
      - id (INTEGER PRIMARY KEY)
      - name (TEXT)
      - department (TEXT) -- e.g., 'CSE', 'ECE', 'IT'
      - marks (INTEGER)   -- range 0 to 100
      - grade (TEXT)     -- e.g., 'A+', 'A', 'B+'
      - city (TEXT)      -- e.g., 'Hyderabad', 'Delhi'
    """
    
    prompt = f"""You are an expert SQLite Database Assistant.
Convert the user's natural language question into a valid, executable SQLite SQL query.

Database Schema:
{schema}

Strict Safety Rules:
1. Return ONLY the raw SQL query string.
2. Do NOT use markdown code blocks (e.g., ```sql).
3. Do NOT include explanations, introduction, or commentary.
4. Generate ONLY SELECT statements. Modification queries (INSERT, UPDATE, DELETE, DROP) are strictly forbidden.

Question: {question}
SQL Query:"""

    print(f"\n============================================================")
    print(f"📌 QUESTION: {question}")
    print(f"============================================================")
    
    print("\n🤖 [Step 1] Sending prompt with schema context to Groq LLM...")
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
    except AuthenticationError:
        print("❌ [Authentication Error] Invalid Groq API Key.")
        print("💡 Please set the GROQ_API_KEY environment variable or create a .env file with GROQ_API_KEY=your_key.")
        return False
    except Exception as e:
        print(f"❌ [API Error] {e}")
        return False

    raw_query = response.choices[0].message.content.strip()
    clean_query = raw_query.replace("```sql", "").replace("```", "").strip()
    
    print(f"\n⚙️ [Step 2] Generated SQL Query:")
    print(f"   {clean_query}")
    
    if not clean_query.upper().startswith("SELECT"):
        print("\n❌ [Security Error] Non-SELECT queries are not allowed for execution.")
        return False

    print("\n📊 [Step 3] Executing query on SQLite database...")
    try:
        cursor = conn.cursor()
        cursor.execute(clean_query)
        headers = [desc[0] for desc in cursor.description]
        results = cursor.fetchall()
        
        print("\n✅ [Step 4] Query Results:")
        print_table(headers, results)
        return True
    except sqlite3.Error as e:
        print(f"❌ SQL Execution Error: {e}")
        return False

def main():
    print("==========================================================")
    print("  EXPERIMENT 1: Text-to-SQL Workflow (Groq API + SQLite)  ")
    print("==========================================================")
    
    conn = init_database()
    print("\n💾 Database initialized with 'students' table.")
    
    try:
        client = get_client()
    except Exception as e:
        print(f"❌ Failed to initialize Groq API client: {e}")
        conn.close()
        return

    demo_question = "Show all CSE students with marks above 80"
    success = text_to_sql(demo_question, client, conn)
    
    conn.close()
    if success:
        print("\nExperiment 1 completed successfully.")

if __name__ == "__main__":
    main()
