# logic.py

SEGMENT_LABELS = {"small": "Малый бизнес", "medium": "Средний бизнес"}


def is_relevant(text: str) -> bool:
    """True if text looks like a real answer (≥ 5 non-space chars)."""
    return len(text.strip()) >= 5


def format_client_card(data: dict) -> str:
    """Confirmation card sent back to the client before the hot/cold choice."""
    segment = SEGMENT_LABELS.get(data["segment"], data["segment"])
    pain = data["answers"].get("q1", "—")[:100]
    slots = data.get("time_slots", "—")
    return (
        "Отлично, всё записала!\n\n"
        "Вот что я получила:\n"
        f"• {segment}\n"
        f"• {pain}\n"
        f"• Удобное время: {slots}\n\n"
        "Подтвердите, что готовы к звонку:"
    )


def format_marga_card(data: dict, status: str) -> str:
    """Notification card sent to Marga after hot/cold decision."""
    emoji = "🔥" if status == "hot" else "🧊"
    status_label = "горячий" if status == "hot" else "холодный"
    segment = SEGMENT_LABELS.get(data["segment"], data["segment"])
    username = f"@{data['username']}" if data.get("username") else "без ника"

    answers_lines = ""
    for key in sorted(data["answers"].keys()):
        num = int(key[1:]) + 1
        answers_lines += f"{num}. {data['answers'][key]}\n"

    return (
        f"{emoji} Новая заявка — {status_label}\n\n"
        f"Сегмент: {segment}\n"
        f"Имя/ник: {username}\n\n"
        f"Ответы:\n{answers_lines}\n"
        f"Удобное время: {data.get('time_slots', '—')}"
    )
