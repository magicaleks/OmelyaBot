from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from ..config import config


_client = AsyncIOMotorClient(config['db']['uri'], serverSelectionTimeoutMS=config['db']['timeout'])
_db: AsyncIOMotorDatabase = _client[config['db']['name']]


class DatabaseConnectError(Exception):
    pass


async def check_db_conn():
    logger.info('trying to connect to database')
    try:
        await _client.server_info()
    except Exception as e:
        logger.error(e)
        raise DatabaseConnectError
    logger.info('database connection was inited')
