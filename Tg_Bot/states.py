from aiogram.dispatcher.filters.state import StatesGroup, State


class Select_account(StatesGroup):
    account_id_1lvl = State()
    account_id_2lvl = State()

class AddExpenditure(StatesGroup):
    product = State()
    flow_direction = State()
    count = State()
    price = State()

