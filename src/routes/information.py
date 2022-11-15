from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from ..utils import check_user
from ..replies import replies
from ..misc.keyboards import (
    information_kb,
)

information_router = Router()

@information_router.callback_query(text='information')
async def contacts(call: types.CallbackQuery, state: FSMContext) -> None:
    flag = await check_user(call.from_user.id)
    if not flag:
        return

    for c, i in enumerate(replies['massage']['information'], 1):
        await call.message.answer(i, reply_markup=information_kb() if c == len(replies['massage']['information']) else None)
    await call.answer()
