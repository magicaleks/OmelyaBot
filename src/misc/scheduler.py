from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.mongodb import MongoClient, MongoDBJobStore
from aiogram import Bot

from ..config import config

client = MongoClient(config.db.url)

jobstores = {
    'default': MongoDBJobStore(database=config.db.name, collection=config.scheduler.task_collection_name, client=client)
}

task_scheduler = AsyncIOScheduler(jobstores=jobstores)

jobstores = {
    'default': MongoDBJobStore(database=config.db.name, collection=config.scheduler.sub_collection_name, client=client)
}

sub_scheduler = AsyncIOScheduler(jobstores=jobstores)

async def start_scheduler():
    # task_scheduler.start()
    # sub_scheduler.start()
    pass
