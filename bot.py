import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties
import personal_chat
import group_chat
from config import API_TOKEN

# ✅ Logging
logging.basicConfig(level=logging.INFO)

# ✅ Initialize bot
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

# ✅ Dispatcher
dp = Dispatcher()

# ✅ Include handlers
dp.include_router(personal_chat.router)  # ✅ Private chat
dp.include_router(group_chat.router)  # ✅ Group chat

# ✅ Set bot commands
async def set_bot_commands():
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="help", description="Get help"),
        BotCommand(command="pricing", description="View design pricing"),
    ]
    await bot.set_my_commands(commands)

# ✅ Main function
async def main():
    await set_bot_commands()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
