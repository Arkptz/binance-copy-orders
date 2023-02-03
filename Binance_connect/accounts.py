from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
from binance.um_futures import UMFutures as Client
from binance.error import ClientError
from binance.lib.utils import config_logging
import traceback
from dataclasses import dataclass
import logging
import os
from .classes import *
from .decors import catch_eroor, send_log_thr
from DB import SessionDb, ClientOrderIdAssociationDb
from config import log_path, SSL_CERT_FILE
from threading import Thread
from time import sleep
import sys

#precisions = {'BTCUSDT': 3, 'ETHUSDT': 3, 'BCHUSDT': 3, 'XRPUSDT': 1, 'EOSUSDT': 1, 'LTCUSDT': 3, 'TRXUSDT': 0, 'ETCUSDT': 2, 'LINKUSDT': 2, 'XLMUSDT': 0, 'ADAUSDT': 0, 'XMRUSDT': 3, 'DASHUSDT': 3, 'ZECUSDT': 3, 'XTZUSDT': 1, 'BNBUSDT': 2, 'ATOMUSDT': 2, 'ONTUSDT': 1, 'IOTAUSDT': 1, 'BATUSDT': 1, 'VETUSDT': 0, 'NEOUSDT': 2, 'QTUMUSDT': 1, 'IOSTUSDT': 0, 'THETAUSDT': 1, 'ALGOUSDT': 1, 'ZILUSDT': 0, 'KNCUSDT': 0, 'ZRXUSDT': 1, 'COMPUSDT': 3, 'OMGUSDT': 1, 'DOGEUSDT': 0, 'SXPUSDT': 1, 'KAVAUSDT': 1, 'BANDUSDT': 1, 'RLCUSDT': 1, 'WAVESUSDT': 1, 'MKRUSDT': 3, 'SNXUSDT': 1, 'DOTUSDT': 1, 'DEFIUSDT': 3, 'YFIUSDT': 3, 'BALUSDT': 1, 'CRVUSDT': 1, 'TRBUSDT': 1, 'RUNEUSDT': 0, 'SUSHIUSDT': 0, 'SRMUSDT': 0, 'EGLDUSDT': 1, 'SOLUSDT': 0, 'ICXUSDT': 0, 'STORJUSDT': 0, 'BLZUSDT': 0, 'UNIUSDT': 0, 'AVAXUSDT': 0, 'FTMUSDT': 0, 'HNTUSDT': 0, 'ENJUSDT': 0, 'FLMUSDT': 0, 'TOMOUSDT': 0, 'RENUSDT': 0, 'KSMUSDT': 1, 'NEARUSDT': 0, 'AAVEUSDT': 1, 'FILUSDT': 1, 'RSRUSDT': 0, 'LRCUSDT': 0, 'MATICUSDT': 0, 'OCEANUSDT': 0, 'CVCUSDT': 0, 'BELUSDT': 0, 'CTKUSDT': 0, 'AXSUSDT': 0, 'ALPHAUSDT': 0, 'ZENUSDT': 1, 'SKLUSDT': 0, 'GRTUSDT': 0, '1INCHUSDT': 0, 'BTCBUSD': 3, 'CHZUSDT': 0, 'SANDUSDT': 0, 'ANKRUSDT': 0, 'BTSUSDT': 0, 'LITUSDT': 1, 'UNFIUSDT': 1, 'REEFUSDT': 0, 'RVNUSDT': 0, 'SFPUSDT': 0, 'XEMUSDT': 0, 'BTCSTUSDT': 1, 'COTIUSDT': 0, 'CHRUSDT': 0, 'MANAUSDT': 0, 'ALICEUSDT': 1, 'HBARUSDT': 0, 'ONEUSDT': 0, 'LINAUSDT': 0, 'STMXUSDT': 0, 'DENTUSDT': 0, 'CELRUSDT': 0, 'HOTUSDT': 0, 'MTLUSDT': 0, 'OGNUSDT': 0, 'NKNUSDT': 0, 'SCUSDT': 0, 'DGBUSDT': 0, '1000SHIBUSDT': 0, 'BAKEUSDT': 0, 'GTCUSDT': 1, 'ETHBUSD': 3, 'BTCDOMUSDT': 3, 'TLMUSDT': 0, 'BNBBUSD': 2, 'ADABUSD': 0, 'XRPBUSD': 1, 'IOTXUSDT': 0, 'DOGEBUSD': 0, 'AUDIOUSDT': 0, 'RAYUSDT': 1, 'C98USDT': 0, 'MASKUSDT': 0, 'ATAUSDT': 0, 'SOLBUSD': 0, 'FTTBUSD': 1, 'DYDXUSDT': 1, '1000XECUSDT': 0, 'GALAUSDT': 0, 'CELOUSDT': 1, 'ARUSDT': 1, 'KLAYUSDT': 1, 'ARPAUSDT': 0, 'CTSIUSDT': 0, 'LPTUSDT': 1, 'ENSUSDT': 1, 'PEOPLEUSDT': 0, 'ANTUSDT': 1, 'ROSEUSDT': 0, 'DUSKUSDT': 0, 'FLOWUSDT': 1, 'IMXUSDT': 0, 'API3USDT': 1, 'GMTUSDT': 0, 'APEUSDT': 0, 'BNXUSDT': 1, 'WOOUSDT': 0, 'FTTUSDT': 1, 'JASMYUSDT': 0, 'DARUSDT': 1, 'GALUSDT': 0, 'AVAXBUSD': 1, 'NEARBUSD': 1, 'GMTBUSD': 1, 'APEBUSD': 1, 'GALBUSD': 0, 'FTMBUSD': 0, 'DODOBUSD': 0, 'ANCBUSD': 0, 'GALABUSD': 0, 'TRXBUSD': 0, '1000LUNCBUSD': 0, 'LUNA2BUSD': 0, 'OPUSDT': 1, 'DOTBUSD': 1, 'TLMBUSD': 0, 'ICPBUSD': 1, 'WAVESBUSD': 1, 'LINKBUSD': 1, 'SANDBUSD': 1, 'LTCBUSD': 2, 'MATICBUSD': 0, 'CVXBUSD': 1, 'FILBUSD': 1, '1000SHIBBUSD': 0, 'LEVERBUSD': 0, 'ETCBUSD': 1, 'LDOBUSD': 1, 'UNIBUSD': 1, 'AUCTIONBUSD': 1, 'INJUSDT': 1, 'STGUSDT': 0, 'FOOTBALLUSDT': 2, 'SPELLUSDT': 0, '1000LUNCUSDT': 0, 'LUNA2USDT': 0, 'AMBBUSD': 0, 'PHBBUSD': 0, 'LDOUSDT': 0, 'CVXUSDT': 0, 'ICPUSDT': 0, 'APTUSDT': 1, 'QNTUSDT': 1, 'APTBUSD': 1, 'BLUEBIRDUSDT': 1, 'ETHUSDT_230331': 3, 'BTCUSDT_230331': 3, 'FETUSDT': 0, 'AGIXBUSD': 0, 'FXSUSDT': 1, 'HOOKUSDT': 1, 'MAGICUSDT': 1, 'TUSDT': 0}



