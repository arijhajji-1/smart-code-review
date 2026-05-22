import os
import tempfile
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from groq import Groq
from core.tools import run_tools
from core.memory import save_review

load_dotenv()

def get_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/review")
async def review_code(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    language, linter_output, complexity_output = run_tools(tmp_path)
    code = content.decode("utf-8")

    def stream_review():
        stream = get_client().chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=800,
            messages=[
                {
                    "role": "system",
                    "content": f"""You are an expert {language} code reviewer.
Be concise. Review in this format:

🐛 BUGS: list each bug with line number
⚠️ BAD PRACTICES: list each bad practice
🔒 SECURITY: list each security issue
📊 COMPLEXITY: list complex functions
✅ FIXES: list each fix

Keep each point to one line."""
                },
                {
                    "role": "user",
                    "content": f"CODE:\n{code}\n\nLINTER:\n{linter_output}\n\nCOMPLEXITY:\n{complexity_output}"
                }
            ],
            stream=True
        )

        full_response = ""
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                full_response += delta
                yield delta

        save_review(
            filename=file.filename,
            ai_feedback=full_response,
            flake8_output=linter_output,
            complexity_output=complexity_output
        )

        os.unlink(tmp_path)

    return StreamingResponse(stream_review(), media_type="text/plain")


@app.get("/search")
async def search_reviews_endpoint(q: str):
    from core.memory import search_reviews

    relevant = search_reviews(q, n_results=3)

    if relevant == "No matching reviews found.":
        return {"results": "No matching reviews found."}

    response = get_client().chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=500,
        messages=[
            {
                "role": "system",
                "content": """You are a helpful assistant that answers questions
about past code reviews. You will receive raw review data from memory.

STRICT RULES:
- Only answer based on files directly relevant to the question
- If the user asks about a specific file, ONLY talk about that file
- If no relevant data exists for the asked file, say so clearly
- Never mention unrelated files
- Give a clear, concise, human-readable answer"""
            },
            {
                "role": "user",
                "content": f"QUESTION: {q}\n\nRELEVANT REVIEWS FROM MEMORY:\n{relevant}"
            }
        ]
    )

    return {"results": response.choices[0].message.content}


@app.get("/health")
async def health():
    return {"status": "ok"}