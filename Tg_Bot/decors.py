from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from DB import SessionDb, AdminDb
from .bot import bot


def admin(input_func):
    async def output_func(*args, **kwargs):
        msg = args[0]
        if type(msg) != Message:
            msg = msg.message  # каллбек
        list_admins = [i[0] for i in SessionDb.query(AdminDb.user_id).all()]
        if msg.chat.id in list_admins:
            try:
                await input_func(*args)
            except:
                await input_func(state=kwargs['state'], *args)
        else:
            await bot.send_message(chat_id=msg.chat.id, text='У тебя нет прав на использование')
    return output_func