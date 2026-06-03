# tests/test_logic.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from logic import is_relevant, format_client_card, format_marga_card


def test_is_relevant_too_short():
    assert is_relevant("ok") is False
    assert is_relevant("   ") is False
    assert is_relevant("") is False


def test_is_relevant_long_enough():
    assert is_relevant("Мы занимаемся ремонтом, 8 человек") is True
    assert is_relevant("нет") is False        # < 5 символов
    assert is_relevant("да да") is True       # ровно 5


def test_format_client_card_small():
    data = {
        "segment": "small",
        "answers": {
            "q0": "Продаём мебель, 5 человек",
            "q1": "Много времени уходит на ручной учёт заказов в таблицах"
        },
        "time_slots": "вторник или среда, после 18:00"
    }
    card = format_client_card(data)
    assert "Малый бизнес" in card
    assert "Много времени уходит" in card
    assert "вторник или среда" in card
    assert "Подтвердите" in card


def test_format_client_card_truncates_pain():
    long_answer = "А" * 200
    data = {
        "segment": "medium",
        "answers": {"q0": "компания", "q1": long_answer},
        "time_slots": "пятница"
    }
    card = format_client_card(data)
    assert long_answer[:100] in card
    assert long_answer[101:] not in card


def test_format_marga_card_hot():
    data = {
        "segment": "small",
        "username": "alice",
        "answers": {"q0": "мебель", "q1": "учёт"},
        "time_slots": "пт 15:00"
    }
    card = format_marga_card(data, "hot")
    assert "🔥" in card
    assert "горячий" in card
    assert "@alice" in card
    assert "Малый бизнес" in card


def test_format_marga_card_cold_no_username():
    data = {
        "segment": "medium",
        "username": None,
        "answers": {"q0": "a"},
        "time_slots": "пн"
    }
    card = format_marga_card(data, "cold")
    assert "🧊" in card
    assert "холодный" in card
    assert "без ника" in card
    assert "Средний бизнес" in card
