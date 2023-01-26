from binance.websocket.cm_futures.websocket_client import CMFuturesWebsocketClient
from binance.um_futures import UMFutures as Client
from binance.error import ClientError
from binance.lib.utils import config_logging
import traceback
from dataclasses import dataclass
import logging
import os
from .classes import *
from .decors import catch_eroor
from DB import SessionDb, ClientOrderIdAssociationDb
from config import log_path, SSL_CERT_FILE, trade_pair
from threading import Thread





@dataclass
class Account_2Lvl:
    name_account:str
    api_key: str
    secret: str
    multiplicator: float = 1

    def __post_init__(self) -> None:
        self.client = Client(self.api_key, self.secret,
                             base_url='https://testnet.binancefuture.com')#base_url="https://fapi.binance.com")

    @catch_eroor
    def new_order(self, order: Order):
        need_sp = [OrderTypes.TAKE_PROFIT_MARKET, OrderTypes.STOP_MARKET, OrderTypes.TAKE_PROFIT]
        kwargs = {'symbol':order.s,
            'side':order.S,
            'type':order.o,
            'quantity':round(order.q * self.multiplicator,3),}
        if order.R:
            kwargs['reduceOnly'] = True
        if not order.o in [OrderTypes.MARKET] + need_sp:
            kwargs['price'] = order.p
            kwargs['timeInForce'] = 'GTC'
        if order.o in need_sp + [OrderTypes.STOP]:
            kwargs['stopPrice'] = order.sp
            kwargs['quantity'] = round(order.q * self.multiplicator,3)
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
        ass = ClientOrderIdAssociationDb(lvl_1=order.i, lvl_2=open_order.orderId)
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
    def change_leverage(self, config: ChangeLeverage) -> dict:
        response = self.client.change_leverage(
            symbol=config.s,
            leverage=config.l,
            recvWindow=6000
        )
        return response


    @catch_eroor
    def change_multi_asset_mode(self, config: ChangeConfiguration) -> dict:
        response = self.client.change_multi_asset_mode(
            multiAssetsMargin=f'{config.j}'
        )
        return response

    @catch_eroor
    def change_pos_mode(self, dualSidePosition: bool):
        response = self.client.change_position_mode(
            dualSidePosition=dualSidePosition,
            recvWindow=2000
        )
        return response

    @catch_eroor
    def cancel_order(self, order: Order):
        open_orders = self.get_open_orders(order.s)
        ass_dct = self.get_association_dict()
        if order.i in ass_dct:
            ordId = ass_dct[order.i]
            logging.info(f'Closing order with orderId = {ordId}')
            response = self.client.cancel_order(
                symbol=order.s,
                orderId=ordId,
                recvWindow=2000
            )
            logging.info(response)
            cl = SessionDb.query(ClientOrderIdAssociationDb).filter(ClientOrderIdAssociationDb.lvl_1 == order.i).first()
            SessionDb.delete(cl)
            SessionDb.commit()
        else:
            logging.error(
                f'{order} - Bd association not have current order')

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
    ws_client: CMFuturesWebsocketClient = CMFuturesWebsocketClient(
        stream_url='wss://stream.binancefuture.com')#stream_url='wss://fstream.binance.com')

    def inizialize(self) -> None:
        os.environ['SSL_CERT_FILE'] = SSL_CERT_FILE
        config_logging(logging, logging.DEBUG,
                       log_file=log_path + self.name_account)
        self.client = Client(self.api_key, secret=self.secret,base_url='https://testnet.binancefuture.com')
        self.listen_key = self.client.new_listen_key()["listenKey"]
        self.check_position_mode()
        self.check_multi_asset_mode()


    @catch_eroor
    def check_position_mode(self):
        response = self.client.get_position_mode(recvWindow=2000)
        mode = response['dualSidePosition']
        logging.info(f'1lvl - position mode - {response}')
        self.copy('change_pos_mode', [mode])

    @catch_eroor
    def check_multi_asset_mode(self):
        response = self.client.get_multi_asset_mode(recvWindow=2000)
        mode = response['multiAssetsMargin']
        logging.info(f'1lvl - multi_asset_mode - {response}')
        self.copy('change_multi_asset_mode', [ChangeConfiguration(j=mode)])


    @catch_eroor
    def copy(self, name_func:str, args:list):
        for i in self.account_2lvls:
            func = getattr(i, name_func)
            Thread(target=func, args=args).start()

    def _handler(self, message):
        txt = f'Callback____ {message}'
        print(txt)
        logging.debug(txt)
        try:
            if 'e' in message:
                event_type = message['e']
                if event_type == EventTypes.ORDER_TRADE_UPDATE:
                    otp = ORDER_TRADE_UPDATE(**message)
                    Thread(target = self.copy, args =['copy_order', [otp.o]]).start()
                    logging.debug(otp)
                elif event_type == EventTypes.ACCOUNT_CONFIG_UPDATE:
                    acu = ACCOUNT_CONFIG_UPDATE(**message)
                    if acu.ac:
                        Thread(target = self.copy, args =['change_leverage', [acu.ac]]).start()
                    elif acu.ai:
                        Thread(target = self.copy, args =['change_multi_asset_mode', [acu.ai]]).start()
        except:
            logging.error(traceback.format_exc())
            pass

    def start_polling(self):
        self.ws_client.start()
        self.ws_client.user_data(listen_key=self.listen_key,
                                 id=1,
                                 callback=self._handler)
