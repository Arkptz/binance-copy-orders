from typing import Optional
from sqlalchemy import create_engine, MetaData, Column, Integer, String, DateTime, ForeignKey
import sqlalchemy as db
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from .models import Base, engine, AccountsDb, AccountFirstLvlDb, AccountSecondLvlDb, BotStatusDb, AdminDb


Base.metadata.create_all(engine)
SessionDb = sessionmaker(bind=engine)()

def clear_statuses():
    for i in SessionDb.query(AdminDb.user_id).all():
        ui = i[0]
        status = SessionDb.query(BotStatusDb).filter(BotStatusDb.user_id == ui).first()
        if not status:
            SessionDb.add(BotStatusDb(status=False, user_id = ui))
        else:
            SessionDb.query(BotStatusDb).filter(BotStatusDb.status == True and BotStatusDb.user_id == ui).update({BotStatusDb.status: False})
        SessionDb.commit()

for i in range(10):
    acc = AccountsDb(user_id = 1021524873, name_account=f'test_par{i}{i}', api_key='3323', api_secret='44343', account = AccountFirstLvlDb())
    SessionDb.add(acc)
    SessionDb.commit()
    ch = AccountsDb(user_id = 1021524873, name_account=f'test_chi{i}{i}', api_key='3323', api_secret='44343', account_2lvl = AccountSecondLvlDb(parent_id=acc.id))
    SessionDb.add(ch)
    SessionDb.commit()
# ac = SessionDb.get(AccountFirstLvlDb, 1)
# print(ac)
# print(ac.Second_levels_accounts)
# owner = SessionDb.get(AccountFirstLvlDb, 1)
# SessionDb.delete(owner)
# SessionDb.commit()
# test = ProductDb(product_name='Сыр2')
# test2 = ProductDb(product_name='молоко2')
# flow_list = [FlowDb(
#     flow_exp='дом'), FlowDb(flow_exp='дом2'), FlowDb(
#     flow_exp='дом3'), FlowDb(flow_exp='дом4')]
# SessionDb.add_all([test, test2, *flow_list])
# print(SessionDb.query(ProductDb).all())
# # session.add_all([test, test2])
# SessionDb.commit()
