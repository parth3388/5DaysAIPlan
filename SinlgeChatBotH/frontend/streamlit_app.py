"""
Single-Agent AI Chatbot — Streamlit Frontend
=============================================
A clean, professional chat UI that calls the FastAPI /chat endpoint.
"""

import time
import requests
import streamlit as st

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Single-Agent AI Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Backend URL ───────────────────────────────────────────────────────────────
BACKEND_URL = "http://127.0.0.1:8000/chat"

# ── Custom CSS — sleek dark theme ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Sora:wght@300;400;600;700&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
    background-color: #0d0f14;
    color: #e8eaf0;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 820px; }

/* ── Header ── */
.chat-header {
    text-align: center;
    padding: 2rem 0 1rem;
}
.chat-header h1 {
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    font-size: 2.1rem;
    color: #ffffff;
    letter-spacing: -0.02em;
    margin: 0;
}
.chat-header .subtitle {
    font-size: 0.88rem;
    color: #7a7f94;
    margin-top: 0.35rem;
    font-weight: 300;
}
.agent-badge {
    display: inline-block;
    background: linear-gradient(135deg, #1a1f2e, #232840);
    border: 1px solid #2e3455;
    border-radius: 20px;
    padding: 0.25rem 0.85rem;
    font-size: 0.75rem;
    color: #7c9fff;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.04em;
    margin-top: 0.6rem;
}

/* ── Chat bubbles ── */
.msg-row {
    display: flex;
    margin-bottom: 1.2rem;
    animation: fadeUp 0.3s ease;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}

.msg-row.user  { justify-content: flex-end; }
.msg-row.agent { justify-content: flex-start; }

.bubble {
    max-width: 78%;
    padding: 0.85rem 1.1rem;
    border-radius: 18px;
    font-size: 0.92rem;
    line-height: 1.65;
    word-wrap: break-word;
}
.bubble.user {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: #fff;
    border-bottom-right-radius: 4px;
    box-shadow: 0 4px 18px rgba(37,99,235,0.35);
}
.bubble.agent {
    background: #1a1e2d;
    color: #dde1f0;
    border: 1px solid #252c42;
    border-bottom-left-radius: 4px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.4);
}

