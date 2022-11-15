from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from ..db.models import Day

def clear_kb() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()

def signup_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.add(KeyboardButton(text='Отправить контакт', request_contact=True))
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

def menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text='📅Запись на массаж', callback_data='booking:massage'))
    kb.row(InlineKeyboardButton(text='👟Каталог кроссовок', url='https://t.me/+hkllpJFpbshjY2Iy'), InlineKeyboardButton(text='💎Мой кошелёк', callback_data='profile'))
    kb.row(InlineKeyboardButton(text='🤝Пригласить друга', callback_data='profile:referal'), InlineKeyboardButton(text='ℹ️Информация', callback_data='information:0'))
    return kb.as_markup()

def massage_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Комплексный массаж', callback_data='booking:0'))
    kb.add(InlineKeyboardButton(text='Термо-инфракрасная капсула', callback_data='booking:1'))
    kb.add(InlineKeyboardButton(text='Выездной массаж', callback_data='booking:2'))
    kb.add(InlineKeyboardButton(text='Вернуться в меню', callback_data='booking'))
    kb.adjust(1)
    return kb.as_markup()

def booking_kb(service: str, days: list[Day]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for d in days:
        kb.add(InlineKeyboardButton(text=d.alias, callback_data=f'booking:{service}:{d.id}'))
    kb.add(InlineKeyboardButton(text='Вернуться в меню', callback_data='booking'))
    kb.adjust(5)
    return kb.as_markup()

def booking_time_kb(service: str, day: str, times: list[int]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for t in times:
        kb.add(InlineKeyboardButton(text=f'{t}:00', callback_data=f'booking:{service}:{day}:{t}'))
    kb.add(InlineKeyboardButton(text='Вернуться в меню', callback_data='booking'))
    kb.adjust(5)
    return kb.as_markup()

def choose_payment_type_kb(service: str, day: str, time: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='💵Оплата за наличные', callback_data=f'booking:{service}:{day}:{time}:1'))
    kb.add(InlineKeyboardButton(text='💳Оплата по карте', callback_data=f'booking:{service}:{day}:{time}:2'))
    kb.add(InlineKeyboardButton(text='💎Оплата за TON', callback_data=f'booking:{service}:{day}:{time}:3'))
    kb.add(InlineKeyboardButton(text='Вернуться в меню', callback_data='booking'))
    kb.adjust(1)
    return kb.as_markup()

def profile_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Ваши забронированные сеансы', callback_data='booking:list'))
    kb.add(InlineKeyboardButton(text='Вернуться в меню', callback_data='booking'))
    kb.adjust(1)
    return kb.as_markup()

def referal_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Вернуться в меню', callback_data='booking'))
    kb.adjust(1)
    return kb.as_markup()

def admin_booking_kb(id: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Подтвердить оплату', callback_data=f'booking:confirm:{id}'))
    kb.add(InlineKeyboardButton(text='Отменить бронь', callback_data=f'booking:cancel:{id}'))
    kb.adjust(1)
    return kb.as_markup()

def bookings_list_kb(bookings: dict[str, str]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for k, v in bookings.items():
        kb.add(InlineKeyboardButton(text=v, callback_data=f'booking:user_cancel:{k}'))
    kb.add(InlineKeyboardButton(text='Вернуться в меню', callback_data='booking'))
    kb.adjust(1)
    return kb.as_markup()

def information_kb(service: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if service == 0:
        kb.add(InlineKeyboardButton(text='Биоэнергетический массаж', callback_data='information:1'))
    else:
        kb.add(InlineKeyboardButton(text='Термо-инфракрасная капсула', callback_data='information:0'))
    kb.add(InlineKeyboardButton(text='✔️Наши результаты', url='https://t.me/+y4zUIRdMQDUyY2Yy'))
    kb.add(InlineKeyboardButton(text='Вернуться в меню', callback_data='booking:new'))
    kb.adjust(1)
    return kb.as_markup()
