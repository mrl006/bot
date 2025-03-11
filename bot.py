import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties
import personal_chat  # ✅ Import private chat handler
import group_chat  # ✅ Import group chat handler
from config import API_TOKEN

# ✅ Configure logging
logging.basicConfig(level=logging.INFO)

# ✅ Initialize bot with default settings
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

# ✅ Initialize dispatcher
dp = Dispatcher()

# ✅ Include separate routers for private & group chats
dp.include_router(personal_chat.router)  # ✅ Private chat handler
dp.include_router(group_chat.router)     # ✅ Group chat handler

# ✅ Set bot commands
async def set_bot_commands():
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="help", description="Get help"),
        BotCommand(command="pricing", description="View pricing"),
        BotCommand(command="contact", description="Contact Murali")
    ]
    await bot.set_my_commands(commands)

# ✅ Main function to start the bot
async def main():
    await set_bot_commands()
    await dp.start_polling(bot)

# ✅ Run the bot
if __name__ == "__main__":
    asyncio.run(main())