.sender-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    margin-bottom: 0.25rem;
    text-transform: uppercase;
}
.sender-label.user  { text-align: right; color: #6b8cff; }
.sender-label.agent { color: #4ade80; }

.msg-col { display: flex; flex-direction: column; }
.msg-col.user  { align-items: flex-end; }
.msg-col.agent { align-items: flex-start; }

/* ── Divider ── */
.chat-divider {
    border: none;
    border-top: 1px solid #1e2235;
    margin: 1.5rem 0;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #10131c;
    border-right: 1px solid #1e2235;
}
.sidebar-section h3 {
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #4a5070;
    margin-bottom: 0.5rem;
}
.sidebar-tag {
    display: inline-block;
    background: #1a1f30;
    border: 1px solid #252c42;
    border-radius: 6px;
    padding: 0.2rem 0.6rem;
    font-size: 0.78rem;
    color: #7c9fff;
    font-family: 'JetBrains Mono', monospace;
    margin: 0.2rem 0.2rem 0 0;
}
.workflow-step {
    display: flex;
    align-items: flex-start;
    gap: 0.65rem;
    margin-bottom: 0.7rem;
}
.step-num {
    flex-shrink: 0;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: #fff;
    font-size: 0.68rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
}
.step-text {
    font-size: 0.82rem;
    color: #9aa0bb;
    line-height: 1.5;
    padding-top: 2px;
}

/* ── Input area ── */
.stTextArea textarea {
    background: #13161f !important;
    border: 1px solid #252c42 !important;
    border-radius: 12px !important;
    color: #e8eaf0 !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 0.92rem !important;
    resize: none !important;
}
.stTextArea textarea:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 2px rgba(37,99,235,0.2) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.55rem 1.5rem !important;
    width: 100% !important;
    transition: opacity 0.15s ease, transform 0.1s ease !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []  # list of {"role": "user"|"agent", "content": str}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 Agent Info")
    st.markdown("""
<div class="sidebar-section">
  <h3>Stack</h3>
  <span class="sidebar-tag">FastAPI</span>
  <span class="sidebar-tag">Streamlit</span>
  <span class="sidebar-tag">OpenAI</span>
  <span class="sidebar-tag">GPT-4o-mini</span>
</div>
""", unsafe_allow_html=True)

    st.markdown("<hr class='chat-divider'>", unsafe_allow_html=True)

    st.markdown("""
<div class="sidebar-section">
  <h3>Single-Agent Workflow</h3>
  <div class="workflow-step"><div class="step-num">1</div><div class="step-text">User sends a message via Streamlit UI</div></div>
  <div class="workflow-step"><div class="step-num">2</div><div class="step-text">FastAPI validates the request via Pydantic</div></div>
  <div class="workflow-step"><div class="step-num">3</div><div class="step-text">Agent injects the system prompt</div></div>
  <div class="workflow-step"><div class="step-num">4</div><div class="step-text">Calls OpenAI GPT-4o-mini API</div></div>
  <div class="workflow-step"><div class="step-num">5</div><div class="step-text">Returns one final, clean response</div></div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<hr class='chat-divider'>", unsafe_allow_html=True)

    st.markdown("""
<div class="sidebar-section">
  <h3>System Prompt</h3>
</div>
""", unsafe_allow_html=True)
    st.caption(
        "You are a helpful single-agent AI chatbot for students. "
        "Explain concepts in simple English, give practical examples, "
        "and keep answers clear, short, and interview-friendly."
    )

    st.markdown("<hr class='chat-divider'>", unsafe_allow_html=True)

    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="chat-header">
  <h1>🤖 Single-Agent AI Chatbot</h1>
  <div class="subtitle">Powered by FastAPI · OpenAI GPT-4o-mini · Streamlit</div>
  <div class="agent-badge">⬡ SINGLE-AGENT MODE ACTIVE</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='chat-divider'>", unsafe_allow_html=True)

# ── Chat History ──────────────────────────────────────────────────────────────
def render_messages():
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        label = "You" if role == "user" else "AI Agent"
        st.markdown(f"""
<div class="msg-row {role}">
  <div class="msg-col {role}">
    <div class="sender-label {role}">{label}</div>
    <div class="bubble {role}">{content}</div>
  </div>
</div>
""", unsafe_allow_html=True)

render_messages()

# ── Input Area ────────────────────────────────────────────────────────────────
st.markdown("<hr class='chat-divider'>", unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_area(
        label="Your message",
        placeholder="Ask me anything… e.g. What is FastAPI? Explain recursion with an example.",
        height=90,
        label_visibility="collapsed",
        key="user_input_box",
    )
with col2:
    send_clicked = st.button("Send ➤", use_container_width=True)

# ── Handle Send ───────────────────────────────────────────────────────────────
def call_backend(message: str) -> str:
    """POST to FastAPI /chat and return the agent's response."""
    try:
        resp = requests.post(
            BACKEND_URL,
            json={"message": message},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json().get("response", "⚠️ No response field in API reply.")
    except requests.exceptions.ConnectionError:
        return (
            "❌ **Cannot connect to the backend.**\n\n"
            "Make sure the FastAPI server is running:\n"
            "`uvicorn app:app --reload` inside the `backend/` folder."
        )
    except requests.exceptions.Timeout:
        return "⏱️ The request timed out. Please try again."
    except requests.exceptions.HTTPError as e:
        return f"🚫 Backend error: {e.response.status_code} — {e.response.text}"
    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)}"


if send_clicked and user_input.strip():
    # 1. Store user message
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})

    # 2. Call FastAPI with spinner
    with st.spinner("Agent is thinking…"):
        time.sleep(0.2)  # tiny delay for UX feel
        reply = call_backend(user_input.strip())

    # 3. Store agent reply
    st.session_state.messages.append({"role": "agent", "content": reply})

    # 4. Rerun to refresh chat
    st.rerun()

elif send_clicked and not user_input.strip():
    st.warning("Please type a message before sending.")

# ── Empty state hint ──────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
<div style="text-align:center; padding: 2.5rem 0; color: #3a4060;">
  <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">💬</div>
  <div style="font-size: 0.9rem;">Start a conversation — ask about any programming or CS concept!</div>
</div>
""", unsafe_allow_html=True)
