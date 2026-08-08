# Applied Agentic AI – Laboratory Experiments

This repository contains the completed, tested, and fully functional implementations for Laboratory Experiments 1, 2, and 3 for the **Applied Agentic AI** course (MR23-1CS0436) at **Malla Reddy University (MRU)**.

---

## 📚 Course Details

* **Course Name**: Applied Agentic AI
* **Course Code**: MR23-1CS0436
* **Degree / Branch**: B.Tech – Cyber Security (III Year B.Tech)
* **Regulation**: R-23
* **Student Name**: Aditya Raj

---

## 🎯 Experiments Included

1. **Experiment 1: Text-to-SQL Workflow**
   * *Objective*: Build an end-to-end natural language to SQL workflow using database schema indexing, LLM prompt engineering, and SQLite database execution.
2. **Experiment 2: RAG-Based Question Answering System**
   * *Objective*: Implement a zero-dependency TF-IDF vector index, cosine similarity retriever, context augmentation, and grounded response generation.
3. **Experiment 3: Prompt Chaining for Summarization**
   * *Objective*: Design a multi-stage sequential LLM pipeline (Extraction $\rightarrow$ Synthesis $\rightarrow$ Refinement) for document summarization.

---

## 📁 Repository Structure

```text
Agentic-AI-Labs/
│
├── README.md                                  # Main repository documentation & lab report
├── Experiment_1_Text_to_SQL_Groq.py           # Experiment 1 static script (for faculty evaluation)
├── Experiment_2_RAG_QA_Groq.py                # Experiment 2 static script (for faculty evaluation)
├── Experiment_3_Prompt_Chaining_Groq.py       # Experiment 3 static script (for faculty evaluation)
│
├── dynamic_experiments/                       # 🌟 Interactive & Dynamic CLI Applications
│   ├── Experiment_1_Text_to_SQL_Dynamic.py    # Interactive Text-to-SQL engine with custom query loop
│   ├── Experiment_2_RAG_QA_Dynamic.py         # Dynamic RAG engine with live custom document indexing
│   └── Experiment_3_Prompt_Chaining_Dynamic.py # Interactive Prompt Chaining pipeline for custom text
│
├── Experiment_1_Text-to-SQL_Workflow_Groq.docx
├── Experiment_2_RAG-Based_Question_Answering_System_Groq.docx
└── Experiment_3_Prompt_Chaining_for_Summarization_Groq.docx
```

---

## 🛠️ Requirements & Prerequisites

