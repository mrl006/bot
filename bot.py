import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand
from config import API_TOKEN
import personal_chat, group_chat  # Import chat handlers

# ✅ Configure logging
logging.basicConfig(level=logging.INFO)

# ✅ Initialize bot
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# ✅ Include routers for private & group chats
dp.include_router(personal_chat.router)  # Private chat handler
dp.include_router(group_chat.router)  # Group chat handler

# ✅ Set bot commands
async def set_bot_commands():
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="help", description="Get help"),
        BotCommand(command="pricing", description="View pricing"),
    ]
    await bot.set_my_commands(commands)

# ✅ Start the bot
async def main():
    await set_bot_commands()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
