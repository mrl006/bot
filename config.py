import os
from dotenv import load_dotenv

# ✅ Load environment variables from .env file
load_dotenv()

# ✅ Secure API keys
API_TOKEN = os.getenv("API_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
API_URL = os.getenv("API_URL")
MODEL_NAME = os.getenv("MODEL_NAME")  # ✅ AI Model for Groq

# ✅ Database Path
DB_PATH = os.getenv("DB_PATH")

# ✅ Owner Information
OWNER_USERNAME = os.getenv("OWNER_USERNAME")

# ✅ Supported Languages (Loaded from .env)
LANGUAGES = {
    "en": os.getenv("LANG_EN"),
    "es": os.getenv("LANG_ES"),
    "fr": os.getenv("LANG_FR"),
    "de": os.getenv("LANG_DE"),
}

# ✅ Crypto Wallets (Loaded Securely from .env)
CRYPTO_WALLETS = {
    "USDT_BEP20": os.getenv("USDT_BEP20"),
    "BNB_BEP20": os.getenv("BNB_BEP20"),
    "SOLANA": os.getenv("SOLANA"),
    "ETH_ERC20": os.getenv("ETH_ERC20"),
}
