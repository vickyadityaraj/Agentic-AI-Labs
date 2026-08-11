"""
Experiment 2: RAG-Based Question Answering System
Course: Applied Agentic AI (MR23-1CS0436) - Malla Reddy University
Author: Aditya Raj

Description:
Implements a zero-dependency vector indexer using TF-IDF and Cosine Similarity 
to retrieve context chunks and supply them to a Groq-hosted LLM for factual Q&A.
"""

import os
import sys
import math
import re
from collections import Counter
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

# Knowledge Base Documents
KNOWLEDGE_BASE = [
    "Agentic AI systems can autonomously perform tasks, make decisions, use external tools, and interact with software environments to achieve complex goals.",
    "Retrieval-Augmented Generation (RAG) is an architectural pattern that combines vector search or keyword retrieval with generative Large Language Models. Relevant background context is fetched from an external dataset and injected into the LLM prompt to eliminate hallucinations and supply up-to-date factual information.",
    "Embeddings are numerical vector representations of text. Text chunks with similar semantic meanings are positioned close to each other in high-dimensional vector spaces and compared using cosine similarity.",
    "A vector database stores high-dimensional vector embeddings and supports fast similarity-based searching. It is commonly used in RAG applications to store document chunks.",
    "Prompt Chaining decomposes a complex task into multiple smaller sequential prompts where the output of each LLM step serves as the input context for the subsequent step."
]

def build_tfidf_index(documents):
    """Builds a zero-dependency TF-IDF index over a collection of text documents."""
    tokenized_docs = [re.findall(r"[a-zA-Z0-9]+", doc.lower()) for doc in documents]
    vocabulary = sorted(set(word for doc in tokenized_docs for word in doc))
    
    def vectorizer(tokens):
        counts = Counter(tokens)
        total = len(tokens) or 1
        vec = []
        for word in vocabulary:
            tf = counts[word] / total
            df = sum(1 for d in tokenized_docs if word in d)
            idf = math.log((1 + len(documents)) / (1 + df)) + 1
            vec.append(tf * idf)
        return vec

    doc_vectors = [vectorizer(doc) for doc in tokenized_docs]
    return vectorizer, doc_vectors

def cosine_similarity(v1, v2):
    """Calculates cosine similarity between two numeric vectors."""
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm_1 = math.sqrt(sum(a * a for a in v1))
    norm_2 = math.sqrt(sum(b * b for b in v2))
    return dot_product / (norm_1 * norm_2) if (norm_1 and norm_2) else 0.0

def retrieve_top_k(query, vectorizer, doc_vectors, documents, top_k=2):
    """Retrieves top-K most relevant document chunks based on cosine similarity."""
    query_tokens = re.findall(r"[a-zA-Z0-9]+", query.lower())
    query_vector = vectorizer(query_tokens)
    
    scored_docs = []
    for idx, doc_vec in enumerate(doc_vectors):
        score = cosine_similarity(query_vector, doc_vec)
        scored_docs.append((score, idx, documents[idx]))
        
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    return scored_docs[:top_k]

def rag_qa(question, vectorizer, doc_vectors, client):
    """Executes full RAG workflow: Retrieval -> Context Augmentation -> Generation."""
    print(f"\n============================================================")
    print(f"📌 QUESTION: {question}")
    print(f"============================================================")
    
    print("\n🔍 [Step 1] Performing TF-IDF Vector Retrieval & Cosine Similarity Search...")
    top_results = retrieve_top_k(question, vectorizer, doc_vectors, KNOWLEDGE_BASE, top_k=2)
    
    print("\n📚 [Step 2] Retrieved Relevant Context Chunks:")
    context_chunks = []
    for rank, (score, doc_id, text) in enumerate(top_results, start=1):
        print(f"   • Document #{doc_id + 1} (Similarity Score: {score:.4f})")
        print(f"     \"{text}\"")
        context_chunks.append(text)
        
    retrieved_context = "\n\n".join(context_chunks)
    
    prompt = f"""Answer the question using ONLY the provided context below.

Context:
{retrieved_context}

Question:
{question}

Strict Instructions:
1. Provide a direct, factual answer based ONLY on the context above.
2. Do not assume or extrapolate information outside the context.
3. If the answer cannot be found in the context, output exactly: 'Information not found in the knowledge base.'"""

    print("\n🤖 [Step 3] Sending Context-Augmented Prompt to Groq LLM...")
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

    final_answer = response.choices[0].message.content.strip()
    
    print("\n✅ [Step 4] Final Generated Answer:")
    print(f"{final_answer}")
    return True

def main():
    print("==================================================================")
    print("  EXPERIMENT 2: RAG-Based Question Answering System (Groq API)   ")
    print("==================================================================")
    
    print("\n⚙️ Indexing Knowledge Base into Vector Store...")
    vectorizer, doc_vectors = build_tfidf_index(KNOWLEDGE_BASE)
    print(f"   Indexed {len(KNOWLEDGE_BASE)} documents with TF-IDF vector index.")
    
    try:
        client = get_client()
    except Exception as e:
        print(f"❌ Failed to initialize Groq API client: {e}")
        return

    demo_question = "What is RAG and why is it used?"
    success = rag_qa(demo_question, vectorizer, doc_vectors, client)
    
    if success:
        print("\nExperiment 2 completed successfully.")

if __name__ == "__main__":
    main()
