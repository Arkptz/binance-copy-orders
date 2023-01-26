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



if __name__  == '__main__':
    from Tg_Bot.bot import start_bot
    start_bot()
