from .accounts import Account_1Lvl, Account_2Lvl
from DB import SessionDb, AccountsDb, AccountFirstLvlDb


def generate_account_to_work(acc:AccountsDb, only_check=False) -> list:
    au_1 = acc
    lvl2_accs = acc.account.Second_levels_accounts
    lst = []
    for i in lvl2_accs:
        au = i.account_info
        lst.append(Account_2Lvl(name_account =au.name_account, api_key=au.api_key, secret=au.api_secret, multiplicator=i.multiplicator, only_check=only_check))
    
    return [au_1.name_account, au_1.api_key, au_1.api_secret, lst]