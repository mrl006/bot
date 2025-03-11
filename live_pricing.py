import json
import os

def get_live_pricing():
    instructions_file = "instructions.json"

    # 🛠 Check if file exists before loading
    if not os.path.exists(instructions_file):
        return "❌ *Pricing data unavailable.* Please try again later."

    try:
        with open(instructions_file, "r") as file:
            instructions = json.load(file)

        discount = instructions.get("pricing_discount", 30) / 100  # Default to 30% 🔥

        # 💰 Base pricing for different plans
        base_prices = {
            "Basic": 100,
            "Standard": 200,
            "Premium": 300
        }
        discounted_prices = {k: v * (1 - discount) for k, v in base_prices.items()}

        # 📊 Generate the pricing response with markdown formatting
        pricing_details = (
            f"💰 **Exclusive Design Pricing (-{discount * 100:.0f}% OFF)**\n\n"
            f"🎨 **Basic Package** – ~~${base_prices['Basic']}~~ ➝ **${discounted_prices['Basic']:.2f}**\n"
            f"🔥 **Standard Package** – ~~${base_prices['Standard']}~~ ➝ **${discounted_prices['Standard']:.2f}**\n"
            f"🚀 **Premium Package** – ~~${base_prices['Premium']}~~ ➝ **${discounted_prices['Premium']:.2f}**\n\n"
            f"💳 **Payment Methods:** USDT | BTC | ETH\n"
            f"📩 **Contact:** [@MrlCreation](https://t.me/MrlCreation)"
        )

        return pricing_details

    except (json.JSONDecodeError, KeyError) as e:
        return f"❌ *Error loading pricing data:* {str(e)}"
