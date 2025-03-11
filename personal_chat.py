import logging
import asyncio
from aiogram import Router
from aiogram.types import Message
import ai_services  

router = Router()

@router.message()
async def ai_private_response(message: Message):
    """Handles AI responses in private chat (detailed responses)."""
    user_message = message.text.strip()

    if not user_message:
        return  

    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    await asyncio.sleep(2)

    # ✅ Get AI response in a detailed form for private chat
    ai_reply = ai_services.get_detailed_ai_response(user_message)
    await message.answer(ai_reply)
