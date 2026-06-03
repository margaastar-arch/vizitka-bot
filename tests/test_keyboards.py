# tests/test_keyboards.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from keyboards import consent_kb, segment_kb, budget_small_kb, budget_medium_kb, confirm_kb
from aiogram.types import InlineKeyboardMarkup


def _buttons(kb: InlineKeyboardMarkup) -> list:
    return [b for row in kb.inline_keyboard for b in row]


def test_consent_kb():
    kb = consent_kb()
    btns = _buttons(kb)
    datas = [b.callback_data for b in btns]
    assert "consent:yes" in datas
    assert "consent:no" in datas


def test_segment_kb():
    kb = segment_kb()
    btns = _buttons(kb)
    datas = [b.callback_data for b in btns]
    assert "segment:small" in datas
    assert "segment:medium" in datas


def test_budget_small_has_four_options():
    kb = budget_small_kb()
    assert len(_buttons(kb)) == 4


def test_budget_medium_has_four_options():
    kb = budget_medium_kb()
    assert len(_buttons(kb)) == 4


def test_confirm_kb():
    kb = confirm_kb()
    datas = [b.callback_data for b in _buttons(kb)]
    assert "confirm:hot" in datas
    assert "confirm:cold" in datas


def test_restart_or_continue_kb():
    from keyboards import restart_or_continue_kb
    kb = restart_or_continue_kb()
    datas = [b.callback_data for b in _buttons(kb)]
    assert "restart:yes" in datas
    assert "restart:no" in datas
