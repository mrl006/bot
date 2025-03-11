import logging
import asyncio
from aiogram import Router
from aiogram.types import Message, ChatMemberUpdated, ReactionTypeEmoji
from aiogram.filters import Command
import ai_services  # ✅ Import AI response module

# ✅ Enable logging for debugging
logging.basicConfig(level=logging.INFO)

router = Router()
user_last_message_time = {}  # ✅ Dictionary to track message cooldowns

# ✅ List of keywords related to design topics
DESIGN_KEYWORDS = ["design", "logo", "poster", "flyer", "branding", "graphic", "animation", "banner", "motion graphics"]

# ✅ FUNCTION TO CHECK IMPORTANT MESSAGES FOR REACTIONS
def get_reaction(user_message):
    """Determine the right emoji reaction based on the message content."""
    reaction_map = {
        "great": "🔥",
        "amazing": "🔥",
        "congratulations": "🎉",
        "sad": "💔",
        "sorry": "😢",
        "awesome": "💯",
        "wow": "🤩",
        "heartbreaking": "💔",
        "love": "❤️",
        "thank you": "🙏",
        "happy": "😊",
        "good job": "👏",
        "success": "🏆",
        "bad news": "😞",
        "best": "🌟",
        "worst": "😓"
    }
    
    for word, emoji in reaction_map.items():
        if word in user_message.lower():
            return emoji
    return None

# ✅ AI RESPONSE HANDLER: Only Responds When Tagged OR When User Asks About Design
@router.message()
async def ai_response(message: Message):
    user_message = message.text.strip()
    user_id = message.from_user.id  
    user_name = message.from_user.first_name  
    current_time = asyncio.get_event_loop().time()

    if not user_message:
        return  

    # ✅ Detect if Murali or MRL was explicitly mentioned/tagged
    bot_username = "@mrlcreation"  # Replace with your bot's username
    user_mentioned = bot_username in user_message or "mrl" in user_message.lower() or "murali" in user_message.lower()

    # ✅ Check if message contains design-related words
    is_design_related = any(keyword in user_message.lower() for keyword in DESIGN_KEYWORDS)

    # ✅ Ignore messages if AI is in a group and NOT tagged, unless it's about design
    if message.chat.type in ["group", "supergroup"] and not user_mentioned and not is_design_related:
        logging.info(f"Ignoring untagged, non-design message: {user_message}")
        return  

    # ✅ Prevent spam (5-second cooldown per user)
    if user_id in user_last_message_time:
        time_diff = current_time - user_last_message_time[user_id]
        if time_diff < 5:
            logging.info(f"Spam prevented: {message.from_user.username}")
            return

    # ✅ Update last message time
    user_last_message_time[user_id] = current_time

    # ✅ React to important messages in groups (Removed unsupported `message.react`)
    reaction_emoji = get_reaction(user_message)
    if reaction_emoji:
        try:
            await message.bot.send_message(
                chat_id=message.chat.id,
                text=f"{reaction_emoji}"  # ✅ Sends reaction as a separate message
            )
            logging.info(f"Reacted with {reaction_emoji} to: {user_message}")
        except Exception as e:
            logging.error(f"Failed to react: {str(e)}")

    # ✅ Show "typing..." before responding
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

    # ✅ Log the incoming user message
    logging.info(f"User Message: {user_message}")

    # ✅ Get AI response in SHORT form for group chat
    ai_reply = ai_services.get_short_ai_response(user_message, user_mentioned=user_mentioned)

    # ✅ Send the AI's response
    await message.answer(ai_reply, parse_mode="Markdown")

    # ✅ Log AI response for debugging
    logging.info(f"AI Response Sent: {ai_reply}")

