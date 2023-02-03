from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from ...bot import bot, dp
from ...decors import admin
from ...states import Select_account, AddExpenditure
from ...keyboards import kbd
from Tg_Bot.handlers import back_to_menu
from DB import AccountFirstLvlDb, SessionDb, AccountsDb
from Binance_connect import Account_1Lvl, generate_account_to_work
import traceback


@dp.callback_query_handler(text='my_accounts')
@admin
async def select_ac_1lvl_(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    await state.update_data(page=0)
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='Выбери аккаунт(с которого копируем):', reply_markup=kbd.all_accounts_1lvl(user_id))
    await Select_account.account_id_1lvl.set()


@dp.callback_query_handler(text='my_accounts', state=Select_account.account_1lvl_menu)
@admin
async def select_ac_1lvl_(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    await state.update_data(page=0)
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='Выбери аккаунт(с которого копируем):', reply_markup=kbd.all_accounts_1lvl(user_id))
    await Select_account.account_id_1lvl.set()


@dp.callback_query_handler(Text(startswith='select_account_1lvl_'), state=[Select_account.account_id_1lvl,
                                                                           Select_account.new_api_key,
                                                                           Select_account.new_api_secret,
                                                                           Select_account.new_name,
                                                                           Select_account.account_id_2lvl,
                                                                           ])
@admin
async def account_1lvl_menu(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    account_id_1lvl = int(cq.data.split('select_account_1lvl_')[1])
    await state.update_data(account_id_1lvl=account_id_1lvl, lvl=1)
    account = SessionDb.get(AccountsDb, account_id_1lvl)
    au = account
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id,
                                text=f'О аккаунте:\n'
                                     f' Имя акканта: {au.name_account}\n'
                                     f' api_key аккаунта: {au.api_key}\n'
                                     f' api_secret аккаунта: {au.api_secret}', reply_markup=kbd.account_markup(back_ref='my_accounts'))
    await Select_account.account_1lvl_menu.set()


@dp.callback_query_handler(Text(startswith='check_balance'), state=Select_account.account_1lvl_menu)
@admin
async def check_balance(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    data = await state.get_data()
    account_id_1lvl = data['account_id_1lvl']
    au = SessionDb.get(AccountsDb, account_id_1lvl)
    info = generate_account_to_work(au, only_check=True)
    text = Account_1Lvl(*info).check_balance()
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id,
                                text=f'О аккаунте:\n'
                                     f' Имя акканта: {au.name_account}\n'
                                     f' api_key аккаунта: {au.api_key}\n'
                                     f' api_secret аккаунта: {au.api_secret}\n'+text, reply_markup=kbd.account_markup(back_ref='my_accounts'))
    await Select_account.account_1lvl_menu.set()


@dp.callback_query_handler(text='view_2lvl_accounts', state=[Select_account.account_1lvl_menu,
                                                             Select_account.account_2lvl_menu])
@admin
async def view_2lvl_accounts(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    data = await state.get_data()
    account_id_1lvl = data['account_id_1lvl']
    await state.update_data(page=0)
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='Выбери аккаунт(с которого копируем):', reply_markup=kbd.all_accounts_2lvl(account_id_1lvl, back_ref=f'select_account_1lvl_{account_id_1lvl}'))
    await Select_account.account_id_2lvl.set()


@dp.callback_query_handler(Text(startswith='select_account_2lvl_'), state=[Select_account.account_id_2lvl,
                                                                           Select_account.new_api_key,
                                                                           Select_account.new_api_secret,
                                                                           Select_account.new_name,
                                                                           Select_account.new_multiplicator,
                                                                           ])
@admin
async def select_ac_2lvl_(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    account_id_2lvl = int(cq.data.split('select_account_2lvl_')[1])
    await state.update_data(account_id_2lvl=account_id_2lvl, lvl=2)
    account = SessionDb.get(AccountsDb, account_id_2lvl)
    au = account
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id,
                                text=f'О аккаунте:\n'
                                     f' Имя акканта: {au.name_account}\n'
                                     f' api_key аккаунта: {au.api_key}\n'
                                     f' api_secret аккаунта: {au.api_secret}', reply_markup=kbd.account_markup(lvl1=False, back_ref='view_2lvl_accounts'))
    await Select_account.account_2lvl_menu.set()


@dp.callback_query_handler(text='delete_account', state=[Select_account.account_1lvl_menu, Select_account.account_2lvl_menu])
@admin
async def delete_account(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    data = await state.get_data()
    lvl = data['lvl']
    account_id = data['account_id_1lvl'] if lvl == 1 else data['account_id_2lvl']
    account = SessionDb.get(AccountsDb, account_id)
    SessionDb.delete(account)
    SessionDb.commit()
    await state.finish()
    await back_to_menu(cq, txt='Аккаунт успешно удалён!\n')


@dp.callback_query_handler(Text(startswith='replace_page_'), state=Select_account.account_id_1lvl)
@admin
async def replace_page_(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    page_new = int(cq.data.split('replace_page_')[1])
    await state.update_data(page_1lvl=page_new)
    await bot.edit_message_reply_markup(chat_id=user_id, message_id=msg.message_id, reply_markup=kbd.all_accounts_1lvl(user_id, page=page_new))


@dp.callback_query_handler(Text(startswith='replace_page_'), state=Select_account.account_id_2lvl)
@admin
async def replace_page_(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    data = await state.get_data()
    page_new = int(cq.data.split('replace_page_')[1])
    await state.update_data(page_2lvl=page_new)
    await bot.edit_message_reply_markup(chat_id=user_id, message_id=msg.message_id,
                                        reply_markup=kbd.all_accounts_2lvl(account_1lvl_id=data['account_id_1lvl'],
                                                                           page=page_new, back_ref=f'select_account_1lvl_{data["account_id_1lvl"]}'))
