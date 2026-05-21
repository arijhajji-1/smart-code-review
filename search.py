import os
from dotenv import load_dotenv
from groq import Groq
from memory import search_reviews

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask_memory(question):
    print(f"\n🔍 Searching memory for: '{question}'\n")

    # Step 1: Search vector DB for relevant reports
    relevant_reports = search_reviews(question, n_results=3)

    if relevant_reports == "No matching reviews found.":
        print("❌ No relevant reviews found in memory.")
        return

    # Step 2: Send question + relevant reports to LLM
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a helpful assistant that answers questions
about past code reviews. You will receive:
1. A question from the user
2. Relevant code review reports from memory

Answer the question clearly and specifically based on the reports.
Always mention which file and date you're referring to."""
            },
            {
                "role": "user",
                "content": f"QUESTION: {question}\n\nRELEVANT REPORTS:\n{relevant_reports}"
            }
        ]
    )

    answer = response.choices[0].message.content
    print(f"🤖 {answer}")


# Interactive loop — keep asking questions until you type 'exit'
print("💬 Ask questions about your past code reviews (type 'exit' to quit)\n")
while True:
    question = input("You: ").strip()
    if question.lower() == "exit":
        break
    if question:
        ask_memory(question)