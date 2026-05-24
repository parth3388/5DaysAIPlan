"""
Single-Agent AI Chatbot Backend
================================
FastAPI backend with OpenAI integration.
One agent. One system prompt. One clean response.
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv

# ── Load environment variables from .env ──────────────────────────────────────
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set. Please add it to the .env file.")

# ── OpenAI client (OpenRouter) ────────────────────────────────────────────────
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# ── Single-Agent System Prompt ────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "You are a helpful single-agent AI chatbot for students. "
    "Explain concepts in simple English, give practical examples, "
    "and keep answers clear, short, and interview-friendly."
)

# ── FastAPI app ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="Single-Agent AI Chatbot API",
    description="A beginner-friendly FastAPI backend powered by OpenAI GPT.",
    version="1.0.0",
)

# ── CORS Middleware (allows Streamlit frontend to call this API) ───────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Pydantic Schemas ──────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="User's message to the chatbot")

class ChatResponse(BaseModel):
    response: str = Field(..., description="AI agent's response")

# ── Health Check ──────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Single-Agent Chatbot API is running."}

# ── Chat Endpoint ─────────────────────────────────────────────────────────────
@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
def chat(request: ChatRequest):
    """
    Single-Agent Workflow:
    1. Receive user message.
    2. Inject system prompt (agent persona).
    3. Call OpenAI GPT API via OpenRouter.
    4. Return the agent's response.
    """
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": request.message},
            ],
            temperature=0.7,
            max_tokens=800,
        )
        agent_reply = completion.choices[0].message.content.strip()
        return ChatResponse(response=agent_reply)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"OpenAI API error: {str(e)}"
        )