# handlers/fallback.py
# Last-resort router: included after all others, it catches anything no other
# handler picked up (e.g. a message that arrived after the session was lost),
# so the bot never goes silent on the user.
from aiogram import Router
from aiogram.types import Message, CallbackQuery

router = Router()

RECOVERY = "Случился непредвиденный сбой. Пожалуйста, нажмите /start чтобы продолжить."


@router.message()
async def fallback_message(message: Message):
    await message.answer(RECOVERY)


@router.callback_query()
async def fallback_callback(callback: CallbackQuery):
    await callback.answer()
    if callback.message:
        await callback.message.answer(RECOVERY)
