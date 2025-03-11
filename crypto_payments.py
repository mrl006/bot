from aiogram import Router, types
from aiogram.filters import Command
from config import CRYPTO_WALLETS

router = Router()

@router.message(Command("pay"))
async def show_payment_options(message: types.Message):
    """Send crypto payment details to the user."""
    
    payment_info = (
        "💰 **Payment Options** 💰\n\n"
        "**USDT (BEP20):**\n"
        f"`{CRYPTO_WALLETS['USDT_BEP20']}`\n\n"
        
        "**BNB (BEP20):**\n"
        f"`{CRYPTO_WALLETS['BNB_BEP20']}`\n\n"
        
        "**Solana (SOL):**\n"
        f"`{CRYPTO_WALLETS['SOLANA']}`\n\n"
        
        "**ETH (ERC20):**\n"
        f"`{CRYPTO_WALLETS['ETH_ERC20']}`\n\n"
        
        "⚡ **After sending payment, please send a screenshot & TX ID for confirmation!**"
    )

    await message.answer(payment_info, parse_mode="Markdown")