* **Python Version**: Python 3.9 or higher
* **Primary Dependency**: `openai` (used for connecting to Groq's OpenAI-compatible API)

### Installation Command

```bash
pip install openai
```

*(Note: Experiments 2 and 3 use standard library `math` and `collections` modules, so external libraries like `numpy` are not required, guaranteeing maximum portability.)*

---

## 🔑 Groq API Setup

The scripts connect to Groq via its OpenAI-compatible endpoint:

* **Base URL**: `https://api.groq.com/openai/v1`
* **Default LLM Model**: `llama-3.3-70b-versatile`
* **Embedded API Key**: Pre-configured in the code for instant faculty execution out-of-the-box.

---

## 🧪 Experiment 1: Text-to-SQL Workflow

### File: `Experiment_1_Text_to_SQL_Groq.py`

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

### Key Features
* Creates a SQLite database (`college.db`) with a `students` table containing columns: `id`, `name`, `department`, `marks`, `grade`, `city`.
* Implements safety verification (only permits `SELECT` statements).
* Cleans markdown formatting fences (` ```sql `) automatically.
* Renders query results in a clean, aligned tabular format.

### Execution Command

```bash
python Experiment_1_Text_to_SQL_Groq.py
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

🤖 [Step 1] Sending prompt to Groq LLM (llama-3.3-70b-versatile)...

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

### File: `Experiment_2_RAG_QA_Groq.py`

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

### Key Features
* Built-in zero-dependency vector index using pure Python TF-IDF vectorization and Cosine Similarity calculation.
* Displays similarity scores (e.g., `0.3529`) and retrieved text chunks during execution.
* Strict grounding prompt instructions prevent model hallucinations.

### Execution Command

```bash
python Experiment_2_RAG_QA_Groq.py
```

### Sample Output

```text
==================================================================
  EXPERIMENT 2: RAG-Based Question Answering System (Groq API)   
==================================================================

⚙️ Indexing Knowledge Base into Vector Store...
   Indexed 5 documents with vocabulary size of 143 words.

============================================================
📌 QUESTION: What is RAG and why is it used?
============================================================

🔍 [Step 1] Performing TF-IDF Vector Retrieval & Cosine Similarity Search...

📚 [Step 2] Retrieved Relevant Context Chunks:
   • Document #2 [Retrieval-Augmented Generation (RAG)] (Similarity Score: 0.3529)
     "Retrieval-Augmented Generation (RAG) is an architectural pattern that combines vector search or keyword retrieval with generative Large Language Models. Relevant background context is fetched from an external dataset and injected into the LLM prompt to eliminate hallucinations and supply up-to-date factual information."

🤖 [Step 3] Sending Context-Augmented Prompt to Groq LLM (llama-3.3-70b-versatile)...

✅ [Step 4] Final Generated Answer:
RAG stands for Retrieval-Augmented Generation. It is an architectural pattern that combines vector search or keyword retrieval with generative Large Language Models. RAG is used to eliminate hallucinations and supply up-to-date factual information by fetching relevant background context from an external dataset and injecting it into the LLM prompt.

Experiment 2 completed successfully.
```

---

## 🧪 Experiment 3: Prompt Chaining for Summarization

### File: `Experiment_3_Prompt_Chaining_Groq.py`

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

### Key Features
* Multi-stage prompt chain where output of each stage feeds directly as context to the next stage.
* Demonstrates modular task decomposition for complex NLP workflows.
* Calculates word counts and compression efficiency metrics across all stages.

### Execution Command

```bash
python Experiment_3_Prompt_Chaining_Groq.py
```

### Sample Output

```text
==================================================================
  EXPERIMENT 3: Prompt Chaining for Summarization (Groq API)    
==================================================================

📄 ORIGINAL SOURCE TEXT (164 words)

🔗 STAGE 1: Extracting Core Key Points
🤖 LLM Output:
* Agentic AI systems can reason, plan, and adapt to achieve complex objectives.
* Core components include reasoning models, memory systems, tool integration, and workflow orchestration.
* Interacts with external tools such as databases, web search APIs, and python code execution environments.
* Techniques like RAG and Prompt Chaining enable domain-specific knowledge and modular workflows.
* Deployment requires addressing challenges like security, cost, latency, reliability, and governance.

🔗 STAGE 2: Synthesizing Initial Summary from Key Points (74 words)

🔗 STAGE 3: Refining & Polishing Summary
🤖 LLM Output:
Agentic AI systems leverage Large Language Models (LLMs) and techniques like Retrieval-Augmented Generation (RAG) and Prompt Chaining to enable complex reasoning and autonomous execution. However, deployment requires careful consideration of security, cost, and reliability.

📈 PROMPT CHAINING COMPRESSION METRICS
  • Original Document : 164 words
  • Draft Summary     : 74 words
  • Final Summary     : 38 words (76.8% compression)

Experiment 3 completed successfully.
```

---

## 🎓 Summary of Learning Outcomes

* **Agentic Workflows**: Understood how LLMs transition from single-prompt chatbots into tool-using, context-retrieving, and multi-stage workflow agents.
* **Text-to-SQL & Database Grounding**: Learned how to ground LLM query generation within strict database schemas and execute dynamic SQL queries safely.
* **Vector Indexing & RAG**: Built a zero-dependency retrieval engine using TF-IDF and Cosine Similarity to supply grounded context to LLMs.
* **Prompt Chaining**: Implemented sequential LLM task decomposition to produce concise summaries without losing technical accuracy.

---

## 👤 Author & Academic Details

* **Student Name**: Aditya Raj
* **Course**: B.Tech (Cyber Security) - III Year
* **Institution**: Malla Reddy University (MRU)
* **Subject**: Applied Agentic AI (MR23-1CS0436)
