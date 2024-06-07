from pybit.unified_trading import HTTP
from Crypto.Cipher import AES
import json

session = HTTP()

req = session.get_kline(category="linear", symbol="BTCUSDT", interval=5,)
print(req)

with open('json/klines.json', 'w', encoding='utf-8') as f:
    json.dump(req, f, indent=4, ensure_ascii=False)