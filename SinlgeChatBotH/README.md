# 🤖 Single-Agent AI Chatbot
### FastAPI · OpenAI GPT-4o-mini · Streamlit

A beginner-friendly yet professional **single-agent chatbot** built for students.
Ideal for academic submission, interview explanation, and GitHub portfolios.

---

## 📐 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    SINGLE-AGENT WORKFLOW                     │
│                                                             │
│   [User]  ──►  [Streamlit UI]  ──►  POST /chat             │
│                                          │                  │
│                                    [FastAPI Backend]        │
│                                          │                  │
│                              ┌───────────▼──────────────┐  │
│                              │     SINGLE AI AGENT       │  │
│                              │  ┌────────────────────┐   │  │
│                              │  │   System Prompt    │   │  │
│                              │  │ (Student assistant)│   │  │
│                              │  └────────────────────┘   │  │
│                              │           │                │  │
│                              │  ┌────────▼───────────┐   │  │
│                              │  │  OpenAI GPT-4o-mini│   │  │
│                              │  └────────────────────┘   │  │
│                              └───────────────────────────┘  │
│                                          │                  │
│   [User]  ◄──  [Streamlit UI]  ◄──  JSON Response          │
└─────────────────────────────────────────────────────────────┘
```

**Key principle:** One agent. One system prompt. One response. No multi-agent loops.

---

## 📁 Project Structure

```
single-agent-chatbot/
│
├── backend/
│   ├── app.py               ← FastAPI app with /chat endpoint
│   ├── requirements.txt     ← Backend Python dependencies
│   └── .env                 ← Your OpenAI API key (keep secret!)
│
├── frontend/
│   ├── streamlit_app.py     ← Streamlit chat UI
│   └── requirements.txt     ← Frontend Python dependencies
│
└── README.md                ← This file
```

---

## ⚙️ Setup & Run Instructions

### Step 1 — Clone or download the project

```bash
cd single-agent-chatbot
```

---

### Step 2 — Backend Setup

```bash
# Navigate to backend folder
cd backend

# Create and activate a virtual environment (recommended)
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### Step 3 — Configure your OpenAI API Key

Open `backend/.env` and replace the placeholder:

```env
OPENAI_API_KEY=sk-your-real-openai-api-key-here
```

> 🔑 Get your API key at: https://platform.openai.com/api-keys

---

### Step 4 — Start the FastAPI Backend

```bash
# Inside the backend/ folder, with venv activated:
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

✅ Backend is live at: **http://127.0.0.1:8000**
📖 Swagger docs at: **http://127.0.0.1:8000/docs**

---

### Step 5 — Frontend Setup (new terminal)

```bash
# Open a NEW terminal window/tab
cd single-agent-chatbot/frontend

# Create and activate a virtual environment
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### Step 6 — Start the Streamlit Frontend

```bash
streamlit run streamlit_app.py
```

✅ Frontend is live at: **http://localhost:8501**

---

## 🔌 API Reference

### `POST /chat`

**Request body:**
```json
{
  "message": "What is FastAPI?"
}
```

**Response:**
```json
{
  "response": "FastAPI is a modern, fast Python web framework for building APIs..."
}
```

**Test with curl:**
```bash
curl -X POST http://127.0.0.1:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "Explain recursion with an example"}'
```

---

## 🧠 Single-Agent Workflow Explained

| Step | Component | What Happens |
|------|-----------|--------------|
| 1 | Streamlit | User types a message and clicks **Send** |
| 2 | requests  | HTTP POST to `http://127.0.0.1:8000/chat` |
| 3 | FastAPI   | Pydantic validates the JSON body |
| 4 | AI Agent  | System prompt + user message assembled |
| 5 | OpenAI    | GPT-4o-mini generates a completion |
| 6 | FastAPI   | Returns `{"response": "..."}` |
| 7 | Streamlit | Displays the response in chat history |

### Why "single-agent"?
- ✅ **One agent** handles the full conversation turn
- ✅ **One system prompt** sets the agent's persona
- ✅ **One API call** per user message
- ✅ **One response** returned — no chaining, no routing, no sub-agents

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Streamlit 1.41 | Chat UI with session state |
| **HTTP Client** | requests | Frontend → Backend calls |
| **Backend** | FastAPI 0.115 | REST API server |
| **Validation** | Pydantic v2 | Request/response schemas |
| **AI Model** | GPT-4o-mini | Language model |
| **AI SDK** | openai 1.57 | OpenAI Python client |
| **Config** | python-dotenv | Loads `.env` file |
| **Server** | Uvicorn | ASGI server for FastAPI |

---

## 🔒 Security Notes

- Never commit your `.env` file to Git. Add it to `.gitignore`:
  ```
  backend/.env
  backend/venv/
  frontend/venv/
  __pycache__/
  *.pyc
  ```
- In production, restrict CORS `allow_origins` to your frontend's domain.

---

## 💡 Sample Questions to Try

- "What is FastAPI and why is it fast?"
- "Explain recursion with a real-world example"
- "What is the difference between SQL and NoSQL?"
- "How does REST API work? Explain for a beginner"
- "What is a decorator in Python?"

---

## 🎓 About This Project

Built as a **beginner-to-intermediate** showcase demonstrating:
- Clean REST API design with FastAPI
- Input validation using Pydantic models
- OpenAI API integration
- Single-agent AI architecture
- Professional Streamlit UI with session management
- Environment-based configuration with `.env`

Perfect for: academic projects · interview walkthroughs · GitHub portfolios

---

*Made with ❤️ using FastAPI + OpenAI + Streamlit*
