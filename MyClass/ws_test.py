from pybit.unified_trading import WebSocket
from time import sleep
import json
import itertools
from db.models import ByVolume
from db.conn import engine, SessionLocal, Base
import requests

from sqlalchemy.sql import func

import decimal
from datetime import datetime, timedelta
import time

from WebSocketClass import WebSocketClass

token = '6619773915:AAGZKwI6x4SUxrzChQQ2aAOV_csCXRaYDW4'
channel = '5650732610'



if __name__ == '__main__':
    ws = WebSocketClass(token, channel)

    while True:
        ws.start()
        sleep(1)
