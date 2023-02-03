from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from Tg_Bot.bot import bot, dp
from Tg_Bot.decors import owner
from Tg_Bot.keyboards import kbd
from Tg_Bot.handlers import back_to_menu, states
from Tg_Bot.states import Select_account
from DB import AccountFirstLvlDb, SessionDb, AccountsDb, AccountSecondLvlDb, BotStatusDb
from Binance_connect import Account_1Lvl, generate_account_to_work, send_log_thr
import multiprocessing as mp



@dp.message_handler(commands=['owner'])
@owner
async def owner_menu(msg: Message):
    user_id = msg.chat.id
    menu_markup = kbd.owner_menu()
    await bot.send_message(
        chat_id=user_id,
        text='<b>Owner меню:</b>',
        reply_markup=menu_markup
    )

@dp.message_handler(commands=['owner'], state=states)
@owner
async def owner_menu(msg: Message, state:FSMContext):
    user_id = msg.chat.id
    menu_markup = kbd.owner_menu()
    await bot.send_message(
        chat_id=user_id,
        text='<b>Owner меню:</b>',
        reply_markup=menu_markup
    )
    await state.finish()

@dp.callback_query_handler(text='owner_menu', state=states)
@owner
async def owner_menu(cq: CallbackQuery, state:FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    menu_markup = kbd.owner_menu()
    await bot.edit_message_text(
        chat_id=user_id, message_id=msg.message_id,
        text='<b>Owner меню:</b>',
        reply_markup=menu_markup
    )
    await state.finish()


@dp.callback_query_handler(text='owner_menu')
@owner
async def owner_menu(cq: CallbackQuery):
    msg = cq.message
    user_id = msg.chat.id
    menu_markup = kbd.owner_menu()
    await bot.edit_message_text(
        chat_id=user_id, message_id=msg.message_id,
        text='<b>Owner меню:</b>',
        reply_markup=menu_markup
    )


@dp.callback_query_handler(text='view_user_accs')
@owner
async def view_user_accs(cq: CallbackQuery):
    msg = cq.message
    user_id = msg.chat.id
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='Выбери юзера, которого хочешь посмотреть:',
                                reply_markup=kbd.user_accs())


@dp.callback_query_handler(Text(startswith='select_user_'))
@owner
async def select_user_(cq: CallbackQuery):
    msg = cq.message
    user_id = msg.chat.id
    select_user_id = int(cq.data.split('select_user_')[1])
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='Выбери аккаунт(с которого копируем):', reply_markup=kbd.all_accounts_1lvl(select_user_id, back_menu_cd='owner_menu'))
    await Select_account.account_id_1lvl.set()
    
