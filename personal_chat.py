import logging
import asyncio
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import ai_services  # ✅ Import AI response module

# ✅ Enable logging for debugging
logging.basicConfig(level=logging.INFO)

router = Router()
user_last_message_time = {}  # ✅ Dictionary to track message cooldowns

# ✅ AI RESPONSE HANDLER FOR PRIVATE CHAT
@router.message()
async def ai_private_response(message: Message):
    user_message = message.text.strip()
    user_id = message.from_user.id  
    current_time = asyncio.get_event_loop().time()

    if not user_message:
        return  

    # ✅ Prevent spam (5-second cooldown per user)
    if user_id in user_last_message_time:
        time_diff = current_time - user_last_message_time[user_id]
        if time_diff < 5:
            logging.info(f"Spam prevented: {message.from_user.username}")
            return

    # ✅ Update last message time
    user_last_message_time[user_id] = current_time

    # ✅ Show "typing..." before responding
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

    # ✅ Log the incoming user message
    logging.info(f"[PRIVATE CHAT] User Message: {user_message}")

    # ✅ Get AI response
    ai_reply = ai_services.get_short_ai_response(user_message, user_mentioned=True)  # ✅ Always treat private chat as direct request

    # ✅ Send the AI's response
    await message.answer(ai_reply, parse_mode="Markdown")

    # ✅ Log AI response for debugging
    logging.info(f"[PRIVATE CHAT] AI Response Sent: {ai_reply}")
