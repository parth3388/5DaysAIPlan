"""
router_agent.py
---------------
The Router Agent: analyzes the user query and classifies it into
one of the specialized agent categories.
"""

from utils.gemini_client import generate_response

ROUTER_SYSTEM_PROMPT = """You are a query classification expert. Your ONLY job is to classify student queries 
into exactly one of these four categories:

- coding     → programming, code, debugging, syntax, algorithms, web dev, data structures, tech concepts
- resume     → resume, CV, cover letter, ATS, skills section, work experience, job application, professional summary
- career     → internship, job search, career path, interview prep, project ideas, skill development, roadmap, placement
- general    → greetings, thank you, anything that doesn't fit the above categories

Rules:
1. Respond with ONLY the lowercase category label (coding / resume / career / general)
2. Do NOT add any explanation, punctuation, or extra words
3. When in doubt between coding and career, pick the more specific match
"""


def route_query(user_query: str, api_key: str) -> str:
    """
    Classify the user query and return the appropriate agent name.

    Returns one of: 'coding', 'resume', 'career', 'general'
    """
    classification = generate_response(
        system_prompt=ROUTER_SYSTEM_PROMPT,
        user_query=f"Classify this query: {user_query}",
        chat_history=None,
        model_name="llama-3.1-8b-instant",  # Fast Groq model for routing
    ).strip().lower()

    # Sanitize output — only accept valid labels
    valid_labels = {"coding", "resume", "career", "general"}
    
    # Check if response contains any valid label
    for label in valid_labels:
        if label in classification:
            return label

    return "general"
