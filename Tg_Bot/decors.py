from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from DB import SessionDb, AdminDb
from .bot import bot
from config import owners

def admin(input_func):
    async def output_func(msg:Message|CallbackQuery, state:FSMContext):
        args = [msg, state][:input_func.__code__.co_argcount]
        if type(msg) == CallbackQuery:
            msg = msg.message  # каллбек
        list_admins = [i[0] for i in SessionDb.query(AdminDb.user_id).all()]
        if msg.chat.id in list_admins:
            await input_func(*args)
        else:
            await bot.send_message(chat_id=msg.chat.id, text='У тебя нет прав на использование')
    return output_func


def owner(input_func):
    async def output_func(msg:Message|CallbackQuery, state:FSMContext):
        args = [msg, state][:input_func.__code__.co_argcount]
        msg = args[0]
        if type(msg) == CallbackQuery:
            msg = msg.message  # каллбек
        if msg.chat.id in owners:
            await input_func(*args)
        else:
            await bot.send_message(chat_id=msg.chat.id, text='У тебя нет прав на использование')
    return output_func