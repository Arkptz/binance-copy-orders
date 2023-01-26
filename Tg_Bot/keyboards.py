from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import config as cfg
from DB import SessionDb, AccountFirstLvlDb, AccountSecondLvlDb, BotStatusDb, AccountsDb


class Keyboards:
    butt_on_page = 20

    def __init__(self):
        self.btn_back_to_menu = InlineKeyboardButton(
            text='↩️Главное меню',
            callback_data='back_to_menu'
        )

    def single_back(self):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.insert(self.btn_back_to_menu)
        return markup

    def back_with_back_to_menu(self, back_ref=''):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.row(InlineKeyboardButton(
            text='⬅️Назад', callback_data=back_ref))
        markup.insert(self.btn_back_to_menu)
        return markup

    def account_markup(self, lvl1=True, back_ref='//'):
        markup = InlineKeyboardMarkup(row_width=2)
        markup.insert(InlineKeyboardButton(
            text='⚒Поменять api_key', callback_data='replace_api_key'))
        markup.insert(InlineKeyboardButton(
            text='⚒Поменять api_secret', callback_data='replace_api_secret'))
        markup.insert(InlineKeyboardButton(
            text='⚒Поменять имя аккаунта', callback_data='replace_name'))
        if lvl1:
            markup.row(InlineKeyboardButton(
                text='Посмотреть аккаунты, на которые копируем', callback_data='view_2lvl_accounts'))
        else:
            markup.insert(InlineKeyboardButton(
                text='⚒Поменять мультипликатор', callback_data='replace_multiplicator'))
        markup.row(InlineKeyboardButton(
            text='❌Удалить', callback_data='delete_account'))
        markup.row(InlineKeyboardButton(
            text='⬅️Назад', callback_data=back_ref))
        markup.row(self.btn_back_to_menu)
        return markup

    def main_menu(self, user_id: int):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.insert(InlineKeyboardButton(
            text='Мои аккаунты', callback_data='my_accounts'))
        markup.insert(self.btn_to_setup_bot(user_id))
        return markup

    def btn_to_setup_bot(self, user_id: int) -> InlineKeyboardButton:
        """Keyboard on or off bot."""
        bot_status = SessionDb.query(BotStatusDb).filter(
            BotStatusDb.user_id == user_id).first()
        btn_on = InlineKeyboardButton(
            text='✅Бот включен',
            callback_data=f'Bot_off'
        )

        btn_off = InlineKeyboardButton(
            text='⛔️Бот отключен',
            callback_data=f'Bot_on'
        )

        if bot_status.status:
            return btn_on
        else:
            return btn_off

    def all_accounts_1lvl(self, user_id: int, page=0):
        markup = InlineKeyboardMarkup(row_width=2)
        start = page * 20
        end = start+self.butt_on_page
        try:
            accs = SessionDb.query(AccountsDb).filter(
                AccountsDb.account != None, AccountsDb.user_id == int(user_id)).all()
        except Exception as e:
            print(e)
            accs = []
        select_accs = accs[start:end]
        next_page = accs[end:end+self.butt_on_page]
        for account in select_accs:
            markup.insert(InlineKeyboardButton(text=account.name_account,
                          callback_data=f'select_account_1lvl_{account.id}'))
        markup.row(InlineKeyboardButton(
            text='------------------------------------------', callback_data='.....'))
        footer = []
        markup.row(InlineKeyboardButton(
            text='➕Добавить аккаунт', callback_data='add_account'))
        if page != 0:
            footer.append(InlineKeyboardButton(
                text='⬅️Предыдущая страница', callback_data=f'replace_page_{page-1}'))
        footer.append(InlineKeyboardButton(
            text=f'Стр. №{page+1}', callback_data=f'{page}'))
        if len(next_page) > 0:
            footer.append(InlineKeyboardButton(
                text='➡️Следующая страница', callback_data=f'replace_page_{page+1}'))
        markup.row(*footer)
        markup.row(self.btn_back_to_menu)
        return markup

    def all_accounts_2lvl(self, account_1lvl_id: int, page=0):
        markup = InlineKeyboardMarkup(row_width=2)
        start = page * 20
        end = start+self.butt_on_page
        accs: AccountsDb = SessionDb.get(AccountsDb, account_1lvl_id)
        accs = accs.account.Second_levels_accounts
        select_accs = accs[start:end]
        next_page = accs[end:end+self.butt_on_page]
        for account in select_accs:
            markup.insert(InlineKeyboardButton(text=account.account_info.name_account,
                          callback_data=f'select_account_2lvl_{account.account_id}'))
        markup.row(InlineKeyboardButton(
            text='------------------------------------------', callback_data='.....'))
        footer = []
        markup.row(InlineKeyboardButton(
            text='➕Добавить аккаунт', callback_data='add_account'))
        if page != 0:
            footer.append(InlineKeyboardButton(
                text='⬅️Предыдущая страница', callback_data=f'replace_page_{page-1}'))
        footer.append(InlineKeyboardButton(
            text=f'Стр. №{page+1}', callback_data=f'{page}'))
        if len(next_page) > 0:
            footer.append(InlineKeyboardButton(
                text='➡️Следующая страница', callback_data=f'replace_page_{page+1}'))
        markup.row(*footer)
        markup.row(self.btn_back_to_menu)
        return markup


kbd = Keyboards()
