from binance.websocket.cm_futures.websocket_client import CMFuturesWebsocketClient
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

@dataclass
class Account_2Lvl:
    name_account: str
    api_key: str
    secret: str
    multiplicator: float = 1

    def __post_init__(self) -> None:
        self.client = Client(self.api_key, self.secret,)
                             #base_url='https://testnet.binancefuture.com')  # 
                             #base_url="https://fapi.binance.com")
        send_log_thr(
            f'Инициализация аккаунта {self.name_account} 2 уровня прошла успешно ')

    @catch_eroor
    def new_order(self, order: Order):
        need_sp = [OrderTypes.TAKE_PROFIT_MARKET,
                   OrderTypes.STOP_MARKET, OrderTypes.TAKE_PROFIT]
        kwargs = {'symbol': order.s,
                  'side': order.S,
                  'type': order.o,
                  'quantity': round(order.q * self.multiplicator, 3), }
        if order.R:
            kwargs['reduceOnly'] = True
        if order.ps:
            kwargs['positionSide'] = order.ps
        if not order.o in [OrderTypes.MARKET] + need_sp:
            kwargs['price'] = order.p
            kwargs['timeInForce'] = 'GTC'
        if order.o in need_sp + [OrderTypes.STOP]:
            kwargs['stopPrice'] = order.sp
            kwargs['quantity'] = round(order.q * self.multiplicator, 3)
            if 'reduceOnly' in kwargs:
                del kwargs['reduceOnly']
        if order.cp:
            kwargs['closePosition'] = True
        if order.o == OrderTypes.TRAILING_STOP_MARKET:
            kwargs['callbackRate'] = order.cr
            kwargs['activationPrice'] = order.AP
        kwargs['workingType'] = order.wt
        response = self.client.new_order(**kwargs)
        open_order = OpenOrder(**response)
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
        open_orders = self.get_open_orders(order.s)
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
            logging.info(response)
            send_log_thr(
                f'{self.name_account} -- Успешно закрыли ордер с orderId = {ordId}')
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
    ws_client: CMFuturesWebsocketClient = CMFuturesWebsocketClient()
        #stream_url='wss://stream.binancefuture.com')

    def inizialize(self) -> None:
        os.environ['SSL_CERT_FILE'] = SSL_CERT_FILE
        print(log_path + self.name_account+'.log')
        config_logging(logging, logging.DEBUG,
                       log_file=log_path + self.name_account+'.log')
        self.client = Client(self.api_key, secret=self.secret,)
                             #base_url='https://testnet.binancefuture.com')
        send_log_thr(
            f'Инициализация аккаунта {self.name_account} 1 уровня прошла успешно ')
        self.listen_key = self.client.new_listen_key()["listenKey"]
        send_log_thr(f'{self.name_account} -- Получен ключ для вебсокета')
        self.start_checks()

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
        logging.debug('statup')
        send_log_thr(f'{self.name_account} -- Запуск вебсокета...')
