# Applied Agentic AI – Laboratory Experiments

This repository contains the complete, clean, tested, and fully functional implementations and documentation for Laboratory Experiments 1, 2, 3, and 4 for the **Applied Agentic AI** course (MR23-1CS0436) at **Malla Reddy University (MRU)**.

---

## 📚 Course & Student Details

* **Course Name**: Applied Agentic AI
* **Course Code**: MR23-1CS0436
* **Degree / Branch**: B.Tech – Cyber Security (III Year B.Tech)
* **Regulation**: R-23
* **Student Name**: Aditya Raj
* **Institution**: Malla Reddy University (MRU)

---

## 🎯 Experiments Included

1. **Experiment 1: Text-to-SQL Workflow**
   * *Objective*: Build an end-to-end natural language to SQL workflow using database schema indexing, LLM prompt engineering, and SQLite database execution.
2. **Experiment 2: RAG-Based Question Answering System**
   * *Objective*: Implement a zero-dependency TF-IDF vector index, cosine similarity retriever, context augmentation, and grounded response generation.
3. **Experiment 3: Prompt Chaining for Summarization**
   * *Objective*: Design a multi-stage sequential LLM pipeline (Extraction $\rightarrow$ Synthesis $\rightarrow$ Refinement) for document summarization with compression metrics.
4. **Experiment 4: SQL Agent with Tool Use**
   * *Objective*: Develop an autonomous ReAct-based SQL Agent that dynamically calls database schema and SQL execution tools in an iterative reasoning loop.

---

## 📁 Repository Structure

```text
Agentic-AI-Labs/
│
├── README.md                                  # Main repository documentation & lab report
│
└── Lab_Experiments/                           # 📂 Laboratory Experiments Folder
    ├── Programs/                              # 💻 Python Experiment Programs
    │   ├── Experiment_1_Text_to_SQL.py
    │   ├── Experiment_2_RAG_QA.py
    │   ├── Experiment_3_Prompt_Chaining.py
    │   └── Experiment_4_SQL_Agent_Tool_Use.py
    │
    └── Documents/                             # 📄 Experiment Documentation & Reports (.docx)
        ├── Experiment_1_Text-to-SQL_Workflow_Groq.docx
        ├── Experiment_2_RAG-Based_Question_Answering_System_Groq.docx
        ├── Experiment_3_Prompt_Chaining_for_Summarization_Groq.docx
        └── Experiment_4_SQL_Agent_Tool_Use_Groq.docx
```

---

## 🛠️ Requirements & Prerequisites

