from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from Tg_Bot.bot import bot, dp
from Tg_Bot.decors import admin, owner
from Tg_Bot.states import Select_account, AddExpenditure
from Tg_Bot.keyboards import kbd
from Tg_Bot.handlers import back_to_menu
from DB import AccountFirstLvlDb, SessionDb, AccountsDb, AccountSecondLvlDb, BotStatusDb
from Binance_connect import Account_1Lvl, generate_account_to_work, send_log_thr
import multiprocessing as mp

proc_list:dict[int, dict[str, mp.Process]] = {}

def process(args:list):
    acc = Account_1Lvl(*args)
    acc.inizialize()
    acc.start_polling()

@dp.callback_query_handler(text='Bot_on')
@admin
async def Bot_on(cq: CallbackQuery):
    msg = cq.message
    user_id = msg.chat.id
    accs:list[AccountsDb] = SessionDb.query(AccountsDb).filter(
                AccountsDb.account != None, AccountsDb.user_id == int(user_id)).all()
    for i in accs:
        send_log_thr(f'{i.name_account} -- Запуск процесса')
        args = generate_account_to_work(i)
        pr = mp.Process(target=process, args =[args])
        pr.start()
        proc_list[user_id][i.name_account] = pr
    
    bot_status = SessionDb.query(BotStatusDb).filter(
            BotStatusDb.user_id == user_id).first()
    bot_status.status = True
    SessionDb.commit()
    await back_to_menu(cq)


@dp.callback_query_handler(text='Bot_off')
@admin
async def Bot_on(cq: CallbackQuery):
    msg = cq.message
    user_id = msg.chat.id
    if user_id in proc_list:
        for pr in proc_list[user_id]:
            send_log_thr(f'{pr} -- Выключение процесса')
            proc_list[user_id][pr].kill()
        del proc_list[user_id]
    
    bot_status = SessionDb.query(BotStatusDb).filter(
            BotStatusDb.user_id == user_id).first()
    bot_status.status = False
    SessionDb.commit()
    await back_to_menu(cq)


@dp.callback_query_handler(Text(startswith='Bot_on_owner_'))
@owner
async def Bot_on(cq: CallbackQuery):
    msg = cq.message
    user_id = int(cq.data.split('Bot_on_owner_')[1])
    accs:list[AccountsDb] = SessionDb.query(AccountsDb).filter(
                AccountsDb.account != None, AccountsDb.user_id == int(user_id)).all()
    for i in accs:
        send_log_thr(f'{i.name_account} -- Запуск процесса')
        args = generate_account_to_work(i)
        pr = mp.Process(target=process, args =[args])
        pr.start()
        proc_list[user_id] = {}
        proc_list[user_id][i.name_account] = pr
    
    bot_status = SessionDb.query(BotStatusDb).filter(
            BotStatusDb.user_id == user_id).first()
    bot_status.status = True
    SessionDb.commit()
    await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text='Выбери юзера, которого хочешь посмотреть:',
                                reply_markup=kbd.user_accs())



@dp.callback_query_handler(Text(startswith='Bot_off_owner_'))
@owner
async def Bot_on(cq: CallbackQuery):
    msg = cq.message
    user_id = int(cq.data.split('Bot_off_owner_')[1])
    if user_id in proc_list:
        for pr in proc_list[user_id]:
            send_log_thr(f'{pr} -- Выключение процесса')
            proc_list[user_id][pr].kill()
        del proc_list[user_id]
    
    bot_status = SessionDb.query(BotStatusDb).filter(
            BotStatusDb.user_id == user_id).first()
    bot_status.status = False
    SessionDb.commit()
    await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text='Выбери юзера, которого хочешь посмотреть:',
                                reply_markup=kbd.user_accs())