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

# 🎉 START COMMAND: General AI Greeting
@router.message(Command("start"))
async def send_welcome(message: Message):
    welcome_text = (
        "👋 **Welcome to MRL AI Assistant!** 🚀\n\n"
        "💡 **I am here to assist you with your questions and provide useful responses.**\n"
        "✅ **Ask me anything, and I'll do my best to help!**\n\n"
        "📩 **Need assistance? Just send a message!**"
    )
    await message.answer(welcome_text, parse_mode="Markdown")

# 🎊 WELCOME NEW USERS IN GROUPS
@router.chat_member()
async def welcome_new_member(update: ChatMemberUpdated):
    """Automatically welcomes new users in a group chat."""
    if update.new_chat_member.status == "member":  # ✅ Detects new member join
        welcome_message = (
            f"👋 Welcome {update.new_chat_member.user.first_name}!\n"
            "✨ We are happy to have you here. Feel free to ask questions and join the conversation!"
        )
        await update.chat.send_message(welcome_message, parse_mode="Markdown")

# ✅ FUNCTION TO CHECK IMPORTANT MESSAGES FOR REACTIONS
def get_reaction(user_message):
    """Determine the right emoji reaction based on the message content."""
    reaction_map = {
        "amazing": "🔥",
        "great": "🔥",
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

# 💬 AI RESPONSE HANDLER: Responds in groups if "MRL" or "Murali" is mentioned & reacts to important messages
@router.message()
async def ai_response(message: Message):
    user_message = message.text.strip()
    user_id = message.from_user.id  # ✅ Track user for cooldown
    user_name = message.from_user.first_name  # ✅ Get user's first name
    current_time = asyncio.get_event_loop().time()

    if not user_message:
        return  # Ignore empty messages

    # ✅ Prevent spam (5-second cooldown per user)
    if user_id in user_last_message_time:
        time_diff = current_time - user_last_message_time[user_id]
        if time_diff < 5:  # ✅ 5-second cooldown
            logging.info(f"Spam prevented: {message.from_user.username}")
            return

    # ✅ Update last message time
    user_last_message_time[user_id] = current_time

    # ✅ React to important messages in groups
    if message.chat.type in ["group", "supergroup"]:
        reaction_emoji = get_reaction(user_message)
        if reaction_emoji:
            try:
                await message.react(ReactionTypeEmoji(emoji=reaction_emoji))
                logging.info(f"Reacted with {reaction_emoji} to: {user_message}")
            except Exception as e:
                logging.error(f"Failed to react: {str(e)}")

        # ✅ Only respond if "MRL" or "Murali" is in the message
        if "mrl" not in user_message.lower() and "murali" not in user_message.lower():
            logging.info(f"Ignoring message in group: {user_message}")  # ✅ Debugging log
            return  # Ignore messages without "MRL" or "Murali" in groups

    # ✅ Show "typing..." before responding
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

    # ✅ Get AI response and personalize it
    ai_reply = ai_services.get_ai_response(user_message)
    personalized_reply = f"👋 {user_name}, {ai_reply}"  # ✅ Add user's name to AI response

    await message.answer(personalized_reply, parse_mode="Markdown")

    # ✅ Log AI response for debugging
    logging.info(f"AI Response Sent: {ai_reply}")
