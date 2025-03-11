import requests
import json
import ai_protection
import logging
from functools import lru_cache
from config import GROQ_API_KEY, API_URL, MODEL_NAME  # ✅ Load model from config.py

# ✅ Configure logging for debugging
logging.basicConfig(level=logging.INFO)

# ✅ Load instructions.json for AI restrictions
instructions_file = "instructions.json"

def load_instructions():
    """Loads instructions.json to get AI restrictions and responses."""
    try:
        with open(instructions_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

instructions = load_instructions()

@lru_cache(maxsize=100)  # ✅ Cache responses to reduce API calls
def get_ai_response(user_message):
    """Fetch AI-generated responses while following restrictions."""

    # ✅ Step 1: Check if the message contains restricted topics
    for restricted_topic in instructions.get("restricted_topics", []):
        if restricted_topic.lower() in user_message.lower():
            return "🚫 *Sorry, I can't discuss that topic.*"

    # ✅ Step 2: Check if there's a pre-defined response in default_responses
    for key, response in instructions.get("default_responses", {}).items():
        if key.replace("_", " ") in user_message.lower():
            return response  # ✅ Return the pre-defined response

    # ✅ Step 3: If no restrictions, proceed with AI API call
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": MODEL_NAME,  # ✅ Now using the correct Groq model
        "messages": [{"role": "user", "content": user_message}],
        "temperature": 0.7,
        "max_tokens": 1024,
        "top_p": 1,
        "stream": False,  # ✅ Set to False for a normal response
        "stop": None
    }

    try:
        logging.info(f"🔍 Sending AI request to: {API_URL}")
        logging.info(f"📡 Request Data: {json.dumps(data, indent=2)}")

        response = requests.post(API_URL, json=data, headers=headers, timeout=10)
        response_json = response.json()
        
        logging.info(f"✅ API Response: {json.dumps(response_json, indent=2)}")

        if "choices" in response_json and response_json["choices"]:
            return response_json["choices"][0]["message"]["content"]
        else:
            return "⚠️ *AI is currently unavailable. Please check API configuration.*"
    
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ AI connection error: {str(e)}")
        return f"⚠️ *AI connection error: {str(e)}*"
