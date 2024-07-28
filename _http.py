from pybit.unified_trading import HTTP
import json
import time
import decimal

from datetime import datetime, timedelta
futuredate = datetime.now() + timedelta(days=10)

import json
import itertools
from db import models
from db.conn import engine, SessionLocal, Base
import requests

from sqlalchemy import create_engine, select
from sqlalchemy.sql import func, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:root@127.0.0.1:3306/volume'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=20, 
    max_overflow=0
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


models.Base.metadata.create_all(bind=engine)


def analize( db):

    TELEGRAM_TOKEN = '6619773915:AAGZKwI6x4SUxrzChQQ2aAOV_csCXRaYDW4'
    TELEGRAM_CHANNEL = '5650732610'

    volumes = db.query(func.avg(models.Volume.volume)).limit(5).scalar()

    last_volume = db.query(models.Volume.volume).limit(1).scalar()

    # last_5 = db.query(models.Volume.volume).limit(5).all()


    print("___________________________________NEW___________________________________________")

    # print(last_5)
    print('Volume')
    print(f"avg: {round(decimal.Decimal(volumes), 0)}")
    print(f"last: {round(decimal.Decimal(last_volume), 0)}")

    if round(decimal.Decimal(last_volume), 0) / 2 > round(decimal.Decimal(volumes), 0):
        text = "VOLUME STRONG GROWS"

        print(text)

        res = requests.get(f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage', params=dict(
            chat_id=TELEGRAM_CHANNEL, text=text
        ))

    # if float(volumes)/2 > float(last_volume):
    #     text = "Volume Down"
    #
    #     print(text)
    #
    #     res = requests.get(f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage', params=dict(
    #         chat_id=TELEGRAM_CHANNEL, text=text
    #     ))

    # PRICE

    # closes = db.query(func.avg(models.Volume.close)).limit(5).scalar()
    last_close = db.query(models.Volume.close).limit(1).scalar()
    pre_last_close = db.query(models.Volume).order_by(models.Volume.id.asc()).limit(2)

    arr = []

    for pls in pre_last_close:
        arr.append(pls.as_dict())

    print('Price')
    print(f"last: {last_close}")
    print(f"pre last: {arr[1]['close']}")

    if float(last_close) > float(arr[1]['close']) + 0.50:
        text = "PRICE STRONG GROWS"

        print(text)

        res = requests.get(f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage', params=dict(
            chat_id=TELEGRAM_CHANNEL, text=text
        ))

    if float(arr[1]['close']) - 0.50 > float(last_close):
        text = "PRICE STRONG DOWN"

        print(text)

        res = requests.get(f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage', params=dict(
            chat_id=TELEGRAM_CHANNEL, text=text
        ))


def get_klines():

    session = HTTP()
    req = session.get_kline(category="linear", symbol="TONUSDT", interval=1,)

    db = SessionLocal()
    db.query(models.Volume).delete()

    for m in req['result']['list']:

        kline_info = models.Volume()

        unix_timestamp = m[0]
        unix_timestamp = unix_timestamp[:-3]
        unix_timestamp = int(unix_timestamp)

        stamp = datetime.fromtimestamp(unix_timestamp)

        kline_info.stamp = stamp
        kline_info.open = m[1]
        kline_info.high = m[2]
        kline_info.low = m[3]
        kline_info.close = m[4]
        kline_info.volume = m[5]

        db.add(kline_info)
        db.commit()

    analize(db)

def main():
    while True:
        get_klines()
        time.sleep(5)

if __name__ == '__main__':
    print("Hola")
    main()
    # while True:
    #     main()
    #     sleep(10)


