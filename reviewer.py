import os
import sys
import subprocess
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
from memory import save_review

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- TOOL 1: Read the file ---
def read_code_file(filepath):
    with open(filepath, "r") as f:
        return f.read()

# --- TOOL 2: Run flake8 linter ---
def run_flake8(filepath):
    result = subprocess.run(
        ["flake8", filepath],
        capture_output=True,
        text=True
    )
    output = result.stdout.strip()
    return output if output else "No flake8 issues found."

# --- TOOL 3: Run radon complexity ---
def run_radon(filepath):
    result = subprocess.run(
        ["radon", "cc", filepath, "-s", "-a"],
        capture_output=True,
        text=True
    )
    output = result.stdout.strip()
    return output if output else "No complexity issues found."

# --- TOOL 4: Save report to file ---
def save_report(filepath, flake8_output, complexity_output, ai_feedback):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = os.path.basename(filepath)
    report_name = f"report_{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    report = f"""
AI CODE REVIEW REPORT
=====================
File    : {filename}
Date    : {timestamp}

--- FLAKE8 LINTER ---
{flake8_output}

--- COMPLEXITY ANALYSIS ---
{complexity_output}

--- AI REVIEW ---
{ai_feedback}
"""
    with open(report_name, "w", encoding="utf-8") as f:
        f.write(report.strip())

    return report_name

# --- AGENT ---
def review_code(filepath):
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        sys.exit(1)

    print(f"📂 Reading {filepath}...")
    code = read_code_file(filepath)

    print("🔍 Running flake8 linter...")
    linter_output = run_flake8(filepath)
    print(f"{linter_output}\n")

    print("📊 Running complexity analysis...")
    complexity_output = run_radon(filepath)
    print(f"{complexity_output}\n")

    print("🤖 Sending everything to AI...\n")
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are an expert Python code reviewer.
You will receive:
1. The raw source code
2. Real flake8 linter output
3. Radon complexity scores (A=simple, F=very complex)

Use ALL THREE to give a complete review in this format:

🐛 BUGS & ERRORS:
- list each bug with line number

⚠️ BAD PRACTICES:
- list each bad practice

🔒 SECURITY ISSUES:
- list each security issue

📊 COMPLEXITY:
- list functions that are too complex and why

✅ SUGGESTIONS:
- list each fix with example code where helpful"""
            },
            {
                "role": "user",
                "content": f"CODE:\n{code}\n\nFLAKE8:\n{linter_output}\n\nCOMPLEXITY:\n{complexity_output}"
            }
        ]
    )

    ai_feedback = response.choices[0].message.content
    print(ai_feedback)

    # Save to file
    report_name = save_report(filepath, linter_output, complexity_output, ai_feedback)
    print(f"\n💾 Report saved to: {report_name}")

    # Save to vector memory
    save_review(
        filename=os.path.basename(filepath),
        ai_feedback=ai_feedback,
        flake8_output=linter_output,
        complexity_output=complexity_output
    )

# --- Run: accept any file as argument ---
if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "sample_code.py"
    review_code(target)


