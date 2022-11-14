from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from ..utils import check_user
from ..replies import replies

contacts_router = Router()

@contacts_router.callback_query(text='contacts')
async def contacts(call: types.CallbackQuery, state: FSMContext) -> None:
    flag = await check_user(call.from_user.id)
    if not flag:
        return

    await call.message.answer(replies['contacts']['contacts'])
    await call.answer()
    