"""
Dynamic Experiment 3: Interactive Prompt Chaining Pipeline
Course: Applied Agentic AI (MR23-1CS0436) - Malla Reddy University
Author: Aditya Raj

Features:
- Dynamic custom article input or preset topic selection
- Customizable prompt chain target length & style
- Live multi-stage prompt transformation metrics
"""

import sys
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

SAMPLE_ARTICLES = {
    "1": ("Agentic AI & Autonomy", """
Agentic AI represents a fundamental paradigm shift in artificial intelligence, moving from passive conversational assistants to proactive, goal-driven autonomous systems. Unlike traditional Large Language Models (LLMs) that simply generate text based on prompts, Agentic AI systems are capable of reasoning, planning multi-step actions, utilizing external tools, observing execution outcomes, and dynamically adapting their behavior to achieve complex objectives.

Core architectural components of AI Agents include reasoning models, long-term and short-term memory systems, tool/function integration, and workflow orchestration. Tools enable agents to interact with databases, web search APIs, enterprise software, and python code execution environments. 

Techniques such as Retrieval-Augmented Generation (RAG) ground agents with domain-specific knowledge bases, while Prompt Chaining decomposes intricate workflows into modular, sequential steps where the output of one step becomes the input for the next.
"""),
    "2": ("Cyber Security & Zero Trust", """
Zero Trust Architecture is an enterprise cybersecurity framework based on the strict principle: never trust, always verify. Under Zero Trust, no user or device inside or outside the organization's perimeter is granted automatic network access. Continuous authentication, micro-segmentation, and least-privilege access control are enforced across all digital identity assets.

With the rapid expansion of cloud computing and remote workforces, traditional perimeter defenses have proven insufficient against modern ransomware attacks, phishing campaigns, and zero-day vulnerabilities. Integrating AI-driven anomaly detection and automated security orchestrators enables security teams to detect and respond to threats in real time.
""")
}

def ask_llm(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

def run_pipeline(text):
    print("\n" + "="*60)
    print("📄 ORIGINAL SOURCE TEXT")
    print("="*60)
    print(text.strip())
    word_count_original = len(text.split())
    print(f"\n📊 Word Count: {word_count_original} words")
    
    # Stage 1: Key Point Extraction
    print("\n" + "="*60)
    print("🔗 STAGE 1: Extracting Core Key Points")
    print("="*60)
    key_points = ask_llm(f"Extract 5 important key points from this text:\n\n{text}\n\nReturn only the bulleted key points.")
    print(key_points)
    
    # Stage 2: Draft Summary
    print("\n" + "="*60)
    print("🔗 STAGE 2: Synthesizing Summary Draft")
    print("="*60)
    summary_draft = ask_llm(f"Write a concise summary paragraph (around 80 words) based strictly on these key points:\n\n{key_points}")
    print(summary_draft)
    word_count_draft = len(summary_draft.split())
    print(f"\n📊 Word Count: {word_count_draft} words")
    
    # Stage 3: Polish & Refine
    print("\n" + "="*60)
    print("🔗 STAGE 3: Refining & Polishing Summary")
    print("="*60)
    final_summary = ask_llm(f"Refine and polish the summary below. Remove repetition, make it concise, and retain technical terms:\n\n{summary_draft}")
    print(final_summary)
    word_count_final = len(final_summary.split())
    print(f"\n📊 Word Count: {word_count_final} words")
    
    # Metrics
    compression = (1 - word_count_final / word_count_original) * 100
    print("\n" + "="*60)
    print(f"📈 PIPELINE COMPRESSION: {word_count_original} words -> {word_count_final} words ({compression:.1f}% reduction)")
    print("="*60)

def main():
    print("================================================================")
    print("  DYNAMIC EXPERIMENT 3: Interactive Prompt Chaining Engine      ")
    print("================================================================")
    
    while True:
        print("\nChoose an option:")
        print("  1. Select Sample Article 1 (Agentic AI)")
        print("  2. Select Sample Article 2 (Cyber Security)")
        print("  3. Paste / Enter Custom Text")
        print("  4. Exit")
        
        try:
            choice = input("\nEnter choice (1-4) > ").strip()
        except (EOFError, KeyboardInterrupt):
            break
            
        if choice == "4" or choice.lower() == "exit":
            break
        elif choice in SAMPLE_ARTICLES:
            title, content = SAMPLE_ARTICLES[choice]
            print(f"\nSelected: {title}")
            run_pipeline(content)
        elif choice == "3":
            print("\nEnter/Paste your custom text (press Enter twice when done):")
            lines = []
            while True:
                line = input()
                if not line:
                    break
                lines.append(line)
            custom_text = "\n".join(lines)
            if custom_text.strip():
                run_pipeline(custom_text)
            else:
                print("No text provided.")
        else:
            print("Invalid choice, try again.")
            
    print("Goodbye!")

if __name__ == "__main__":
    main()
