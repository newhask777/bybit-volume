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


class WebSocketClass(WebSocket):
    def __init__(self, token=None, channel=None):
        super().__init__('linear', testnet=False)
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()

        self.token = token
        self.channel = channel

        print('ok')


    def save_klines(message):
        print(message['data'])


    def analize_klines(self):
        pass


    def start(self):
        ws = WebSocket(
            testnet=False,
            channel_type="linear",
        )

        ws.kline_stream(
            symbol='TONUSDT',
            interval=1,
            callback=self.save_klines
        )
