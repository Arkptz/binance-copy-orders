from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from Tg_Bot.bot import bot, dp
from Tg_Bot.decors import admin
from Tg_Bot.states import Select_account, AddExpenditure
from Tg_Bot.keyboards import kbd
from Tg_Bot.handlers import back_to_menu
from DB import AccountFirstLvlDb, SessionDb, AccountsDb, AccountSecondLvlDb, BotStatusDb
from Binance_connect import Account_1Lvl, generate_account_to_work
import multiprocessing as mp

proc_list:list[mp.Process] = []

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
        args = generate_account_to_work(i)
        pr = mp.Process(target=process, args =[args])
        pr.start()
        proc_list.append(pr)
    
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
    for i in proc_list:
        i.kill()
    
    bot_status = SessionDb.query(BotStatusDb).filter(
            BotStatusDb.user_id == user_id).first()
    bot_status.status = False
    SessionDb.commit()
    await back_to_menu(cq)
