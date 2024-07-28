from pybit.unified_trading import WebSocket
from time import sleep
import json
import itertools
from db import models
from db.conn import engine, SessionLocal, Base
import requests

from sqlalchemy.sql import func

import decimal
from datetime import datetime, timedelta
futuredate = datetime.now() + timedelta(days=10)
import time


models.Base.metadata.create_all(bind=engine)

token = '6619773915:AAGZKwI6x4SUxrzChQQ2aAOV_csCXRaYDW4'
channel = '5650732610'

def analize(db, token, channel):
    volumes = db.query(func.avg(models.ByVolume.volume)).limit(5).scalar()
    last_volume = db.query(models.ByVolume.volume).limit(1).scalar()

    print("___________________________________NEW___________________________________________")

    print('Volume')
    print(f"avg: {round(decimal.Decimal(volumes), 0)}")
    print(f"last: {round(decimal.Decimal(last_volume), 0)}")
    print(f"last: {last_volume}")

    if round(decimal.Decimal(last_volume), 0)/2 > round(decimal.Decimal(volumes), 0):
        text = "VOLUME STRONG GROWS"

        print(text)

        res = requests.get(f'https://api.telegram.org/bot{token}/sendMessage', params=dict(
            chat_id=channel, text=text
        ))

    if round(decimal.Decimal(volumes), 0)/2 > round(decimal.Decimal(last_volume), 0):
        text = "VOLUME STRONG DOWN"

        print(text)

        res = requests.get(f'https://api.telegram.org/bot{token}/sendMessage', params=dict(
            chat_id=channel, text=text
        ))

    # PRICE

    closes = db.query(func.avg(models.ByVolume.close)).limit(5).scalar()
    last_close = db.query(models.ByVolume.close).limit(1).scalar()

    print('Price')
    print(f"avg: {closes}")
    print(f"last: {last_close}")

    if float(last_close)/2 > float(closes):
        text = "PRICE STRONG GROWS"

        print(text)

        res = requests.get(f'https://api.telegram.org/bot{token}/sendMessage', params=dict(
            chat_id=channel, text=text
        ))

    if float(closes)/2 > float(last_close):
        text = "PRICE STRONG DOWN"

        print(text)

        res = requests.get(f'https://api.telegram.org/bot{token}/sendMessage', params=dict(
            chat_id=channel, text=text
        ))

    # db.close()

    print('__________________________________new____________________________________')


def get_klines(message):
    print(message['data'])

    db = SessionLocal()

    for m in message['data']:
        kline_info = models.ByVolume()

        kline_info.open = m['open']
        kline_info.high = m['high']
        kline_info.low = m['low']
        kline_info.close = m['close']
        kline_info.volume = m['volume']

        db.add(kline_info)
        db.commit()

    # vls = db.query(models.ByVolume.id).count()
    # # print(vls)
    #
    # if vls > 5:
    #     print(vls)
    #     analize(db, token, channel)
    #     # if vls > 100:
    #     #     db.query(models.ByVolume).delete()
    # else:
    #     print('no')


    analize(db, token, channel)



def main():

    ws = WebSocket(
        testnet=False,
        channel_type="linear",
    )

    ws.kline_stream(
            symbol='TONUSDT',
            interval=5,
            callback=get_klines
        )

    while True:
        sleep(5)

if __name__ == '__main__':
    print("START")
    main()


