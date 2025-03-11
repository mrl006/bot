import logging
import asyncio
from aiogram import Router
from aiogram.types import Message
import ai_services  

router = Router()

@router.message()
async def ai_private_response(message: Message):
    """Handles private chat responses for client inquiries and pricing."""
    user_message = message.text.strip()
    user_id = message.from_user.id  

    if not user_message:
        return  

    # ✅ Simulate typing delay
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    await asyncio.sleep(2)

    # ✅ Generate AI response (detailed for private chat)
    ai_reply = ai_services.get_long_ai_response(user_message)
    await message.answer(ai_reply)
