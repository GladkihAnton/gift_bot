import random
from typing import Dict, List

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from db import async_db_connection

from action.customer import (
    CHOSE_HOLIDAY_ACTION,
    MANUALLY_CHOOSING,
    RANDOM_CHOOSING,
    TO_CHOOSE_ACTION,
)
from crud.customer import get_recipients_for_customer
from handlers.customer.helpers import (
    ActionData,
    HolidayData,
    group_recipient_and_holidays,
)
from models.postgres import Holiday, Recipient
from state.customer import CustomerState
from template.loader import render_template


async def to_choose_handler(message: Message, state: FSMContext):
    await state.set_state(CustomerState.RANDOM_OR_NOT_CHOOSING)

    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text='Случайный', callback_data=ActionData.new(action=RANDOM_CHOOSING)
        ),
        InlineKeyboardButton(
            text='Конкретный',
            callback_data=ActionData.new(action=MANUALLY_CHOOSING),
        ),
    )

    return await message.answer('Выберите формат выбора', reply_markup=keyboard)


async def random_choose_handler(call: CallbackQuery, state: FSMContext):
    async with async_db_connection() as conn:
        rows = (
            await get_recipients_for_customer(conn, username=call.from_user.username)
        ).all()

    if not rows:
        return await call.message.answer(render_template('error/no_recipients.jinja2'))

    recipient_to_holidays = group_recipient_and_holidays(rows)

    (recipient, holidays) = random.choice(list(recipient_to_holidays.items()))

    await state.set_data({'chosen_recipient': recipient.id})

    await state.set_state(CustomerState.CHOOSING_HOLIDAY)

    await call.message.answer(render_template('recipient.jinja2', recipient=recipient))

    return await call.message.answer(
        render_template('choose_holiday.jinja2'),
        reply_markup=_prepare_holidays_button(holidays),
    )


async def manually_choose_handler(call: CallbackQuery, state: FSMContext):
    await state.set_state(CustomerState.CHOOSING_RECIPIENT)

    async with async_db_connection() as conn:
        rows = (
            await get_recipients_for_customer(conn, username=call.from_user.username)
        ).all()

    if not rows:
        return await call.message.answer(render_template('error/no_recipients.jinja2'))

    recipients_info: Dict[int, Dict[str, List[Dict] | Recipient]] = {
        index: {'info': recipient.to_dict(), 'holidays': holidays}
        for index, (recipient, holidays) in enumerate(
            group_recipient_and_holidays(rows).items()
        )
    }

    await state.update_data({'recipients_info': recipients_info})
    await state.set_state(CustomerState.CHOOSING_RECIPIENT)
    return await call.message.answer(
        render_template('choose_recipient.jinja2', recipients_info=recipients_info)
    )


async def choose_recipient_handler(message: Message, state: FSMContext):
    state_data = await state.get_data()
    recipients_info = state_data.pop('recipients_info', None)
    await state.set_data(state_data)

    recipient_index = message.text
    if not recipient_index.isdigit():
        return await message.answer('Введен неверный номер получателя')

    if not (recipient_data := recipients_info.get(recipient_index)):
        return await message.answer('Данный номер отсутствует в списке получателей')

    recipient: Dict = recipient_data['info']
    await state.set_data({'chosen_recipient': recipient['id']})

    await message.answer(render_template('recipient.jinja2', recipient=recipient))

    await state.set_state(CustomerState.CHOOSING_HOLIDAY)
    return await message.answer(
        render_template('choose_holiday.jinja2'),
        reply_markup=_prepare_holidays_button(recipient_data['holidays']),
    )


def _prepare_holidays_button(holidays: List[Holiday]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup().add(
        *[
            InlineKeyboardButton(
                text=holiday['name'],
                callback_data=HolidayData.new(
                    action=CHOSE_HOLIDAY_ACTION, holiday_id=holiday['id']
                ),
            )
            for holiday in holidays
        ]
    )

    return keyboard


def register_handlers_choose_recipient(dp: Dispatcher):
    dp.register_message_handler(
        to_choose_handler, lambda message: message.text == TO_CHOOSE_ACTION, state="*"
    )

    dp.register_message_handler(
        choose_recipient_handler,
        state=CustomerState.CHOOSING_RECIPIENT,
    )

    dp.register_callback_query_handler(
        manually_choose_handler,
        ActionData.filter(action=MANUALLY_CHOOSING),
        state=CustomerState.RANDOM_OR_NOT_CHOOSING,
    )

    dp.register_callback_query_handler(
        random_choose_handler,
        ActionData.filter(action=RANDOM_CHOOSING),
        state=CustomerState.RANDOM_OR_NOT_CHOOSING,
    )
