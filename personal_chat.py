import logging
import asyncio
from aiogram import Router
from aiogram.types import Message
import ai_services
import pricing
from ai_memory import remember_user_preference

router = Router()

@router.message()
async def ai_private_response(message: Message):
    """Handles private chat responses for pricing."""
    user_message = message.text.strip()
    user_id = str(message.from_user.id)

    if "price" in user_message.lower():
        await message.answer("What type of design do you need? (Logo, Branding, Poster, Flyer)")
        return

    if any(word in user_message.lower() for word in ["logo", "branding", "poster", "flyer"]):
        await message.answer("What complexity do you need? (Simple, Medium, Complex)")
        return

    words = user_message.lower().split()
    if len(words) == 2:
        design_type, complexity = words
        price = pricing.calculate_design_price(design_type, complexity)
        await message.answer(price)
        remember_user_preference(user_id, f"{complexity} {design_type}")
        return

    ai_reply = ai_services.get_long_ai_response(user_message)
    await message.answer(ai_reply)
