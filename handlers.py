from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import ai_services, live_pricing, database
from ai_protection import check_group_mention
from config import OWNER_USERNAME

router = Router()

# 🎉 START COMMAND: Welcomes the user
@router.message(Command("start"))
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

# 💰 PRICING COMMAND: Displays current pricing list
@router.message(Command("pricing"))
async def send_pricing(message: Message):
    try:
        pricing_text = live_pricing.get_live_pricing()
        response = (
            "💎 *Exclusive Design Pricing* 💎\n\n"
            f"{pricing_text}\n\n"
            "📢 *Limited-Time Discounts Available!*"
        )
        await message.answer(response, parse_mode="Markdown")
    except Exception as e:
        await message.answer("❌ *Error fetching pricing. Please try again later.*", parse_mode="Markdown")

# 📩 CONTACT COMMAND: Provides contact details
@router.message(Command("contact"))
async def send_contact(message: Message):
    contact_text = (
        "📩 *Contact MRL Creation* 🎨\n\n"
        "📞 *Telegram:* [@MrlCreation](https://t.me/MrlCreation)\n"
        "🌐 *Website:* Coming Soon!\n"
        "📌 *For premium design services, reach out now!*"
    )
    await message.answer(contact_text, parse_mode="Markdown")

# 🔐 ADMIN PANEL COMMAND: Only accessible by the owner
@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.username != OWNER_USERNAME:
        await message.answer("❌ *Access Denied:* You are not authorized to access the Admin Panel.", parse_mode="Markdown")
        return

    total_users = database.get_total_users()
    response = (
        "📊 *Admin Panel*\n\n"
        f"👥 *Total Users:* {total_users}\n\n"
        "🔍 Use /users to see all registered users."
    )
    await message.answer(response, parse_mode="Markdown")
