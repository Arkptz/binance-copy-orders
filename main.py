from binance.websocket.cm_futures.websocket_client import CMFuturesWebsocketClient
from binance.um_futures import UMFutures
from binance.lib.utils import config_logging
from pydantic import BaseModel
import logging
import time
import os
import requests
import traceback


class Order(BaseModel):
    s: str
    c: str
    S: str
    o: str
    f: str
    q: float
    ap: float
    sp: float
    x: str
    X: str
    i: int
    l: float
    z: float
    L: float
    T: int
    t: int
    b: float
    a: float
    m: bool
    R: bool
    wt: str
    ot: str
    ps: str
    cp: bool
    pP: bool
    si: float
    ss: float
    rp: float
    N: str = None
    n: float = None
    AP: float = None
    cr: float = None
class ORDERTRADEUPDATE(BaseModel):
    e: str
    E: int
    T: int
    o: Order


class Account:
    api_key: str
    secret: str
    ws_client: CMFuturesWebsocketClient = CMFuturesWebsocketClient(
        stream_url='wss://fstream.binance.com')

    def __init__(self, api_key: str, secret: str) -> None:
        os.environ['SSL_CERT_FILE'] = r'cacert.pem'
        config_logging(logging, logging.DEBUG)
        self.api_key, self.secret, = api_key, secret
        self.client = UMFutures(api_key, secret=secret)
        self.listen_key = self.client.new_listen_key()["listenKey"]

    def _handler(self, message, *args):
        print('Callback____', message, args)
        try:
            print(ORDERTRADEUPDATE(**message))
        except:
            traceback.print_exc()
            pass

    def start_polling(self):
        self.ws_client.start()
        self.ws_client.user_data(listen_key=self.listen_key,
                                 id=1,
                                 callback=self._handler)


# "6f390885925c52bbc5a3bbf79b1935855c947144da2db41c787007ab88cd02eb"
api_key = 'sozayGAh6KvhUDC3HoK9asmW4YGD0sY7q7zsEYpzaAIPEky7M70Y8wxks1qdt8S9'
# 'ee231aee0c502563c94c84e017599b9bc786e35a550ebf646f21c7ff7b2b6a2c'
secret = 'iZTKd9N9l3wcQDjJqX5XoXWXzYD9cNGS157djyc6ftAoueqVOK65pQjPU61SQA0n'
if __name__ == '__main__':
    Account(api_key, secret).start_polling()
