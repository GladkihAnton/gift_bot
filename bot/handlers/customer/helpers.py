from collections import namedtuple
from pathlib import Path
from typing import Dict, List

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.emoji import emojize
from db import async_db_connection
from jinja2 import Template

from action.customer import LIKE_OR_DISLIKE_ACTION
from crud.gift import get_and_update_gift, update_gift_file_id
from crud.package import update_package_file_id
from models.postgres import Holiday, Recipient
from state.customer import CustomerState
from template.loader import render_template

ActionData = CallbackData('vote', 'action')
ReactionData = CallbackData('vote', 'action', 'has_liked', 'gift_id', 'package_id')
RecipientData = CallbackData('vote', 'action', 'recipient_id', 'holidays')
HolidayData = CallbackData('vote', 'action', 'holiday_id')
PackageData = CallbackData(
    'vote', 'action', 'is_package_needed', 'gift_id', 'package_id'
)

cache_folder = Path('../media')


async def prepare_gift_message(
    call: CallbackQuery, state: FSMContext, recipient_id: int
):
    (gift, sex, gift_type) = await get_and_update_gift(
        call.from_user.username, recipient_id
    )

    if not gift:
        await state.set_state(CustomerState.COMMENTING)
        return await call.message.answer(render_template('error/no_gift.jinja2'))

    button_data = {
        'gift_id': gift.id,
        'package_id': gift.package_id,
    }

    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text=emojize(':thumbsup:'),
            callback_data=ReactionData.new(
                action=LIKE_OR_DISLIKE_ACTION, has_liked=True, **button_data
            ),
        ),
        InlineKeyboardButton(
            text=emojize(':thumbsdown:'),
            callback_data=ReactionData.new(
                action=LIKE_OR_DISLIKE_ACTION, has_liked=False, **button_data
            ),
        ),
    )

    text = render_template('gift.jinja2', gift=gift, sex=sex, type=gift_type)
    path = cache_folder / gift.image

    if not gift.file_id:
        await upload_gift_img_and_save_file_id(path, call, keyboard, text, gift.id)
        return await state.set_state(CustomerState.TINDER)

    await call.message.answer_photo(
        gift.file_id,
        caption=text,
        reply_markup=keyboard,
    )
    return await state.set_state(CustomerState.TINDER)


def group_recipient_and_holidays(rows: namedtuple) -> Dict[Recipient, List[Dict]]:
    result = {}
    for recipient, holiday in rows:
        if recipient not in result:
            result[recipient] = [holiday.to_dict()]
            continue

        result[recipient].append(holiday.to_dict())

    return result


async def upload_package_img_and_save_file_id(
    path: Path, call: CallbackQuery, keyboard: InlineKeyboardMarkup, package_id: int
) -> None:
    with open(path, 'rb') as pic:
        message = await call.message.answer_photo(
            pic.read(),
            caption=render_template('package.jinja2'),
            reply_markup=keyboard,
        )

    file_id = message.photo[0].file_id
    async with async_db_connection() as conn:
        await update_package_file_id(conn, package_id, file_id)
        await conn.commit()


async def upload_gift_img_and_save_file_id(
    path: Path,
    call: CallbackQuery,
    keyboard: InlineKeyboardMarkup,
    text: Template | str,
    gift_id: int,
) -> None:
    with open(path, 'rb') as pic:
        message = await call.message.answer_photo(
            pic.read(),
            caption=text,
            reply_markup=keyboard,
        )

    file_id = message.photo[0].file_id
    async with async_db_connection() as conn:
        await update_gift_file_id(conn, gift_id, file_id)
        await conn.commit()
