# handlers/flow.py
import json
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states import Flow
from questions import QUESTIONS
from keyboards import budget_small_kb, budget_medium_kb, confirm_kb
from logic import is_relevant, format_client_card
import db

router = Router()


def _budget_kb(segment: str):
    return budget_small_kb() if segment == "small" else budget_medium_kb()


async def _send_question(target, state: FSMContext):
    """Send the current question. target is Message or the message from a CallbackQuery."""
    data = await state.get_data()
    segment = data["segment"]
    idx = data["question_index"]
    questions = QUESTIONS[segment]
    q = questions[idx]

    if q["type"] == "text":
        await target.answer(q["text"])
    else:
        await target.answer(q["text"], reply_markup=_budget_kb(segment))


async def _advance_or_timeslot(target, user_id: int, state: FSMContext, answer: str):
    """Save answer, move to next question or timeslot state."""
    data = await state.get_data()
    segment = data["segment"]
    idx = data["question_index"]
    answers = data.get("answers", {})

    answers[f"q{idx}"] = answer
    questions = QUESTIONS[segment]

    if idx + 1 < len(questions):
        await state.update_data(
            question_index=idx + 1,
            retry=False,
            answers=answers,
        )
        await _send_question(target, state)
    else:
        # Brief complete — ask for time slot
        await state.update_data(answers=answers)
        await state.set_state(Flow.timeslot)
        db.update_lead(user_id, answers=json.dumps(answers, ensure_ascii=False))
        await target.answer(
            "Почти готово! Когда Вам удобно созвониться? "
            "Укажите 2–3 варианта дней и времени."
        )


@router.callback_query(F.data.startswith("segment:"))
async def handle_segment(callback: CallbackQuery, state: FSMContext):
    segment = callback.data.split(":")[1]  # "small" or "medium"
    await state.update_data(segment=segment, question_index=0, retry=False, answers={})
    await state.set_state(Flow.question)
    await callback.message.edit_reply_markup(reply_markup=None)
    await _send_question(callback.message, state)
    await callback.answer()


@router.message(Flow.question)
async def handle_text_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    segment = data["segment"]
    idx = data["question_index"]
    q = QUESTIONS[segment][idx]

    # Budget question expects a button, not text
    if q["type"] != "text":
        await message.answer("Пожалуйста, выберите вариант из кнопок выше.")
        return

    if not is_relevant(message.text):
        if not data.get("retry"):
            await state.update_data(retry=True)
            await message.answer("Не совсем поняла — уточните, пожалуйста?")
            return
        # Second irrelevant answer — accept and move on

    db.update_lead(message.from_user.id)  # bump last_active_at
    await _advance_or_timeslot(message, message.from_user.id, state, message.text)


@router.callback_query(Flow.question, F.data.startswith("budget:"))
async def handle_budget_answer(callback: CallbackQuery, state: FSMContext):
    budget_value = callback.data.split(":", 1)[1]
    await callback.message.edit_reply_markup(reply_markup=None)
    db.update_lead(callback.from_user.id)  # bump last_active_at
    await _advance_or_timeslot(callback.message, callback.from_user.id, state, budget_value)
    await callback.answer()


@router.message(Flow.timeslot)
async def handle_timeslot(message: Message, state: FSMContext):
    data = await state.get_data()
    time_slots = message.text

    await state.update_data(time_slots=time_slots)
    await state.set_state(Flow.confirm)

    db.update_lead(message.from_user.id, time_slots=time_slots)

    card_text = format_client_card({
        "segment": data["segment"],
        "answers": data.get("answers", {}),
        "time_slots": time_slots,
    })
    await message.answer(card_text, reply_markup=confirm_kb())
