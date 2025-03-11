import requests
import json
import ai_protection
import logging
from functools import lru_cache
from config import GROQ_API_KEY, API_URL, MODEL_NAME

# ✅ Configure logging
logging.basicConfig(level=logging.INFO)

# ✅ Load instructions.json
instructions_file = "instructions.json"

def load_instructions():
    """Loads instructions.json to get AI restrictions and responses."""
    try:
        with open(instructions_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

instructions = load_instructions()

# ✅ Manually update availability status (You can integrate a live update feature)
MURALI_AVAILABLE = True  # Change to False when unavailable

# ✅ Predefined responses to recognize when people mention you
PREDEFINED_RESPONSES = {
    "who are you": "🤖 **I am MRL AI, an AI-powered assistant ready to help with your requests!**",
    "what is your name": "🤖 **I am MRL AI, here to assist you with all your needs!**",
    "is murali available": "🟢 **Murali is currently available! How can I assist you on his behalf?**" if MURALI_AVAILABLE else "🔴 **Murali is currently unavailable, but I can take a message or assist you right now. Let me know what you need!**",
    "where is murali": "📍 **Murali might be busy at the moment. Would you like me to take a message or help you with anything in the meantime?**",
    "can i talk to murali": "📩 **I can check if Murali is available. What would you like to discuss?**",
}

@lru_cache(maxsize=100)  # ✅ Cache responses to reduce API calls
def get_ai_response(user_message, user_mentioned=False):
    """Fetch AI-generated responses while ensuring the bot correctly understands user intent."""

    # ✅ Step 1: If the user mentioned Murali or MRL, handle availability
    if user_mentioned:
        if "available" in user_message.lower():
            return PREDEFINED_RESPONSES["is murali available"]
        elif "talk to murali" in user_message.lower():
            return PREDEFINED_RESPONSES["can i talk to murali"]
        elif "where is murali" in user_message.lower():
            return PREDEFINED_RESPONSES["where is murali"]

    # ✅ Step 2: Check if message has a predefined response
    for key, response in PREDEFINED_RESPONSES.items():
        if key in user_message.lower():
            return response  

    # ✅ Step 3: If it's a client request, ask clarifying questions before calling AI
    if "need" in user_message.lower() or "looking for" in user_message.lower() or "want" in user_message.lower():
        return "🔍 **Can you provide more details about what you need? I'm here to help!**"

    # ✅ Step 4: If no predefined response, proceed with AI API call
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": user_message}],
        "temperature": 0.7,
        "max_tokens": 1024,
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
            return "⚠️ **I'm currently unable to process your request. Please try again later.**"
    
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ AI connection error: {str(e)}")
        return f"⚠️ **AI connection error: {str(e)}**"
