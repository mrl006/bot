import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties
import personal_chat
import group_chat
from config import API_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

dp.include_router(personal_chat.router)
dp.include_router(group_chat.router)

async def set_bot_commands():
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="help", description="Get help"),
        BotCommand(command="pricing", description="View design pricing"),
    ]
    await bot.set_my_commands(commands)

async def main():
    await set_bot_commands()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
