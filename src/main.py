import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
import logging as logger

from .config import config
from .db.base import check_db_conn
from .routes import register_all_routes
from .payments import init_webhook

from aiohttp import web


async def _main():
    logger.basicConfig(
        level=logger.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    await check_db_conn()

    # bot = Bot(token=config['bot']['token'], parse_mode='MarkdownV2')
    bot = Bot(token=config['bot']['token'])
    await bot.set_my_commands([
        BotCommand(command='/start', description='Начать сначала'),
        BotCommand(command='/how', description='Показать интсрукцию'),
        BotCommand(command='/booking', description='Забронировать сеанс'),
        BotCommand(command='/profile', description='Ваш кошелёк'),
        BotCommand(command='/referal', description='Пригласить друга'),
    ])
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    register_all_routes(dp)
    try:
        logger.info('Starting bot')
        await bot.get_updates(timeout=50)
        await dp.start_polling(bot, polling_timeout=150)
    finally:
        await storage.close()
        await bot.session.close()


def main():
    loop = asyncio.get_event_loop()
    loop.create_task(_main())
    loop.run_forever()
    app = init_webhook()
    web.run_app(app, host='0.0.0.0', port=49344)
