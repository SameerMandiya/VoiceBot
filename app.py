import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from google import genai

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = """You are Sameer, engineering student applying for AI roles.
Answer confidently, professionally, concise.

Life story: Final-year Elecrical student, built multiple side projects in ML and web dev. Started with tutorials, moved to shipping real products. Passion for AI grew from curiosity to career goal.

Superpower: fast learner + builder. I pick up new tech in days, ship prototypes in weeks. When I commit to something, I see it through.

Growth areas: system design, ML depth, communication. I focus on execution but want to deepen theoretical foundations and present ideas more clearly.

Misconception: quiet but highly execution focused. People assume introverted means passive. I deliver results.

Boundaries: build projects, push deadlines, constant learning. I work best with clear goals and autonomy."""


class ChatRequest(BaseModel):
    text: str


class ChatResponse(BaseModel):
    text: str


@app.post("/chat", response_model=ChatResponse)
async def chat(body: ChatRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Missing GEMINI_API_KEY in .env")
    user_text = (body.text or "").strip()
    if not user_text:
        raise HTTPException(status_code=400, detail="No text provided")
    client = genai.Client(api_key=api_key)
    full_prompt = f"{SYSTEM_PROMPT}\n\nUser question: {user_text}\n\nYour response:"
    models = ["gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-1.5-flash", "gemini-1.5-pro"]
    last_err = None
    for model in models:
        try:
            response = await asyncio.to_thread(
                client.models.generate_content,
                model=model,
                contents=full_prompt
            )
            reply = (getattr(response, "text", None) or "").strip()
            if not reply and hasattr(response, "candidates") and response.candidates:
                c = response.candidates[0]
                if hasattr(c, "content") and c.content and hasattr(c.content, "parts"):
                    for p in c.content.parts:
                        if hasattr(p, "text") and p.text:
                            reply = (reply + " " + p.text).strip()
                            break
            if reply:
                return ChatResponse(text=reply)
        except HTTPException:
            raise
        except Exception as e:
            last_err = e
            msg = str(e) or ""
            if "429" in msg or "quota" in msg.lower() or "rate" in msg.lower() or "RESOURCE_EXHAUSTED" in msg:
                await asyncio.sleep(3)
                continue
            if "404" in msg or "not found" in msg.lower():
                continue
            raise HTTPException(status_code=500, detail=msg[:200] or "API error")
    if last_err:
        msg = str(last_err) or ""
        if "429" in msg or "quota" in msg.lower() or "RESOURCE_EXHAUSTED" in msg:
            return ChatResponse(
                text="I'm temporarily busy due to high demand. Please wait about a minute and try again."
            )
    raise HTTPException(
        status_code=503,
        detail="Service busy. Wait 1 min, then try again."
    )


@app.get("/")
async def root():
    return FileResponse(BASE_DIR / "index.html")


@app.get("/health")
async def health():
    return {"status": "ok"}
