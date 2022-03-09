from aiogram.dispatcher.filters.state import State, StatesGroup


class CustomerState(StatesGroup):
    START = State()
    RANDOM_OR_NOT_CHOOSING = State()
    CHOOSING_HOLIDAY = State()
    CHOOSING_RECIPIENT = State()
    CHECKING_STATUS = State()
    TINDER = State()
    CHOOSING_PACKAGE = State()
    COMMENTING = State()
    FINISH = State()
