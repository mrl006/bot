import requests
import json
import logging
from config import GROQ_API_KEY, API_URL, MODEL_NAME

def get_ai_response(user_message, max_tokens):
    """Send AI request to Groq API with dynamic token settings."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": user_message}],
        "temperature": 0.7,
        "max_tokens": max_tokens,  # ✅ Shorter for group, longer for private
        "top_p": 1,
        "stream": False,
        "stop": None
    }

    try:
        response = requests.post(API_URL, json=data, headers=headers, timeout=10)
        response_json = response.json()

        if "choices" in response_json and response_json["choices"]:
            return response_json["choices"][0]["message"]["content"]
        else:
            return "⚠️ AI is unavailable right now. Try again later."
    
    except requests.exceptions.RequestException as e:
        logging.error(f"AI error: {str(e)}")
        return "⚠️ Connection issue. Try again later."

def summarize_content(content):
    """Summarize long user messages related to design."""
    if len(content.split()) > 50:  # ✅ Only summarize if the message is long
        summary_prompt = f"Summarize this design request in one sentence:\n{content}"
        return get_ai_response(summary_prompt, max_tokens=50)
    return content  # ✅ Return original message if short

def get_short_ai_response(user_message, is_group_chat=True):
    """Generate short responses for group chat."""
    return get_ai_response(user_message, max_tokens=30 if is_group_chat else 150)

def get_long_ai_response(user_message):
    """Generate detailed responses for private chat."""
    return get_ai_response(user_message, max_tokens=200)  # ✅ More tokens for private chat
