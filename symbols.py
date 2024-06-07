import requests
import json

bybit = requests.get("https://api-testnet.bybit.com//v5/market/tickers?category=linear")
e = bybit.json()['result']['list']

# print(e)

# with open('json/tickers.json', 'w', encoding='utf-8') as f:
#     json.dump(e, f, indent=4, ensure_ascii=False)

symbols = []

for pair in e:
    symbol = pair['symbol']
    symbols.append(symbol)
    # print (symbol)


    with open('json/symbols.json', 'w', encoding='utf-8') as f:
        json.dump(symbols, f, indent=4, ensure_ascii=False)