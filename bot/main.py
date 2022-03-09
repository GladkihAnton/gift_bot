import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from handlers.auth.auth import AuthMiddleware, register_handlers_auth
from handlers.customer.choose_recipient import register_handlers_choose_recipient
from handlers.customer.comment import register_handlers_customer_comments
from handlers.customer.gift_tinder import register_handlers_gift_tinder
from handlers.customer.holiday import register_handlers_choose_holiday
from handlers.customer.package import register_handlers_choose_package
from handlers.customer.status_order import register_handlers_check_order_status


async def main():
    api_token = '5209986910:AAEGPFweAFi2WJ1gFnNZgBuwWyUHxwkf0aE'

    logging.basicConfig(level=logging.DEBUG)
    storage = RedisStorage2('redis', 6379, db=5, pool_size=10, prefix='state')

    bot = Bot(token=api_token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    dp.middleware.setup(AuthMiddleware())

    register_handlers_auth(dp)
    register_handlers_check_order_status(dp)
    register_handlers_choose_recipient(dp)
    register_handlers_choose_holiday(dp)
    register_handlers_gift_tinder(dp)
    register_handlers_choose_package(dp)
    register_handlers_customer_comments(dp)

    # await set_commands(bot)
    await dp.skip_updates()
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
