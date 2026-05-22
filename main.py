import os
from dotenv import load_dotenv
from groq import Groq
from core.memory import search_reviews

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

conversation_history = []


def chat(user_message):
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    if "review" in user_message.lower():
        words = user_message.split()
        filename = next((w for w in words if "." in w), None)
        if filename:
            from core.reviewer import review_code
            filepath = os.path.join("data", "samples", filename)
            review_code(filepath)
            reply = f"✅ Review complete for {filename}."
        else:
            reply = "Please specify a file to review (e.g. review sample_code.py)"

    elif "fix" in user_message.lower():
        words = user_message.split()
        filename = next((w for w in words if "." in w), None)
        if filename:
            from core.fixer import fix_code
            filepath = os.path.join("data", "samples", filename)
            fix_code(filepath)
            reply = f"✅ Fixed version saved."
        else:
            reply = "Please specify a file to fix (e.g. fix sample_code.py)"

    else:
        relevant = search_reviews(user_message, n_results=2)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant for a code review tool. Answer questions based on past reviews."
                },
                *conversation_history,
                {
                    "role": "user",
                    "content": f"MEMORY:\n{relevant}\n\nQUESTION: {user_message}"
                }
            ]
        )
        reply = response.choices[0].message.content

    conversation_history.append({
        "role": "assistant",
        "content": reply
    })

    print(f"\n🤖 {reply}\n")


print("🤖 AI Code Assistant — type 'exit' to quit")
print("Commands: 'review <file>' | 'fix <file>' | ask anything\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        break
    if user_input:
        chat(user_input)