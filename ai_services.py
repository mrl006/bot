import requests
import json
import ai_protection
import logging
from functools import lru_cache
from config import GROQ_API_KEY, API_URL, MODEL_NAME

# ✅ Configure logging
logging.basicConfig(level=logging.INFO)

# ✅ Murali's availability status (Update as needed)
MURALI_AVAILABLE = True  # Change to False when unavailable

# ✅ Short responses for group chats
SHORT_RESPONSES = {
    "who are you": "🤖 MRL AI, here to help!",
    "what is your name": "🤖 MRL AI, your assistant!",
    "is murali available": "🟢 Yes, Murali is around!" if MURALI_AVAILABLE else "🔴 Murali is currently busy.",
    "where is murali": "📍 Murali will be here soon!",
    "can i talk to murali": "📩 I’ll let him know!",
    "need design": "🎨 Noted! Murali will handle it.",
    "i need a logo": "🖌 Got it! Murali will design it.",
    "need a poster": "📜 Understood! Murali will create it.",
}

@lru_cache(maxsize=100)  # ✅ Cache responses to reduce API calls
def get_short_ai_response(user_message, user_mentioned=False):
    """Provide short AI responses in group chats."""

    # ✅ If the user mentioned Murali, handle availability first
    if user_mentioned:
        if "available" in user_message.lower():
            return SHORT_RESPONSES["is murali available"]
        elif "talk to murali" in user_message.lower():
            return SHORT_RESPONSES["can i talk to murali"]
        elif "where is murali" in user_message.lower():
            return SHORT_RESPONSES["where is murali"]

    # ✅ Check for predefined short responses
    for key, response in SHORT_RESPONSES.items():
        if key in user_message.lower():
            return response  

    # ✅ If the client provides design content, summarize it
    if len(user_message) > 20 and "design" in user_message.lower():
        return "🎨 Noted! Murali will check this."

    # ✅ If no predefined response, proceed with AI API call
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": user_message}],
        "temperature": 0.7,
        "max_tokens": 50,  # ✅ Limit response length
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
            return "⚠️ Try again later."
    
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ AI connection error: {str(e)}")
        return f"⚠️ Connection error."
