from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from ..bot import bot, dp
from ..decors import admin
from ..states import Select_account, AddExpenditure
from ..keyboards import kbd
from DB import AccountFirstLvlDb, SessionDb
import traceback


@dp.callback_query_handler(text='my_accounts')
@admin
async def select_ac_1lvl_(cq: CallbackQuery, state:FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    await state.update_data(page=0)
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='Выбери аккаунт(с которого копируем):', reply_markup=kbd.all_accounts_1lvl(user_id))
    await Select_account.account_id_1lvl.set()


@dp.callback_query_handler(Text(startswith='select_account_1lvl_'), state=Select_account.account_id_1lvl)
@admin
async def select_ac_2lvl_(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    account_id_1lvl = int(cq.data.split('select_account_1lvl_')[1])
    await state.update_data(account_id_1lvl=account_id_1lvl)
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='Выбери аккаунт на который копируем:', reply_markup=kbd.all_accounts_2lvl(account_1lvl_id=account_id_1lvl))
    await Select_account.next()


@dp.callback_query_handler(Text(startswith='select_account_2lvl_'), state=Select_account.account_id_2lvl)
@admin
async def select_ac_2lvl_(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    account_id_2lvl = int(cq.data.split('select_account_2lvl_')[1])
    await state.update_data(account_id_2lvl=account_id_2lvl)




@dp.callback_query_handler(Text(startswith='replace_page_'), state=Select_account.account_id_1lvl)
@admin
async def replace_page_(cq: CallbackQuery, state:FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    page_new = int(cq.data.split('replace_page_')[1])
    await state.update_data(page_1lvl=page_new)
    await bot.edit_message_reply_markup(chat_id=user_id, message_id=msg.message_id, reply_markup=kbd.all_accounts_1lvl(user_id, page=page_new))


@dp.callback_query_handler(Text(startswith='replace_page_'), state=Select_account.account_id_2lvl)
@admin
async def replace_page_(cq: CallbackQuery, state:FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    data = await state.get_data()
    page_new = int(cq.data.split('replace_page_')[1])
    await state.update_data(page_2lvl=page_new)
    await bot.edit_message_reply_markup(chat_id=user_id, message_id=msg.message_id, reply_markup=kbd.all_accounts_2lvl(account_1lvl_id=data['account_id_1lvl'], page=page_new))