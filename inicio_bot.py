import sys
sys.path.append(r"C:\Python37\Scripts")
import config_acc_testnet as config_acc
from binance.client import Client
from binance.enums import *
import time, ta
import math,btalib
import datetime
import numpy as np
import pandas as pd

client = Client(config_acc.API_KEY, config_acc.API_SECRET)

symbol = "BTCUSDT"
candles = 15
minutesa = candles*300
candle = str(candles)+"m"
minutes = str(minutesa) + " min ago UTC"
bars = client.get_historical_klines(symbol,candle,minutes)

for line in bars:
    del line[5:]


btc_df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close'])
btc_df.set_index('date', inplace=True)
btc_df.index = pd.to_datetime(btc_df.index, unit='ms')
btc_df = btc_df.astype(float)
print(btc_df.head())
btc_df['sma'] = btalib.sma(btc_df.close, period=20).df
print(btc_df.tail())
rsi = btalib.rsi(btc_df, period=14).mean()
macd = btalib.macd(btc_df.close, pfast=12, pslow=26, psignal=9)
#btc_df = btc_df.join([rsi.df, macd.df])
print(btc_df.tail())

btc_df["rsi_ta"] = ta.momentum.rsi(btc_df.close, window = 14)


btc_df['20sma'] = btc_df.close.rolling(20).mean()
print(btc_df.tail(5))

