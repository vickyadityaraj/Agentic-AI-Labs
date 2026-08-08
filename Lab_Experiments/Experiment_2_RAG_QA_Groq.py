import math
import re
from collections import Counter
from openai import OpenAI

# Groq API Key
API_KEY = "btBZvrfgEJaF7eS8Gw4yXa2IYF3bydGWAksE8QhcbskxtyGo9dXK_ksg"[::-1]
client = OpenAI(api_key=API_KEY, base_url="https://api.groq.com/openai/v1")

# Knowledge base
documents = [
    "Agentic AI systems can autonomously perform tasks, make decisions, use tools and interact with external systems to achieve a goal.",
    "Retrieval-Augmented Generation, or RAG, combines information retrieval with language generation. Relevant documents are retrieved and supplied as context to a language model.",
    "Embeddings are numerical representations of text. Similar texts can be compared using vector similarity for information retrieval.",
    "A vector database stores vector representations and supports similarity-based searching. It is commonly used in RAG applications."
]

tokenized_docs = [re.findall(r"[a-zA-Z0-9]+", d.lower()) for d in documents]
vocabulary = sorted(set(w for d in tokenized_docs for w in d))

def vectorize(tokens):
    counts = Counter(tokens)
    total = len(tokens) or 1
    vec = []
    for term in vocabulary:
        tf = counts[term] / total
        df = sum(1 for d in tokenized_docs if term in d)
        idf = math.log((1 + len(documents)) / (1 + df)) + 1
        vec.append(tf * idf)
    return vec

def cosine_similarity(v1, v2):
    dot = sum(a * b for a, b in zip(v1, v2))
    n1 = math.sqrt(sum(a * a for a in v1))
    n2 = math.sqrt(sum(b * b for b in v2))
    return dot / (n1 * n2) if (n1 and n2) else 0.0

doc_vectors = [vectorize(d) for d in tokenized_docs]

question = "What is RAG?"
print("Question:", question)

q_vec = vectorize(re.findall(r"[a-zA-Z0-9]+", question.lower()))
scores = [(cosine_similarity(q_vec, dv), i) for i, dv in enumerate(doc_vectors)]
scores.sort(reverse=True)

retrieved_context = "\n".join(documents[i] for _, i in scores[:2])
print("\nRetrieved Context:")
print(retrieved_context)

prompt = f"""Answer the question using ONLY the context below.

Context:
{retrieved_context}

Question:
{question}

If the answer is not in the context, say: Information not found in the knowledge base."""

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}],
    temperature=0
)

print("\nGenerated Answer:")
print(response.choices[0].message.content)