@dataclass
class Account_2Lvl:
    name_account: str
    api_key: str
    secret: str
    multiplicator: float = 1
    precisions: dict[str, int] | None = None
    only_check:bool = False

    def __post_init__(self) -> None:
        self.client = Client(self.api_key, self.secret,)
        # base_url='https://testnet.binancefuture.com')  #
        # base_url="https://fapi.binance.com")
        if not self.only_check:
            send_log_thr(
                f'Инициализация аккаунта {self.name_account} 2 уровня прошла успешно ')
            self.update_precisions()

    @catch_eroor
    def update_precisions(self):
        info: dict = self.client.exchange_info()['symbols']
        self.precisions = {i['symbol']: i['quantityPrecision'] for i in info}
        print(self.precisions)
        logging.info(
            f'{self.name_account} -- Update precision -- {self.precisions}')

    def check_balance(self):
        balance = self.client.balance()
        _str = f'   {self.name_account} баланс:\n'
        for i in balance:#float(i["balance"]) + 
            _str += f'              {float(i["crossWalletBalance"]) + float(i["crossUnPnl"])} {i["asset"]}\n'
        return _str

    @catch_eroor
    def new_order(self, order: Order):
        
        need_sp = [OrderTypes.TAKE_PROFIT_MARKET,
                   OrderTypes.STOP_MARKET, OrderTypes.TAKE_PROFIT]
        kwargs = {'symbol': order.s,
                  'side': order.S,
                  'type': order.o,
                  'quantity': round(order.q * self.multiplicator, self.precisions[order.s]), }
        if order.R:
            kwargs['reduceOnly'] = True
        if order.ps:
            kwargs['positionSide'] = order.ps
        if not order.o in [OrderTypes.MARKET] + need_sp:
            kwargs['price'] = order.p
            kwargs['timeInForce'] = 'GTC'
        if order.o in need_sp + [OrderTypes.STOP]:
            kwargs['stopPrice'] = order.sp
            kwargs['quantity'] = round(order.q * self.multiplicator, self.precisions[order.s])
            if 'reduceOnly' in kwargs:
                del kwargs['reduceOnly']
        if order.cp:
            kwargs['closePosition'] = True
        if order.o == OrderTypes.TRAILING_STOP_MARKET:
            kwargs['callbackRate'] = order.cr
            kwargs['activationPrice'] = order.AP
        kwargs['workingType'] = order.wt
        logging.info(
            f'{self.name_account} -- открываем ордер: {kwargs}')
        response = self.client.new_order(**kwargs)
        open_order = OpenOrder(**response)
        logging.info(
            f'{self.name_account} -- Успешно открыли новый ордер {order.o}: {open_order}')
        send_log_thr(
            f'{self.name_account} -- Успешно открыли новый ордер {order.o}: {open_order}')
        ass = ClientOrderIdAssociationDb(
            lvl_1=order.i, lvl_2=open_order.orderId)
        SessionDb.add(ass)
        SessionDb.commit()
        logging.info(response)

    @catch_eroor
    def get_association_dict(self) -> dict:
        lst = SessionDb.query(ClientOrderIdAssociationDb).all()
        ans = {i.lvl_1: i.lvl_2 for i in lst}
        logging.info(f'Get association_dict -- {ans}')
        return ans

    @catch_eroor
    def get_open_orders(self, symbol):
        response = self.client.get_orders(
            symbol=symbol,
            recvWindow=2000
        )
        ans = [OpenOrder(**i) for i in response]
        logging.info(f'Get open orders -- {ans}')
        return ans

    @catch_eroor
    def change_margin_type(self, mg_type: str, symbol: str):
        if mg_type == 'cross':
            mg_type = 'CROSSED'
        elif mg_type == 'isolated':
            mg_type == 'ISOLATED'
        self.client.change_margin_type(symbol=symbol, marginType=mg_type)
        send_log_thr(
            f'{self.name_account} -- Успешно поставили margin_type: {mg_type}')

    @catch_eroor
    def change_leverage(self, config: ChangeLeverage) -> dict:
        response = self.client.change_leverage(
            symbol=config.s,
            leverage=config.l,
            recvWindow=6000
        )
        send_log_thr(
            f'{self.name_account} -- Успешно поставили плечо на {config.s}: {config.l}')
        return response

    @catch_eroor
    def get_position_risk(self) -> list[PositionModes]:
        response = self.client.get_position_risk()
        response = [PositionModes(**i) for i in response]
        return response

    @catch_eroor
    def check_position_risk(self, cf_original: dict[str, PositionModes]):
        this_posR = self.get_position_risk()
        for symb in this_posR:
            lvl1_posR = cf_original[symb.symbol]
            if symb.leverage != lvl1_posR.leverage:
                self.change_leverage(ChangeLeverage(
                    s=symb.symbol, l=lvl1_posR.leverage))
            elif symb.marginType != lvl1_posR.marginType:
                self.change_margin_type(
                    lvl1_posR.marginType, symbol=symb.symbol)

    @catch_eroor
    def change_multi_asset_mode(self, config: ChangeConfiguration) -> dict:
        response = self.client.change_multi_asset_mode(
            multiAssetsMargin=f'{config.j}'
        )
        send_log_thr(
            f"{self.name_account} -- Успешно {'включили' if config.j else 'выключили'} multi_asset_mode")
        return response

    @catch_eroor
    def change_pos_mode(self, dualSidePosition: bool):
        response = self.client.change_position_mode(
            dualSidePosition=dualSidePosition,
            recvWindow=2000
        )
        send_log_thr(
            f"{self.name_account} -- Успешно {'включили' if dualSidePosition else 'выключили'} dualSidePosition")
        return response

    @catch_eroor
    def cancel_order(self, order: Order):
        #open_orders = self.get_open_orders(order.s)
        ass_dct = self.get_association_dict()
        if order.i in ass_dct:
            ordId = ass_dct[order.i]
            logging.info(f'Closing order with orderId = {ordId}')
            # send_log_thr(f'{self.name_account} -- Закрываем ордер с orderId = {ordId}')
            response = self.client.cancel_order(
                symbol=order.s,
                orderId=ordId,
                recvWindow=2000
            )
            logging.info(
                f'{self.name_account} -- Успешно закрыли ордер с orderId = {ordId}')
            logging.info(response)
            send_log_thr(
                f'{self.name_account} -- Успешно закрыли ордер с orderId = {ordId}')
            if order.cp:
                cl = SessionDb.query(ClientOrderIdAssociationDb).filter(
                    ClientOrderIdAssociationDb.lvl_1 == order.i).first()
                SessionDb.delete(cl)
                SessionDb.commit()
        else:
            txt = f'{self.name_account} -- {order} - Отсутсвует подходящий ордер для закрытия'
            logging.error(
                f'{order} - Bd association not have current order')
            send_log_thr(txt)

    def copy_order(self, order: Order):
        if order.x == ExecutioTypes.NEW:
            self.new_order(order)
        elif order.x == ExecutioTypes.CANCELED:
            self.cancel_order(order)


