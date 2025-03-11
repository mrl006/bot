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

# ✅ Predefined responses to ensure AI knows that "MRL" and "Murali" refer to the user
PREDEFINED_RESPONSES = {
    "who are you": "🤖 **I am MRL AI, an AI-powered assistant designed to help manage tasks, answer questions, and assist with conversations.**",
    "what is your name": "🤖 **I am MRL AI, your assistant, ready to help!**",
    "who is murali": "🔥 **Murali is the expert behind MRL Creation. Need to reach out? Let me know how I can assist!**",
    "who is mrl": "🎨 **MRL stands for Murali, a creative mind in branding, design, and digital services. How can I help with that?**",
    "i need to talk to murali": "📩 **Murali is available for discussions. Do you need direct contact or information on services?**",
    "is murali online": "🟢 **Murali might be available. Do you want me to pass a message or assist you in any way?**",
    "how is murali": "😊 **Murali is always focused on creativity! How can I assist you today?**"
}

@lru_cache(maxsize=100)  # ✅ Cache responses to reduce API calls
def get_ai_response(user_message):
    """Fetch AI-generated responses while ensuring responses align with user intent."""

    # ✅ Step 1: Check if message is related to Murali or MRL and respond correctly
    for key, response in PREDEFINED_RESPONSES.items():
        if key in user_message.lower():
            return response  # ✅ AI recognizes MRL & Murali correctly

    # ✅ Step 2: If no predefined response, proceed with AI API call
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
