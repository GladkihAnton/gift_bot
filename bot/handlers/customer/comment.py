import logging
from datetime import datetime

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from db import async_db_connection

from crud.comment import create_comment
from handlers.customer.helpers import cache_folder
from state.customer import CustomerState
from template.loader import render_template


async def commenting_handler(message: Message, state: FSMContext):
    comment_data = {
        'customer_id': message.from_user.username,
        'recipient_id': int((await state.get_data())['chosen_recipient']),
    }

    if not message.text and not message.voice:
        return await message.answer(render_template('error/comment_format.jinja2'))

    if text := message.text:
        comment_data |= {'comment': text}

    if voice := message.voice:
        try:
            voice_bytes = await message.bot.download_file_by_id(voice.file_id)
            voice_path = 'voice_cache' + str(datetime.now()) + '.ogg'
            with open(cache_folder / voice_path, 'wb') as voice:
                voice.write(voice_bytes.read())

            comment_data |= {'voice': voice_path}
        except Exception:
            logging.exception('Error while uploading audio')
            return await message.answer(render_template('error/file_save.jinja2'))

    async with async_db_connection() as conn:
        await create_comment(conn, **comment_data)
        await conn.commit()

    await state.set_state(CustomerState.START)
    return await message.answer(render_template('comment_finish.jinja2'))


def register_handlers_customer_comments(dp: Dispatcher):
    dp.register_message_handler(
        commenting_handler,
        state=CustomerState.COMMENTING,
        content_types=['text', 'voice'],
    )
