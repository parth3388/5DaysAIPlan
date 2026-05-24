"""
app.py - Multi-Agent Student Assistant powered by Gemini API
"""

import streamlit as st
from dotenv import load_dotenv
import os

from utils.gemini_client import initialize_gemini
from agents.router_agent import route_query
from agents.coding_agent import get_coding_response, AGENT_META as CODING_META
from agents.resume_agent import get_resume_response, AGENT_META as RESUME_META
from agents.career_agent import get_career_response, AGENT_META as CAREER_META

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="StudyMate AI – Multi-Agent Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #080c14 !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stAppViewContainer"] { background: #080c14 !important; }
[data-testid="stSidebar"] { background: #0d1220 !important; border-right: 1px solid #1e293b !important; }
[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding: 1.5rem 2rem 2rem !important; max-width: 900px !important; margin: 0 auto; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 2rem;
    background: linear-gradient(135deg, #0f172a 0%, #1a1040 50%, #0f172a 100%);
    border-radius: 20px;
    border: 1px solid #1e293b;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(99,102,241,0.18) 0%, transparent 65%);
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(135deg, #6366f1, #a78bfa, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
}
.hero-sub {
    font-size: 1rem;
    color: #94a3b8;
    margin-top: 0.5rem;
    font-weight: 400;
}

/* ── Agent cards ── */
.agents-row {
    display: flex;
    gap: 0.75rem;
    justify-content: center;
    margin: 1.5rem 0 0.5rem;
    flex-wrap: wrap;
}
.agent-card {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.55rem 1rem;
    border-radius: 50px;
    font-size: 0.82rem;
    font-weight: 600;
    border: 1px solid;
    transition: transform 0.2s, box-shadow 0.2s;
    cursor: default;
}
.agent-card:hover { transform: translateY(-2px); }
.agent-coding  { background: rgba(59,130,246,0.12); border-color: rgba(59,130,246,0.4); color: #93c5fd; }
.agent-resume  { background: rgba(16,185,129,0.12); border-color: rgba(16,185,129,0.4); color: #6ee7b7; }
.agent-career  { background: rgba(139,92,246,0.12); border-color: rgba(139,92,246,0.4); color: #c4b5fd; }

/* ── Chat messages ── */
.msg-wrap { display: flex; flex-direction: column; gap: 1rem; padding: 0.5rem 0; }

.msg-user {
    align-self: flex-end;
    background: linear-gradient(135deg, #4338ca, #6366f1);
    color: #fff;
    padding: 0.85rem 1.2rem;
    border-radius: 18px 18px 4px 18px;
    max-width: 75%;
    font-size: 0.95rem;
    line-height: 1.6;
    box-shadow: 0 4px 15px rgba(99,102,241,0.3);
    animation: fadeUp 0.3s ease;
}

.msg-ai {
    align-self: flex-start;
    background: #111827;
    border: 1px solid #1e293b;
    color: #e2e8f0;
    padding: 1rem 1.2rem;
    border-radius: 18px 18px 18px 4px;
    max-width: 85%;
    font-size: 0.93rem;
    line-height: 1.7;
    animation: fadeUp 0.3s ease;
    position: relative;
}
.msg-ai.coding { border-left: 3px solid #3b82f6; }
.msg-ai.resume { border-left: 3px solid #10b981; }
.msg-ai.career { border-left: 3px solid #8b5cf6; }
.msg-ai.general{ border-left: 3px solid #64748b; }

.agent-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    margin-bottom: 0.6rem;
    letter-spacing: 0.03em;
}
.badge-coding  { background: rgba(59,130,246,0.2);  color: #93c5fd; }
.badge-resume  { background: rgba(16,185,129,0.2);  color: #6ee7b7; }
.badge-career  { background: rgba(139,92,246,0.2);  color: #c4b5fd; }
.badge-general { background: rgba(100,116,139,0.2); color: #94a3b8; }

/* ── Suggested questions ── */
.suggestions {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    margin: 1rem 0 1.5rem;
    justify-content: center;
}
.suggestion-btn {
    background: #111827;
    border: 1px solid #1e293b;
    color: #94a3b8;
    padding: 0.45rem 0.9rem;
    border-radius: 20px;
    font-size: 0.8rem;
    cursor: pointer;
    transition: all 0.2s;
}
.suggestion-btn:hover {
    border-color: #6366f1;
    color: #a5b4fc;
    background: rgba(99,102,241,0.08);
}

/* ── Sidebar ── */
.sidebar-header {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 0.25rem;
}
.status-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    margin-right: 6px;
    animation: pulse 2s infinite;
}
.dot-green  { background: #10b981; }
.dot-red    { background: #ef4444; }
.dot-yellow { background: #f59e0b; }

.active-agent-box {
    background: #111827;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 0.75rem 1rem;
    margin: 0.75rem 0;
    font-size: 0.85rem;
}

/* ── Input ── */
[data-testid="stChatInput"] textarea {
    background: #111827 !important;
    border: 1px solid #1e293b !important;
    color: #e2e8f0 !important;
    border-radius: 14px !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.2) !important;
}

/* Streamlit elements */
.stButton>button {
    background: linear-gradient(135deg, #4338ca, #6366f1) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: opacity 0.2s !important;
}
.stButton>button:hover { opacity: 0.85 !important; }

/* Code blocks */
code { background: #1e293b !important; border-radius: 4px; padding: 1px 5px; }
pre  { background: #0f1729 !important; border: 1px solid #1e293b !important; border-radius: 10px !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0d1220; }
::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #334155; }

/* Animations */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.4; }
}

/* Hide default streamlit elements */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Agent metadata map ────────────────────────────────────────────────────────
AGENT_MAP = {
    "coding":  CODING_META,
    "resume":  RESUME_META,
    "career":  CAREER_META,
    "general": {
        "name": "General Assistant",
        "emoji": "🎓",
        "color": "#64748b",
        "badge_color": "#475569",
        "description": "General student queries",
    },
}

SUGGESTIONS = [
    "How do I reverse a linked list in Python?",
    "Write a resume summary for a CS fresher",
    "Best internships for 2nd year students",
    "Explain recursion with an example",
    "How to make my resume ATS-friendly?",
    "What projects should I build for ML roles?",
]


# ── Session state init ────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []          # [{role, content, agent}]
if "active_agent" not in st.session_state:
    st.session_state.active_agent = None
# Load API key once from .env at startup
API_KEY = os.getenv("GROQ_API_KEY", "")
if API_KEY:
    initialize_gemini(API_KEY)

if "pending_query" not in st.session_state:
    st.session_state.pending_query = None


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="sidebar-header">🎓 StudyMate AI</p>', unsafe_allow_html=True)
    st.markdown("---")

    # Active agent display
    st.markdown("**🤖 Active Agent**")
    if st.session_state.active_agent:
        meta = AGENT_MAP[st.session_state.active_agent]
        st.markdown(f"""
        <div class="active-agent-box">
            {meta['emoji']} <strong>{meta['name']}</strong><br>
            <span style="color:#64748b;font-size:0.78rem">{meta['description']}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="active-agent-box">
            <span style="color:#64748b">Waiting for your first message...</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Agents legend
    st.markdown("**📋 Agents**")
    for key, meta in AGENT_MAP.items():
        if key == "general":
            continue
        st.markdown(f"**{meta['emoji']} {meta['name']}**  \n<span style='color:#64748b;font-size:0.8rem'>{meta['description']}</span>", unsafe_allow_html=True)
        st.write("")

    st.markdown("---")

    # Clear chat
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.active_agent = None
        st.rerun()

    st.markdown("""
    <div style='color:#475569;font-size:0.75rem;margin-top:1rem;text-align:center'>
    Powered by Groq · LLaMA 3.3 70B<br>Multi-Agent Architecture
    </div>
    """, unsafe_allow_html=True)


# ── Main content ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-title">🎓 StudyMate AI</div>
    <div class="hero-sub">Your intelligent multi-agent assistant for coding, resumes & career growth</div>
    <div class="agents-row">
        <div class="agent-card agent-coding">💻 Coding Agent</div>
        <div class="agent-card agent-resume">📄 Resume Agent</div>
        <div class="agent-card agent-career">🚀 Career Agent</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Suggested questions (only when chat is empty) ─────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div style='text-align:center;color:#64748b;font-size:0.85rem;margin-bottom:0.5rem'>
    ✨ Try asking one of these:
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    for i, suggestion in enumerate(SUGGESTIONS):
        with cols[i % 3]:
            if st.button(suggestion, key=f"sug_{i}", use_container_width=True):
                st.session_state.pending_query = suggestion
                st.rerun()


# ── Helper: render a single message ──────────────────────────────────────────
def render_message(msg: dict):
    role = msg["role"]
    content = msg["content"]
    agent = msg.get("agent", "general")

    if role == "user":
        st.markdown(f'<div class="msg-user">{content}</div>', unsafe_allow_html=True)
    else:
        meta = AGENT_MAP.get(agent, AGENT_MAP["general"])
        st.markdown(f"""
        <div class="msg-ai {agent}">
            <div class="agent-badge badge-{agent}">{meta['emoji']} {meta['name']}</div>
            <div>{content}</div>
        </div>
        """, unsafe_allow_html=True)


# ── Helper: get agent response ────────────────────────────────────────────────
def get_agent_response(agent: str, query: str, history: list) -> str:
    # Filter history to only user/model messages (exclude agent key)
    gemini_history = [
        {"role": "user" if m["role"] == "user" else "model", "content": m["content"]}
        for m in history
    ]
    if agent == "coding":
        return get_coding_response(query, gemini_history)
    elif agent == "resume":
        return get_resume_response(query, gemini_history)
    elif agent == "career":
        return get_career_response(query, gemini_history)
    else:
        from utils.gemini_client import generate_response
        return generate_response(
            "You are a helpful student assistant. Answer briefly and helpfully.",
            query,
            gemini_history,
        )


# ── Render chat history ───────────────────────────────────────────────────────
if st.session_state.messages:
    st.markdown('<div class="msg-wrap">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        render_message(msg)
    st.markdown('</div>', unsafe_allow_html=True)


# ── Process pending query (from suggestion buttons) ───────────────────────────
if st.session_state.pending_query:
    query = st.session_state.pending_query
    st.session_state.pending_query = None

    if not API_KEY:
        st.error("⚠️ GROQ_API_KEY not found. Please add it to your .env file.")
    else:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": query, "agent": None})

        with st.spinner("🤔 Routing your query..."):
            agent = route_query(query, API_KEY)

        st.session_state.active_agent = agent

        with st.spinner(f"{AGENT_MAP[agent]['emoji']} {AGENT_MAP[agent]['name']} is thinking..."):
            response = get_agent_response(agent, query, st.session_state.messages[:-1])

        st.session_state.messages.append({"role": "assistant", "content": response, "agent": agent})
        st.rerun()


# ── Chat input ────────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask me anything — coding, resume, or career guidance...")

if user_input:
    if not API_KEY:
        st.error("⚠️ GROQ_API_KEY not found. Please add it to your .env file.")
    else:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input, "agent": None})

        with st.spinner("🤔 Routing your query..."):
            agent = route_query(user_input, API_KEY)

        st.session_state.active_agent = agent

        with st.spinner(f"{AGENT_MAP[agent]['emoji']} {AGENT_MAP[agent]['name']} is thinking..."):
            response = get_agent_response(agent, user_input, st.session_state.messages[:-1])

        st.session_state.messages.append({"role": "assistant", "content": response, "agent": agent})
        st.rerun()
