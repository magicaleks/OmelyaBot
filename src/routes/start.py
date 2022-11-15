from aiogram import types, Router, Bot
from aiogram.filters.command import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType

from ..utils import check_user
from ..db.database import db
from ..config import config

from ..replies import replies
from ..misc.keyboards import (
    menu_kb,
    clear_kb,
    signup_kb
)


start_router = Router()


@start_router.message(CommandStart())
async def start_command(m: types.Message, state: FSMContext, bot: Bot) -> None:
    user = await db.get_user(m.from_user.id)
    if user:
        data = await state.get_data()
        if not data.get('new_user', False):
            await m.answer(replies['menu']['menu'], reply_markup=menu_kb())
            await state.clear()
    else:
        await m.answer(replies['start']['greeting'])
        user = await db.create_user(m.from_user.id)
        if ' ' in m.text:
            try:
                referer_id = int(m.text.split(' ')[1])
                referer = await db.get_user(referer_id)
                if user.id != referer_id and referer:
                    user.referer_id = referer_id
                    await db.update_user(user)

                    u_referer = await bot.get_chat(referer.id)
                    await m.answer(replies['start']['had_referer'].format(u_referer.username))

                    referer = await db.get_user(referer_id)
                    referer.add_referal(user.id)
                    await db.update_user(referer)
            except Exception:
                pass

        await m.answer(replies['start']['signup'], reply_markup=signup_kb())


@start_router.message(Command(commands='how', commands_ignore_case=True))
async def instruction(m: types.Message, state: FSMContext):
    flag = await check_user(m.from_user.id)
    if not flag:
        return

    await state.clear()
    if m.from_user.id in config['bot']['admins']:
        await m.answer(replies['start']['admin_instruction'])
    else:
        await m.answer(replies['start']['instruction'])


@start_router.message(content_types=[ContentType.CONTACT])
async def signup(m: types.Message, state: FSMContext):
    user = await db.get_user(m.from_user.id)
    if not user:
        await m.answer("Пожалуйста, начните работу с ботом с команды /start :)")
        return
    if not user.phone:
        user.phone = m.contact.phone_number
        user.name = m.from_user.full_name
        await db.update_user(user)
        await m.answer(replies['start']['signup_completed'], reply_markup=clear_kb())
        await m.answer(replies['menu']['menu'].format(user.name), reply_markup=menu_kb())


@start_router.message()
async def cap(m: types.Message):
    await m.answer('Я не знаю такой команды, озакомьтесь с инструкций /how и попробуйте ещё раз')
