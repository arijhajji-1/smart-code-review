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
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()

# Allow React frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/review")
async def review_code(file: UploadFile = File(...)):
    # Save uploaded file to a temp location
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    # Run tools
    language, linter_output, complexity_output = run_tools(tmp_path)
    code = content.decode("utf-8")

    # Stream the AI response
    def stream_review():
        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": f"""You are an expert {language} code reviewer.
You will receive:
1. The source code
2. Static analysis output

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
            ],
            stream=True
        )

        full_response = ""
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                full_response += delta
                yield delta

        # Save to memory after streaming completes
        save_review(
            filename=file.filename,
            ai_feedback=full_response,
            flake8_output=linter_output,
            complexity_output=complexity_output
        )

        # Cleanup temp file
        os.unlink(tmp_path)

    return StreamingResponse(stream_review(), media_type="text/plain")


@app.get("/search")
async def search_reviews_endpoint(q: str):
    from core.memory import search_reviews

    relevant = search_reviews(q, n_results=3)

    if relevant == "No matching reviews found.":
        return {"results": "No matching reviews found."}

    # Pass through LLM for a smart answer
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
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