from typing import Dict

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from db import async_db_connection

from action.customer import CHOOSE_PACKAGE_ACTION
from crud.gift import update_suggested_gift
from crud.order import create_order
from handlers.customer.helpers import PackageData
from state.customer import CustomerState
from state.order_status import OrderStatus
from template.loader import render_template


async def choose_package_handler(
    call: CallbackQuery, state: FSMContext, callback_data: Dict
):
    state_data = await state.get_data()

    chosen_recipient_id, chosen_holiday_id = (
        state_data['chosen_recipient'],
        state_data['chosen_holiday'],
    )

    gift_id = int(callback_data['gift_id'])

    order_data = {
        'customer_id': call.from_user.username,
        'recipient_id': chosen_recipient_id,
        'gift_id': gift_id,
        'holiday_id': chosen_holiday_id,
        'status_id': OrderStatus.CHOSEN,
    }
    if callback_data['is_package_needed'] == 'True':
        order_data.update({'package_id': int(callback_data['package_id'])})

    async with async_db_connection() as conn:
        await create_order(conn, **order_data)
        await update_suggested_gift(
            conn, call.from_user.username, chosen_recipient_id, gift_id
        )
        await conn.commit()

    await state.set_state(CustomerState.COMMENTING)
    return await call.message.answer(render_template('comment.jinja2'))


def register_handlers_choose_package(dp: Dispatcher):
    dp.register_callback_query_handler(
        choose_package_handler,
        PackageData.filter(action=CHOOSE_PACKAGE_ACTION),
        state=CustomerState.CHOOSING_PACKAGE,
    )
