# handlers/commands.py
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(Command("stop"))
async def cmd_stop(message: Message, state: FSMContext):
    current = await state.get_state()
    await state.clear()
    if current is not None:
        await message.answer(
            "Хорошо, остановились. Если захотите вернуться — напишите /start."
        )
    else:
        await message.answer("Если понадоблюсь — напишите /start.")
