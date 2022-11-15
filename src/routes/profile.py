from aiogram import types, Bot, Router
from aiogram.filters.command import Command
from ..replies import replies
from ..utils import check_user

from ..misc.keyboards import (
    profile_kb,
    referal_kb,
    
)
from ..db.database import db

profile_router = Router()


@profile_router.message(Command(commands='profile', commands_ignore_case=True))
@profile_router.callback_query(text='profile')
async def profile(obj):
    flag = await check_user(obj.from_user.id)
    if not flag:
        return

    user = await db.get_user(obj.from_user.id)

    if isinstance(obj, types.Message):
        # await obj.answer(replies['profile']['profile'].format(user.id, user.name, '\\'+user.phone if user.phone.startswith('+') else user.phone, user.points, ref_text), reply_markup=profile_kb())
        await obj.answer(replies['profile']['profile'].format(user.id, user.name, user.phone, user.points), reply_markup=profile_kb())
    elif isinstance(obj, types.CallbackQuery):
        # await obj.message.edit_text(replies['profile']['profile'].format(user.id, user.name, '\\'+user.phone if user.phone.startswith('+') else user.phone, user.points, ref_text), reply_markup=profile_kb())
        await obj.message.edit_text(replies['profile']['profile'].format(user.id, user.name, user.phone, user.points), reply_markup=profile_kb())

        await obj.answer()

@profile_router.message(Command(commands='referal', commands_ignore_case=True))
@profile_router.callback_query(text='profile:referal')
async def referal(obj, bot: Bot):
    flag = await check_user(obj.from_user.id)
    if not flag:
        return

    user = await db.get_user(obj.from_user.id)

    me = await bot.me()
    # ref_link = f"<a href=\"https://t.me/{me.username}?start={user.id}\">ссылка</a>"
    ref_link = f"`https://t.me/{me.username}?start={user.id} `"
    ref_text = ''

    if not len(user.referals_ids):
        ref_text = f'Вот ваша {ref_link}'

    elif 9 < len(user.referals_ids) % 100 < 22:
        ref_text = f"Ты уже пригласил {len(user.referals_ids)} человек\nВот ваша {ref_link}"
    elif 1 <= len(user.referals_ids) % 10 < 5:
        ref_text = f"Ты уже пригласил {len(user.referals_ids)} человека\nВот ваша {ref_link}"
    else:
        ref_text = f"Ты уже пригласил {len(user.referals_ids)} человек\nВот ваша {ref_link}"

    try:
        if user.referer_id:
            referer_chat = await bot.get_chat(user.referer_id)
            ref_text += f'\nВас пригласил @{referer_chat.username}\n\n'
    except Exception:
        pass

    if isinstance(obj, types.Message):
        # await obj.answer(replies['profile']['profile'].format(user.id, user.name, '\\'+user.phone if user.phone.startswith('+') else user.phone, user.points, ref_text), reply_markup=profile_kb())
        await obj.answer(replies['profile']['referal'].format(ref_text), reply_markup=referal_kb(), parse_mode='HTML')
    elif isinstance(obj, types.CallbackQuery):
        # await obj.message.edit_text(replies['profile']['profile'].format(user.id, user.name, '\\'+user.phone if user.phone.startswith('+') else user.phone, user.points, ref_text), reply_markup=profile_kb())
        await obj.message.edit_text(replies['profile']['referal'].format(ref_text), reply_markup=referal_kb(), parse_mode='HTML')

        await obj.answer()
