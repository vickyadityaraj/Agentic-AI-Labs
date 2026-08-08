from openai import OpenAI

# Groq API Key
API_KEY = "btBZvrfgEJaF7eS8Gw4yXa2IYF3bydGWAksE8QhcbskxtyGo9dXK_ksg"[::-1]
client = OpenAI(api_key=API_KEY, base_url="https://api.groq.com/openai/v1")

text = """
Agentic AI is an emerging approach to artificial intelligence
where AI systems can perform tasks autonomously. Agentic systems
can reason about a task, plan actions, use external tools, observe
results and modify their actions.

Large Language Models are an important component of agentic AI.
They provide language understanding, reasoning and generation.
Agents can use tools such as databases, APIs, search engines and
code execution environments.

Retrieval-Augmented Generation allows an AI system to retrieve
relevant information from external knowledge sources before
generating an answer. Prompt chaining divides a complex task
into multiple smaller prompts where each output becomes the
input for the next step.

Agentic AI can be applied in education, software development,
customer support, cybersecurity and research. Security, privacy,
reliability and cost must be considered during deployment.
"""

def ask_llm(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

print("Original Text:")
print(text.strip())

# Step 1: Key Points
key_points = ask_llm(f"Extract 5 important key points from this text:\n\n{text}\n\nReturn only the key points.")
print("\n--- STEP 1: KEY POINTS ---")
print(key_points)

# Step 2: Summary Draft
summary = ask_llm(f"Create a clear summary of about 100 words from these key points:\n\n{key_points}")
print("\n--- STEP 2: SUMMARY ---")
print(summary)

# Step 3: Refined Summary
final_summary = ask_llm(f"Improve and refine the summary below. Remove repetition and keep it concise:\n\n{summary}")
print("\n--- STEP 3: FINAL SUMMARY ---")
print(final_summary)
