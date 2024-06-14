from pybit.unified_trading import WebSocket
from time import sleep
import json
import itertools
from db import models
from db.conn import engine, SessionLocal, Base
import requests

TELEGRAM_TOKEN = '6619773915:AAGZKwI6x4SUxrzChQQ2aAOV_csCXRaYDW4'
TELEGRAM_CHANNEL = '5650732610'


models.Base.metadata.create_all(bind=engine)

def handle_ticker(message):
    # print(message['data'])

    db = SessionLocal()

    for m in message['data']:
        # print(message['topic'])
        # print(m['volume'])

        kline_info = models.ByVolume()

        kline_info.symbol = message['topic']
        kline_info.volume = m['volume']

        # db.add(kline_info)
        # db.commit()
        


    vols = db.query(models.ByVolume).all()

    sum_vols = []

    for vol in vols[-5:]:
        # print(vol.as_dict())
        print(vol.volume)

        sum_vols.append(vol.volume)
        sums = sum(sum_vols)/5

    kline_info.smvol = sums

    db.add(kline_info)
    db.commit()

    # print(sum_vols)
    # print(sum(sum_vols)/5)

    vols_res = db.query(models.ByVolume).filter(models.ByVolume.smvol).all()

    vls_list = []

    for vls in vols_res[-2:]:
        # print(vls.smvol)
        vls_list.append(vls.smvol)

    # print(vls_list)


    for a, b in itertools.combinations(vls_list, 2):
        if(a < b):
            print(a, b)
    

            text = 'TON GROWS'
            print(text)
        else:
            text = 'TON DOWN'
            print(text)

    res = requests.get(f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage', params=dict(
        chat_id=TELEGRAM_CHANNEL, text=text
    ))

    sleep(5)

    print('__________________________________new____________________________________')



def main():

    # print(symbols)

    # with open('json/symbols.json', 'r', encoding='utf-8')  as f:
    #     symbols = json.load(f)

    # print(symbols)

    ws = WebSocket(
        testnet=False,
        channel_type="linear",
    )

    ws.kline_stream(
            symbol='TONUSDT',
            interval=5,
            callback=handle_ticker
        )

    # for symbol in symbols:

    #     ws.kline_stream(
    #         symbol=symbol,
    #         interval=5,
    #         callback=handle_ticker
    #     )

    while True:
        sleep(5)

if __name__ == '__main__':
    print("Hola")
    main()


