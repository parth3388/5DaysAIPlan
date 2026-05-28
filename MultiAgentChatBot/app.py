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

st.set_page_config(
    page_title="StudyMate AI",
    page_icon="A",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

*, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html, body, [data-testid="stAppViewContainer"] {
    background: #f8fafc !important;
    color: #1e293b !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background: #f8fafc !important;
}

[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

.block-container {
    padding: 1.5rem 2rem 2rem !important;
    max-width: 900px !important;
    margin: 0 auto;
}

.hero {
    text-align: center;
    padding: 2rem 1rem;
    background: #ffffff;
    border-radius: 18px;
    border: 1px solid #e2e8f0;
    margin-bottom: 1.5rem;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #1e293b;
    line-height: 1.2;
}

.hero-sub {
    font-size: 1rem;
    color: #475569;
    margin-top: 0.5rem;
    font-weight: 400;
}

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
    cursor: default;
    background: #f8fafc;
}

.agent-coding {
    border-color: #bfdbfe;
    color: #1d4ed8;
}

.agent-resume {
    border-color: #bbf7d0;
    color: #047857;
}

.agent-career {
    border-color: #ddd6fe;
    color: #6d28d9;
}

.msg-wrap {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 0.5rem 0;
}

.msg-user {
    align-self: flex-end;
    background: #2563eb;
    color: #ffffff;
    padding: 0.85rem 1.2rem;
    border-radius: 18px 18px 4px 18px;
    max-width: 75%;
    font-size: 0.95rem;
    line-height: 1.6;
}

.msg-ai {
    align-self: flex-start;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    color: #1e293b;
    padding: 1rem 1.2rem;
    border-radius: 18px 18px 18px 4px;
    max-width: 85%;
    font-size: 0.93rem;
    line-height: 1.7;
}

.msg-ai.coding {
    border-left: 3px solid #2563eb;
}

.msg-ai.resume {
    border-left: 3px solid #059669;
}

.msg-ai.career {
    border-left: 3px solid #7c3aed;
}

.msg-ai.general {
    border-left: 3px solid #64748b;
}

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

.badge-coding {
    background: #dbeafe;
    color: #1d4ed8;
}

.badge-resume {
    background: #dcfce7;
    color: #047857;
}

.badge-career {
    background: #ede9fe;
    color: #6d28d9;
}

.badge-general {
    background: #e2e8f0;
    color: #475569;
}

.sidebar-header {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 0.25rem;
}

.active-agent-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 0.75rem 1rem;
    margin: 0.75rem 0;
    font-size: 0.85rem;
}

[data-testid="stChatInput"] textarea {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    color: #1e293b !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stChatInput"] textarea:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 2px rgba(37,99,235,0.15) !important;
}

.stButton>button {
    background: #2563eb !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

.stButton>button:hover {
    background: #1d4ed8 !important;
}

code {
    background: #f1f5f9 !important;
    color: #1e293b !important;
    border-radius: 4px;
    padding: 1px 5px;
}

pre {
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
}

::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: #f1f5f9;
}

::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


AGENT_MAP = {
    "coding": CODING_META,
    "resume": RESUME_META,
    "career": CAREER_META,
    "general": {
        "name": "General Assistant",
        "emoji": "",
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


if "messages" not in st.session_state:
    st.session_state.messages = []

if "active_agent" not in st.session_state:
    st.session_state.active_agent = None

API_KEY = os.getenv("GROQ_API_KEY", "")

if API_KEY:
    initialize_gemini(API_KEY)

if "pending_query" not in st.session_state:
    st.session_state.pending_query = None


with st.sidebar:
    st.markdown('<p class="sidebar-header">StudyMate AI</p>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("**Active Agent**")

    if st.session_state.active_agent:
        meta = AGENT_MAP[st.session_state.active_agent]
        st.markdown(f"""
        <div class="active-agent-box">
            <strong>{meta['name']}</strong><br>
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

    st.markdown("**Agents**")

    for key, meta in AGENT_MAP.items():
        if key == "general":
            continue

        st.markdown(
            f"**{meta['name']}**  \n"
            f"<span style='color:#64748b;font-size:0.8rem'>{meta['description']}</span>",
            unsafe_allow_html=True
        )
        st.write("")

    st.markdown("---")

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.active_agent = None
        st.rerun()

    st.markdown("""
    <div style='color:#64748b;font-size:0.75rem;margin-top:1rem;text-align:center'>
    Powered by Groq · LLaMA 3.3 70B<br>Multi-Agent Architecture
    </div>
    """, unsafe_allow_html=True)


st.markdown("""
<div class="hero">
    <div class="hero-title">StudyMate AI</div>
    <div class="hero-sub">A multi-agent assistant for coding, resumes and career guidance</div>
    <div class="agents-row">
        <div class="agent-card agent-coding">Coding Agent</div>
        <div class="agent-card agent-resume">Resume Agent</div>
        <div class="agent-card agent-career">Career Agent</div>
    </div>
</div>
""", unsafe_allow_html=True)


if not st.session_state.messages:
    st.markdown("""
    <div style='text-align:center;color:#64748b;font-size:0.85rem;margin-bottom:0.5rem'>
    Try asking one of these:
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)

    for i, suggestion in enumerate(SUGGESTIONS):
        with cols[i % 3]:
            if st.button(suggestion, key=f"sug_{i}", use_container_width=True):
                st.session_state.pending_query = suggestion
                st.rerun()


def render_message(msg: dict):
    role = msg["role"]
    content = msg["content"]
    agent = msg.get("agent", "general")

    if role == "user":
        st.markdown(
            f'<div class="msg-user">{content}</div>',
            unsafe_allow_html=True
        )
    else:
        meta = AGENT_MAP.get(agent, AGENT_MAP["general"])
        st.markdown(f"""
        <div class="msg-ai {agent}">
            <div class="agent-badge badge-{agent}">{meta['name']}</div>
            <div>{content}</div>
        </div>
        """, unsafe_allow_html=True)


def get_agent_response(agent: str, query: str, history: list) -> str:
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


if st.session_state.messages:
    st.markdown('<div class="msg-wrap">', unsafe_allow_html=True)

    for msg in st.session_state.messages:
        render_message(msg)

    st.markdown('</div>', unsafe_allow_html=True)


if st.session_state.pending_query:
    query = st.session_state.pending_query
    st.session_state.pending_query = None

    if not API_KEY:
        st.error("GROQ_API_KEY not found. Please add it to your .env file.")
    else:
        st.session_state.messages.append({
            "role": "user",
            "content": query,
            "agent": None
        })

        with st.spinner("Routing your query..."):
            agent = route_query(query, API_KEY)

        st.session_state.active_agent = agent

        with st.spinner(f"{AGENT_MAP[agent]['name']} is thinking..."):
            response = get_agent_response(
                agent,
                query,
                st.session_state.messages[:-1]
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "agent": agent
        })

        st.rerun()


user_input = st.chat_input("Ask me anything about coding, resume or career guidance...")

if user_input:
    if not API_KEY:
        st.error("GROQ_API_KEY not found. Please add it to your .env file.")
    else:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "agent": None
        })

        with st.spinner("Routing your query..."):
            agent = route_query(user_input, API_KEY)

        st.session_state.active_agent = agent

        with st.spinner(f"{AGENT_MAP[agent]['name']} is thinking..."):
            response = get_agent_response(
                agent,
                user_input,
                st.session_state.messages[:-1]
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "agent": agent
        })

        st.rerun()