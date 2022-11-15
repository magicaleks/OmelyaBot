from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from ..utils import check_user
from ..replies import replies
from ..misc.keyboards import (
    information_kb,
)

information_router = Router()

@information_router.callback_query(text_startswith='information')
async def information(call: types.CallbackQuery) -> None:
    flag = await check_user(call.from_user.id)
    if not flag:
        return
    
    service = [1, 0][int(call.data.split(':')[1])]

    if service:
        await call.message.answer_photo(types.URLInputFile('https://i.ytimg.com/vi/RkkAYjm6ves/maxresdefault.jpg'))
        await call.message.answer(replies['massage']['information'][service], reply_markup=information_kb(service))
    else:
        await call.message.edit_text(replies['massage']['information'][service], reply_markup=information_kb(service))
    await call.answer()
