from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from ...bot import bot, dp
from ...decors import admin
from ...states import Select_account, AddExpenditure
from ...keyboards import kbd
from DB import AccountFirstLvlDb, SessionDb, AccountsDb
import traceback


@dp.callback_query_handler(text='replace_api_key', state=[Select_account.account_1lvl_menu, Select_account.account_2lvl_menu])
@admin
async def replace_api_key(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    data = await state.get_data()
    lvl = data["lvl"]
    id = data[f'account_id_{lvl}lvl']
    await state.update_data(msg=msg)
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id,
                                text='Окей, отправь мне новый api_key', reply_markup=kbd.back_with_back_to_menu(back_ref=f'select_account_{lvl}lvl_{id}'))
    await Select_account.new_api_key.set()


@dp.message_handler(state=Select_account.new_api_key)
@admin
async def replace_api_key(msg: Message, state: FSMContext):
    new_api_key = msg.text
    user_id = msg.chat.id
    await bot.delete_message(chat_id=user_id, message_id=msg.message_id)
    data = await state.get_data()
    msg_ = data['msg']
    lvl = data['lvl']
    account_id = data['account_id_1lvl'] if lvl == 1 else data['account_id_2lvl']
    account = SessionDb.get(AccountsDb, account_id)
    account.api_key = new_api_key
    SessionDb.commit()
    au = account
    txt = 'Api_key успешно записан!\n'
    txt2 = f'\n    Мультипликатор аккаунта: {account.account_2lvl.multiplicator}' if lvl == 2 else ''
    await bot.edit_message_text(chat_id=user_id, message_id=msg_.message_id,
                                text=txt + f'О аккаунте:\n'
                                f'    Имя акканта: {au.name_account}\n'
                                f'    api_key аккаунта: {au.api_key}\n'
                                f'    api_secret аккаунта: {au.api_secret}' + txt2, reply_markup=kbd.account_markup(lvl1=lvl == 1, back_ref='my_accounts'))
    if lvl == 1:
        await Select_account.account_1lvl_menu.set()
    elif lvl == 2:
        await Select_account.account_2lvl_menu.set()


@dp.callback_query_handler(text='replace_api_secret', state=[Select_account.account_1lvl_menu, Select_account.account_2lvl_menu])
@admin
async def replace_api_secret(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    data = await state.get_data()
    lvl = data["lvl"]
    id = data[f'account_id_{lvl}lvl']
    await state.update_data(msg=msg)
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id,
                                text='Окей, отправь мне новый api_secret', reply_markup=kbd.back_with_back_to_menu(back_ref=f'select_account_{lvl}lvl_{id}'))
    await Select_account.new_api_secret.set()


@dp.message_handler(state=Select_account.new_api_secret)
@admin
async def replace_api_secret(msg: Message, state: FSMContext):
    new_api_secret = msg.text
    user_id = msg.chat.id
    await bot.delete_message(chat_id=user_id, message_id=msg.message_id)
    data = await state.get_data()
    msg_ = data['msg']
    lvl = data['lvl']
    account_id = data['account_id_1lvl'] if lvl == 1 else data['account_id_2lvl']
    account = SessionDb.get(AccountsDb, account_id)
    account.api_secret = new_api_secret
    SessionDb.commit()
    au = account
    txt = 'Api_secret успешно записан!\n'
    txt2 = f'\n    Мультипликатор аккаунта: {account.account_2lvl.multiplicator}' if lvl == 2 else ''
    await bot.edit_message_text(chat_id=user_id, message_id=msg_.message_id,
                                text=txt + f'О аккаунте:\n'
                                f'    Имя акканта: {au.name_account}\n'
                                f'    api_key аккаунта: {au.api_key}\n'
                                f'    api_secret аккаунта: {au.api_secret}' + txt2, reply_markup=kbd.account_markup(lvl1=lvl == 1, back_ref='my_accounts'))
    if lvl == 1:
        await Select_account.account_1lvl_menu.set()
    elif lvl == 2:
        await Select_account.account_2lvl_menu.set()


