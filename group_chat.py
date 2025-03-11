import logging
import asyncio
from aiogram import Router
from aiogram.types import Message, ReactionTypeEmoji
import ai_services  # ✅ Import AI response module

# ✅ Enable logging for debugging
logging.basicConfig(level=logging.INFO)

router = Router()
user_last_message_time = {}  # ✅ Dictionary to track message cooldowns
chat_history = {}  # ✅ Stores recent chat history per group

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

# ✅ FUNCTION TO ANALYZE CHAT CONTEXT
def is_chat_relevant(chat_id):
    """Checks if previous messages in the chat are related to design, branding, or Murali."""
    if chat_id not in chat_history:
        return False
    
    last_messages = chat_history[chat_id][-5:]  # ✅ Analyze last 5 messages
    combined_text = " ".join(last_messages).lower()

    # ✅ Check if any recent messages contain design-related keywords
    if any(keyword in combined_text for keyword in DESIGN_KEYWORDS):
        return True
    
    # ✅ Check if recent messages mention Murali, MRL, or the bot name
    if "mrl" in combined_text or "murali" in combined_text or "@mrlcreation" in combined_text:
        return True
    
    return False

# ✅ AI RESPONSE HANDLER FOR GROUP CHATS
@router.message()
async def ai_group_response(message: Message):
    user_message = message.text.strip()
    user_id = message.from_user.id  
    chat_id = message.chat.id
    current_time = asyncio.get_event_loop().time()

    if not user_message:
        return  

    # ✅ Store chat history (track last 10 messages per chat)
    if chat_id not in chat_history:
        chat_history[chat_id] = []
    
    chat_history[chat_id].append(user_message)
    chat_history[chat_id] = chat_history[chat_id][-10:]  # ✅ Keep only the last 10 messages

    # ✅ Detect if Murali or MRL was explicitly mentioned/tagged
    bot_username = "@mrlcreation"  # Replace with your bot's username
    user_mentioned = bot_username in user_message or "mrl" in user_message.lower() or "murali" in user_message.lower()

    # ✅ Check if the entire chat context is relevant to you
    chat_is_relevant = is_chat_relevant(chat_id)

    # ✅ Ignore messages if AI is in a group and NOT tagged, unless the chat is relevant
    if message.chat.type in ["group", "supergroup"] and not user_mentioned and not chat_is_relevant:
        logging.info(f"Ignoring non-relevant chat message: {user_message}")
        return  

    # ✅ Prevent spam (5-second cooldown per user)
    if user_id in user_last_message_time:
        time_diff = current_time - user_last_message_time[user_id]
        if time_diff < 5:
            logging.info(f"Spam prevented: {message.from_user.username}")
            return

    # ✅ Update last message time
    user_last_message_time[user_id] = current_time

    # ✅ React to important messages in groups
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
    logging.info(f"[GROUP CHAT] User Message: {user_message}")

    # ✅ If message contains design content, generate a short summary
    if len(user_message.split()) > 15:  # ✅ Only summarize long messages
        ai_reply = ai_services.summarize_design_content(user_message)
    else:
        ai_reply = ai_services.get_short_ai_response(user_message, user_mentioned=user_mentioned)

    # ✅ Send the AI's **short response**
    await message.answer(ai_reply, parse_mode="Markdown")

    # ✅ Log AI response for debugging
    logging.info(f"[GROUP CHAT] AI Response Sent: {ai_reply}")
