# states.py
from aiogram.fsm.state import State, StatesGroup


class Flow(StatesGroup):
    consent   = State()   # Ждём согласия на 152-ФЗ
    segment   = State()   # Ждём выбор сегмента (до 20 / от 20)
    question  = State()   # Ждём ответ на текущий вопрос или кнопку бюджета
    timeslot  = State()   # Ждём удобное время
    confirm   = State()   # Ждём кнопку hot/cold
