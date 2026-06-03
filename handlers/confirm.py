# handlers/confirm.py
import json
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from states import Flow
from logic import format_marga_card
import db
import config

router = Router()


@router.callback_query(Flow.confirm, F.data == "confirm:hot")
async def confirm_hot(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await _finalize(callback, state, bot, status="hot")


@router.callback_query(Flow.confirm, F.data == "confirm:cold")
async def confirm_cold(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await _finalize(callback, state, bot, status="cold")


async def _finalize(callback: CallbackQuery, state: FSMContext, bot: Bot, status: str):
    data = await state.get_data()
    await state.clear()

    db.update_lead(callback.from_user.id, status=status)

    await callback.message.edit_reply_markup(reply_markup=None)

    # Message to client
    if status == "hot":
        client_msg = "Я позвоню Вам в один из указанных промежутков. До встречи!"
    else:
        client_msg = "Понятно! Если решитесь — я здесь. Можете написать в любой момент."
    await callback.message.answer(client_msg)

    # Notification card to Marga
    lead = db.get_lead(callback.from_user.id)
    answers_raw = lead.get("answers", "{}")
    try:
        answers = json.loads(answers_raw) if isinstance(answers_raw, str) else answers_raw
    except Exception:
        answers = {}

    card = format_marga_card(
        {
            "segment": data.get("segment", lead.get("segment", "?")),
            "username": callback.from_user.username,
            "answers": answers,
            "time_slots": data.get("time_slots", lead.get("time_slots", "—")),
        },
        status=status,
    )
    await bot.send_message(config.MARGA_CHAT_ID, card)
    await callback.answer()
