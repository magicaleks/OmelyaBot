import asyncio
from .db.database import db
from .misc.scheduler import task_scheduler
from .services.sender import sender
from .services.cycles import services

async def _worker():
    while True:
        users = await db.get_users()
        for u in users:
            for s in u.subscriptions_services:
                if not task_scheduler.get_job(s+u.id.__str__()):
                    cycle = await services[s].execute(u.get_task_payload())
                    task_scheduler.add_job(sender, 'interval', next_run_time=cycle.end, id=s+u.id.__str__(), args=(s, u.id))
        await asyncio.sleep(30)

def start_worker():
    loop = asyncio.get_event_loop()
    loop.create_task(_worker())
