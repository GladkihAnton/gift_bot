from typing import Dict

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from db import async_db_connection

from action.customer import CHOOSE_PACKAGE_ACTION, LIKE_OR_DISLIKE_ACTION
from crud.package import get_package_by_id
from handlers.customer.helpers import (
    PackageData,
    ReactionData,
    cache_folder,
    prepare_gift_message,
    upload_package_img_and_save_file_id,
)
from state.customer import CustomerState
from template.loader import render_template


async def like_or_dislike_handler(
    call: CallbackQuery, state: FSMContext, callback_data: Dict
):
    if callback_data['has_liked'] == 'True':
        return await _like_handler(call, state, callback_data)

    chosen_recipient_id = int((await state.get_data())['chosen_recipient'])
    return await prepare_gift_message(call, state, chosen_recipient_id)


async def _like_handler(call: CallbackQuery, state: FSMContext, callback_data: Dict):
    package_id = int(callback_data['package_id'])
    data = {
        'gift_id': callback_data['gift_id'],
        'package_id': package_id,
    }

    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text='Да',
            callback_data=PackageData.new(
                CHOOSE_PACKAGE_ACTION, is_package_needed=True, **data
            ),
        ),
        InlineKeyboardButton(
            text='Нет',
            callback_data=PackageData.new(
                CHOOSE_PACKAGE_ACTION, is_package_needed=False, **data
            ),
        ),
    )

    async with async_db_connection() as conn:
        package_img, file_id = (
            await get_package_by_id(conn, package_id=package_id)
        ).one()

    # if not file_id:
    path = cache_folder / package_img
    await upload_package_img_and_save_file_id(path, call, keyboard, package_id)
    return await state.set_state(CustomerState.CHOOSING_PACKAGE)

    # await call.message.answer_photo(
    #     file_id,
    #     caption=render_template('package.jinja2'),
    #     reply_markup=keyboard,
    # )
    # return await state.set_state(CustomerState.CHOOSING_PACKAGE)


def register_handlers_gift_tinder(dp: Dispatcher):
    dp.register_callback_query_handler(
        like_or_dislike_handler,
        ReactionData.filter(action=LIKE_OR_DISLIKE_ACTION),
        state=CustomerState.TINDER,
    )
