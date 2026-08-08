"""
Dynamic Experiment 2: Interactive RAG Question Answering System
Course: Applied Agentic AI (MR23-1CS0436) - Malla Reddy University
Author: Aditya Raj

Features:
- Dynamic custom document insertion into vector knowledge base
- Live TF-IDF vector indexing & Cosine Similarity search
- Grounded AI response generation using Groq API
"""

import sys
import math
import re
from collections import Counter
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

class DynamicKnowledgeBase:
    def __init__(self):
        self.documents = [
            "Agentic AI systems can autonomously perform tasks, make decisions, use tools and interact with external systems to achieve a goal.",
            "Retrieval-Augmented Generation, or RAG, combines information retrieval with language generation. Relevant documents are retrieved and supplied as context to a language model.",
            "Embeddings are numerical representations of text. Similar texts can be compared using vector similarity for information retrieval.",
            "A vector database stores vector representations and supports similarity-based searching. It is commonly used in RAG applications.",
            "Prompt chaining divides a complex task into multiple smaller prompts where each output becomes the input for the next step."
        ]
        self._reindex()

    def add_document(self, text):
        if text.strip():
            self.documents.append(text.strip())
            self._reindex()
            print(f"✅ Added new document! Total documents: {len(self.documents)}")

    def _reindex(self):
        self.tokenized_docs = [re.findall(r"[a-zA-Z0-9]+", d.lower()) for d in self.documents]
        self.vocabulary = sorted(set(w for d in self.tokenized_docs for w in d))
        self.doc_vectors = [self._vectorize(d) for d in self.tokenized_docs]

    def _vectorize(self, tokens):
        counts = Counter(tokens)
        total = len(tokens) or 1
        vec = []
        for term in self.vocabulary:
            tf = counts[term] / total
            df = sum(1 for d in self.tokenized_docs if term in d)
            idf = math.log((1 + len(self.documents)) / (1 + df)) + 1
            vec.append(tf * idf)
        return vec

    def _cosine_similarity(self, v1, v2):
        dot = sum(a * b for a, b in zip(v1, v2))
        n1 = math.sqrt(sum(a * a for a in v1))
        n2 = math.sqrt(sum(b * b for b in v2))
        return dot / (n1 * n2) if (n1 and n2) else 0.0

    def search(self, query, top_k=2):
        q_tokens = re.findall(r"[a-zA-Z0-9]+", query.lower())
        q_vec = self._vectorize(q_tokens)
        scores = [(self._cosine_similarity(q_vec, dv), idx) for idx, dv in enumerate(self.doc_vectors)]
        scores.sort(reverse=True)
        return [(score, self.documents[idx]) for score, idx in scores[:top_k]]

def ask_rag(kb, question):
    retrieved = kb.search(question, top_k=2)
    print("\n🔍 [Retrieval Phase] Top Relevant Contexts:")
    for score, text in retrieved:
        print(f"   • Score {score:.4f}: {text}")
        
    context = "\n".join(text for _, text in retrieved)
    prompt = f"""Answer the question based ONLY on the context below.

Context:
{context}

Question:
{question}

If the answer is not in the context, say: Information not found in the knowledge base."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        print("\n🤖 [Generation Phase] AI Answer:")
        print(f"   {response.choices[0].message.content.strip()}")
    except Exception as e:
        print(f"❌ Error generating response: {e}")

def main():
    kb = DynamicKnowledgeBase()
    print("================================================================")
    print("  DYNAMIC EXPERIMENT 2: Interactive RAG QA Engine               ")
    print("================================================================")
    print("Commands: 'list' (view docs), 'add' (add doc), 'exit' (quit)")
    
    while True:
        try:
            user_input = input("\n[RAG System] Ask a question > ").strip()
        except (EOFError, KeyboardInterrupt):
            break
            
        if not user_input:
            continue
            
        cmd = user_input.lower()
        if cmd == "exit" or cmd == "quit":
            break
        elif cmd == "list":
            print(f"\n--- Knowledge Base ({len(kb.documents)} documents) ---")
            for i, doc in enumerate(kb.documents, 1):
                print(f"  {i}. {doc}")
        elif cmd == "add":
            new_doc = input("Enter new document text: ").strip()
            kb.add_document(new_doc)
        else:
            ask_rag(kb, user_input)
            
    print("Goodbye!")

if __name__ == "__main__":
    main()
