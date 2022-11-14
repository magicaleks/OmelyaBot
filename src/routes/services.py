import datetime
import time
from aiogram import types, Bot, Router
from aiogram.filters.command import Command
from ..replies import replies
from ..utils import check_user

from ..misc.keyboards import (
    menu_kb,
    massage_kb,
    booking_kb,
    booking_time_kb,
    choose_payment_type_kb,
    admin_booking_kb,
    bookings_list_kb
)

from ..db.database import db
from ..config import config
from ..db.models import PaymentTypes
from ..config import config

services_router = Router()


@services_router.message(Command(commands='booking', commands_ignore_case=True))
@services_router.callback_query(text='booking')
async def menu(obj):
    flag = await check_user(obj.from_user.id)
    if not flag:
        return
    
    if isinstance(obj, types.Message):
        await obj.answer(replies['menu']['menu'], reply_markup=menu_kb())
    elif isinstance(obj, types.CallbackQuery):
        await obj.message.edit_text(replies['menu']['menu'], reply_markup=menu_kb())

        await obj.answer()
    

@services_router.callback_query(text='booking:massage')
async def menu(obj):
    flag = await check_user(obj.from_user.id)
    if not flag:
        return
    
    if isinstance(obj, types.Message):
        await obj.answer(replies['menu']['massage'], reply_markup=massage_kb())
    elif isinstance(obj, types.CallbackQuery):
        await obj.message.edit_text(replies['menu']['massage'], reply_markup=massage_kb())

        await obj.answer()


@services_router.callback_query(text_startswith='booking:')
async def booking(call: types.CallbackQuery, bot: Bot):
    flag = await check_user(call.from_user.id)
    if not flag:
        return

    params = call.data.split(':')

    if params[1] == 'confirm':
        await db.confirm_booking(params[2])
        await call.message.edit_reply_markup(None)
        await call.answer(replies['menu']['booking_confirmed'], show_alert=True)
        return

    elif params[1] == 'cancel':
        await db.cancel_booking(params[2])
        await call.message.edit_reply_markup(None)
        await call.answer(replies['menu']['booking_cancelled'], show_alert=True)
        return
    
    elif params[1] == 'user_cancel':
        await db.cancel_booking(params[2])
        _bookings = await db.get_user_bookings(call.from_user.id)
        bookings = {}
        for b in _bookings:
            # if b.id == params[2]:
            #     continue
            day = await db.get_day(b.id.split('@')[0])
            bookings[b.id] = f'{b.massage} {day.alias}'
        await call.message.edit_reply_markup(reply_markup=bookings_list_kb(bookings))
        await call.answer(replies['menu']['booking_cancelled'], show_alert=True)
        return
    
    elif params[1] == 'list':
        _bookings = await db.get_user_bookings(call.from_user.id)
        bookings = {}
        for b in _bookings:
            day = await db.get_day(b.id.split('@')[0])
            bookings[b.id] = f'{b.massage} {day.alias}'
        await call.message.edit_text(replies['menu']['bookings_list'], reply_markup=bookings_list_kb(bookings))

    elif len(params) == 2:
        days = await db.get_days(15)
        await call.message.edit_text(replies['massage'][config['services']['massages'][int(params[1])]], reply_markup=booking_kb(params[1], days))
    elif len(params) == 3:
        day = await db.get_day(params[2])
        times = [t for t, v in day.booked[config['services']['massages'][int(params[1])]].items() if not v and (day.timestamp+int(t)*3600 > time.time())]
        await call.message.edit_text(replies['menu']['booking_hour'] if times else replies['menu']['error_booking_hour'], reply_markup=booking_time_kb(params[1], params[2], times))
    elif len(params) == 4:
        await call.message.edit_text(replies['menu']['choose_payment_type'], reply_markup=choose_payment_type_kb(params[1], params[2], params[3]))
    elif len(params) == 5:
        await call.message.edit_text(replies['menu']['menu'], reply_markup=menu_kb())
        _date = datetime.datetime.strptime(params[2], '%d/%m/%Y')
        if _date.timestamp() + int(params[3])*3600 <= time.time():
            await call.answer(replies['menu']['error_booked'], show_alert=True)
            return

        day = await db.get_day(params[2])
        user = await db.get_user(call.from_user.id)

        booking = await db.book(config['services']['massages'][int(params[1])], params[1], day.id, params[3], user.id, PaymentTypes(int(params[4])))
        payment_text = 'наличными' if params[4] == '1' else 'картой'
        for admin in config['bot']['admins']:
            await bot.send_message(admin, replies['menu']['booked_notification'].format(config['services']['massages'][int(params[1])], f'{day.alias} {params[3]}:00', user.name, user.phone, user.points, payment_text, user.id), reply_markup=admin_booking_kb(booking.id))

        await call.answer(replies['menu']['booked'], show_alert=True)
        return
    
    await call.answer()
