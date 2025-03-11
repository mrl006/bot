import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties  # ✅ Import required fix
from config import API_TOKEN, OWNER_USERNAME
import handlers, ai_services, admin_panel, database

# ✅ Fix: Set default parse mode using DefaultBotProperties
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# Dispatcher for handling messages
dp = Dispatcher()

# 📌 START COMMAND: Handles /start message
@dp.message(Command("start"))
async def send_welcome(message: Message):
    welcome_text = (
        "👋 *Welcome to MRL AI Assistant!* 🚀\n\n"
        "💡 I can help you with:\n"
        "📌 *Design Pricing*\n"
        "📌 *AI-Powered Services*\n"
        "📌 *Crypto Transactions*\n\n"
        "🔹 Use /pricing to check design prices.\n"
        "🔹 Use /contact to reach MRL Creation.\n\n"
        "✨ *Let's get started!* ✨"
    )
    await message.answer(welcome_text, parse_mode="Markdown")

# 📌 MAIN FUNCTION TO START BOT
async def main():
    try:
        # Register handlers
        dp.include_router(handlers.router)

        # ✅ Set bot commands
        await bot.set_my_commands([
            types.BotCommand(command="start", description="Start MRL AI Assistant"),
            types.BotCommand(command="pricing", description="View Design Pricing"),
            types.BotCommand(command="contact", description="Contact MRL"),
        ])

        # ✅ Start polling (bot keeps running)
        await dp.start_polling(bot)

    except Exception as e:
        logging.error(f"Error occurred: {e}")

# ✅ Run the bot using asyncio.run()
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())  # ✅ FIXED: Proper async execution
