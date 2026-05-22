import os
from groq import Groq
from dotenv import load_dotenv
from core.memory import search_reviews, save_review
from datetime import datetime

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def fix_code(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        original_code = f.read()

    filename = os.path.basename(filepath)
    ext = os.path.splitext(filepath)[1]

    print(f"🔍 Fetching last review of {filename} from memory...")
    past_review = search_reviews(f"review of {filename}", n_results=1)

    if past_review == "No matching reviews found.":
        print("❌ No past review found. Run reviewer first.")
        return

    print("🔧 Fixing code based on review...\n")
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are an expert developer.
You will receive:
1. Original buggy code
2. A code review report listing all issues

Your job: rewrite the ENTIRE file fixing ALL issues mentioned.

Rules:
- Fix every bug, bad practice, and security issue
- Keep the same logic and functionality
- Add brief inline comments explaining what you fixed
- Return ONLY the fixed code, no explanations, no markdown backticks"""
            },
            {
                "role": "user",
                "content": f"ORIGINAL CODE:\n{original_code}\n\nREVIEW:\n{past_review}"
            }
        ]
    )

    fixed_code = response.choices[0].message.content
    fixed_filename = filepath.replace(ext, f"_fixed{ext}")

    with open(fixed_filename, "w", encoding="utf-8") as f:
        f.write(fixed_code)

    print(f"✅ Fixed code saved to: {fixed_filename}")
    print(f"\n--- PREVIEW ---\n{fixed_code[:500]}...")

    save_review(
        filename=f"{filename}_fixed",
        ai_feedback=f"Auto-fixed version of {filename}.",
        flake8_output="N/A",
        complexity_output="N/A"
    )

    return fixed_filename