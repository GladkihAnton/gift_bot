from typing import Dict

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from action.customer import CHOSE_HOLIDAY_ACTION
from handlers.customer.helpers import HolidayData, prepare_gift_message
from state.customer import CustomerState


async def choose_holiday_handler(
    call: CallbackQuery, state: FSMContext, callback_data: Dict
):
    holiday_id = int(callback_data['holiday_id'])
    recipient_id = int((await state.get_data())['chosen_recipient'])
    await state.update_data({'chosen_holiday': holiday_id})

    return await prepare_gift_message(call, state, recipient_id)


def register_handlers_choose_holiday(dp: Dispatcher):
    dp.register_callback_query_handler(
        choose_holiday_handler,
        HolidayData.filter(action=CHOSE_HOLIDAY_ACTION),
        state=CustomerState.CHOOSING_HOLIDAY,
    )
