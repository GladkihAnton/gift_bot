from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from db import async_db_connection

from action.customer import CHECK_STATUS_ACTION
from crud.order import get_orders
from state.customer import CustomerState
from template.loader import render_template


async def check_status_handler(message: Message, state: FSMContext):
    await state.set_state(CustomerState.CHECKING_STATUS)

    async with async_db_connection() as conn:
        orders = (await get_orders(conn, username=message.from_user.username)).all()

    if not orders:
        return await message.answer('Заказов нет')

    return await message.answer(render_template('status_order.jinja2', orders=orders))


def register_handlers_check_order_status(dp: Dispatcher):
    dp.register_message_handler(
        check_status_handler,
        lambda message: message.text == CHECK_STATUS_ACTION,
        state="*",
    )
