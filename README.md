# 🤖 AI Code Reviewer

An agentic AI tool that automatically reviews Python code by combining a real linter, complexity analysis, and an LLM — producing detailed, structured feedback reports.

---

## 🧠 How it works

Instead of just asking an AI to "review my code", this tool runs **3 real tools** and feeds all results to the LLM for a richer, more accurate review:

```
Your Python file
      │
      ├── Tool 1: flake8      → finds syntax errors, style violations
      ├── Tool 2: radon        → measures function complexity
      └── Tool 3: Groq LLM    → synthesizes everything into a full report
                                        │
                                        ▼
                              report_yourfile.txt
```

---

## 📋 What the report contains

- 🐛 **Bugs & Errors** — with exact line numbers
- ⚠️ **Bad Practices** — non-pythonic patterns, silent failures
- 🔒 **Security Issues** — hardcoded secrets, unsafe patterns
- 📊 **Complexity Analysis** — functions that are too complex to maintain
- ✅ **Suggestions** — concrete fixes with example code

---

## 🚀 Getting started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/ai-code-reviewer.git
cd ai-code-reviewer
```

### 2. Create a virtual environment

```bash
# Mac/Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install groq flake8 radon python-dotenv
```

### 4. Get a free Groq API key

Sign up at [console.groq.com](https://console.groq.com) → API Keys → Create Key

### 5. Create a `.env` file

```
GROQ_API_KEY=your-key-here
```

### 6. Run the reviewer

```bash
python reviewer.py your_file.py
```

---

## 📁 Project structure

```
ai-code-reviewer/
│
├── reviewer.py        # Main agent — orchestrates all tools
├── sample_code.py     # Example file with intentional bad code
├── .env               # Your API key (never commit this)
├── .gitignore
└── README.md
```

---

## 💡 Example output

```
📂 Reading sample_code.py...
🔍 Running flake8 linter...
sample_code.py:3:1: F811 redefinition of unused 'os' from line 1
sample_code.py:2:1: F401 'sys' imported but unused
...

📊 Running complexity analysis...
F 5:0 calculate - B (7)
F 21:0 process_data - A (3)

🤖 Sending everything to AI...

🐛 BUGS & ERRORS:
- Line 3: duplicate import of os module
- Line 14: division by zero returns None instead of raising ZeroDivisionError
...

💾 Report saved to: report_sample_code.py_20260521_120000.txt
```

---

## 🛠️ Tech stack

| Tool | Role |
|---|---|
| [Groq](https://groq.com) + Llama 3.3 70b | LLM reasoning engine |
| [flake8](https://flake8.pycqa.org) | Static linter |
| [radon](https://radon.readthedocs.io) | Complexity analysis |
| python-dotenv | API key management |

---

## 📚 Concepts demonstrated

- **Agentic AI** — LLM used as a reasoning engine, not just a chatbot
- **Tool use** — multiple real tools run and fed to the LLM as context
- **ReAct pattern** — gather observations (tools) → reason (LLM) → produce output
- **Prompt engineering** — structured system prompt for consistent output format

---

## 📄 License

MIT
