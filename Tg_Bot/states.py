from aiogram.dispatcher.filters.state import StatesGroup, State


class Select_account(StatesGroup):
    account_id_1lvl = State()
    account_1lvl_menu = State()
    account_id_2lvl = State()
    account_2lvl_menu = State()
    new_api_key = State()
    new_api_secret = State()
    new_name = State()
    new_account = State()
    new_multiplicator = State()

class AddExpenditure(StatesGroup):
    product = State()
    flow_direction = State()
    count = State()
    price = State()

