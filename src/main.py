import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
import logging as logger

from .config import config
from .db.base import check_db_conn
from .routes import register_all_routes
# from .worker import start_worker

async def main():
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
        # start_worker()

        logger.info('Starting bot')
        await bot.get_updates(timeout=30)
        await dp.start_polling(bot)
    finally:
        await storage.close()
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
