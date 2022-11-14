from aiogram import Dispatcher, Router

from .start import start_router
from .services import services_router
from .contacts import contacts_router
from .profile import profile_router


def register_all_routes(dp: Dispatcher) -> None:
    master_router = Router()
    dp.include_router(master_router)
    master_router.include_router(profile_router)
    master_router.include_router(services_router)
    master_router.include_router(contacts_router)
    master_router.include_router(start_router)
