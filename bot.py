import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
from config import API_TOKEN, OWNER_USERNAME
import handlers, ai_services, admin_panel, database

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize Dispatcher
dp = Dispatcher()

# Initialize Bot
bot = Bot(
    token=API_TOKEN,
    parse_mode=ParseMode.HTML  # Use parse_mode directly
)

async def main():
    try:
        # Register routes
        dp.include_router(handlers.router)
        
        # Set bot commands
        await bot.set_my_commands([
            types.BotCommand(command="start", description="Start MRL AI Assistant"),
            types.BotCommand(command="pricing", description="View Design Pricing"),
            types.BotCommand(command="contact", description="Contact MRL"),
        ])
        
        # Start polling
        await dp.start_polling(bot)
    
    except Exception as e:
        logging.error(f"Error occurred: {e}")

# Run the bot using asyncio.run() for modern Python
if __name__ == "__main__":
    asyncio.run(main())  # Replacing loop.create_task() with asyncio.run()
