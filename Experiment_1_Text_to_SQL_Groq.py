import sqlite3
from openai import OpenAI

# Groq API Key
API_KEY = "btBZvrfgEJaF7eS8Gw4yXa2IYF3bydGWAksE8QhcbskxtyGo9dXK_ksg"[::-1]
client = OpenAI(api_key=API_KEY, base_url="https://api.groq.com/openai/v1")

# Create database and sample table
conn = sqlite3.connect("college.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS students")
cursor.execute("""
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    marks INTEGER
)
""")

cursor.executemany("INSERT INTO students VALUES (?, ?, ?, ?)", [
    (1, "Aditya", "CSE", 85),
    (2, "Rahul", "ECE", 78),
    (3, "Priya", "CSE", 92),
    (4, "Arjun", "IT", 88),
    (5, "Sneha", "ECE", 81)
])
conn.commit()

schema = "Table: students (id, name, department, marks)"

print("Database initialized.")
question = "Show all CSE students"
print(f"Question: {question}")

prompt = f"""You are an SQL expert.
Convert the user's question into a valid SQLite SQL query.

Database schema:
{schema}

Rules:
- Return ONLY the SQL query.
- Do not use markdown or explanations.
- Generate only SELECT statements.

Question: {question}"""

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}],
    temperature=0
)

sql_query = response.choices[0].message.content.strip()
sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

print("\nGenerated SQL:")
print(sql_query)

try:
    cursor.execute(sql_query)
    print("\nQuery Result:")
    for row in cursor.fetchall():
        print(row)
except Exception as e:
    print("Error executing query:", e)
finally:
    conn.close()
