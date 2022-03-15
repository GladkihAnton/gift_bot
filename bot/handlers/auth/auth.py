from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from db import async_db_connection
from sqlalchemy.exc import NoResultFound

from action.customer import CHECK_STATUS_ACTION, TO_CHOOSE_ACTION
from crud.customer import get_customer
from state.auth import AuthState
from state.customer import CustomerState


class AuthMiddleware(BaseMiddleware):
    async def on_process_message(self, message: Message, data):
        state: FSMContext = data['state']
        if not await state.get_state() and message.get_command() not in ['/start']:
            await message.answer(
                'Воспользуйтесь командой /start', reply_markup=ReplyKeyboardRemove()
            )
            raise CancelHandler()


async def start_cmd(message: Message, state: FSMContext):
    await state.set_state(AuthState.CHECKING_PASSWORD)
    return await message.answer('Введите пароль')


async def check_password(message: Message, state: FSMContext):
    async with async_db_connection() as conn:
        try:
            (customer,) = (
                await get_customer(conn, username=message.from_user.username)
            ).one()
        except NoResultFound:
            return await message.answer(
                'Проверьте, верный ли пароль?'
            )

    if message.text != customer.password:
        return await message.answer(
            'Проверьте, верный ли пароль?'
        )

    await state.set_state(CustomerState.START)

    button_to_choose = KeyboardButton(TO_CHOOSE_ACTION)
    button_to_status = KeyboardButton(CHECK_STATUS_ACTION)
    main_buttons = ReplyKeyboardMarkup()
    main_buttons.add(button_to_choose, button_to_status)

    return await message.answer(
        'Добро пожаловать, воспользуйтесь меню', reply_markup=main_buttons
    )


def register_handlers_auth(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands="start", state="*")
    dp.register_message_handler(check_password, state=AuthState.CHECKING_PASSWORD)
