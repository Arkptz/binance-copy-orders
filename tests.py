# from main import ORDERTRADEUPDATE
# from DB import db_connector

# short = {'e': 'ORDER_TRADE_UPDATE', 'T': 1674496521960, 'E': 1674496521963, 'o': {'s': 'BTCUSDT', 'c': 'web_D0wuri6Xl5NYjjdtseYW', 'S': 'SELL', 'o': 'MARKET', 'f': 'GTC', 'q': '0.001', 'p': '0', 'ap': '0', 'sp': '0', 'x': 'NEW', 'X': 'NEW',
#                                                                                   'i': 110986342950, 'l': '0', 'z': '0', 'L': '0', 'T': 1674496521960, 't': 0, 'b': '0', 'a': '0', 'm': False, 'R': False, 'wt': 'CONTRACT_PRICE', 'ot': 'MARKET', 'ps': 'BOTH', 'cp': False, 'rp': '0', 'pP': False, 'si': 0, 'ss': 0}}
# tp = {'e': 'ORDER_TRADE_UPDATE', 'T': 1674496560252, 'E': 1674496560256, 'o': {'s': 'BTCUSDT', 'c': 'web_tv9AQtixv5kbexa5KGq3', 'S': 'BUY', 'o': 'TAKE_PROFIT_MARKET', 'f': 'GTE_GTC', 'q': '0', 'p': '0', 'ap': '0', 'sp': '20000', 'x': 'NEW',
#                                                                                'X': 'NEW', 'i': 110986571331, 'l': '0', 'z': '0', 'L': '0', 'T': 1674496560252, 't': 0, 'b': '0', 'a': '0', 'm': False, 'R': True, 'wt': 'MARK_PRICE', 'ot': 'TAKE_PROFIT_MARKET', 'ps': 'BOTH', 'cp': True, 'rp': '0', 'pP': False, 'si': 0, 'ss': 0}}
# sl = {'e': 'ORDER_TRADE_UPDATE', 'T': 1674496613421, 'E': 1674496613426, 'o': {'s': 'BTCUSDT', 'c': 'web_QU3I8EVsznRImuLxqK3q', 'S': 'BUY', 'o': 'STOP_MARKET', 'f': 'GTE_GTC', 'q': '0', 'p': '0', 'ap': '0', 'sp': '25000', 'x': 'NEW',
#                                                                                'X': 'NEW', 'i': 110986926983, 'l': '0', 'z': '0', 'L': '0', 'T': 1674496613421, 't': 0, 'b': '0', 'a': '0', 'm': False, 'R': True, 'wt': 'MARK_PRICE', 'ot': 'STOP_MARKET', 'ps': 'BOTH', 'cp': True, 'rp': '0', 'pP': False, 'si': 0, 'ss': 0}}
# cl_tp = {'e': 'ORDER_TRADE_UPDATE', 'T': 1674496652318, 'E': 1674496652323, 'o': {'s': 'BTCUSDT', 'c': 'web_tv9AQtixv5kbexa5KGq3', 'S': 'BUY', 'o': 'TAKE_PROFIT_MARKET', 'f': 'GTE_GTC', 'q': '0', 'p': '0', 'ap': '0', 'sp': '20000', 'x': 'CANCELED',
#                                                                                   'X': 'CANCELED', 'i': 110986571331, 'l': '0', 'z': '0', 'L': '0', 'T': 1674496652318, 't': 0, 'b': '0', 'a': '0', 'm': False, 'R': True, 'wt': 'MARK_PRICE', 'ot': 'TAKE_PROFIT_MARKET', 'ps': 'BOTH', 'cp': True, 'rp': '0', 'pP': False, 'si': 0, 'ss': 0}}
# cl_sl = {'e': 'ORDER_TRADE_UPDATE', 'T': 1674496684065, 'E': 1674496684069, 'o': {'s': 'BTCUSDT', 'c': 'web_QU3I8EVsznRImuLxqK3q', 'S': 'BUY', 'o': 'STOP_MARKET', 'f': 'GTE_GTC', 'q': '0', 'p': '0', 'ap': '0', 'sp': '25000', 'x': 'CANCELED',
#                                                                                   'X': 'CANCELED', 'i': 110986926983, 'l': '0', 'z': '0', 'L': '0', 'T': 1674496684065, 't': 0, 'b': '0', 'a': '0', 'm': False, 'R': True, 'wt': 'MARK_PRICE', 'ot': 'STOP_MARKET', 'ps': 'BOTH', 'cp': True, 'rp': '0', 'pP': False, 'si': 0, 'ss': 0}}
# tr_sl = {'e': 'ORDER_TRADE_UPDATE', 'T': 1674496737497, 'E': 1674496737501, 'o': {'s': 'BTCUSDT', 'c': 'web_1Fx8ch7RpPQm44LKgWMp', 'S': 'SELL', 'o': 'TRAILING_STOP_MARKET', 'f': 'GTC', 'q': '0.015', 'p': '0', 'ap': '0', 'sp': '21854.75', 'x': 'NEW', 'X': 'NEW',
#                                                                                   'i': 110987662941, 'l': '0', 'z': '0', 'L': '0', 'T': 1674496737497, 't': 0, 'b': '0', 'a': '0', 'm': False, 'R': False, 'wt': 'MARK_PRICE', 'ot': 'TRAILING_STOP_MARKET', 'ps': 'BOTH', 'cp': False, 'AP': '24000', 'cr': '5.0', 'rp': '0', 'pP': True, 'si': 0, 'ss': 0}}
# cl_tr_sl = {'e': 'ORDER_TRADE_UPDATE', 'T': 1674496762229, 'E': 1674496762235, 'o': {'s': 'BTCUSDT', 'c': 'web_1Fx8ch7RpPQm44LKgWMp', 'S': 'SELL', 'o': 'TRAILING_STOP_MARKET', 'f': 'GTC', 'q': '0.015', 'p': '0', 'ap': '0', 'sp': '21854.75', 'x': 'CANCELED', 'X': 'CANCELED',
#                                                                                      'i': 110987662941, 'l': '0', 'z': '0', 'L': '0', 'T': 1674496762229, 't': 0, 'b': '0', 'a': '0', 'm': False, 'R': False, 'wt': 'MARK_PRICE', 'ot': 'TRAILING_STOP_MARKET', 'ps': 'BOTH', 'cp': False, 'AP': '24000', 'cr': '5.0', 'rp': '0', 'pP': True, 'si': 0, 'ss': 0}}
# cl_short = {'e': 'ORDER_TRADE_UPDATE', 'T': 1674496832606, 'E': 1674496832611, 'o': {'s': 'BTCUSDT', 'c': 'web_KDTDExy73NXcSK0zhZch', 'S': 'BUY', 'o': 'MARKET', 'f': 'GTC', 'q': '0.001', 'p': '0', 'ap': '0', 'sp': '0', 'x': 'NEW', 'X': 'NEW',
#                                                                                      'i': 110988383439, 'l': '0', 'z': '0', 'L': '0', 'T': 1674496832606, 't': 0, 'b': '0', 'a': '0', 'm': False, 'R': True, 'wt': 'CONTRACT_PRICE', 'ot': 'MARKET', 'ps': 'BOTH', 'cp': False, 'rp': '0', 'pP': False, 'si': 0, 'ss': 0}}


# for i in [short, tp, sl, cl_tp, cl_sl, tr_sl, cl_tr_sl, cl_short]:
#     print(i['o']['o'] + '\n\n')
#     print(i, end='\n\n')
#     print(ORDERTRADEUPDATE(**i))
#     # print('\n\n\n\n\n\n\n')

if __name__  == '__main__':
    from Tg_Bot.bot import start_bot
    start_bot()
