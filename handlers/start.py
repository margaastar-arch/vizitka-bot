# handlers/start.py
from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states import Flow
from keyboards import consent_kb, segment_kb, restart_or_continue_kb
import db

router = Router()

GREETING = (
    "Привет! Я Марга АСТ — помогаю бизнесу внедрять ИИ-решения, "
    "которые реально окупаются.\n"
    "Чтобы наш разговор был по делу, задам Вам несколько вопросов. "
    "Это займёт 5–10 минут.\n\n"
    "Для этого мне нужно Ваше согласие на обработку персональных данных "
    "в соответствии с 152-ФЗ."
)


async def _send_greeting(message: Message, state: FSMContext):
    await state.set_state(Flow.consent)
    await message.answer(GREETING, reply_markup=consent_kb())


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, command: CommandObject):
    current = await state.get_state()

    if current is not None:
        # Уже в процессе заполнения — предложить выбор
        await message.answer(
            "Вы уже заполняете бриф. Начать заново или продолжить?",
            reply_markup=restart_or_continue_kb(),
        )
        return

    # Новый пользователь или чистый старт
    username = message.from_user.username
    source = "vizitka"
    if command.args:
        source = command.args  # e.g. "vizitka" из ?start=vizitka

    db.save_lead(message.from_user.id, username=username, source=source)
    await _send_greeting(message, state)


@router.callback_query(F.data == "restart:yes")
async def restart_yes(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    username = callback.from_user.username
    db.save_lead(callback.from_user.id, username=username, source="vizitka")
    await callback.message.edit_reply_markup(reply_markup=None)
    await _send_greeting(callback.message, state)
    await callback.answer()


@router.callback_query(F.data == "restart:no")
async def restart_no(callback: CallbackQuery):
    await callback.answer("Продолжаем с того места, где остановились.")


@router.callback_query(F.data == "consent:yes")
async def consent_yes(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Flow.segment)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        "Скажите, сколько человек в Вашей команде?",
        reply_markup=segment_kb(),
    )
    await callback.answer()


@router.callback_query(F.data == "consent:no")
async def consent_no(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        "Понятно, не проблема. Если захотите поговорить — напишите /start."
    )
    await callback.answer()
