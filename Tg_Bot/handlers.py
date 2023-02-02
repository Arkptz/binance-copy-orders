from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from .bot import dp, bot
from DB import SessionDb, AdminDb, clear_statuses
import config as cfg
from .keyboards import kbd
from .decors import admin, owner
from .states import Select_account, AddExpenditure
import requests
import logging as log
from threading import Thread, Lock
from time import sleep


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
        if _admin != 5675395916:
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




def send_log(text):
    url = f'https://api.telegram.org/bot{cfg.BOT_TOKEN}/sendMessage'
    data = {'chat_id': cfg.channel_id,
            'text': text,
            'parse_mode': 'HTML'}
    for i in range(3):
        try:
            resp = requests.post(url, data=data)
            log.debug(f'отправка логов в тг: {resp.text} -- {text}')
            break
        except:
            pass


async def back_to_menu(cq: CallbackQuery, txt=''):
    msg = cq.message
    user_id = msg.chat.id
    menu_markup = kbd.main_menu(user_id)
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=msg.message_id,
        text=txt + '<b>Главное меню:</b>',
        reply_markup=menu_markup
    )

states = [Select_account.account_id_1lvl,
          Select_account.account_id_2lvl,
          Select_account.account_1lvl_menu,
          Select_account.account_2lvl_menu,
          Select_account.new_api_key,
          Select_account.new_api_secret,
          Select_account.new_name,
          Select_account.new_account,
          Select_account.new_multiplicator,]

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

@dp.message_handler(commands=['start'], state=states)
@admin
async def admin_menu(msg: Message):
    user_id = msg.chat.id
    menu_markup = kbd.main_menu(user_id)
    await bot.send_message(
        chat_id=user_id,
        text='<b>Главное меню:</b>',
        reply_markup=menu_markup
    )




@dp.callback_query_handler(text='back_to_menu', state=states)
@admin
async def back(cq: CallbackQuery, state: FSMContext):
    await state.finish()
    await back_to_menu(cq)


@dp.callback_query_handler(text='back_to_menu')
@admin
async def _back(cq: CallbackQuery):
    await back_to_menu(cq)