@dp.callback_query_handler(text='replace_name', state=[Select_account.account_1lvl_menu, Select_account.account_2lvl_menu])
@admin
async def replace_name(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    data = await state.get_data()
    lvl = data["lvl"]
    id = data[f'account_id_{lvl}lvl']
    await state.update_data(msg=msg)
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id,
                                text='Окей, отправь мне новое имя для аккаунта', reply_markup=kbd.back_with_back_to_menu(back_ref=f'select_account_{lvl}lvl_{id}'))
    await Select_account.new_name.set()


@dp.message_handler(state=Select_account.new_name)
@admin
async def replace_name(msg: Message, state: FSMContext):
    new_name = msg.text
    user_id = msg.chat.id
    await bot.delete_message(chat_id=user_id, message_id=msg.message_id)
    data = await state.get_data()
    msg_ = data['msg']
    lvl = data['lvl']
    account_id = data['account_id_1lvl'] if lvl == 1 else data['account_id_2lvl']
    account = SessionDb.get(AccountsDb, account_id)
    account.name_account = new_name
    SessionDb.commit()
    au = account
    txt = 'Имя успешно записано!\n'
    txt2 = f'\n    Мультипликатор аккаунта: {account.account_2lvl.multiplicator}' if lvl == 2 else ''
    await bot.edit_message_text(chat_id=user_id, message_id=msg_.message_id,
                                text=txt + f'О аккаунте:\n'
                                f'    Имя акканта: {au.name_account}\n'
                                f'    api_key аккаунта: {au.api_key}\n'
                                f'    api_secret аккаунта: {au.api_secret}' + txt2, reply_markup=kbd.account_markup(lvl1=lvl == 1, back_ref='my_accounts'))
    if lvl == 1:
        await Select_account.account_1lvl_menu.set()
    elif lvl == 2:
        await Select_account.account_2lvl_menu.set()


@dp.callback_query_handler(text='replace_multiplicator', state=[Select_account.account_2lvl_menu])
@admin
async def replace_multiplicator(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    data = await state.get_data()
    lvl = data["lvl"]
    id = data[f'account_id_{lvl}lvl']
    await state.update_data(msg=msg)
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id,
                                text='Окей, отправь мне новый мультипликатор для аккаунта (не целые числа через точку)', reply_markup=kbd.back_with_back_to_menu(back_ref=f'select_account_{lvl}lvl_{id}'))
    await Select_account.new_multiplicator.set()


@dp.message_handler(state=Select_account.new_multiplicator)
@admin
async def replace_multiplicator(msg: Message, state: FSMContext):
    new_mp = msg.text
    user_id = msg.chat.id
    await bot.delete_message(chat_id=user_id, message_id=msg.message_id)
    try:
        float(new_mp)
    except:
        await bot.edit_message_text(chat_id=user_id, message_id=msg_.message_id,
                                    text=f'Неверный формат - "{msg.text}\n'
                                    'Попробуй ещё раз:', reply_markup=kbd.single_back())
        return ''
    
    data = await state.get_data()
    msg_ = data['msg']
    account_id = data['account_id_2lvl']
    account = SessionDb.get(AccountsDb, account_id)
    account.account_2lvl.multiplicator = float(new_mp)
    SessionDb.commit()
    au = account
    txt = 'Мультипликатор успешно записан!\n'
    txt2 = f'\n    Мультипликатор аккаунта: {account.account_2lvl.multiplicator}'
    await bot.edit_message_text(chat_id=user_id, message_id=msg_.message_id,
                                text=txt + f'О аккаунте:\n'
                                f'    Имя акканта: {au.name_account}\n'
                                f'    api_key аккаунта: {au.api_key}\n'
                                f'    api_secret аккаунта: {au.api_secret}' + txt2, reply_markup=kbd.account_markup(lvl1=False))

    await Select_account.account_2lvl_menu.set()
