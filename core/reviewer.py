import os
import sys
from dotenv import load_dotenv
from groq import Groq
from core.tools import run_tools
from core.memory import save_review
from datetime import datetime

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def read_code_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def save_report(filepath, language, linter, complexity, ai_feedback):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = os.path.basename(filepath)
    report_name = os.path.join(
        "data", "reports",
        f"report_{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )
    report = f"""
AI CODE REVIEW REPORT
=====================
File     : {filename}
Language : {language}
Date     : {timestamp}

--- LINTER ---
{linter}

--- COMPLEXITY ---
{complexity}

--- AI REVIEW ---
{ai_feedback}
"""
    with open(report_name, "w", encoding="utf-8") as f:
        f.write(report)
    return report_name


def review_code(filepath):
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        sys.exit(1)

    print(f"\n📂 Reading {filepath}...")
    code = read_code_file(filepath)

    language, linter_output, complexity_output = run_tools(filepath)

    print("🤖 Sending to AI...\n")
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": f"""You are an expert {language} code reviewer.
You will receive:
1. The source code
2. Static analysis output (linter + complexity if available)

Give a complete review in this format:

🐛 BUGS & ERRORS:
- list each bug with line number

⚠️ BAD PRACTICES:
- list each bad practice

🔒 SECURITY ISSUES:
- list each security issue

📊 COMPLEXITY:
- list functions that are too complex

✅ SUGGESTIONS:
- list each fix with example code"""
            },
            {
                "role": "user",
                "content": f"CODE:\n{code}\n\nLINTER:\n{linter_output}\n\nCOMPLEXITY:\n{complexity_output}"
            }
        ]
    )

    ai_feedback = response.choices[0].message.content
    print(ai_feedback)

    report_name = save_report(
        filepath, language,
        linter_output, complexity_output, ai_feedback
    )
    print(f"\n💾 Report saved to: {report_name}")

    save_review(
        filename=os.path.basename(filepath),
        ai_feedback=ai_feedback,
        flake8_output=linter_output,
        complexity_output=complexity_output
    )