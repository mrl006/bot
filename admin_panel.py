from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import database
from config import OWNER_USERNAME  # Import owner username from config

router = Router()

@router.message(Command("admin"))
async def admin_panel(message: Message):
    # Check if the user is the bot owner
    if message.from_user.username != OWNER_USERNAME:
        await message.answer("❌ *Access Denied:* You are not authorized to access the Admin Panel.", parse_mode="Markdown")
        return

    total_users = database.get_total_users()
    response = f"📊 *Admin Panel*\n👥 *Total Users:* {total_users}\n\n🔍 Use /users to see all registered users."
    await message.answer(response, parse_mode="Markdown")
