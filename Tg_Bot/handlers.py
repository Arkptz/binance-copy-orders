from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from loguru import logger as log
from .bot import dp, bot
from DB import SessionDb, AdminDb, clear_statuses
import config as cfg
from .keyboards import Keyboards
from .decors import admin
from .states import Select_account, AddExpenditure

kbd = Keyboards()


async def on_startup(dp):
    """ try to add admins and create table to add MAIN admin from cfg.admin_list"""
    """ notify admins when bot started """
    log.info('send main menu')
    list_actual_admins = [i[0] for i in SessionDb.query(AdminDb.user_id).all()]
    list_admins_new = []
    for id in cfg.admin_list:
        if not id in list_actual_admins:
            ad = AdminDb(user_id=id)
            list_admins_new.append(ad)
    SessionDb.add_all(list_admins_new)
    SessionDb.commit()
    clear_statuses()
    for _admin in cfg.admin_list:
        menu_markup = kbd.main_menu(_admin)
        try:
            await bot.send_message(
                chat_id=_admin,
                text='<b>Бот запущен.</b>',
                reply_markup=menu_markup
            )
        except Exception as e:
            print(e)
            pass


@dp.message_handler(commands=['start'])
@admin
async def admin_menu(msg: Message):
    user_id = msg.chat.id
    menu_markup = kbd.main_menu(user_id)
    await bot.send_message(
        chat_id=user_id,
        text='<b>Главное меню:</b>',
        reply_markup=menu_markup
    )


async def back_to_menu(cq: CallbackQuery):
    msg = cq.message
    user_id = msg.chat.id
    menu_markup = kbd.main_menu(user_id)
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=msg.message_id,
        text='<b>Главное меню:</b>',
        reply_markup=menu_markup
    )

states = [Select_account.account_id_1lvl,
          Select_account.account_id_2lvl,
          AddExpenditure.count,
          AddExpenditure.price,
          AddExpenditure.product,
          AddExpenditure.flow_direction]


@dp.callback_query_handler(text='back_to_menu', state=states)
@admin
async def back(cq: CallbackQuery, state: FSMContext):
    await state.finish()
    await back_to_menu(cq)


@dp.callback_query_handler(text='back_to_menu')
@admin
async def _back(cq: CallbackQuery):
    await back_to_menu(cq)