@dataclass
class Account_1Lvl:
    name_account: str
    api_key: str
    secret: str
    account_2lvls: list[Account_2Lvl]
    ws_client: UMFuturesWebsocketClient = UMFuturesWebsocketClient(
        stream_url='wss://fstream.binance.com')
    listen_key:str|None = None
    # stream_url='wss://stream.binancefuture.com')

    def __post_init__(self):
        os.environ['SSL_CERT_FILE'] = SSL_CERT_FILE
        # config_logging(logging, logging.DEBUG,
        #                log_file=log_path + self.name_account+'.log')
        self.client = Client(self.api_key, secret=self.secret,)

    def inizialize(self) -> None:
        # base_url='https://testnet.binancefuture.com')
        print(log_path + self.name_account+'.log')
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(
            level=logging.DEBUG,
            format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
            datefmt="%d/%b/%Y %H:%M:%S",
            filename=log_path + self.name_account+'.log', filemode='a')
        self.update_listen_key()
        if not self.listen_key:
            send_log_thr('Error - проверь правильность апи ключей и перезапусти бота')
            sleep(5)
            sys.exit()
        self.start_checks()
        send_log_thr(
            f'Инициализация аккаунта {self.name_account} 1 уровня прошла успешно ')

    def check_balance(self):
        balance = self.client.balance()
        _str = f'{self.name_account} баланс:\n'
        for i in balance:
            _str += f'      {float(i["crossWalletBalance"]) + float(i["crossUnPnl"])}\n'
        for acc in self.account_2lvls:
            _str += acc.check_balance()
        return _str


    @catch_eroor
    def update_listen_key(self):
        self.listen_key = self.client.new_listen_key()["listenKey"]
        send_log_thr(f'{self.name_account} -- Получен ключ для вебсокета')

    def start_checks(self):
        send_log_thr(f'{self.name_account} -- Начинаю сверку position_mode')
        pos_mode = self.check_position_mode()
        send_log_thr(f'{self.name_account} -- Начинаю сверку multi_asset_mode')
        mam = self.check_multi_asset_mode()
        send_log_thr(
            f'{self.name_account} -- Начинаю сверку margin_type and leverage')
        pr = self.check_position_risk()
        self.wait_threads(pos_mode)
        send_log_thr(
            f'{self.name_account} -- Сверка position_mode - закончена')
        self.wait_threads(mam)
        send_log_thr(
            f'{self.name_account} -- Сверка multi_asset_mode - закончена')
        self.wait_threads(pr)
        send_log_thr(
            f'{self.name_account} -- Сверка margin_type and leverage - закончена')

    @catch_eroor
    def check_position_risk(self):
        response = self.client.get_position_risk()
        response = [PositionModes(**i) for i in response]
        response = {i.symbol: i for i in response}
        return self.copy('check_position_risk', args=[response])

    def wait_threads(self, lst: list[Thread]):
        for i in lst:
            i.join()

    @catch_eroor
    def check_position_mode(self):
        response = self.client.get_position_mode(recvWindow=2000)
        mode = response['dualSidePosition']
        logging.info(f'1lvl - position mode - {response}')
        return self.copy('change_pos_mode', [mode])

    @catch_eroor
    def check_multi_asset_mode(self):
        response = self.client.get_multi_asset_mode(recvWindow=2000)
        mode = response['multiAssetsMargin']
        logging.info(f'1lvl - multi_asset_mode - {response}')
        return self.copy('change_multi_asset_mode', [ChangeConfiguration(j=mode)])

    @catch_eroor
    def copy(self, name_func: str, args: list):
        thread_list = []
        for i in self.account_2lvls:
            func = getattr(i, name_func)
            t = Thread(target=func, args=args)
            t.start()
            thread_list.append(t)
        return thread_list

    def _handler(self, message):
        txt = f'Callback____ {message}'
        print(txt)
        logging.debug(txt)
        try:
            if 'e' in message:
                event_type = message['e']
                if event_type == EventTypes.ORDER_TRADE_UPDATE:
                    otp = ORDER_TRADE_UPDATE(**message)
                    send_log_thr(
                        f'{self.name_account} -- получен новый ордер: {otp}')
                    Thread(target=self.copy, args=[
                           'copy_order', [otp.o]]).start()
                    logging.debug(otp)
                elif event_type == EventTypes.ACCOUNT_CONFIG_UPDATE:
                    acu = ACCOUNT_CONFIG_UPDATE(**message)
                    send_log_thr(
                        f'{self.name_account} -- получен новый апдейт конфига: {acu}')
                    if acu.ac:
                        Thread(target=self.copy, args=[
                               'change_leverage', [acu.ac]]).start()
                    elif acu.ai:
                        Thread(target=self.copy, args=[
                               'change_multi_asset_mode', [acu.ai]]).start()
        except:
            logging.error(traceback.format_exc())
            pass

    @catch_eroor
    def start_polling(self):
        self.ws_client.start()
        self.ws_client.user_data(listen_key=self.listen_key,
                                 id=1,
                                 callback=self._handler)
        sleep(5)
        logging.info('startup')
        send_log_thr(f'{self.name_account} -- Запуск вебсокета...')