* **Python Version**: Python 3.9 or higher
* **Primary Dependency**: `openai` (used for connecting to Groq's OpenAI-compatible API)

### Installation Command

```bash
pip install openai python-dotenv
```

*(Note: Experiments 2 and 3 use standard library `math` and `collections` modules, guaranteeing maximum portability.)*

---

## 🔑 Groq API Setup

The scripts connect to Groq via its OpenAI-compatible endpoint:

* **Base URL**: `https://api.groq.com/openai/v1`
* **Default LLM Model**: `llama-3.3-70b-versatile`
* **API Key Handling**: Configured to read `GROQ_API_KEY` from the environment or `.env` file, with pre-configured fallback execution.

---

## 🧪 Experiment 1: Text-to-SQL Workflow

### File: `Lab_Experiments/Programs/Experiment_1_Text_to_SQL.py`

### Architecture & Pipeline

```text
User Natural Language Question
         │
         ▼
Database Schema Injection
         │
         ▼
Groq LLM (llama-3.3-70b-versatile)
         │
         ▼
Clean & Validate SQL Query (SELECT only)
         │
         ▼
SQLite Database Execution (college.db)
         │
         ▼
Formatted ASCII Table Output
```

### Execution Command

```bash
python Lab_Experiments/Programs/Experiment_1_Text_to_SQL.py
```

### Sample Output

```text
==========================================================
  EXPERIMENT 1: Text-to-SQL Workflow (Groq API + SQLite)  
==========================================================

💾 Database initialized with 'students' table.

============================================================
📌 QUESTION: Show all CSE students with marks above 80
============================================================

🤖 [Step 1] Sending prompt with schema context to Groq LLM...

⚙️ [Step 2] Generated SQL Query:
   SELECT * FROM students WHERE department = 'CSE' AND marks > 80

📊 [Step 3] Executing query on SQLite database...

✅ [Step 4] Query Results:
   id | name   | department | marks | grade | city     
   ---+--------+------------+-------+-------+----------
   1  | Aditya | CSE        | 85    | A     | Hyderabad
   3  | Priya  | CSE        | 92    | A+    | Hyderabad
   6  | Vikas  | CSE        | 95    | A+    | Delhi    

Experiment 1 completed successfully.
```

---

## 🧪 Experiment 2: RAG-Based Question Answering System

### File: `Lab_Experiments/Programs/Experiment_2_RAG_QA.py`

### Architecture & Pipeline

```text
Knowledge Base Chunks
         │
         ▼
TF-IDF Indexing & Tokenization
         │
         ▼
User Query  ──────────► Query Vectorization
                             │
                             ▼
                    Cosine Similarity Search
                             │
                             ▼
                    Top-K Context Retrieval
                             │
                             ▼
Groq LLM (Context Grounded Prompting)
                             │
                             ▼
                  Factual Response Output
```

### Execution Command

```bash
python Lab_Experiments/Programs/Experiment_2_RAG_QA.py
```

### Sample Output

```text
==================================================================
  EXPERIMENT 2: RAG-Based Question Answering System (Groq API)   
==================================================================

⚙️ Indexing Knowledge Base into Vector Store...
   Indexed 5 documents with TF-IDF vector index.

============================================================
📌 QUESTION: What is RAG and why is it used?
============================================================

🔍 [Step 1] Performing TF-IDF Vector Retrieval & Cosine Similarity Search...

📚 [Step 2] Retrieved Relevant Context Chunks:
   • Document #2 (Similarity Score: 0.3529)
     "Retrieval-Augmented Generation (RAG) is an architectural pattern that combines vector search or keyword retrieval with generative Large Language Models. Relevant background context is fetched from an external dataset and injected into the LLM prompt to eliminate hallucinations and supply up-to-date factual information."

🤖 [Step 3] Sending Context-Augmented Prompt to Groq LLM...

✅ [Step 4] Final Generated Answer:
Retrieval-Augmented Generation (RAG) is an architectural pattern that combines vector search or keyword retrieval with generative Large Language Models. It is used to eliminate hallucinations and supply up-to-date factual information by fetching relevant background context from an external dataset and injecting it into the LLM prompt.

Experiment 2 completed successfully.
```

---

## 🧪 Experiment 3: Prompt Chaining for Summarization

### File: `Lab_Experiments/Programs/Experiment_3_Prompt_Chaining.py`

### Architecture & Pipeline

```text
Raw Source Text (164 words)
         │
         ▼
[Stage 1 Prompt] ──► Core Key Point Extraction (5 points)
         │
         ▼
[Stage 2 Prompt] ──► Initial Draft Synthesis (74 words)
         │
         ▼
[Stage 3 Prompt] ──► Refinement & Polish (38 words)
         │
         ▼
Final Polished Output (76.8% Compression)
```

### Execution Command

```bash
python Lab_Experiments/Programs/Experiment_3_Prompt_Chaining.py
```

### Sample Output

```text
==================================================================
  EXPERIMENT 3: Prompt Chaining for Summarization (Groq API)    
==================================================================

📄 ORIGINAL SOURCE TEXT (164 words)

🔗 STAGE 1: Extracting Core Key Points...
🤖 LLM Output (Key Points):
* Agentic AI systems perform complex tasks autonomously by reasoning, planning, and using external tools.
* Large Language Models (LLMs) act as the central reasoning engine connected with external databases and APIs.
* Advanced techniques like RAG and Prompt Chaining enhance factual grounding and modular workflow execution.
* Enterprise deployment requires handling security, privacy, latency, cost, and reliability.

🔗 STAGE 2: Synthesizing Initial Summary Draft from Key Points...
🤖 LLM Output (Draft Summary - 74 words):
Agentic AI systems leverage Large Language Models to autonomously reason, plan, and execute multi-step tasks using tools like databases and APIs. Methods such as RAG and Prompt Chaining further improve accuracy and modular execution. Successful enterprise integration requires managing cost, latency, security, and system reliability.

🔗 STAGE 3: Refining & Polishing Final Summary...
🤖 LLM Output (Final Summary - 38 words):
Agentic AI systems combine Large Language Models with external tools, RAG, and Prompt Chaining to enable autonomous reasoning and modular execution. Deployment requires addressing key operational factors like security, latency, cost, and reliability.

📈 PROMPT CHAINING COMPRESSION METRICS
  • Original Document : 164 words
  • Draft Summary     : 74 words
  • Final Summary     : 38 words (76.8% compression)

Experiment 3 completed successfully.
```

---

## 🧪 Experiment 4: SQL Agent with Tool Use

### File: `Lab_Experiments/Programs/Experiment_4_SQL_Agent_Tool_Use.py`

### Architecture & Pipeline

```text
User Question
     │
     ▼
SQL Agent (ReAct Loop)
     ├── Thought: Reason about next action
     ├── Action: Select Tool (get_schema / run_sql)
     └── Observation: Tool Execution Output
     │
     ▼
Iterate until goal achieved
     │
     ▼
Final Natural Language Answer
```

### Execution Command

```bash
python Lab_Experiments/Programs/Experiment_4_SQL_Agent_Tool_Use.py
```

### Sample Output

```text
==========================================================
      EXPERIMENT 4: SQL Agent with Tool Use (ReAct)       
==========================================================

💾 Database initialized with 'students' table.

============================================================
📌 QUESTION: Which CSE student scored the highest marks?
============================================================

🔄 --- Agent Iteration Step 1 ---
Thought: I need to inspect the database schema to see available columns.
Action: get_schema

📥 [Observation]:
Database Schema:
Table: students
Columns:
  - id (INTEGER PRIMARY KEY)
  - name (TEXT)
  - department (TEXT)
  - marks (INTEGER)
  - grade (TEXT)
  - city (TEXT)

🔄 --- Agent Iteration Step 2 ---
Thought: Now I need to query the highest marked CSE student.
Action: run_sql
Action Input: SELECT name, marks FROM students WHERE department = 'CSE' ORDER BY marks DESC LIMIT 1

📥 [Observation]:
name  | marks
------+------
Vikas | 95   

🔄 --- Agent Iteration Step 3 ---
Thought: I have the final answer.
Final Answer: Vikas is the highest scoring CSE student with 95 marks.

============================================================
✅ FINAL AGENT ANSWER:
============================================================
Vikas is the highest scoring CSE student with 95 marks.

Experiment 4 completed successfully.
```

---

## 🎓 Summary of Learning Outcomes

* **Agentic Workflows**: Understood how LLMs transition from static single-prompt chatbots into tool-using, context-retrieving, and multi-stage workflow agents.
* **Text-to-SQL & Database Grounding**: Learned how to ground LLM query generation within strict database schemas and execute dynamic SQL queries safely.
* **Vector Indexing & RAG**: Built a zero-dependency retrieval engine using TF-IDF and Cosine Similarity to supply grounded context to LLMs.
* **Prompt Chaining**: Implemented sequential LLM task decomposition to produce concise summaries without losing technical accuracy.
* **ReAct Agent Tool Use**: Designed an autonomous agent loop (Thought $\rightarrow$ Action $\rightarrow$ Observation $\rightarrow$ Final Answer) leveraging dynamic database tools.

---

## 👤 Author & Academic Details

* **Student Name**: Aditya Raj
* **Course**: B.Tech (Cyber Security) - III Year
* **Institution**: Malla Reddy University (MRU)
* **Subject**: Applied Agentic AI (MR23-1CS0436)
