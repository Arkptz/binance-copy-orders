from binance.websocket.cm_futures.websocket_client import CMFuturesWebsocketClient
from binance.um_futures import UMFutures
from binance.cm_futures import CMFutures as Client
from binance.lib.utils import config_logging
from binance.error import ClientError
from DB import ClientOrderIdAssociationDb, SessionDb
from config import log_path
from pydantic import BaseModel
import logging
import time
import os
import requests
import traceback

config_logging(logging, logging.DEBUG, log_file=log_path)



# "6f390885925c52bbc5a3bbf79b1935855c947144da2db41c787007ab88cd02eb"
api_key = 'sozayGAh6KvhUDC3HoK9asmW4YGD0sY7q7zsEYpzaAIPEky7M70Y8wxks1qdt8S9'
# 'ee231aee0c502563c94c84e017599b9bc786e35a550ebf646f21c7ff7b2b6a2c'
secret = 'iZTKd9N9l3wcQDjJqX5XoXWXzYD9cNGS157djyc6ftAoueqVOK65pQjPU61SQA0n'
if __name__ == '__main__':
    Account_1Lvl(api_key, secret).start_polling()
