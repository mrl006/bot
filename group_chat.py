import logging
import asyncio
from aiogram import Router
from aiogram.types import Message, ReactionTypeEmoji
import ai_services  

router = Router()
user_last_message_time = {}

DESIGN_KEYWORDS = ["design", "logo", "poster", "flyer", "branding", "graphic", "animation", "banner", "motion graphics"]

REACTION_MAP = {
    "great": "🔥", "amazing": "🔥", "awesome": "💯", "congratulations": "🎉",
    "thank you": "🙏", "love": "❤️", "happy": "😊", "good job": "👏", "success": "🏆"
}

def get_reaction(user_message):
    for word, emoji in REACTION_MAP.items():
        if word in user_message.lower():
            return emoji
    return None

@router.message()
async def ai_group_response(message: Message):
    """Handles AI responses in group chat (only when tagged or about design)."""
    user_message = message.text.strip()
    user_mentioned = "@mrlcreation" in user_message or "mrl" in user_message.lower() or "murali" in user_message.lower()
    is_design_related = any(keyword in user_message.lower() for keyword in DESIGN_KEYWORDS)

    if not user_mentioned and not is_design_related:
        return  # ✅ Ignore unrelated messages

    reaction_emoji = get_reaction(user_message)
    if reaction_emoji:
        try:
            await message.react(ReactionTypeEmoji(emoji=reaction_emoji))
        except Exception as e:
            logging.error(f"Reaction failed: {str(e)}")

    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    await asyncio.sleep(2)

    # ✅ Instead of listing everything, give a **short response**
    if "design" in user_message.lower():
        ai_reply = "🎨 Noted! What kind of design do you need? (Logo, Poster, Branding?)"
    elif "where is mrl" in user_message.lower():
        ai_reply = "🔹 MRL will be available shortly!"
    else:
        ai_reply = ai_services.get_short_ai_response(user_message, is_group_chat=True)

    await message.answer(ai_reply)
