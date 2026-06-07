# keyboards.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def _kb(*rows: list[tuple[str, str]]) -> InlineKeyboardMarkup:
    """Helper: each row is a list of (label, callback_data) tuples."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=label, callback_data=data) for label, data in row]
            for row in rows
        ]
    )


def consent_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📄 Политика конфиденциальности", url="https://telegra.ph/Politika-konfidencialnosti-MargaA-Brief-06-07")],
        [
            InlineKeyboardButton(text="Согласен(на)", callback_data="consent:yes"),
            InlineKeyboardButton(text="Не согласен(на)", callback_data="consent:no"),
        ],
    ])


def segment_kb() -> InlineKeyboardMarkup:
    return _kb([("до 20 человек", "segment:small"), ("от 20 человек", "segment:medium")])


def budget_small_kb() -> InlineKeyboardMarkup:
    return _kb(
        [("до 30 000 ₽", "budget:до 30 000 ₽")],
        [("30 000 – 80 000 ₽", "budget:30 000 – 80 000 ₽")],
        [("от 80 000 ₽", "budget:от 80 000 ₽")],
        [("пока не определились", "budget:пока не определились")],
    )


def budget_medium_kb() -> InlineKeyboardMarkup:
    return _kb(
        [("до 80 000 ₽", "budget:до 80 000 ₽")],
        [("80 000 – 200 000 ₽", "budget:80 000 – 200 000 ₽")],
        [("от 200 000 ₽", "budget:от 200 000 ₽")],
        [("обсуждаем после оценки", "budget:обсуждаем после оценки")],
    )


def confirm_kb() -> InlineKeyboardMarkup:
    return _kb(
        [("✅ Да, жду звонка", "confirm:hot")],
        [("⏸ Пока просто смотрю", "confirm:cold")],
    )


def restart_or_continue_kb() -> InlineKeyboardMarkup:
    return _kb(
        [("Начать заново", "restart:yes")],
        [("Продолжить", "restart:no")],
    )
