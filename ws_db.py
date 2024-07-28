from pybit.unified_trading import WebSocket
from pybit import exceptions
from time import sleep

from db import models
from db.conn import engine, SessionLocal, Base

from sqlalchemy import select
from sqlalchemy.sql import func

import decimal
import requests
from datetime import datetime, timedelta





def data_analize(db):
    token = '6619773915:AAGZKwI6x4SUxrzChQQ2aAOV_csCXRaYDW4'
    channel = '5650732610'

    # VOLUME

    try:
        last_volume = db.query(models.ByVolume.volume).order_by(models.ByVolume.id.desc()).limit(1).scalar()

        last_2v = db.query(models.ByVolume.volume).order_by(models.ByVolume.id.desc()).limit(2).all()
        last_2v = [float(value) for (value,) in last_2v]

        last_5 = db.query(models.ByVolume.volume).order_by(models.ByVolume.id.desc()).limit(5).all()
        last_5 = [float(value) for (value,) in last_5]
        last_5 = sum(last_5) / 5

        print("___________________________________NEW___________________________________________")

        print('Volume')
        print(f"last 5 avg: {round(decimal.Decimal(last_5), 0)}")
        print(f"last: {round(decimal.Decimal(last_volume), 0)}")
        print(f"pre_last: {last_2v[1]}")

        if round(decimal.Decimal(last_volume), 0) / 2 > round(decimal.Decimal(last_5), 0):
            text = "VOLUME STRONG GROWS"

            print(text)

            res = requests.get(f'https://api.telegram.org/bot{token}/sendMessage', params=dict(
                chat_id=channel, text=text
            ))

        if round(decimal.Decimal(last_volume), 0) > last_2v[1] * 1.25:
            text = "VOLUME MORE THAN PREV"

            print(text)

            res = requests.get(f'https://api.telegram.org/bot{token}/sendMessage', params=dict(
                chat_id=channel, text=text
            ))
    except:
        print('data analise volume error')

    # PRICE

    try:
        last_close = db.query(models.ByVolume.close).order_by(models.ByVolume.id.desc()).limit(1).scalar()

        last_2 = db.query(models.ByVolume.close).order_by(models.ByVolume.id.desc()).limit(2).all()
        last_2 = [float(value) for (value,) in last_2]

        print('Price')
        print(f"pre_last: {last_2[1]}")
        print(f"last: {round(decimal.Decimal(last_close), 4)}")

        if float(last_close) > last_2[1] + 0.001:
            text = f"PRICE STRONG GROWS {last_close}:{last_2[1]}"

            print(text)

            res = requests.get(f'https://api.telegram.org/bot{token}/sendMessage', params=dict(
                chat_id=channel, text=text
            ))

        if last_2[1] - 0.001 > float(last_close):
            text = "PRICE STRONG DOWN"

            print(text)

            res = requests.get(f'https://api.telegram.org/bot{token}/sendMessage', params=dict(
                chat_id=channel, text=text
            ))
    except:
        print('data analise price error')


def get_klines(message):
    print(message['data'])

    db = SessionLocal()

    try:
        for m in message['data']:
            kline_info = models.ByVolume()

            kline_info.open = m['open']
            kline_info.high = m['high']
            kline_info.low = m['low']
            kline_info.close = m['close']
            kline_info.volume = m['volume']

            db.add(kline_info)
            db.commit()
    except:
        print('db save error')

    data_analize(db)


def main():
    try:
        ws = WebSocket(
            testnet=False,
            channel_type="linear",
        )

        ws.kline_stream(
            symbol='HIFIUSDT',
            interval=5,
            callback=get_klines
        )
        # print(r)

    except exceptions.InvalidRequestError as e:
        print("Bybit Request Error", e.status_code, e.message, sep=' | ')
    except exceptions.FailedRequestError as e:
        print("Bybit Request Failed", e.status_code, e.message, sep=' | ')
    except Exception as e:
        print(e)



    while True:
        sleep(5)

if __name__ == '__main__':
    print("START")
    main()