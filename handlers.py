import logging
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import ai_services  # ✅ Import AI response module

# ✅ Enable logging for debugging
logging.basicConfig(level=logging.INFO)

router = Router()

# 🎉 START COMMAND: Welcomes the user
@router.message(Command("start"))
async def send_welcome(message: Message):
    welcome_text = (
        "👋 *Welcome to MRL AI Assistant!* 🚀\n\n"
        "💡 I can help you with:\n"
        "📌 *Design Pricing*\n"
        "📌 *AI-Powered Services*\n"
        "📌 *Crypto Transactions*\n\n"
        "🔹 Use /pricing to check design prices.\n"
        "🔹 Use /contact to reach MRL Creation.\n\n"
        "✨ *Let's get started!* ✨"
    )
    await message.answer(welcome_text, parse_mode="Markdown")

# 💬 AI RESPONSE HANDLER: Handles all text messages
@router.message()
async def ai_response(message: Message):
    user_message = message.text.strip()

    if not user_message:
        return  # Ignore empty messages

    # ✅ FIX: Use send_chat_action() instead of answer_chat_action()
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

    ai_reply = ai_services.get_ai_response(user_message)  # ✅ Send message to AI
    await message.answer(ai_reply, parse_mode="Markdown")  # ✅ Reply to user
