from typing import Optional, Union
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session, sessionmaker
from sqlalchemy import create_engine, MetaData, Column, Integer, String, DateTime, ForeignKey, TIMESTAMP, Table
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from config import db_path

engine = create_engine(f'sqlite:///{db_path}', echo=False,
                       connect_args={"check_same_thread": False})
conn = engine.connect()


class Base(DeclarativeBase):
    pass

class AdminDb(Base):
    __tablename__ = "Admin"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column()



class AccountFirstLvlDb(Base):
    __tablename__ = "AccountFirstLvl"
    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey('Accounts.id'))
    account_info: Mapped["AccountsDb"] = relationship(back_populates="account", cascade="all, delete-orphan", single_parent=True)

    Second_levels_accounts: Mapped[list["AccountSecondLvlDb"]] = relationship(
        back_populates="first_level", cascade="all, delete"
    )
    def __repr__(self) -> str:
        ai = self.account_info
        return f'AccountSecondLvlDb(id={self.id}, account_id = {self.account_id}, user_id={ai.user_id}, name_account={ai.name_account}, api_key ={ai.api_key}, api_secret = {ai.api_secret})'


class AccountSecondLvlDb(Base):
    __tablename__ = "AccountSecondLvl"
    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey('AccountFirstLvl.account_id'))
    account_id: Mapped[int] = mapped_column(ForeignKey('Accounts.id'))
    multiplicator: Mapped[float]  = mapped_column()
    account_info: Mapped["AccountsDb"] = relationship(back_populates="account_2lvl", cascade="all, delete-orphan", single_parent=True)
    first_level: Mapped["AccountFirstLvlDb"] = relationship(
        back_populates="Second_levels_accounts", single_parent=True, order_by=AccountFirstLvlDb.account_id)

    def __repr__(self) -> str:
        ai = self.account_info
        return f'AccountSecondLvlDb(id={self.id}, parent_id={self.parent_id}, account_id = {self.account_id}, user_id={ai.user_id}, name_account={ai.name_account}, api_key ={ai.api_key}, api_secret = {ai.api_secret})'

class AccountsDb(Base):
    __tablename__ = "Accounts"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column()
    name_account: Mapped[str] = mapped_column()
    api_key: Mapped[str] = mapped_column()
    api_secret: Mapped[str] = mapped_column()

    account: Mapped["AccountFirstLvlDb"] = relationship(back_populates="account_info", order_by=AccountFirstLvlDb.account_id, cascade="all, delete-orphan")
    account_2lvl: Mapped["AccountSecondLvlDb"] = relationship(back_populates="account_info", order_by=AccountSecondLvlDb.account_id, cascade="all, delete-orphan")


class BotStatusDb(Base):
    __tablename__ = "BotStatus"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column()
    status: Mapped[bool] = mapped_column()


class ClientOrderIdAssociationDb(Base):
    __tablename__ = "ClientOrderIdAssociation"
    id: Mapped[int] = mapped_column(primary_key=True)
    lvl_1: Mapped[int] = mapped_column()
    lvl_2: Mapped[int] = mapped_column()