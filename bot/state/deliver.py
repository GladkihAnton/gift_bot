from aiogram.dispatcher.filters.state import State, StatesGroup


class DeliverState(StatesGroup):
    START = State()
