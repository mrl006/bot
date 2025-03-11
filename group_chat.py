import logging
import asyncio
from aiogram import Router
from aiogram.types import Message, ChatMemberUpdated, ReactionTypeEmoji
import ai_services  

router = Router()
user_last_message_time = {}  # ✅ Prevent spam

# ✅ Keywords for design topics
DESIGN_KEYWORDS = ["design", "logo", "poster", "flyer", "branding", "graphic", "animation", "banner", "motion graphics"]

# ✅ Emoji Reactions
REACTION_MAP = {
    "great": "🔥", "amazing": "🔥", "awesome": "💯", "congratulations": "🎉",
    "thank you": "🙏", "love": "❤️", "happy": "😊", "good job": "👏", "success": "🏆"
}

# ✅ Function to react to important messages
def get_reaction(user_message):
    for word, emoji in REACTION_MAP.items():
        if word in user_message.lower():
            return emoji
    return None

@router.message()
async def ai_group_response(message: Message):
    """Handles AI responses in group chat (only when tagged or about design)."""
    user_message = message.text.strip()
    user_id = message.from_user.id  
    user_mentioned = "@mrlcreation" in user_message or "mrl" in user_message.lower() or "murali" in user_message.lower()

    # ✅ AI responds only when tagged OR when discussing design topics
    is_design_related = any(keyword in user_message.lower() for keyword in DESIGN_KEYWORDS)

    if not user_mentioned and not is_design_related:
        return  # ✅ Ignore unrelated messages

    # ✅ Prevent spam (5-second cooldown)
    current_time = asyncio.get_event_loop().time()
    if user_id in user_last_message_time:
        if current_time - user_last_message_time[user_id] < 5:
            return  
    user_last_message_time[user_id] = current_time

    # ✅ React to important messages
    reaction_emoji = get_reaction(user_message)
    if reaction_emoji:
        try:
            await message.react(ReactionTypeEmoji(emoji=reaction_emoji))
        except Exception as e:
            logging.error(f"Reaction failed: {str(e)}")

    # ✅ Simulate typing delay for realism
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    await asyncio.sleep(2)  # 2-second delay

    # ✅ Generate AI response (short)
    ai_reply = ai_services.get_short_ai_response(user_message, is_group_chat=True)
    await message.answer(ai_reply)
