from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from Tg_Bot.bot import bot, dp
from Tg_Bot.decors import admin
from Tg_Bot.states import Select_account, AddExpenditure
from Tg_Bot.keyboards import kbd
from Tg_Bot.handlers import back_to_menu
from DB import AccountFirstLvlDb, SessionDb, AccountsDb, AccountSecondLvlDb

import traceback


@dp.callback_query_handler(text='add_account', state=[Select_account.account_id_1lvl])
@admin
async def add_account(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    await state.update_data(msg=msg, lvl=1)
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id,
                                text='Окей, отправь аккаунт в таком формате: api_key:api_secret:имя аккаунта', reply_markup=kbd.single_back())
    await Select_account.new_account.set()


@dp.callback_query_handler(text='add_account', state=[Select_account.account_id_2lvl])
@admin
async def add_account(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    await state.update_data(msg=msg, lvl=2)
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id,
                                text='Окей, отправь аккаунт в таком формате: api_key:api_secret:имя аккаунта:мультпликатор(не целые числа через точку)', reply_markup=kbd.single_back())
    await Select_account.new_account.set()


@dp.message_handler(state=Select_account.new_account)
@admin
async def add_account(msg: Message, state: FSMContext):
    new_acc = msg.text.split(':')
    user_id = msg.chat.id
    await bot.delete_message(chat_id=user_id, message_id=msg.message_id)
    data = await state.get_data()
    msg_ = data['msg']
    lvl = data['lvl']
    ln = len(new_acc)
    float_ch = False
    if ln ==4:
        try:
            float(new_acc[3])
        except:
            float_ch =True
    if ln < 3 or ln >4 or float_ch:
        await bot.edit_message_text(chat_id=user_id, message_id=msg_.message_id,
                                    text=f'Неверный формат - "{msg.text}\n'
                                    'Попробуй ещё раз:', reply_markup=kbd.single_back())
        return ''
    account = AccountsDb(
        user_id=user_id, name_account=new_acc[2], api_key=new_acc[0], api_secret=new_acc[1])
    if lvl == 1:
        account.account = AccountFirstLvlDb()
    elif lvl == 2:
        account.account_2lvl = AccountSecondLvlDb(
            parent_id=data['account_id_1lvl'], multiplicator=float(new_acc[3]))
    SessionDb.add(account)
    SessionDb.commit()
    au = account
    if lvl == 1:
        await state.update_data(account_id_1lvl=account.id)
    elif lvl == 2:
        await state.update_data(account_id_2lvl=account.id)
    txt = 'Аккаунт успешно добавлен!\n'
    txt2 = f'\n    Мультипликатор аккаунта: {account.account_2lvl.multiplicator}' if lvl == 2 else ''
    await bot.edit_message_text(chat_id=user_id, message_id=msg_.message_id,
                                text=txt + f'О аккаунте:\n'
                                f'    Имя акканта: {au.name_account}\n'
                                f'    api_key аккаунта: {au.api_key}\n'
                                f'    api_secret аккаунта: {au.api_secret}' + txt2, reply_markup=kbd.account_markup(lvl1=lvl == 1))
    if lvl == 1:
        await Select_account.account_1lvl_menu.set()
    elif lvl == 2:
        await Select_account.account_2lvl_menu.set()
