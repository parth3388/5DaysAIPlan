"""
gemini_client.py  (now powered by Groq)
-----------------------------------------
Centralized Groq API client used by all agents.
Handles initialization, prompt building, and error handling.
"""

from groq import Groq
from typing import Optional

_client: Optional[Groq] = None


def initialize_gemini(api_key: str) -> bool:
    """Initialize the Groq client with the provided API key. Returns True on success."""
    global _client
    try:
        _client = Groq(api_key=api_key)
        return True
    except Exception:
        return False


def generate_response(
    system_prompt: str,
    user_query: str,
    chat_history: Optional[list] = None,
    model_name: str = "llama-3.3-70b-versatile",
) -> str:
    """
    Generate a response from Groq given a system prompt and user query.

    Args:
        system_prompt: The agent's persona/instruction prompt.
        user_query:    The current user message.
        chat_history:  List of dicts [{role: 'user'|'model', content: str}]
        model_name:    Groq model to use (default: llama-3.3-70b-versatile).

    Returns:
        The generated text response as a string.
    """
    global _client
    if _client is None:
        return "⚠️ **Not Initialized**: Groq client is not initialized. Please check your API key."

    try:
        # Build messages list
        messages = [{"role": "system", "content": system_prompt}]

        if chat_history:
            for msg in chat_history:
                role = msg["role"]
                # Normalize 'model' role to 'assistant' for Groq
                if role == "model":
                    role = "assistant"
                messages.append({"role": role, "content": msg["content"]})

        messages.append({"role": "user", "content": user_query})

        response = _client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.7,
            max_tokens=2048,
        )
        return response.choices[0].message.content

    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "invalid_api_key" in error_msg.lower() or "authentication" in error_msg.lower():
            return "⚠️ **Invalid API Key**: Please check your Groq API key in the sidebar."
        elif "429" in error_msg or "rate_limit" in error_msg.lower():
            return "⚠️ **Rate Limited**: Too many requests. Please wait a moment and try again."
        elif "503" in error_msg or "unavailable" in error_msg.lower():
            return "⚠️ **Service Unavailable**: Groq is temporarily unavailable. Please try again shortly."
        else:
            return f"⚠️ **Error**: Something went wrong. Details: {error_msg}"
