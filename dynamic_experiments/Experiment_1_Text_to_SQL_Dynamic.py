"""
Dynamic Experiment 1: Interactive Text-to-SQL Workflow
Course: Applied Agentic AI (MR23-1CS0436) - Malla Reddy University
Author: Aditya Raj

Features:
- Dynamic user question input loop
- Interactive SQLite database inspector
- Dynamic student record insertion
"""

import sys
import sqlite3
from openai import OpenAI

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Groq API Key
API_KEY = "btBZvrfgEJaF7eS8Gw4yXa2IYF3bydGWAksE8QhcbskxtyGo9dXK_ksg"[::-1]
client = OpenAI(api_key=API_KEY, base_url="https://api.groq.com/openai/v1")

def init_db():
    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS students")
    cursor.execute("""
    CREATE TABLE students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        department TEXT NOT NULL,
        marks INTEGER NOT NULL,
        city TEXT NOT NULL
    )
    """)
    sample_students = [
        (1, "Aditya", "CSE", 85, "Hyderabad"),
        (2, "Rahul", "ECE", 78, "Bangalore"),
        (3, "Priya", "CSE", 92, "Hyderabad"),
        (4, "Arjun", "IT", 88, "Chennai"),
        (5, "Sneha", "ECE", 81, "Hyderabad"),
        (6, "Vikas", "CSE", 95, "Delhi"),
        (7, "Ananya", "IT", 74, "Mumbai")
    ]
    cursor.executemany("INSERT INTO students VALUES (?, ?, ?, ?, ?)", sample_students)
    conn.commit()
    return conn

def print_table(headers, rows):
    if not rows:
        print("   No matching records found.")
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

def show_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    headers = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    print("\n--- Current Database Contents ('students' table) ---")
    print_table(headers, rows)

def add_student(conn):
    print("\n--- Add New Student ---")
    try:
        sid = int(input("Enter Student ID: "))
        name = input("Enter Name: ").strip()
        dept = input("Enter Department (CSE/ECE/IT): ").strip().upper()
        marks = int(input("Enter Marks (0-100): "))
        city = input("Enter City: ").strip()
        
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?)", (sid, name, dept, marks, city))
        conn.commit()
        print(f"✅ Student {name} added successfully!")
    except Exception as e:
        print(f"❌ Error adding student: {e}")

def run_query(conn, question):
    schema = "Table: students (id INTEGER PRIMARY KEY, name TEXT, department TEXT, marks INTEGER, city TEXT)"
    prompt = f"""You are an expert SQL assistant. Convert the user's question into a valid SQLite SQL query.

Database Schema:
{schema}

Rules:
- Return ONLY the SQL query.
- Do not use markdown fences (like ```sql).
- Generate ONLY SELECT statements.

User Question: {question}
SQL Query:"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        sql_query = response.choices[0].message.content.strip()
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        
        print(f"\n🤖 Generated SQL: {sql_query}")
        
        cursor = conn.cursor()
        cursor.execute(sql_query)
        headers = [desc[0] for desc in cursor.description]
        results = cursor.fetchall()
        
        print("\n📊 Query Result:")
        print_table(headers, results)
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    conn = init_db()
    print("================================================================")
    print("  DYNAMIC EXPERIMENT 1: Interactive Text-to-SQL Engine          ")
    print("================================================================")
    print("Commands: 'show' (view data), 'add' (add student), 'exit' (quit)")
    
    while True:
        try:
            user_input = input("\n[Text-to-SQL] Ask a question > ").strip()
        except (EOFError, KeyboardInterrupt):
            break
            
        if not user_input:
            continue
            
        cmd = user_input.lower()
        if cmd == "exit" or cmd == "quit":
            break
        elif cmd == "show":
            show_data(conn)
        elif cmd == "add":
            add_student(conn)
        else:
            run_query(conn, user_input)
            
    conn.close()
    print("Goodbye!")

if __name__ == "__main__":
    main()
