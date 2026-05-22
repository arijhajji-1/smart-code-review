# 🤖 Smart Code Review — Backend

An agentic AI pipeline that automatically reviews code in multiple languages by combining real static analysis tools with an LLM — producing detailed, structured feedback with streaming output.

🖥️ **Frontend repo:** [github.com/arijhajji-1/code-reviewer-ui](https://github.com/arijhajji-1/code-reviewer-ui)

---

## 🧠 Architecture

```
Your code file
      │
      ├── Tool 1: flake8 (Python)     → syntax errors, style violations
      ├── Tool 2: radon (Python)      → cyclomatic complexity
      ├── Tool 3: ESLint (JS/TS)      → linting + best practices
      └── Tool 4: Groq LLM            → synthesizes everything
                    │
                    ├── Streams response word by word
                    ├── Saves report to data/reports/
                    └── Stores embedding in ChromaDB (RAG memory)
```

---

## 🌐 Supported Languages

| Language | Static Analysis | LLM Review |
|---|---|---|
| Python | flake8 + radon | ✅ |
| JavaScript | ESLint | ✅ |
| TypeScript | ESLint | ✅ |
| Java | LLM only | ✅ |
| PHP | LLM only | ✅ |
| C# | LLM only | ✅ |

---

## 📋 What the review contains

- 🐛 **Bugs & Errors** — with exact line numbers
- ⚠️ **Bad Practices** — non-idiomatic patterns, silent failures
- 🔒 **Security Issues** — hardcoded secrets, unsafe patterns
- 📊 **Complexity Analysis** — functions that are too complex
- ✅ **Suggestions** — concrete fixes with example code

---

## 🚀 Getting started

### 1. Clone the repo

```bash
git clone https://github.com/arijhajji-1/smart-code-review.git
cd smart-code-review
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
pip install groq flake8 radon python-dotenv fastapi uvicorn python-multipart chromadb
```

### 4. Install ESLint (for JS/TS support)

```bash
npm install -g eslint
```

### 5. Create a `.env` file

```
GROQ_API_KEY=your-groq-key-here
FRONTEND_URL=http://localhost:5173
```

Get a free Groq key at [console.groq.com](https://console.groq.com)

### 6. Run the API

```bash
uvicorn api:app --reload
```

API runs at `http://localhost:8000`

---

## 📁 Project structure

```
smart-code-review/
│
├── api.py                  # FastAPI backend — streaming + search endpoints
├── main.py                 # CLI multi-turn agent entry point
├── search.py               # CLI semantic search entry point
├── cleanup_memory.py       # Utility to clean ChromaDB
│
├── core/
│   ├── reviewer.py         # Main agent — orchestrates all tools
│   ├── tools.py            # Language detection + linter runners
│   ├── memory.py           # ChromaDB vector memory (RAG)
│   ├── fixer.py            # Auto-fixer agent
│   └── __init__.py
│
├── config/                 # Configuration
├── data/
│   └── samples/            # Example files to review
│
├── .env                    # API keys (never committed)
└── .gitignore
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/review` | Upload a file → streams AI review |
| `GET` | `/search?q=...` | Semantic search over past reviews |
| `GET` | `/health` | Health check |

---

## 🛠️ Tech stack

| Tool | Role |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com) | REST API + streaming |
| [Groq](https://groq.com) + Llama 3.3 70b | LLM reasoning engine |
| [ChromaDB](https://www.trychroma.com) | Vector database (RAG memory) |
| [flake8](https://flake8.pycqa.org) | Python static linter |
| [radon](https://radon.readthedocs.io) | Python complexity analysis |
| ESLint | JavaScript/TypeScript linter |

---

## 📚 Concepts demonstrated

- **Agentic AI** — LLM used as a reasoning engine, not just a chatbot
- **Tool use** — multiple real tools run and fed to the LLM as context
- **ReAct pattern** — gather observations → reason → produce output
- **RAG** — ChromaDB stores review embeddings for semantic search
- **Multi-agent** — reviewer agent + auto-fixer agent
- **Streaming** — real-time token-by-token response via SSE
- **Multi-language** — language detection + appropriate toolchain per language

---

## 📄 License

MIT