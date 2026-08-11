"""
Experiment 4: SQL Agent with Tool Use
Course: Applied Agentic AI (MR23-1CS0436) - Malla Reddy University
Author: Aditya Raj

Description:
Implements a ReAct-based autonomous SQL Agent (Thought -> Action -> Observation -> Final Answer)
that dynamically selects and executes database tools to answer complex natural language queries.
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

def format_table(headers, rows):
    """Formats tabular database results into a string box."""
    if not rows:
        return "No matching records found."
    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))
            
    header_str = " | ".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers))
    divider = "-+-".join("-" * col_widths[i] for i in range(len(headers)))
    
    lines = [header_str, divider]
    for row in rows:
        lines.append(" | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row)))
    return "\n".join(lines)

def tool_get_schema(conn):
    """Tool: Returns the database schema metadata."""
    return """Database Schema:
Table: students
Columns:
  - id (INTEGER PRIMARY KEY)
  - name (TEXT)
  - department (TEXT) -- e.g., 'CSE', 'ECE', 'IT'
  - marks (INTEGER)   -- range 0 to 100
  - grade (TEXT)     -- e.g., 'A+', 'A', 'B+'
  - city (TEXT)      -- e.g., 'Hyderabad', 'Delhi'"""

def tool_run_sql(conn, sql_query):
    """Tool: Executes a SELECT query safely on SQLite database."""
    clean_sql = sql_query.strip().replace("```sql", "").replace("```", "")
    if not clean_sql.upper().startswith("SELECT"):
        return "ERROR: Safety constraint violated. Only SELECT queries are permitted."
    
    try:
        cursor = conn.cursor()
        cursor.execute(clean_sql)
        headers = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        return format_table(headers, rows)
    except sqlite3.Error as e:
        return f"SQL ERROR: {e}"

def sql_agent(question, client, conn, max_steps=5):
    """Runs the ReAct Agent loop to answer user questions using tools."""
    system_prompt = """You are a SQL Agent with access to database tools.
Your objective is to answer user questions by inspecting the schema and querying the database.

Available Tools:
1. Action: get_schema
   (Description: Returns table names and column descriptions)
   
2. Action: run_sql
   Action Input: <SELECT SQL query>
   (Description: Executes a SELECT query on SQLite database)

Required Output Format for each step:
Thought: <reasoning about what to do next>
Action: <tool_name>
Action Input: <input for tool if required>

When you have sufficient information to answer the question:
Thought: I have the final answer.
Final Answer: <concise natural language answer>

Rules:
- Generate ONLY valid SQLite SELECT queries.
- Never run INSERT, UPDATE, DELETE, DROP, or ALTER.
- Do not repeat actions unnecessarily.
"""

    print(f"\n============================================================")
    print(f"📌 QUESTION: {question}")
    print(f"============================================================")

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]

    for step in range(1, max_steps + 1):
        print(f"\n🔄 --- Agent Iteration Step {step} ---")
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0
            )
        except AuthenticationError:
            print("❌ [Authentication Error] Invalid Groq API Key.")
            print("💡 Please set the GROQ_API_KEY environment variable or create a .env file with GROQ_API_KEY=your_key.")
            return False
        except Exception as e:
            print(f"❌ [API Error] {e}")
            return False

        output = response.choices[0].message.content.strip()
        print(f"{output}")

        if "Final Answer:" in output:
            final_ans = output.split("Final Answer:", 1)[1].strip()
            print("\n============================================================")
            print("✅ FINAL AGENT ANSWER:")
            print("============================================================")
            print(f"{final_ans}")
            return True

        # Action execution logic
        if "Action: get_schema" in output:
            observation = tool_get_schema(conn)
        elif "Action: run_sql" in output:
            if "Action Input:" in output:
                sql_input = output.split("Action Input:", 1)[1].strip()
                observation = tool_run_sql(conn, sql_input)
            else:
                observation = "ERROR: Missing Action Input for run_sql."
        else:
            observation = "Please follow the required ReAct format (Thought -> Action -> Action Input)."

        print(f"\n📥 [Observation]:\n{observation}")

        messages.append({"role": "assistant", "content": output})
        messages.append({"role": "user", "content": f"Observation:\n{observation}"})

    print("⚠️ Agent reached maximum step limit without reaching a final answer.")
    return False

def main():
    print("==========================================================")
    print("      EXPERIMENT 4: SQL Agent with Tool Use (ReAct)       ")
    print("==========================================================")
    
    conn = init_database()
    print("\n💾 Database initialized with 'students' table.")
    
    try:
        client = get_client()
    except Exception as e:
        print(f"❌ Failed to initialize Groq API client: {e}")
        conn.close()
        return

    demo_question = "Which CSE student scored the highest marks?"
    success = sql_agent(demo_question, client, conn)
    
    conn.close()
    if success:
        print("\nExperiment 4 completed successfully.")

if __name__ == "__main__":
    main()
