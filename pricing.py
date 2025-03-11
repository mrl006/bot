import json
import os
import logging

# ✅ Configure logging for debugging
logging.basicConfig(level=logging.INFO)

PRICING_FILE = "instructions.json"

def get_live_pricing():
    """Fetches live pricing details with discounts and formats it for display."""
    
    # 🛠 Check if pricing file exists
    if not os.path.exists(PRICING_FILE):
        logging.error("Pricing file missing.")
        return "❌ *Pricing data unavailable.* Please try again later."

    try:
        with open(PRICING_FILE, "r") as file:
            instructions = json.load(file)

        # 🔥 Default discount (30%) if not provided in the JSON file
        discount = instructions.get("pricing_discount", 30) / 100  

        # 💰 Base package pricing
        base_prices = {
            "Basic": 100,
            "Standard": 200,
            "Premium": 300
        }

        # ✅ Apply discount and round prices for better readability
        discounted_prices = {k: round(v * (1 - discount), 2) for k, v in base_prices.items()}

        # 🔹 Available payment methods
        payment_methods = instructions.get("payment_methods", ["USDT", "BTC", "ETH"])
        payment_methods_str = " | ".join(payment_methods)

        # ✅ Generate pricing response
        pricing_details = (
            f"💰 **Exclusive Design Pricing (-{discount * 100:.0f}% OFF)**\n\n"
            f"🎨 **Basic Package** – ~~${base_prices['Basic']}~~ ➝ **${discounted_prices['Basic']}**\n"
            f"🔥 **Standard Package** – ~~${base_prices['Standard']}~~ ➝ **${discounted_prices['Standard']}**\n"
            f"🚀 **Premium Package** – ~~${base_prices['Premium']}~~ ➝ **${discounted_prices['Premium']}**\n\n"
            f"💳 **Payment Methods:** {payment_methods_str}\n"
            f"📩 **Contact:** [@MrlCreation](https://t.me/MrlCreation)"
        )

        return pricing_details

    except json.JSONDecodeError:
        logging.error("Error decoding JSON file.")
        return "❌ *Pricing data is corrupted. Please contact support.*"
    except KeyError as e:
        logging.error(f"Missing key in JSON file: {e}")
        return f"❌ *Error: Missing key in pricing data:* `{e}`"
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return f"❌ *Unexpected error:* `{str(e)}`"
