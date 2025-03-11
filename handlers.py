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
        "💡 **I am here to assist you with your queries and tasks.**\n"
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

# ✅ AI RESPONSE HANDLER: Responds ONLY if tagged in a group
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

    # ✅ Ignore messages if AI is in a group and NOT tagged
    if message.chat.type in ["group", "supergroup"] and not user_mentioned:
        logging.info(f"Ignoring untagged message: {user_message}")
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

    # ✅ Get AI response and personalize it
    ai_reply = ai_services.get_ai_response(user_message, user_mentioned=user_mentioned)
    personalized_reply = f"👋 {user_name}, {ai_reply}"

    await message.answer(personalized_reply, parse_mode="Markdown")

    # ✅ Log AI response for debugging
    logging.info(f"AI Response Sent: {ai_reply}")
