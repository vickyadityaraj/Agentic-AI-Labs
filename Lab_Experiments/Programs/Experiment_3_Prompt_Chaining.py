"""
Experiment 3: Prompt Chaining for Summarization
Course: Applied Agentic AI (MR23-1CS0436) - Malla Reddy University
Author: Aditya Raj

Description:
Designs a multi-stage sequential LLM prompt chain (Extraction -> Synthesis -> Refinement)
for document summarization, including automated word count & compression metric calculations.
"""

import os
import sys
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

SOURCE_TEXT = """
Agentic AI is an emerging paradigm in artificial intelligence where AI systems can perform complex tasks 
autonomously with minimal human supervision. Unlike traditional static AI models that only respond to immediate 
prompts, agentic systems can reason about goals, break complex objectives into sequential sub-tasks, plan actions, 
and dynamically adapt their behavior based on intermediate feedback.

Large Language Models (LLMs) serve as the central reasoning engine for agentic AI. They enable natural language 
understanding, logical reasoning, and response generation. To interact with the external world, agents leverage 
tool integration, connecting with SQL databases, web search search APIs, file systems, and code execution sandboxes.

Advanced design patterns like Retrieval-Augmented Generation (RAG) and Prompt Chaining enhance agent capabilities. 
RAG supplies factual background context from external knowledge stores to eliminate hallucinations, while Prompt 
Chaining decomposes multi-step logical operations into modular prompt pipelines.

Deploying agentic AI in enterprise environments requires careful consideration of security, privacy, execution cost, 
latency, system reliability, and governance controls.
"""

def count_words(text):
    """Utility function to count words in a given string."""
    return len(text.strip().split())

def ask_llm(prompt, client):
    """Executes a single prompt request against Groq API."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

def run_prompt_chain(source_text, client):
    """Executes 3-stage Prompt Chaining pipeline for text summarization."""
    orig_word_count = count_words(source_text)
    
    print(f"\n📄 ORIGINAL SOURCE TEXT ({orig_word_count} words)")
    print("-" * 60)
    print(source_text.strip())
    print("-" * 60)
    
    # STAGE 1: Key Point Extraction
    print("\n🔗 STAGE 1: Extracting Core Key Points...")
    stage1_prompt = f"""Analyze the text below and extract 5 essential bullet points summarizing the core concepts.

Source Text:
{source_text}

Rules:
- Return ONLY the 5 bullet points.
- Do not include introductory text or markdown fluff."""

    try:
        key_points = ask_llm(stage1_prompt, client)
    except AuthenticationError:
        print("❌ [Authentication Error] Invalid Groq API Key.")
        print("💡 Please set the GROQ_API_KEY environment variable or create a .env file with GROQ_API_KEY=your_key.")
        return False
    except Exception as e:
        print(f"❌ [API Error] {e}")
        return False

    print("🤖 LLM Output (Key Points):")
    print(key_points)
    
    # STAGE 2: Synthesis into Draft Summary
    print("\n🔗 STAGE 2: Synthesizing Initial Summary Draft from Key Points...")
    stage2_prompt = f"""Using ONLY the key points below, write a cohesive, well-written summary paragraph of approximately 75 words.

Key Points:
{key_points}

Rules:
- Return ONLY the summary paragraph."""

    draft_summary = ask_llm(stage2_prompt, client)
    draft_word_count = count_words(draft_summary)
    
    print(f"🤖 LLM Output (Draft Summary - {draft_word_count} words):")
    print(draft_summary)
    
    # STAGE 3: Refinement & Optimization
    print("\n🔗 STAGE 3: Refining & Polishing Final Summary...")
    stage3_prompt = f"""Improve and refine the summary draft below. Make it highly concise, remove any wordiness or redundancy, and ensure precise technical terminology.

Draft Summary:
{draft_summary}

Rules:
- Return ONLY the polished final summary."""

    final_summary = ask_llm(stage3_prompt, client)
    final_word_count = count_words(final_summary)
    
    print(f"🤖 LLM Output (Final Summary - {final_word_count} words):")
    print(final_summary)
    
    # Compression Metrics
    compression_rate = (1 - (final_word_count / orig_word_count)) * 100
    
    print("\n📈 PROMPT CHAINING COMPRESSION METRICS")
    print("-" * 45)
    print(f"  • Original Document : {orig_word_count} words")
    print(f"  • Draft Summary     : {draft_word_count} words")
    print(f"  • Final Summary     : {final_word_count} words ({compression_rate:.1f}% compression)")
    print("-" * 45)
    return True

def main():
    print("==================================================================")
    print("  EXPERIMENT 3: Prompt Chaining for Summarization (Groq API)    ")
    print("==================================================================")
    
    try:
        client = get_client()
    except Exception as e:
        print(f"❌ Failed to initialize Groq API client: {e}")
        return

    success = run_prompt_chain(SOURCE_TEXT, client)
    
    if success:
        print("\nExperiment 3 completed successfully.")

if __name__ == "__main__":
    main()
