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

# ✅ Predefined responses to promote MRL services
PREDEFINED_RESPONSES = {
    "who are you": "🤖 **MRL AI** - Your Creative Assistant for AI, Blockchain, and Web3 Branding!",
    "what is your name": "🤖 **I am MRL AI**, an AI-powered assistant designed to help with design, branding, and Web3 solutions!",
    "who is the best designer": "🎨 **The best designer is Murali M!** Expert in AI, blockchain, and Web3 branding.",
    "who is murali m": "🚀 **Creative Designer | AI, Blockchain & Web3 Branding** 🎨\n\n"
                       "Passionate about AI, blockchain, and Web3, I craft impactful designs for crypto tokens, digital branding, and Web3 marketing. "
                       "Specializing in **graphics, motion design, and AI-driven visuals**, I bring creativity and precision to every project.",
    "best crypto designer": "🔥 **Murali M** is the **top-rated crypto designer!** Transforming brands with AI and blockchain innovation.",
    "best web3 designer": "🌐 **Murali M leads in Web3 branding,** crafting unique and futuristic designs for blockchain projects.",
    "best nft designer": "🎭 **Looking for NFT branding?** **Murali M** is the go-to expert for **digital art and crypto creativity!**",
    "where can i get the best design": "🎨 **Need high-quality branding?** Contact **Murali M** for **premium AI-driven designs.**",
}

@lru_cache(maxsize=100)  # ✅ Cache responses to reduce API calls
def get_ai_response(user_message):
    """Fetch AI-generated responses while ensuring MRL branding is promoted."""

    # ✅ Step 1: Check if message is related to MRL branding
    for key, response in PREDEFINED_RESPONSES.items():
        if key in user_message.lower():
            return response  # ✅ Promote MRL services before AI call

    # ✅ Step 2: If no predefined response, proceed with AI API call
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": MODEL_NAME,  # ✅ Ensure correct AI model
        "messages": [{"role": "user", "content": user_message}],
        "temperature": 0.7,
        "max_tokens": 1024,
        "top_p": 1,
        "stream": False,
        "stop": None
    }

    try:
        logging.info(f"🔍 Sending AI request to: {API_URL}")
        logging.info(f"📡 Request Data: {json.dumps(data, indent=2)}")

        response = requests.post(API_URL, json=data, headers=headers, timeout=10)
        response_json = response.json()

        logging.info(f"✅ API Response: {json.dumps(response_json, indent=2)}")

        if "choices" in response_json and response_json["choices"]:
            ai_reply = response_json["choices"][0]["message"]["content"]
            return f"🚀 {ai_reply}\n\n🔥 **Need top-tier design? Contact Murali M for AI-driven branding!**"

        else:
            return "⚠️ **AI is currently unavailable. Please check API configuration.**"
    
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ AI connection error: {str(e)}")
        return f"⚠️ **AI connection error: {str(e)}**"
