from aiogram.fsm.state import State, StatesGroup


class SettingsState(StatesGroup):
    location = State()
    birth = State()
    name = State()

